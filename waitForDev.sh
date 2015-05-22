#!/bin/bash


onNewDevice() {
	/usr/bin/diff <(echo "$1") <(echo "$2") | grep ">" | cut -c 3-
}

deamon() {

	dir="$(ls -1 /Volumes/)"
	chsum1=`ls /Volumes/ | md5`

	while [[ true ]]
	do
		chsum2=`ls /Volumes/ | md5`
		if [[ $chsum1 != $chsum2 ]] ; then
			onNewDevice "$dir" "$(ls -1 /Volumes/)"
			break
		fi
		sleep 2
	done
}


deamon
