#!/bin/bash

# perform iteration over all affected docker-compose files to only to populate variable 'citiesPerModule' without performing actions
performIteration "noexecute"

# iterate through associative array 'citiesPerModule'
cd modules
for module in "${!citiesPerModule[@]}"; do # e.g. tileserver, otp, photon
	orangeecho "in module '$module'"
	cd "$module"
	cities=( ${citiesPerModule[$module]} )
	for nameOfCity in "${cities[@]}"; do # e.g. tileserver: Ghana-Accra, Germany-Hamburg
		orangeecho "  of city '$nameOfCity'"
		# get names of all services of that city in the module
		allServices=`sudo docker-compose -p "$projectname" -f "${nameOfCity}.yml" ps --services`
		allServices=( $allServices )
		
		# get running services of that city in the module
		runningServices=`sudo docker-compose -p "$projectname" -f "${nameOfCity}.yml" ps`
		length=${#runningServices[@]}
		
		# iterate through names of all services of that city in the module
		for servicename in "${allServices[@]}"; do # e.g. tileserver-ghana-accra, tileserver-germany-hamburg
			isRunning=`sudo docker container ls | grep "${projectname}-${servicename}"` # prints a status line if the container with the name '${projectname}-${servicename}' is running otherwise it prints nothing
			if [ -n "$isRunning" ]; then
				orangeecho "    - updating docker service '$servicename' without downtime ..."
				
				# obtain container id of service 'servicename' of that city in the module
				IFS=" "
				curContainerId=( $isRunning ) # recycling variable 'isRunning'
				curContainerId="${curContainerId[0]}"
				
				# create a new container of service 'servicename' (scale up)
				sudo docker-compose -p "$projectname" -f "${nameOfCity}.yml" up --detach --scale ${allServices[$i]}=2 --no-recreate ${allServices[$i]}
				
				sleep 5 # TODO: healtheck instead of waiting five seconds in hope this is enough for the startup process
				
				# remove old container
				sudo docker rm -f "$curContainerId"
				
				# scale back
				sudo docker-compose -p "$projectname" -f "${nameOfCity}.yml" up --detach --scale ${allServices[$i]}=1 --no-recreate ${allServices[$i]}
			else
				orangeecho "    - wiring up a docker container for service '$servicename' ..."
				sudo docker-compose -p "$projectname" -f "${nameOfCity}.yml" up --build --detach
			fi
		done
	done
	cd ../
done
cd ../
