#!/bin/python3
from distutils import extension
import os, sys, yaml, subprocess

cmdArgs = sys.argv
del cmdArgs[0]

extensionsDir = "extensions"
configDir = "config"
incDir = "inc"
inc_extensionDir = os.path.join(incDir, "extensions")

for directory in [incDir, inc_extensionDir]:
	if os.path.exists(directory) and os.path.isdir(directory):
		os.mkdir(directory)

nginxEnvConfFile = os.path.join(incDir, "envs.conf")

currentConfigFile = ""

runConfiguration = {
	"production": {
		"nginxconfig": "data/nginx/app.conf",
		"dockercompose": "multipurpose.yml"
	},
	"development": {
		"nginxconfig": "dev/app.conf",
		"dockercompose": "multipurpose.dev.yml"
	}
}

# Helper classes
class CityEnvironBase:
	
	def get(self, key):
		return getattr(self, key)
	
	def set(self, key, value):
		setattr(self, key, value)

	def exists(self, key):
		return hasattr(self, key)

class Utils:
	prefixBeginMarker = "-"
	convertMinusTo = "_"

	@staticmethod
	def execute(cmdline):
		if type(cmdline) is str:
			cmdline = cmdline.split(" ")
		subprocess.Popen(cmdline, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin)
	
	@staticmethod
	def executeAndReturn(cmdline):
		if type(cmdline) is str:
			cmdline = cmdline.split(" ")
		return subprocess.run(cmdline, stdout=subprocess.PIPE).stdout.decode("utf-8")
	@staticmethod
	def printError(text, exit=True):
		print(text, file=sys.sys.stderr)
		if exit:
			sys.exit(1)

	@staticmethod
	def normalizePrefix(prefix):
		return prefix.replace(Utils.prefixBeginMarker, Utils.convertMinusTo).lower()

	@staticmethod
	def insertsPrefix(string, prefix):
		return string + "-" + Utils.normalizePrefix(prefix)
	
	@staticmethod
	def extractPrefix(string):
		splitted = string.split(Utils.prefixBeginMarker)
		return splitted[len(splitted)-1]

	@staticmethod
	def hasPrefix(string, prefix=None):
		if prefix == None:
			return string.find(Utils.prefixBeginMarker) > -1
		if string.find(Utils.prefixBeginMarker) > -1 and Utils.extractPrefix(string) == prefix:
			return True
		return False

	@staticmethod
	def deserializeConfig(self, filename):
		attributes = { "city": filename.replace(".env", "") }

		sfile = open(filename, "r")
		content = sfile.read()
		sfile.close()
		
		for line in content.split("\n"):
			for key, value in line.split("=", 1):
				try:
					attributes[key] = int(value)
				except:
					attributes[key] = value

		attributes["city"] = Utils.normalizePrefix(attributes["city"])

		return type("Environ", (CityEnvironBase, ), attributes)

# for config
class Dockercompose:
	yaml = {}
	environ = None
	
	def __init__(self, filename, environ=None):
		sfile = open(filename, "r")
		self.yaml = yaml.safe_load(sfile.read())
		self.environ = environ
		self.filename = filename
		sfile.close()

	def getAllServiceNames(self):
		return list(self.yaml["services"].keys())
	
	def getOnlyServiceNamesOfCurrentEnvironment(self):
		services = self.getAllServiceNames()
		servicesAtTheEnd = []
		
		for service in services:
			if Utils.hasPrefix(service, self.environ.city):
				servicesAtTheEnd.append(service)
		
		return servicesAtTheEnd
	
	def removeService(self, service):
		del self.yaml[service]

	def getService(self, service):
		return self.yaml[service]
	
	def addService(self, service, extensionname, content):
		# apply convention regarding the 'data' directory
		if "volumes" in content:
			index = 0
			for volume in content["volumes"]:
				host, container = volume.split(":", 1)
				if host.endswith("data"):
					prefixedDataDir = "data-" + self.environ.city
					os.mkdir(os.path.join(extensionsDir, extensionname, prefixedDataDir))
					content["volumes"][index] = host.replace("data", prefixedDataDir) + ":" + container
				index += 1
		
		# apply convention regarding the name of the service
		prefixedServiceName = Utils.insertsPrefix(service, self.environ.city)
		self.yaml[prefixedServiceName] = content
		
		return prefixedServiceName
	

def checkForAnyExistenceOfRunConfiguration():
	global runConfiguration
	active = 0
	for env in runConfiguration:
		if os.path.exists(runConfiguration[env]["nginxconfig"]) and os.path.exists(runConfiguration[env]["dockercompose"]):
			active += 1
			runConfiguration = runConfiguration[env]
	
	if active == 0:
		print("Error: neither the development and the production environment are initialized. Please initialize them first using one of the 'init' scripts we provided.")
		sys.exit(1)

def checkIfConfigFileHasBeenSpecified():
	global currentConfigFile, configDir, cmdArgs

	if len(cmdArgs) == 0:
		Utils.printError("Error: config file as param is needed (e.g. 'Bolivia-Cochabamba')", file=sys.sys.stderr)
	
	currentConfigFile = cmdArgs[0].replace(".env", "")
	if os.path.exists(os.path.join(configDir, currentConfigFile)):
		currentConfigFile = os.path.join(configDir, currentConfigFile)
	
	del cmdArgs[0]

def initIncFolder():
	global nginxEnvConfFile
	sfile = open(nginxEnvConfFile, "w")
	sfile.write("")
	sfile.close()


checkForAnyExistenceOfRunConfiguration()
checkIfConfigFileHasBeenSpecified()