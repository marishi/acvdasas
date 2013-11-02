# coding: utf-8

import webapp2
import datetime
from google.appengine.ext import db
import world_info

class Area(db.Model):

	area_num = db.IntegerProperty()
	base_num = db.IntegerProperty()
	durability = db.IntegerProperty()
	backbone = db.IntegerProperty()
	date = db.DateTimeProperty(auto_now_add=True)

	def setArea(self, world_area):
		self.area_num = world_area.area_num
		self.base_num = world_area.base_num
		self.durability = world_area.durability
		self.backbone = world_area.backbone

# エリア情報を更新します
class AreaUpdater(webapp2.RequestHandler):
	#現在のエリア情報を追加します	
	def addNewAreaInfo(self):
		world = world_info.WorldInformation()
		world.init()
		
		for area in world.areas():
			dbarea = Area()
			dbarea.setArea(area)
			print(dbarea.area_num)
			print(dbarea.date)
			dbarea.put()
		
	#24時間より前のエリア情報を削除します
	def maintainAreaInfo(self):
		lifetime = datetime.timedelta(hours=24)
		threshold = datetime.datetime.now() - lifetime

		results = Area.all().filter("date<", threshold)
		db.delete(results)


	def get(self):
		self.addNewAreaInfo()
		self.maintainAreaInfo()
		

