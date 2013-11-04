import webapp2
import page
import area_updater
import set_dummy_area

app = webapp2.WSGIApplication(
	[
	('/',page.MainPage),
	('/impact_threshold_acv',page.ImpactThresholdAcvPage), 
	('/lockon_range',page.LockonRangePage),
	('/damage',page.DamagePage),
	('/dps',page.DPSPage),
	('/penetration',page.PenetrationPage),
	('/predict_end_of_war',page.PredictEndOfWarPage),
	('/area_updater', area_updater.AreaUpdater),
	('/world_information', page.WorldInformationPage)
	],debug=True)
