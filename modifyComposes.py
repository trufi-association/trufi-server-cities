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
for ext in os.listdir(modulesPath):
	extDir = os.path.join(modulesPath, ext)
	if os.path.exists(os.path.join(extDir, "data")):
		print("    renaming directory 'data' to 'data_template' ...")
		os.rename(os.path.join(extDir, "data"), os.path.join(extDir, "data_template"))
		
	composefile = os.path.join(extDir, "docker-compose.yml")
	if os.path.exists(composefile):
		orangeprint("  modifying module '{}' ('{}') ...".format(ext, extDir))
		sfile = open(composefile, "r")
		dockercompose = yaml.safe_load(sfile.read())
		sfile.close()
		os.remove(composefile)
		
		servicesToRename = []
		for service in dockercompose["services"]:
			if not service.endswith("-$city_normalize"):
				servicesToRename.append(service)
			print("    service '{}'".format(service))
			if "volumes" in dockercompose["services"][service]:
				for index, content in enumerate(dockercompose["services"][service]["volumes"]):
					volumeConf = content.split(":", 1)
					hostVolumePart = volumeConf[0]
					del volumeConf[0]
					normalize = hostVolumePart.lower().replace("./", "").replace("/", "")
					if "data" == normalize:
						print("      volume configuration ...")
						dockercompose["services"][service]["volumes"][index] = hostVolumePart.replace("data", "data_$city") + ":" + ":".join(volumeConf)
			if "ports" in dockercompose["services"][service]:
				print("      remove port binding ...")
				del dockercompose["services"][service]["ports"]
			
		for service in servicesToRename:
			print("      renaming to '{}' ...".format(service + "-$city_normalize"))
			dockercompose["services"][service + "-$city_normalize"] = dockercompose["services"][service]
			del dockercompose["services"][service]
				
		sfile = open(os.path.join(extDir, "docker-compose.yml"), "w")
		sfile.write(yaml.dump(dockercompose, sort_keys=False, default_flow_style=False))
		sfile.close()
