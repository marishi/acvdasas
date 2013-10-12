import webapp2
import page

app = webapp2.WSGIApplication(
	[
	('/',page.MainPage),
	('/impact_threshold_acv.html',page.ImpactThresholdAcvPage), 
	('/lockon_range.html',page.LockonRangePage),
	('/damage.html',page.DamagePage),
	('/dps.html',page.DPSPage)
	],debug=True)
