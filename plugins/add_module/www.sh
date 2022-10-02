#!/bin/bash

copyWWW() {
	local modulefolder="modules/$modulename"
	local modulewwwfolder="$modulefolder/www"
	local nginxwwwfolder="data/www/"
	local wwwenvfiles=( "index" "config" "global" ) # a file containing these strings in its name
	local nginxmodulewwwfolder="${nginxwwwfolder}/${modulename}_${mandant,,}"

	if [ -d "$modulewwwfolder" ] && ! [ -d "$nginxmodulewwwfolder " ]; then
		greenecho "   Found folder 'www' in module '$modulename'"

		if ! [ -d "$nginxwwwfolder" ]; then
			orangeecho "      creating '$nginxwwwfolder' ..."
			mkdir -p "$nginxwwwfolder" --verbose
		fi
		
		if ! [ -d "$nginxmodulewwwfolder" ]; then
			orangeecho "      copying 'www' ..."
			cp -R "$modulewwwfolder" "$nginxmodulewwwfolder"
		else
			greenecho "      not copying as already existing at target '$nginxmodulewwwfolder'"
		fi

		orangeecho "      configuring environment of the copied folder ..."
		local _ls=`ls "$modulewwwfolder"` # for performance reason we cache the result
		for substcandidate in "${wwwenvfiles[@]}"; do
			local wwwenvfile=`echo "$_ls" | grep "$substcandidate"`
			if [ -z "$wwwenvfile" ]; then continue; fi
			echo "$substcandidate"
			(source ./$mandantFile ; export projectname="$projectname" 
			envsubst < "$modulewwwfolder/$wwwenvfile" > "$nginxmodulewwwfolder/$wwwenvfile" )
		done
	else
		greenecho "   Does not exist, skipping ..."
	fi
}

blueecho "PLUGIN: Copy WWW folder"
copyWWW