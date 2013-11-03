# coding: utf-8

import webapp2
import world_info

class SetDummyArea(webapp2.RequestHandler):
	def get(self):
		
		for i in range(1,4):	
			for j in range(1,8):
		
				a = world_info.Area()
				a.area_num = j
				a.base_num = 5
				a.durability = 40000 - 1000*i
				a.backbone = 1

				a.put()
			
