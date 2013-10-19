
#coding=utf-8

import math

def damage(attack,defense):
	if attack <= defense:
		
		dam = attack * ( 0.25 - (0.01 * math.ceil( defense / 500.0 ) ) )
		return ('跳弾',int(dam))

	elif defense < attack and attack < defense*1.3:
		return ('小貫通','未実装')
	else:
		cutdown = 0.8 - ( 0.01 *  math.ceil(defense*0.8/50.0) )

		if cutdown < 0.1:
			print("0.1")
			cutdown = 0.1

		dam = attack * cutdown
		return ('大貫通',int(dam))

def lockon_range(fcs_range,camera):
	return fcs_range * ((camera + 500.0)/1000.0)

def dps(damage,synchro_ammo,rel):
	return damage*synchro_ammo*60.0/rel
