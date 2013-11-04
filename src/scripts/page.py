#coding=utf-8

import webapp2
import cgi
import os
import weapon
import logging
import formula
import app_enviroment
import world_info
import filters.timezone
import filters

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from operator import attrgetter

class Page(webapp2.RequestHandler):
	page_name = ''

	def write(self, template_value):
		template.register_template_library('scripts.filters.timezone')

		path = os.path.join( app_enviroment.template_path , self.page_name)
		self.response.out.write(template.render(path, template_value))

class MainPage(Page):
	page_name = 'index.html'

	def get(self):
		template_value={}
		self.write(template_value)

class ImpactThresholdAcvPage(Page):
	page_name = 'impact_threshold_acv.html'
	
	def get(self):
		template_value = {'is_input_error':False,'has_result':False}
		self.write(template_value)

	def post(self):

		rp = self.request.get('reaction_performance')
		template_value = {}
		if rp.isdigit():
			stagger = int(rp)
			freeze = int(stagger/0.8)

			weapons = weapon.getWeapons()		
			weapons.sort(key=attrgetter('impact'), reverse=True)
	
			freeze_weapons = filter(
				lambda weapon: weapon.impact >= freeze, weapons)

			stagger_weapons = filter(
				lambda weapon: stagger <= weapon.impact and weapon.impact < freeze, weapons)
			normal_weapons = filter(
				lambda weapon: weapon.impact < stagger, weapons)
	
			template_value = {
			'freeze_weapons' : freeze_weapons,
			'stagger_weapons' : stagger_weapons,
			'normal_weapons' : normal_weapons,
			'stagger' : stagger,
			'freeze' : freeze,
			'is_input_error': False,
			'has_result':True}
		else:
			template_value = {'is_input_error' : True, 'has_result':False}
		
		self.write(template_value)

class LockonRangePage(Page):
	page_name = 'lockon_range.html'
	
	def get(self):
		template_value = {'is_input_error':False,'has_result':False}
		self.write(template_value)

	def post(self):

		camera = self.request.get('camera')
		fcs_range = self.request.get('fcs_range')
		template_value = {}

		if camera.isdigit() and fcs_range.isdigit() :
			camera_int = int(camera)
			fcs_range_int = int(fcs_range)

			lockon_range = formula.lockon_range(fcs_range_int,camera_int)
	
			template_value = {
			'lockon_range' : int(lockon_range),
			'is_input_error': False,
			'has_result':True}
		else:
			template_value = {'is_input_error' : True,'has_result':False}
		
		self.write(template_value)

class DamagePage(Page):
	page_name = 'damage.html'
	
	def get(self):
		template_value = {'is_input_error':False,'has_result':False}
		self.write(template_value)		

	def post(self):

		attack = self.request.get('attack')
		defense = self.request.get('defense')
		template_value = {}

		if attack.isdigit() and defense.isdigit() :
			attack_int = int(attack)
			defense_int = int(defense)

			result = formula.damage(attack_int,defense_int)
				
			template_value = {
			'penetration' : result[0] ,
			'damage' :  result[1] ,
			'is_input_error': False ,
			'has_result':True}
		else:
			template_value = {'is_input_error' : True,'has_result':False}
	
		self.write(template_value)

class DPSPage(Page):
	page_name = 'dps.html'
	
	def get(self):
		template_value = {'is_input_error':False,'has_result':False}
		self.write(template_value)

	def paramCheck(self,n):
		if not n.isdigit():
			return False
		
		return int(n) > 0

	def post(self):
		
		damage = self.request.get('damage')
		synchro_num = self.request.get('synchro_num')
		rel = self.request.get('reload')

		template_value = {}

		# damage, synchro_num, relが１以上の整数であるかどうかをチェックする
		if all( self.paramCheck(num) for num in (damage, synchro_num, rel) ): 
			dps = formula.dps( int(damage), int(synchro_num), int(rel) )				
			template_value = {
			'dps' : round(dps,1),
			'is_input_error': False ,
			'has_result':True}
		else:
			template_value = {'is_input_error' : True,'has_result':False}
		self.write(template_value)

class PenetrationPage(Page):
	page_name = 'penetration.html'
	
	def get(self):
		template_value = {'is_input_error':False,'has_result':False}
		self.write(template_value)

	def post(self):
		
		defense = self.request.get('defense')

		template_value = {}

		# damage, synchro_num, relが１以上の整数であるかどうかをチェックする
		if defense.isdigit(): 
			defense_int = int(defense)
			template_value['ricochet']=defense_int
			template_value['penetration']=int(defense_int*1.3)
			template_value['stagger_ricochet']=int(defense_int*0.8)
			template_value['stagger_penetration']=int(defense_int*0.8*1.3)
			template_value['is_input_error']=False
			template_value['has_result']=True
		else:
			template_value = {'is_input_error' : True,'has_result':False}
		self.write(template_value)


class PredictEndOfWarPage(Page):
	page_name = 'predict_end_of_war.html'
	
	def get(self):
		areas = world_info.Area.all().order('-date')

		template_value = { 'areas':areas }
		self.write(template_value)

class WorldInformationPage(Page):
	page_name = 'world_information.html'
	
	def get(self):
		damage_average_3_area1 = world_info.AreaInformation(1).averageDamage(3)
		damage_average_3_area4 = world_info.AreaInformation(4).averageDamage(3)
		
		worldInfo = world_info.WorldInformation()
		damage_average_3 = worldInfo.averageDamage(3)
		damage_average_24 = worldInfo.averageDamage(24)
		template_value = {}
		template_value['damage_average_3_area1'] = damage_average_3_area1
		template_value['damage_average_3_area4'] = damage_average_3_area4
		template_value['damage_average_3'] = damage_average_3
		template_value['damage_average_24'] = damage_average_24
		template_value['latest_remaining_time'] = worldInfo.predictLatestRemainingMinutes(3)
		template_value['latest_time'] = worldInfo.predictLatestTime(3)
		template_value['total_durability'] = worldInfo.totalDurability()
		template_value['fastest_time'] = worldInfo.predictFastestTime(3)

		self.write(template_value)


	
