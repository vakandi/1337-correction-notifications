#!/usr/bin/env python3
import os
import sys
import time
import socket
import pickle
import requests
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# XXX private info
user_login_value = 'wbousfir'                       # XXX
user_password_value = 'xxxxxxx'                # XXX

# settings
sign_out = False            # if set to True, bot will log out of intra, generates unwanted email notifications
save_session = True
save_html = True
debug = True
send_sms = True
send_group_msg = True
send_direct_msg = True
send_direct_msg_if = False   # send direct message only if group message fails

# values the bot searches for (on the login page)
user_login_key = 'user[login]'
user_password_key = 'user[password]'

# urls the bot uses
intra_signin_page = 'https://signin.intra.42.fr/users/sign_in'
intra_signout_page = 'https://signin.intra.42.fr/users/sign_out'
intra_profile_page = 'https://profile.intra.42.fr/'

# once the bot posts login, it compares the html title to this to make sure its on the correct page
intra_profile_page_title = 'Intra Profile Home'

# filename to use for storing requests session,
# this way we can re-use it next time (to prevent multiple logins and email notifications)
intra_session_file = 'intra_session.pickled'

# http user agent, you'll be able to see this on your intra page,
# check your connection logs at    https://profile.intra.42.fr/users/YOUR_INTRA_NAME_HERE/user_logins
user_agent = 'Mozilla/5.0 (Nintendo Banana; U; Windows Like Godzilla; en) Version/0.42.US'

# http headers dict to send
headers = {'User-Agent': user_agent}

# a place to store our correction string, this way we can avoid sending duplicates
log_file = 'corrections.log'

###############################################################################
def is_text_in_file(filename, text):    #returns true if text matches a line in file, false otherwise
    try:
        with open(filename, 'r') as fp:
            for line in fp.read().splitlines():
                if line == text:
                    fp.close()
                    return True
            fp.close()
            return False
    except:
            return False

###############################################################################
def put_text_in_file(filename, text):
    try:
        with open(filename, 'a') as fp:
            print(text, file=fp)
            fp.close()
    except:
        pass

###############################################################################

def is_online(host="8.8.8.8", port=53, timeout=3):      # returns true if we can ping google
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except:
		return False


###############################################################################
def load_session():     # get previously saved session from file
    try:
        with open(intra_session_file, 'rb') as fp:
            result = pickle.load(fp)
            fp.close()
            return result
    except:
        return False

###############################################################################
def store_session(session): #save session into a file
    try:
        with open(intra_session_file, 'wb') as fp:
            pickle.dump(session, fp)
            fp.close()
            return True  #great success
    except:
        return False

###############################################################################
def init_session():     # tries to load a saved session from file, or create a new one
    session = load_session()
    if session == False:
        if debug: print('No saved session found\n[debug] Trying to create new one')
        session = create_session()
        if session == False:
            if debug:
                print('[debug] failed to create session, bad credentials?')
            sys.exit(1)
        session = load_session()
        if debug and not session:
            print('[debug] load_session() failed, something is wrong in the saved sessions, try to remove it')
            sys.exit(1)
    return session

###############################################################################
def create_session():   # creates a session, logs in, saves session to a file
    session = requests.Session()
    session.headers.update({'User-Agent': user_agent})

    req1 = session.get(intra_signin_page)   #request1, get sign-in page
    if req1.status_code == 200:
        page_signin = req1.content.decode('utf-8')
    else:
        if debug:
            print('[debug] failed to get sign-in page, requests.get returned: ', req1.status_code)
        return False
        
    soup1 = BeautifulSoup(page_signin, features="html.parser")  ## prints a warning if not specified

    post_data = {} 
    for form_input in soup1.find_all('input'):
        key = form_input.get('name')
        value = form_input.get('value')
        post_data[key] = value

    post_data[user_login_key] = user_login_value
    post_data[user_password_key] = user_password_value

    req2 = session.post(intra_signin_page, data=post_data, allow_redirects=False)    #request2, post login data
    if req2.status_code == 200 or req2.status_code == 302:
        if save_session == True:
            store_session(session)
        return True
    else:
        if debug:
            print('[debug] failed to post login data, requests.post returned: ', req2.status_code)
        return False

###############################################################################
###############################################################################
# [ main logic here] ##########################################################

if is_online() != True:
	print("offline")
	sys.exit()

session = init_session()
req3 = session.get(intra_profile_page)
if req3.status_code == 200:
    page_profile = req3.content.decode('utf-8')
else:
    if debug:
        print('[debug] failed to get profile page, response code: ', req3.status_code)
    sys.exit(1)


soup2 = BeautifulSoup(page_profile, features="html.parser")

#are we at the right place?
if soup2.title.string != intra_profile_page_title:
    #maybe we're logged out? try to login again?
    if debug:
        print('[debug] wrong profile title page; logged out or bad credentials? deleting stored session file')
    try:
        os.remove(intra_session_file)
    except:
        pass
    sys.exit(1)

if debug:
    print('[debug] got profile page .. ok')
if save_html:
    output = 'profile_' + str(time.time()) + '.html'
    with open(output, 'w') as fp:
        fp.write(page_profile)
        fp.close()

message=None
for reminder in soup2.find_all('div', class_='project-item reminder'):
    for project in reminder.find_all('div', class_='project-item-text'):
        message = ' '.join(project.text.split())
        for span in project.parent.find_all('span'):
            if span.has_attr('data-long-date'):
                message += ' at ' + span.get('title')
                break

        partner = None
        for user in project.parent.find_all('a'):
            if user.has_attr('data-user-link'):
                partner = user.get('data-user-link')

        if is_text_in_file(log_file, message) == False:
            put_text_in_file(log_file, message)                         #save in log file
            now = datetime.now()
            message = message[:-10]
            message_for_url = message.replace(" ", "+")
            if send_sms == True:
                curl_cmd = f"curl http://xdroid.net/api/message\?k\={api_android}\&t\=Correction1337\&c\={message_for_url}\&u\=https://profile.intra.42.fr"
                os.system(curl_cmd)
            
            user_login_value = user_login_value.lower()
            if partner != None:
                partner = partner.lower()         
           
            group_msg_result = False
            if send_group_msg == True:
                if partner != None:
                    group_msg_result = slack_send_group_message(user_login_value, partner, message)
            if send_direct_msg == True:
                if send_direct_msg_if == False:
                    slack_send_direct_message(user_login_value, message)
                elif (send_direct_msg_if == True) and (group_msg_result == False):
                    slack_send_direct_message(user_login_value, message)
            if debug:                                                   #print message
                print(message)
                message = message[:-10]

if debug and not message:
    print('[debug] no corrections on your intra page')

if save_session:
    if debug: print('[debug] saving session')
    store_session(session)

if sign_out:
    if debug: print('[debug] signing out')
    signout_data = {'_method': 'delete', 'authenticity_token': ''}
    for meta in soup2.find_all('meta'):
        if meta.get('name') == 'csrf-token':
            signout_data['authenticity_token'] = meta.get('content')
            break
    req3 = session.post(intra_signout_page, data=signout_data, allow_redirects=True)    #request3, log out

