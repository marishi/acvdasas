import webapp2
import cgi
import os
import weapon
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from operator import attrgetter

class MainPage(webapp2.RequestHandler):
	def get(self):
		template_value={}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_value))

class ImpactThresholdAcvPage(webapp2.RequestHandler):
	page_name = 'impact_threshold_acv.html'
	
	def get(self):
		template_value = {}
		path = os.path.join(os.path.dirname(__file__), self.page_name)
		self.response.out.write(template.render(path, template_value))

	def post(self):

		rp = self.request.get('reaction_performance')
		template_value = {}
		if rp.isdigit():
			stagger = int(rp)
			freeze = stagger/0.8

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
			'isnot_int': True}
		else:
			template_value = {'isnot_int' : False}

		logging.info(template_value)
		path = os.path.join(os.path.dirname(__file__), self.page_name)
		self.response.out.write(template.render(path, template_value))

class LockonRangePage(webapp2.RequestHandler):
	page_name = 'lockon_range.html'
	
	def get(self):
		template_value = {'is_input_error':False,'has_result':False}
		path = os.path.join(os.path.dirname(__file__), self.page_name)
		self.response.out.write(template.render(path, template_value))

	def post(self):

		camera = self.request.get('camera')
		fcs_range = self.request.get('fcs_range')
		template_value = {}

		if camera.isdigit() and fcs_range.isdigit() :
			camera_int = int(camera)
			fcs_range_int = int(fcs_range)

			lockon_range = fcs_range_int * ((camera_int+500.0)/1000.0)
	
			template_value = {
			'lockon_range' : int(lockon_range),
			'is_input_error': False,
			'has_result':True}
		else:
			template_value = {'is_input_error' : True,'has_result':False}

		logging.info(template_value)
		path = os.path.join(os.path.dirname(__file__), self.page_name)
		self.response.out.write(template.render(path, template_value))


