
#coding=utf-8

def damage(attack,defense):
	if attack <= defense:
		defe = int(defense / 500.0 + 0.9)

		dam = attack * 0.25 - ( (attack*0.01) * defe ) 
		return ('跳弾',int(dam))

	elif defense < attack and attack < defense*1.3:
		return ('小貫通','未実装')
	else:
		return ('大貫通','未実装')

def lockon_range(fcs_range,camera):
	return fcs_range * ((camera + 500.0)/1000.0)

def dps(damage,synchro_ammo,rel):
	return damage*synchro_ammo*60/rel
