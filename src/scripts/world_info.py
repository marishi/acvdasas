# -*- coding: utf-8 -*- 

import urllib2
import re
from google.appengine.ext import db

class Area(db.Model):
	area_num = db.IntegerProperty()
	base_num = db.IntegerProperty()
	durability = db.IntegerProperty()
	backbone = db.IntegerProperty()
	date = db.DateTimeProperty(auto_now_add=True)


class WorldInformation:

	html = ""

	def init(self):
		url = 'http://acvdlink.armoredcore.net/p/acop/acvdlink/'
		op = urllib2.urlopen(url)
		self.html = op.read()
		op.close()


	#エリアの情報を取得します
	def current_areas(self):
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
		
			a = Area()
			a.area_num = int(arnum)
			a.base_num = int(data[5])
			a.durability = int(data[9])
			a.backbone = int(data[12])
			areas.append( a )

		return areas


