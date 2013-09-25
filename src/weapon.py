from xml.dom import minidom

def getText(nodelist):
	rc = ""
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc = rc + node.data
	return rc

class Weapon:
	name = ""
	impact = 0

def readWeapon():
	dom = minidom.parse("static_data/weapon.xml")
	
	weapon_list = []
	for weapon_nodes in dom.getElementsByTagName("weapon"):
		weapon = Weapon()
		name_node = weapon_nodes.getElementsByTagName("name")[0]
		weapon.name = getText(name_node.childNodes)

		impact_node = weapon_nodes.getElementsByTagName("impact")[0]
		weapon.impact = int(getText(impact_node.childNodes))

		weapon_list.append(weapon)

	return weapon_list

__weapon_list = readWeapon()

def getWeapons():
	return __weapon_list[:]

