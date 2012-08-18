import webapp2
import urllib2
import cgi, os
import cgitb; cgitb.enable()
from xml.etree import ElementTree
from google.appengine.api import urlfetch 
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
		<html>
		  <body>
				<form action="/" method="post" enctype="multipart/form-data">
					<div>
						Provide a zip code</br>
						<input id="zipcode" name="zipcode" type="text"><br /><br />
						<input name="check" value="Check Wind!" type="submit" />
					</div>
				</form><br />
			</body>
		</html>""")

	def post(self):
		form = cgi.FieldStorage()
		zipcode = form['zipcode'].value
		windurl = "http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?whichClient=NDFDgenMultiZipCode&lat=&lon=&listLatLon=&lat1=&lon1=&lat2=&lon2=&resolutionSub=&listLat1=&listLon1=&listLat2=&listLon2=&resolutionList=&endPoint1Lat=&endPoint1Lon=&endPoint2Lat=&endPoint2Lon=&listEndPoint1Lat=&listEndPoint1Lon=&listEndPoint2Lat=&listEndPoint2Lon=&zipCodeList=" + str(zipcode) + "&listZipCodeList=&centerPointLat=&centerPointLon=&distanceLat=&distanceLon=&resolutionSquare=&listCenterPointLat=&listCenterPointLon=&listDistanceLat=&listDistanceLon=&listResolutionSquare=&citiesLevel=&listCitiesLevel=&sector=&gmlListLatLon=&featureType=&requestedTime=&startTime=&endTime=&compType=&propertyName=&product=time-series&begin=2004-01-01T00%3A00%3A00&end=2016-08-18T00%3A00%3A00&Unit=e&maxt=maxt&wspd=wspd&Submit=Submit"
		

		webfile = urlfetch.fetch(windurl, deadline=60)
		#self.response.out.write(webfile.content)

		tree = ElementTree.fromstring(webfile.content)
		timelayouts = tree.findall(".//time-layout")
		windspeeds = tree.find(".//wind-speed")
		times = None
		windtimelayout = windspeeds.attrib['time-layout']
		winddict = {}

		for tl in timelayouts:
			logging.info("layout is " + str(tl.find('.//layout-key').text))
			if tl.find('.//layout-key').text == windtimelayout:
				logging.info("layout matched!")
				times = tl.findall('start-valid-time')
		i = 0
		for w in windspeeds.findall('.//value'):
			logging.info("value is " + str(w.text))
			if int(w.text) > 5 :
				logging.info("found wind over 5!")
				winddict[times[i].text] = int(w.text)
			i += 1
		
		self.response.out.write(repr(winddict))

app = webapp2.WSGIApplication([('/', MainPage)],
							  debug=True)

def main():
	run_wsgi_app(app)
			
if __name__ == "__main__":
	main()
