import webapp2
import page
import area_updater

app = webapp2.WSGIApplication(
	[
	('/',page.MainPage),
	('/impact_threshold_acv.html',page.ImpactThresholdAcvPage), 
	('/lockon_range.html',page.LockonRangePage),
	('/damage.html',page.DamagePage),
	('/dps.html',page.DPSPage),
	('/penetration.html',page.PenetrationPage),
	('/predict_end_of_war.html',page.PredictEndOfWarPage),
	('/cronjob/area_updater', area_updater.AreaUpdater)
	],debug=True)
