#!/bin/python3 
import yaml, os, sys

def redprint(text):
	print("\033[1;31m{}\033[0;m".format(text))
	
def orangeprint(text):
	print("\033[1;33m{}\033[0;m".format(text))

modulesPath="modules"

if not os.path.exists(modulesPath):
	redprint("Error: init script not executed properly")
	sys.exit(1)

orangeprint("patching modules ...")
for module in os.listdir(modulesPath):
	if module.find("_") > -1:
		os.rename(os.path.join(modulesPath, module), os.path.join(modulesPath, module.replace("_", "-")))
		module = module.replace("_", "-")
	moduleDir = os.path.join(modulesPath, module)
	if os.path.exists(os.path.join(moduleDir, "data")):
		print("    renaming directory 'data' to 'data_template' ...")
		os.rename(os.path.join(moduleDir, "data"), os.path.join(moduleDir, "data_template"))
		
	composefile = os.path.join(moduleDir, "docker-compose.yml")

	if os.path.exists(composefile):
		orangeprint("  modifying module '{}' ('{}') ...".format(module, moduleDir))
		sfile = open(composefile, "r")
		dockercompose = yaml.safe_load(sfile.read())
		sfile.close()
		os.remove(composefile)
		
		servicesToRename = []
		for service in dockercompose["services"]:
			addToRenameList = False
			if not service.endswith("-$city_normalize"):
				addToRenameList = True
			if 2 > service.count(module):
				addToRenameList = True
			if addToRenameList:
				servicesToRename.append(service)
			print("    service '{}'".format(service))
			if "volumes" in dockercompose["services"][service]:
				for index, content in enumerate(dockercompose["services"][service]["volumes"]):
					volumeConf = content.split(":", 1)
					hostVolumePart = volumeConf[0]
					del volumeConf[0]
					normalize = hostVolumePart.lower().replace("./", "").replace("/", "")
					if normalize.find("data") > -1:
						print("      volume configuration ...")
						dockercompose["services"][service]["volumes"][index] = hostVolumePart.replace("data", "data_$city") + ":" + ":".join(volumeConf)
			if "ports" in dockercompose["services"][service]:
				print("      remove port binding ...")
				del dockercompose["services"][service]["ports"]
			
		for service in servicesToRename:
			newName = module + "-" + service.replace("-$city_normalize", "") + "-$city_normalize"
			print("      renaming to '{}' ...".format(newName))
			dockercompose["services"][newName] = dockercompose["services"][service]
			del dockercompose["services"][service]
			
		dockercompose["networks"]["default"]["name"] = "$projectname"
				
		sfile = open(os.path.join(moduleDir, "docker-compose.yml"), "w")
		sfile.write(yaml.dump(dockercompose, sort_keys=False, default_flow_style=False))
		sfile.close()
