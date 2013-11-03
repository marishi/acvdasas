# -*- coding: utf-8 -*- 

import urllib2
import re
from google.appengine.ext import db
import datetime
import logging

class Area(db.Model):
	area_num = db.IntegerProperty()
	base_num = db.IntegerProperty()
	durability = db.IntegerProperty()
	backbone = db.IntegerProperty()
	date = db.DateTimeProperty(auto_now_add=True)

# エリアの経金ダメージを計算します
def calcAverageAreaDamage(areas):
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

# エリアのダメージ平均を求めます
# hours:何時間前までの時間を求めるか指定します
# 
def averageAreaDamage(hours, area_num):
	lifetime = datetime.timedelta(hours=hours)
	threshold = datetime.datetime.now() - lifetime
	
	# 同じエリアで、指定時間内の情報を日付順でソートして取得
	query = "WHERE area_num =:1 AND date > :2 ORDER BY date"

	#同じエリアだけを取得
	areas = Area.gql(query,area_num,threshold).fetch(100)
	return calcAverageAreaDamage(areas)
	

def averageWorldDamage(hours):

	s=0
	count = 0
	for num in range(1,8):
		#指定エリアの平均ダメージを取得
		d = averageAreaDamage(hours,num)
		#潰れたエリアor変化の無いエリアは対象外	
		if d != 0:
			s += d
			count += 1
	
	#　エリアのダメージ平均
	return s / count


def getCurrentArea():
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


