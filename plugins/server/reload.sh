#!/bin/bash 

# reload action for 'nginx' hardcoded as this is the main module not dynamically add-/removeable
if [ "$curModule" = "nginx" ]; then
	orangeecho "reloading nginx configuration without the need to restart nginx ..."
	citiesPerModule["./"]="docker-compose"
	curAction="exec"
	curActionArgs="chief-nginx nginx -s reload"
	performExecution
else
	# check if a modfunctions.sh exists for the module
	if [ -f "./modules/$curModule/modfunctions.sh" ]; then
		source "./modules/$curModule/modfunctions.sh"
		if [ -n "$modreload" ]; then
			curAction="exec"
			for reloadCMD in "${modreload[@]}"; do
				curActionArgs="$reloadCMD" # e.g. tileserver killall -HUP tileserver-gl
				#                                   |
				#                                   --> name of the service without '-${city_normalize}' because will be appended & expanded below
				#orangeecho "Executing \033[0;34m${curActionArgs}\033[0;m inside container '${curActionArgs[0]}-${city,,}' in module '$curModule' of city '$city' ..."
				curActionArgs=( $curActionArgs )
				curActionArgs[0]=${curActionArgs[0]}-${city,,} # name of the service (appended & expanded)
				curActionArgs="${curActionArgs[@]}"
				performExecution
			done
		else
			redecho "No reloading strategy found for module '$curModule'"
		fi
	fi
fi

exit 0
