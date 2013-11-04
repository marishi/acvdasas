# -*- coding: utf-8 -*- 

import urllib2
import re
from google.appengine.ext import db
import datetime
import logging
import app_enviroment
from filters import timezone
import itertools

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
		
		names = [
			"NORTH FRONTIER","FAR EAST","MIDDLE EAST","SOUTH FRONTIER",
			"MID CONTINENT","SOUTH ISLAND","NEW FRONTIER"]

		north_frontier_url = "/images/north_frontier/"
		far_east_url = "/images/far_east/"
		middle_east_url = "/images/middle_east/"
		south_frontier_url = "/images/south_frontier/"
		mid_continent_url = "/images/mid_continent/"
		south_island_url = "/images/south_islands/"
		new_frontier_url = "/images/new_frontier/"

		special_bases = [
			north_frontier_url +  "galef_plant.png",
			far_east_url + "kensky_base.png",
			middle_east_url + "alg742_181.png",
			south_frontier_url + "raziana_base.png",
			mid_continent_url + "zilma_borough.png",
			south_island_url + "fort_denis.png",
			new_frontier_url + "karmat_base.png" ]
		
		hacking_bases = [
			north_frontier_url + "brew_city.png",
			far_east_url + "yunsk_canyon.png",
			middle_east_url + "old_duman.png",
			south_frontier_url + "old_uriae.png",
			mid_continent_url + "pask_field.png",
			south_island_url + "maldan_city.png",
			new_frontier_url + "massif_dolango.png" ]
	
		north_frontier_bases = [
			"alloy_gate_city.png",
			"windy_city.png",
			"windy_city_night.png",
			"big_d_tunnel.png",
			"big_d_tunnel_working.png",
			"brew_city.png",
			"galef_plant.png",
			"agria_m42.png",
			"none.png"]
		north_frontier_bases = map( lambda a : north_frontier_url + a , north_frontier_bases )

		far_east_bases = [
			"andry_city.png",
			"pierm_snowfield.png",
			"yorga_base.png",
			"yorga_base_blizzard.png",
			"yunsk_canyon.png",
			"miynsky_hills.png",
			"miynsky_hills_bombing.png",
			"kensky_base.png",
			"none.png" ]
		far_east_bases = map( lambda a : far_east_url + a , far_east_bases )
	
		middle_east_bases = [
			"ratona_naval_port.png",
			"old_duman.png",
			"mazar_tomb.png",
			"mazar_tomb_night.png",
			"samir_canyon.png",
			"quet_hills.png",
			"alg742_181.png",
			"alg742_181_reboot.png",
			"none.png"]
		middle_east_bases = map( lambda a : middle_east_url + a , middle_east_bases)

		south_frontier_bases = [
			"opal_cave.png",
			"opal_cave_depth.png",
			"tauraca_cave.png",
			"calpin_wetland.png",
			"old_uriae.png",
			"emapolice.png",
			"emapolice_sunrise.png",
			"raziana_base.png",
			"none.png"]
		south_frontier_bases = map( lambda a : south_frontier_url + a, south_frontier_bases)

		mid_continent_bases = [
			"vorka_city.png",
			"magion_city.png",
			"barozniki_ts.png",
			"barozniki_ts_pollution.png",
			"pask_field.png",
			"pask_field_night.png",
			"zilma_borough.png",
			"under_tower_gf710.png",
			"none.png"]
		mid_continent_bases = map( lambda a : mid_continent_url + a, mid_continent_bases )

		south_island_bases = [
			"victoria_city.png",
			"maldan_city.png",
			"maldan_city_night.png",
			"eduna_yard.png",
			"fat_rocks.png",
			"fat_rocks_flooded.png",
			"fort_denis.png",
			"fort_denis_inside_city.png",
			"none.png"]
		south_island_bases = map( lambda a : south_island_url + a, south_island_bases )

		new_frontier_bases = [
			"route_n64.png",
			"route_r1024.png",
			"dozur_desert.png",
			"dozur_desert_bombing.png",
			"vosto_base_duststorm.png",
			"vosto_base.png",
			"massif_dolango.png",
			"karmat_base.png",
			"none.png"]
		new_frontier_bases = map( lambda a : new_frontier_url + a, new_frontier_bases )

		front_bases = [north_frontier_bases[::-1], far_east_bases[::-1], middle_east_bases[::-1],
			south_frontier_bases[::-1],mid_continent_bases[::-1], south_island_bases[::-1],
			new_frontier_bases[::-1]]
	
		self.name = names[area_num-1]
		self.special_base_url = special_bases[area_num-1]
		self.hacking_base_url = hacking_bases[area_num-1]

		area_query = getCurrentArea()
		area = area_query.filter("area_num =", area_num).get()
		self.base_num = area.base_num
		self.front_base_url = front_bases[area_num-1][area.base_num]
		
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
		lifetime = datetime.timedelta(hours=hours)
		threshold = datetime.datetime.now() - lifetime
		
		# 同じエリアで、指定時間内の情報を日付順でソートして取得
		query = "WHERE area_num =:1 AND date > :2 ORDER BY date"
	
		#同じエリアだけを取得
		areas = Area.gql(query,self.area_num,threshold).fetch(1000)
		diffAverage = self.averageDurabilityDiff(areas)
		return diffAverage / app_enviroment.scraping_gap

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


