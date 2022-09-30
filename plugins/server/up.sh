#!/bin/bash

# pleasant up
pleasantUp() {
	local module="$1"
	local nameOfCity="$2"
	# get names of all services of that city in the module
	allServices=`sudo docker compose -p "$projectname" -f "${nameOfCity}.yml" config --services`
	allServices=( $allServices )
	
	# iterate through names of all services of that city in the module
	for servicename in "${allServices[@]}"; do # e.g. tileserver-ghana-accra, tileserver-germany-hamburg
		isRunning=`sudo docker container ls | grep "${projectname}.${servicename}"` # prints a status line if the container with the name '${projectname}-${servicename}' is running otherwise it prints nothing
		if [ -n "$isRunning" ]; then
			orangeecho "    - updating docker service '$servicename' without downtime ..."
			
			# obtain container id of service 'servicename' of that city in the module
			IFS=" "
			curContainerId=( $isRunning ) # recycling variable 'isRunning'
			curContainerId="${curContainerId[0]}"
			
			# create a new container of service 'servicename' (scale up)
			sudo docker compose -p "$projectname" -f "${nameOfCity}.yml" up --detach --scale $servicename=2 --no-recreate $servicename
			
			sleep 5 # TODO: healtheck instead of waiting five seconds in hope this is enough for the startup process
			
			# remove old container
			sudo docker rm -f "$curContainerId"
			
			# scale back
			sudo docker compose -p "$projectname" -f "${nameOfCity}.yml" up --detach --scale $servicename=1 --no-recreate $servicename
		else
			orangeecho "    - wiring up a docker container for service '$servicename' ..."
			sudo docker compose -p "$projectname" -f "${nameOfCity}.yml" up --build --detach $servicename
		fi
	done
}
# perform iteration over all affected docker-compose files
# - to populate variable 'citiesPerModule'
# - and to literate over the populated variable and call our own 'plesantUp' with each city value
performIteration "execute" pleasantUp
