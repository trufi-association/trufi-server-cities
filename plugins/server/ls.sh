#!/bin/bash
# docker trufi name convention:
#  Syntax : <projectname>_<modulename>-<servicename>-<city>_<a number>
#  Example: city-services_tileserver-tileserver-germany-hamburg_1

# Query construction to filter container names (positive filter)
##  Syntax : <projectname>_<modulename>-<servicename>-<city>_<a number>
##           ..............
query="${projectname}_" # match $projectname by default and always

##  Syntax : <projectname>_<modulename>-<servicename>-<city>_<a number>
##                         ............
if [ -n "$curModule" ]; then
	query+="${curModule}-" # and match module $curModule e.g. match module 'tileserver'
else
	query+=".*-" # and match any modules
fi

##  Syntax : <projectname>_<modulename>-<servicename>-<city>_<a number>
##                                      ..............
query+=".*-" # and match any services

##  Syntax : <projectname>_<modulename>-<servicename>-<city>_<a number>
##                                                    ...... 
if [ "$cityScope" = "city" ]; then
	query+="${city,,}" # and match city ${city,,} e.g. match city 'germany-hamburg'
else
	query+=".*" # and match any cities
fi

if [ -z "$curActionArgs" ]; then
	curActionArgs=(--format "\"table {{.Names}} \t {{.CreatedAt}} \t {{.Status}}\"" --no-trunc)
fi
# get status table
#                                get results of query,
#                                        get chief services
#                                                              and the status table heading
#sudo docker container ls --format "table {{.Names}} \t {{.CreatedAt}} \t {{.Status}}" --no-trunc | grep "$query\|${projectname}_chief\|NAMES"
body=`eval sudo docker container ls ${curActionArgs[@]}`
heading=`echo "$body" | sed -ne "1p"`
body=`echo "$body" | grep "$query\|${projectname}_chief"`

body=${body//chief-/"\033[0;35mchief\033[0;m-"}
echo -e "\033[1;37m${heading}\033[0;m"
echo -e "$body"

# This script does not touch the amount of running modules, their services and also does not touch the amount of chiefes so it is a good practise to exit at this time
# Otherwise the `server` script performs a costly calculation if something has been started/stopped/upped/downed.
exit 0
