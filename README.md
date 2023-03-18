## Intra 42 Correction Notifier
This Python script logs in to the Intra 42 website (an online platform for the 42 coding school) using a user-provided login and password. Once logged in, it scrapes the page to find information about any corrections that have been made to submitted assignments. If new corrections are found, the script can send notifications messages.
</br>
The script doesn't print the old corrections still pending to not get a notification every 10min, so it's just gonna notify you once.


### App Notifications "[Push Notifiy API](https://play.google.com/store/apps/details?id=net.xdroid.pn&hl=en_US&pli=1)"
</br>


### Installation the prerequisites:
```bash
apt install python3-pip
pip3 install bs4
```
</br>
</br>


## To run the script, edit your credentials lines 14, 15 & 16 
</br>
</br>


### To run the script manually : 
</br>

```bash
python3 corrections-bot.py
```
(the script check.sh is just here to check if there is a correction currently on the last profile.html created by the python script, so basically for bypassing the "only once" notification features)
</br>


### To make the script run every 15 minutes to check your corrections, add the a crontab (works on termux too
(you should fork it to keep your own config)
```bash
crontab -e
```
(adjust folder paths as necessary)
```bash
*/15 * * * * cd /home/ubuntu/corrections; /usr/bin/python3 corrections-bot.py >> execution.log 2>&1
*/15 * * * * cd /home/ubuntu/corrections; sh check.sh

```
Or if you want to use your phone with Termux : 
```bash
*/15 * * * * cd ; cd {your git fork repo}; python3 corrections-bot.py >> execution.log 2>&1
*/15 * * * * cd ; cd {your git fork repo}; sh check.sh
```
</br>


#### No API key required
</br>
</br>
</br>

### Customization

The script includes a number of customization options that can be modified by editing the appropriate variables at the beginning of the script. These options include:

- `sign_out`: Whether the script should log out of the Intra website after logging in (default: `False`)
- `save_session`: Whether the script should save the login session to a file for future use (default: `True`)
- `save_html`: Whether the script should save the HTML of the profile page to a file for debugging purposes (default: `True`)
- `debug`: Whether to print debug information to the console (default: `True`)
- `send_sms`: Whether to send SMS notifications using the Push Notify Android application (default: `True`)
- `send_group_msg`: Whether to send group messages to Slack (default: `True`)
- `send_direct_msg`: Whether to send direct messages to Slack (default: `True`)
- `send_direct_msg_if`: Whether to send direct messages only if group messages fail (default: `False`)

## Acknowledgments

This script was inspired by the [42-corrections-bot](https://github.com/asarandi/42-corrections-bot) project by [asarandi](https://github.com/asarandi), which provides a similar notification system for Intra 42 corrections using Twilio and Slack to send the notifications.


