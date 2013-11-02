# -*- coding: utf-8 -*- 

import urllib2
import re

class Area:
	
	def __init__(self, area_num, base_num, durability, backbone):
		self.area_num = area_num
		self.base_num = base_num
		self.durability = durability
		self.backbone = backbone

class WorldInformation:

	html = ""

	def init(self):
		url = 'http://acvdlink.armoredcore.net/p/acop/acvdlink/'
		op = urllib2.urlopen(url)
		self.html = op.read()
		op.close()


	#エリアの情報を取得します
	def areas(self):
		#areainfoを取得する
		areas_regstr = "valArr\[\"areainfo\"\] = \[((?:.|\\n)+?)\];"
		match = re.search(areas_regstr, self.html)	

		areainfo = match.group(1)

		#各エリアに分割
		area_strs = re.findall("\[((?:.|\n)+?)\]",areainfo)
	
		areas = []
		#最初の要素はコメントなので無視
		for area in area_strs[1:]:
			data = area.split(',')
			arnum = re.search("([0-9])+",data[0]).group(1)
			a = Area(int(arnum),  int(data[5]) ,int(data[9]), int(data[12]))
			areas.append( a )

		return areas


