#!/bin/sh
api=""

profile_file="$(ls -at profile* | head -n1)"
corrector_profile="$(cat $profile_file | grep -A1 "evaluate"| sed -n -e 's/^.*href="//p' | sed 's/\">.*//')"
corrector_login="$(cat $profile_file | grep -A1 "evaluate"| grep -A1 "evaluate"| sed -n -e 's/^.*data-tooltip-login="//p'| sed 's/\".*//')"
day="$(cat $profile_file | grep -A3 "force_relative"| sed -n -e "s/^.*title='//p"| sed 's/\+.*//' | awk '{ print $1 }' | head -n1)"
hour="$(cat $profile_file | grep -A3 "force_relative"| sed -n -e "s/^.*title='//p"| sed 's/\+.*//' | awk '{ print $2 }' | head -n1)"
project="$(cat $profile_file | grep -A1 "evaluate"| grep -A5 "evaluate" | tail -n1 | awk '{print $2}')"

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

if [ -z "$(cat corrector.tmp)" ]
then
	touch corrector.tmp
fi

if [ -z $corrector_login ]
then
	echo "No Corrections"
else
	while [ $var -le $(cat corrector.tmp | wc -l) ]
	do
		check_corrector="$(cat corrector.tmp |head -n $var | tail -n 1)"
		if [ $corrector_login = $check_corrector ]
		then
			exit
		fi
		var=$((var+1))
	done
	echo "Correction Found!"
	echo "$corrector_login" > corrector.tmp
	nohup curl http://xdroid.net/api/message\?k\=$api\&t\=Correction+Found+with+$corrector_login\&c\=You+have+a+correction+with+$corrector_login+at+$hour+the+$day+on+the+project+$project\&u\=$corrector_profile &
fi
