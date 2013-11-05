# -*- coding: utf-8 -*- 

import urllib2
import re
from google.appengine.ext import db
import datetime
import logging
import app_enviroment
from filters import timezone
import itertools
import area_data

class Area(db.Model):
	area_num = db.IntegerProperty()
	base_num = db.IntegerProperty()
	durability = db.IntegerProperty()
	backbone = db.IntegerProperty()
	date = db.DateTimeProperty(auto_now_add=True)

	def totalDurability(self):
		if self.base_num == 0:
			return 0
	
		predictBaseDurabilities = map( lambda x : x*56000 + 100000 ,  range(0,7) )
		result = sum( predictBaseDurabilities[:self.base_num -1] ) + self.durability
		return result

class AreaInformationImpl:
	area_num = 0
	base_num = 0
	name = ""
	special_base_url = ""
	hacking_base_url = ""
	front_base_url = ""
	backbone = ""
	date = datetime.datetime.now()
	ave_damage = 0
	has_ave_damage = False

	def __init__(self, area_num):
		self.area_num = area_num
	
		area_dict = area_data.dictionary[area_num]
	
		self.name = area_dict.name
		self.special_base_url = area_dict.special_base.image_url
		self.hacking_base_url = area_dict.hacking_base.image_url

		query = getCurrentArea()
		area = query.filter("area_num =", area_num).get()
		
		self.base_num = area.base_num
		if self.base_num == 0:
			self.front_base_url = "/images/none.png"

		self.front_base_url = area_dict.front_base_dict[self.base_num].image_url
		#時刻設定
		backbones = ["シリウス","ヴェニデ","EGF"]
		self.backbone = backbones[area.backbone-1]
		
		#時刻設定
		self.date = area.date.replace(tzinfo=timezone.UtcTzinfo())

	# 保存されているエリア耐久値の時間ごとの差分を平均をします
	def averageDurabilityDiff(self,areas):
	        count = 0
	        s = 0
	
	        for a1,a2 in zip( areas[1:],areas[:-1] ):
	        
	                if a1.base_num != a2.base_num:
	                        continue
	
	                s += a2.durability - a1.durability
	                count +=1
	
		if count == 0:
			return 0
	        result = float(s)/count
	
	        return result
	
	# エリアの１分毎のダメージ平均を求めます
	# hours:何時間前から平均を求める指定します
	# 
	def averageDamage(self,hours):
		if self.has_ave_damage:
			return self.ave_damage

		logging.info("recalc")

		lifetime = datetime.timedelta(hours=hours)
		threshold = datetime.datetime.now() - lifetime
		
		# 同じエリアで、指定時間内の情報を日付順でソートして取得
		query = "WHERE area_num =:1 AND date > :2 ORDER BY date"
	
		#同じエリアだけを取得
		areas = Area.gql(query,self.area_num,threshold).fetch(1000)
		diffAverage = self.averageDurabilityDiff(areas)
		
		result = diffAverage / app_enviroment.scraping_gap

		self.ave_damage = result
		self.has_ave_damage = True
		return result

def clearAreaInformation():
	mod_impl_instances.clear()
mod_impl_instances = {}
class AreaInformation:

	area_num = 0
	base_num = 0
	name = ""
	special_base_url = ""
	hacking_base_url = ""
	front_base_url = ""
	backbone = ""
	date = datetime.datetime.now()

	def __init__(self, area_num):
		self.area_num = area_num
		self.init()

	def init(self):
		if not mod_impl_instances.has_key(self.area_num):
			mod_impl_instances[self.area_num] = AreaInformationImpl(self.area_num)
		instance = mod_impl_instances[self.area_num]

		self.area_num = instance.area_num
		self.base_num = instance.base_num
		self.name = instance.name
		self.special_base_url = instance.special_base_url
		self.hacking_base_url = instance.hacking_base_url
		self.front_base_url = instance.front_base_url
		self.backbone = instance.backbone
		self.date = instance.date


	def averageDamage(self,hours):
		self.init()
		return mod_impl_instances[self.area_num].averageDamage(hours)

def getCurrentArea():
	areas = Area.all().order("-date")
	# 最新のエリアのみを取得
	d = areas.get()

	if d == None:
		return 0

	return areas.filter("date =" , d.date)



class WorldInformation:
	def averageDamage(self, hours):
	
		s=0
		count = 0
		for num in range(1,8):
			#指定エリアの平均ダメージを取得
			areaInfo = AreaInformation(num)
			d = areaInfo.averageDamage(hours)
			#潰れたエリアor変化の無いエリアは対象外	
			if d != 0:
				s += d
				count += 1
		if count == 0:
			return 0
		#　エリアのダメージ平均
		return s / count

	def totalDurability(self):
		current_areas = getCurrentArea()

		s = 0
		for area in current_areas:
			if area.base_num == 0:
				continue
			s += area.totalDurability()

		return s

	def minDurability(self):
		current_areas = getCurrentArea()

		#各勢力の耐久値合計
		s = lambda i : sum( a.totalDurability() for a in current_areas if a.backbone == i ) 
		durabilities = map( s , range(1,4) )

		#耐久値０の勢力は除外
		durabilities = filter( lambda d : d > 0 , durabilities )
		#各勢力の耐久値を組み合わせ、最小のパターンを探す       
		m = min( sum(c) for c in itertools.combinations( durabilities, len(durabilities)-1 ) )
		return m

	def predictRemainingMinutes(self, hours, durability):
		damage = self.averageDamage(hours)
		if damage == 0:
			return 0
		# あと何分で戦争が終わるか求める
		return durability / damage


	def predictLatestRemainingMinutes(self, hours):
		return self.predictRemainingMinutes(hours, self.totalDurability())

	def predictFastestRemainingMinutes(self, hours):
		return self.predictRemainingMinutes(hours, self.minDurability())

	#現在時刻に指定分を足す
	def addMinutesToNow(self, minutes):
		remtime = datetime.timedelta(minutes=minutes)
		remdate = datetime.datetime.now() + remtime
		return remdate.replace(tzinfo=timezone.UtcTzinfo())
	
	def predictLatestTime(self, hours):
		remaining_minutes = self.predictLatestRemainingMinutes(hours)
		return self.addMinutesToNow(remaining_minutes)
	
	def predictFastestTime(self, hours):
		remaining_minutes = self.predictFastestRemainingMinutes(hours)
		return self.addMinutesToNow(remaining_minutes)

def getAcvdLinkArea():
	url = 'http://acvdlink.armoredcore.net/p/acop/acvdlink/'
	op = urllib2.urlopen(url)
	html = op.read()
	op.close()

	#areainfoを取得する
	areas_regstr = "valArr\[\"areainfo\"\] = \[((?:.|\\n)+?)\];"
	match = re.search(areas_regstr, html)	

	areainfo = match.group(1)

	#各エリアに分割
	area_strs = re.findall("\[((?:.|\n)+?)\]",areainfo)
	
	date = datetime.datetime.now()
	areas = []
	#最初の要素はコメントなので無視
	for area in area_strs[1:]:
		data = area.split(',')

                # たまにデータがかけていたりするのでチェック
                if len(data) < 12:
                        continue
		
		arnum = re.search("([0-9])+",data[0]).group(1)
		
		a = Area()
		a.area_num = int(arnum)
		a.base_num = int(data[5])
		a.durability = int(data[9])
		a.backbone = int(data[12])
		a.date = date
		areas.append( a )

	return areas


