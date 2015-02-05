def toQueryString(map):
	return '&'.join([str(q) + '=' + str(map[q]) for q in map]);
	
def manual():
	man = "Usage:\n droplet-manager <option> <arg>\n\n"
	man += "droplet-manager list : Lists all droplets\n"
	man += "droplet-manager list ID: List droplet\n"
	man += "droplet-manager start ID: start droplet\n"
	man += "droplet-manager stop ID: stop droplet\n"
	man += "droplet-manager restart ID: restart droplet\n"
	man += "\n\n ID = regex E.g: ^3.*\n"
	return man