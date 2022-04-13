#!/bin/python3 
import yaml, os, sys

def redprint(text):
	print("\033[1;31m{}\033[0;m".format(text))
	
def orangeprint(text):
	print("\033[1;33m{}\033[0;m".format(text))

extensionsPath=""

for path in ["trufi-server", "trufi-server-cities"]:
	if os.path.exists(path):
		extensionsPath = os.path.join(path, "extensions")

if extensionsPath == "":
	redprint("Error: init script not executed properly")
	sys.exit(1)

orangeprint("patching extensions ...")
for ext in os.listdir(extensionsPath):
	extDir = os.path.join(extensionsPath, ext)
	orangeprint("  modifying extension '{}' ('{}') ...".format(ext, extDir))
	if os.path.exists(os.path.join(extDir, "data")):
		os.rename(os.path.join(extDir, "data"), os.path.join(extDir, "data_template"))
		
	for compose in ["docker-compose.yml", "docker-compose.yml.inactive"]:
		composefile = os.path.join(extDir, compose)
		if os.path.exists(composefile):
			sfile = open(composefile, "r")
			dockercompose = yaml.safe_load(sfile.read())
			sfile.close()
			os.remove(composefile)
			
			servicesToRename = []
			for service in dockercompose["services"]:
				servicesToRename.append(service)
				print("    service '{}'".format(service))
				if "volumes" in dockercompose["services"][service]:
					print("      volume configuration ...")
					for index, content in enumerate(dockercompose["services"][service]["volumes"]):
						volumeConf = content.split(":", 1)
						hostVolumePart = volumeConf[0]
						del volumeConf[0]
						normalize = hostVolumePart.lower().replace("./", "").replace("/", "")
						if "data" == normalize:
							dockercompose["services"][service]["volumes"][index] = hostVolumePart.replace("data", "data_$city") + ":" + ":".join(volumeConf)
				if "ports" in dockercompose["services"][service]:
					print("      remove port binding ...")
					del dockercompose["services"][service]["ports"]
			
			for service in servicesToRename:
				print("      renaming to '{}' ...".format(service + "_$city"))
				dockercompose["services"][service + "_$city"] = dockercompose["services"][service]
				del dockercompose["services"][service]
				
			sfile = open("docker-compose.yml", "w")
			sfile.write(yaml.dump(dockercompose, sort_keys=False, default_flow_style=False))
			sfile.close()
