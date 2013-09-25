import webapp2
import page

app = webapp2.WSGIApplication(
	[('/',page.MainPage),('/impact_threshold_acv.html',page.ImpactThresholdAcvPage) ],debug=True)
