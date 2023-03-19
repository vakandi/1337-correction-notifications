#!/bin/sh
api="k-xxxxxx"

profile_file="$(ls -at profile* | head -n1)"
corrector_profile="$(cat $profile_file | grep -A1 "evaluate"| sed -n -e 's/^.*href="//p' | sed 's/\">.*//')"
corrector_login="$(cat $profile_file | grep -A1 "evaluate"| grep -A1 "evaluate"| sed -n -e 's/^.*data-tooltip-login="//p'| sed 's/\".*//')"
day="$(cat $profile_file | grep -A3 "force_relative"| sed -n -e "s/^.*title='//p"| sed 's/\+.*//' | awk '{ print $1 }' | head -n1)"
hour="$(cat $profile_file | grep -A3 "force_relative"| sed -n -e "s/^.*title='//p"| sed 's/\+.*//' | awk '{ print $2 }' | head -n1)"
project="$(cat $profile_file | grep -A1 "evaluate"| grep -A5 "evaluate" | tail -n1 | awk '{print $2}')"
check_if_you_are_corrector="$(cat $profile_file | grep -A1 "evaluate" | head -n1 | awk '{ print $1 $2 $3 $4 $5 }')"
project_correction="$(cat $profile_file | grep -A1 "evaluate" | head -n1 | awk '{ print $6 }')"

correction_check="$day/$hour"
#rm profile*
#python3 corrections-bot.py >> execution.log 2>&1
echo "Variable:::"
echo "\n\n"

echo "corrector_login:\n"
echo $corrector_login
echo "project:\n"
echo $project
echo "day:\n"
echo $day
echo "hour:\n"
echo $hour
echo "\n\n"
var=1

if [ -z corrector.tmp ]
then
	echo "corrector.tmp found.."
else
	touch corrector.tmp
fi

if [ -z $corrector_login ] && [ -z $check_if_you_are_corrector ]
then
	echo "No Corrections"
else
	while [ $var -le $(cat corrector.tmp | wc -l) ]
	do
		echo "Checking if a notification was already send.."
		check_corrector="$(cat corrector.tmp |head -n $var | tail -n 1)"
		if [ "$corrector_login" = "$check_corrector" ] || [ "$correction_check" = "$check_corrector" ]
		then
			echo "Notification already sent, exiting.."
			exit
		fi
		var=$((var+1))
	done
	echo "Checking done.."
	if [ $check_if_you_are_corrector = "Youwillevaluatesomeone" ] || [ $check_if_you_are_corrector = "Youarereadytoevaluate" ]
	then
		echo "Correction Found!"
		echo "You'll correct someone"
		curl http://xdroid.net/api/message\?k\=$api\&t\=Correction+Found\&c\=You+will+evaluate+someone+on+$project_correction+at+$hour+the+$day\&u\=https://profile.intra.42.fr &
		echo "$day/$hour" >> corrector.tmp
		echo "$(cat corrector.tmp)" | tail -n1
	else
		echo "Correction Found!"
		echo "$corrector_login" >> corrector.tmp
		curl http://xdroid.net/api/message\?k\=$api\&t\=Correction+Found+with+$corrector_login\&c\=You+have+a+correction+with+$corrector_login+at+$hour+the+$day+on+the+project+$project\&u\=$corrector_profile &
	fi
fi
