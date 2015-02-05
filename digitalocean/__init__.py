import urllib.request
import json
import re
from .  import util
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
from urllib.error import HTTPError as HTTPError

class Manager:
	droplets = []
	def __init__(self):
		self.base_url = 'https://api.digitalocean.com/v1/'
	
	def auth(self, client_id, api_key):
		self.auth = {'client_id': client_id, 'api_key': api_key}
		
		try:
			self.getDropletById(1)
		except HTTPError as e:
			raise Exception(e)
		except Exception:
			#Droplet doesn't exist but it did authenticate
			return;
	
	def getDropletById(self, droplet_id):
		parameters = util.toQueryString(self.auth)
		
		response = urllib.request.urlopen(self.base_url + "droplets/" + str(droplet_id) + "?" + parameters)
		result = json.loads(response.read().decode())
		
		if result and result["status"] == "OK":
			return result["droplet"]
		else:
			raise Exception(result["status"] + " - " + result["message"])
	
	def loadDroplets(self):
		parameters = util.toQueryString(self.auth)

		response = urllib.request.urlopen(self.base_url + "droplets/"+"?" + parameters)
		result = json.loads(response.read().decode())
		
		if result and result["status"] == "OK":
			self.droplets = result["droplets"]		
		else:
			raise Exception(result["status"] + " - " + result["message"])
			
	def listDroplets(self, droplets=[]):
		if not droplets:
			self.loadDroplets()
			droplets = self.droplets
		
		table = PrettyTable(['ID', 'Name', 'IP', 'P-IP', 'Locked', 'Status']);
		
		for droplet in droplets:
			table.add_row([droplet["id"], droplet["name"], droplet["ip_address"], droplet["private_ip_address"], droplet["locked"], droplet["status"]])
		
		print(table)
	
	def getFullDropletId(self, droplet_id):		
		pattern = re.compile(str(droplet_id))
		result = list()
		for droplet in self.droplets:
			if pattern.match(str(droplet["id"])):
				result.append(droplet)
		
		if not result:
			raise Exception("Invalid Droplet ID")
		elif len(result) > 1:
			print("Multiple choices")
			self.listDroplets(result)
			raise Exception("")
		else:
			return result[0]["id"]
	
	def actionDroplet(self, droplet_id, action):
		self.loadDroplets();
		droplet_id = self.getFullDropletId(droplet_id);
		
		parameters = util.toQueryString(self.auth)
		
		response = urllib.request.urlopen(self.base_url + "droplets/" + str(droplet_id) + "/" + action + "/"+"?" + parameters)
		result = json.loads(response.read().decode())
		
		if result["status"] == "OK":
			print(result["status"])
		else:
			raise Exception(result["status"] + " - " + result["message"])
	def startDroplet(self, droplet_id):
		self.actionDroplet(droplet_id, "power_on")
		
	def stopDroplet(self, droplet_id):
		self.actionDroplet(droplet_id, "shutdown")
		
	def restartDroplet(self, droplet_id):
		self.actionDroplet(droplet_id, "power_cycle")

	def poweroffDroplet(self, droplet_id):
		self.actionDroplet(droplet_id, "power_off")
		
	def listDroplet(self, droplet_id):
		self.loadDroplets();
		droplet_id = self.getFullDropletId(droplet_id);
		
		parameters = util.toQueryString(self.auth)
		
		response = urllib.request.urlopen(self.base_url + "droplets/" + str(droplet_id) + "?" + parameters)
		result = json.loads(response.read().decode())
		
		if result and result["status"] == "OK":
			table = PrettyTable(border=True, header=False, padding_width=5, padding_height=5);
			table.add_row(["ID", result["droplet"]["id"]])
			table.add_row(["Name", result["droplet"]["name"]])
			table.add_row(["IP", result["droplet"]["ip_address"]])
			table.add_row(["Status", result["droplet"]["status"]])
			print(table)
		else:
			raise Exception(result["status"] + " - " + result["message"])