#!/bin/bash

noTouchDataWWW() {
	local nginxwwwfolder="data/www"
	local nginxmodulewwwfolder="$nginxwwwfolder/${modulename}_${city,,}"

	if [ -d "$nginxmodulewwwfolder" ]; then
		blueecho "   Will NOT delete the content at '$nginxmodulewwwfolder'"
	fi
}

blueecho "PLUGIN: NOT removing WWW folder"
noTouchDataWWW