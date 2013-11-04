# coding: utf-8

import webapp2
import datetime
import world_info
from google.appengine.ext import db

# エリア情報を更新します
class AreaUpdater(webapp2.RequestHandler):
	#現在のエリア情報を追加します	
	def addNewAreaInfo(self):
		
		areas = world_info.getAcvdLinkArea()
		
		for area in areas:
			area.put()
		
	#24時間より前のエリア情報を削除します
	def maintainAreaInfo(self):
		lifetime = datetime.timedelta(hours=24)
		threshold = datetime.datetime.now() - lifetime

		results = world_info.Area.all().filter("date<", threshold)
		db.delete(results)


	def get(self):
		self.addNewAreaInfo()
		self.maintainAreaInfo()
		

