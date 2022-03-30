#!/bin/python3
import sys, os, shutil, re, multipurpose_files as lib
from time import time
args = lib.cmdArgs

# General section
if not len(args) == 0:
	lib.Utils.printError("Error: extension name as param is needed (e.g. 'tileserver')")

environment = lib.Utils.deserializeConfig(lib.currentConfigFile) # load conf file for environment

extensionname = args[0]
extensionDir = os.path.join(lib.extensionsDir, extensionname)
if not os.path.exists(extensionDir) or not os.path.isDir(extensionDir):
	lib.Utils.printError("Error: extension '{}' is not a valid one. Valid ones are listed below:".format(extensionname), exit=False)
	for extdir in os.listdir(lib.extensionsDir):
		if os.path.isdir(os.path.join(lib.extensionsDir, extdir)):
			lib.Utils.printError(extdir, exit=False)
	sys.exit(1)

# Adding extension
print("adding extension '{}' ...".format(extensionname))

## add nginx config
nginxCityFile = os.path.join(lib.inc_extensionDir, extensionname + ".conf")
if not os.path.exists(nginxCityFile):
	### copy nginx configuration specified to the extension to add
	print("adding nginx configuration ...")
	shutil.copyfile(os.path.join(extensionDir, "nginx.conf"), nginxCityFile)

	### modifying the copied nginx config to add city variability
	sfile = open(nginxCityFile, "r")
	inputNginxConfig = sfile.read()
	sfile.close()

	lines = inputNginxConfig.split("\n")
	index = 0
	for line in lines:
		line = line.strip()
		if line.startswith("proxy_pass"):
			hostname = re.search(r'http://(.+?)/', line, re.IGNORECASE).group(0)
			lines[index] = line.replace(hostname, hostname + "-$city")
		index += 1
	
	sfile = open(nginxCityFile, "w")
	sfile.write("\n".join(lines))
	sfile.close()


## integrate docker-compose file of extension
dockercompose = os.path.join(lib.extensionsDir, extensionname, "docker-compose.yml.inactive")
if os.path.exists(dockercompose):
	lib.Utils.printError("Error: '{}' does not exist".format(dockercompose))

### migrate into multipurpose* docker-compose file
dockercompose = lib.Dockercompose(dockercompose, None)
multipurpose = lib.Dockercompose(lib.runConfiguration["dockercompose"], environment)
for service in dockercompose.getAllServiceNames():
	multipurpose.addService(dockercompose.getService(service))

# If nginx is running then build/start the extension and restart nginx afterwards
# Name of "nginx" container is hardcoded here
nginxActive = lib.Utils.executeAndReturn("sudo docker-compose -f {} ps".format(lib.runConfiguration))

if nginxActive.find("nginx") > -1:
	print("  building or starting the extension ...")
	for services in multipurpose.getOnlyServiceNamesOfCurrentEnvironment():
		print("    {} ...".format(service))
		lib.Utils.execute("sudo docker-compose -f {} {} up --detach".format(lib.runConfiguration, service))
	print("  waiting 5 seconds before attempting to restart nginx ...")
	time.sleep(5)
	print("restarting nginx of '{}' ...".format(multipurpose.filename))

print("trufi extension installed")
sys.exit(0)