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

		stagger = int(self.request.get('reaction_performance'))
		freeze = stagger/0.8

		weapons = weapon.getWeapons()		
		weapons.sort(key=attrgetter('impact'), reverse=True)
	
		freeze_weapons = filter(lambda weapon: weapon.impact >= freeze, weapons)
		stagger_weapons = filter(
			lambda weapon: stagger <= weapon.impact and weapon.impact < freeze,
			weapons)
		normal_weapons = filter(lambda weapon: weapon.impact < stagger, weapons)
	
		template_value = {
			'freeze_weapons' : freeze_weapons,
			'stagger_weapons' : stagger_weapons,
			'normal_weapons' : normal_weapons,
			'stagger' : stagger,
			'freeze' : freeze}

		path = os.path.join(os.path.dirname(__file__), self.page_name)
		self.response.out.write(template.render(path, template_value))


