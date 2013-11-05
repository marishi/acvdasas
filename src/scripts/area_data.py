from xml.dom import minidom
import logging

class Base:
	base_id = 0
	name = ""
	image_url = ""

class AreaData:
	area_id = 0
	name = ""
	
	special_base = Base()
	hacking_base = Base()

	def __init__(self):
		self.front_base_dict = {}
	
	def getFrontBaseDict(self):
		return self.front_base_dict

def getText(nodelist):
	rc = ""
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc =  rc + node.data
	return rc

def readBase(area_node,image_url):
	base_dict = {}
	for base_node in area_node.getElementsByTagName('base'):

		base = Base()

		base.base_id = int( base_node.getAttribute("id") )
		
		base.name = getText( base_node.getElementsByTagName('base_name')[0].childNodes )
		base.image_url = image_url + getText( base_node.getElementsByTagName('image_file')[0].childNodes )
	
		base_dict[base.base_id] = base

	return base_dict



def readXml():
	
	dom = minidom.parse('static_data/area_data.xml')

	area_dict = {}

	for area_node in dom.getElementsByTagName('area'):
		area_data = AreaData()
		
		area_data.name = getText( area_node.getElementsByTagName('area_name')[0].childNodes )
		area_data.area_id = int( area_node.getAttribute("id") )

		sp_id = int( area_node.getAttribute("special_id") )
		hc_id = int( area_node.getAttribute("hacking_id") )

		image_url = getText( area_node.getElementsByTagName('url')[0].childNodes )

		base_dict = readBase(area_node,image_url)
		
		area_data.special_base = base_dict[sp_id]
		area_data.hacking_base = base_dict[hc_id]

		area_data.getFrontBaseDict().update( base_dict )
		area_dict[area_data.area_id] = area_data

	return area_dict


dictionary = readXml()
