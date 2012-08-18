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

def getWind(zip):
	windurl = "http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?whichClient=NDFDgenMultiZipCode&lat=&lon=&listLatLon=&lat1=&lon1=&lat2=&lon2=&resolutionSub=&listLat1=&listLon1=&listLat2=&listLon2=&resolutionList=&endPoint1Lat=&endPoint1Lon=&endPoint2Lat=&endPoint2Lon=&listEndPoint1Lat=&listEndPoint1Lon=&listEndPoint2Lat=&listEndPoint2Lon=&zipCodeList=" + str(zip) + "&listZipCodeList=&centerPointLat=&centerPointLon=&distanceLat=&distanceLon=&resolutionSquare=&listCenterPointLat=&listCenterPointLon=&listDistanceLat=&listDistanceLon=&listResolutionSquare=&citiesLevel=&listCitiesLevel=&sector=&gmlListLatLon=&featureType=&requestedTime=&startTime=&endTime=&compType=&propertyName=&product=time-series&begin=2004-01-01T00%3A00%3A00&end=2016-08-18T00%3A00%3A00&Unit=e&maxt=maxt&wspd=wspd&Submit=Submit"

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
		<html>
			<head>
				<link rel="stylesheet" type="text/css" href="stylesheets/main.css" />
				<script src="js/jquery-1.7.2.min.js"></script>
				<script src="js/fadeStuff.js"></script>
			</head>
		  <body>
			<div id="wrapper"><div id="content"><div id="fadeContent">
			<form action="/import" method="post" enctype="multipart/form-data">
			  <div>
				Upload an XML file </br>
				<input id="importfile" name="importfile" type="file"><br /><br />
				Or provide a URL</br>
				<input id="inurl" name="inurl" type="text"><br /><br />
				<input type="hidden" name="check" value="0" />
				<input type="checkbox" name="check" value="1" /> Check if image URLs are valid<br /><br />
				<input name="merge" value="Import Merge" type="submit" />
				<input name="overwrite" value="Import Overwrite" type="submit" />
			  </div>
			</form><br />

			<form method="link" action="http://xkcd.com/353/"><input type="submit" value="Import Antigravity"></form><br />
			
			<a href="/">Home</a>
			</div></div></div>
			<script>$(document).ready(function(){$('#fadeContent').fadeIn(400);$('a').click(function(){$('#fadeContent').fadeOut(400);});});</script>
		  </body>
		</html>""")

class ResultsPage(webapp2.RequestHandler):
	def post(self):
		form = cgi.FieldStorage()
		zipcode = form['inurl'].value
		windurl = "http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?whichClient=NDFDgenMultiZipCode&lat=&lon=&listLatLon=&lat1=&lon1=&lat2=&lon2=&resolutionSub=&listLat1=&listLon1=&listLat2=&listLon2=&resolutionList=&endPoint1Lat=&endPoint1Lon=&endPoint2Lat=&endPoint2Lon=&listEndPoint1Lat=&listEndPoint1Lon=&listEndPoint2Lat=&listEndPoint2Lon=&zipCodeList=" + str(zip) + "&listZipCodeList=&centerPointLat=&centerPointLon=&distanceLat=&distanceLon=&resolutionSquare=&listCenterPointLat=&listCenterPointLon=&listDistanceLat=&listDistanceLon=&listResolutionSquare=&citiesLevel=&listCitiesLevel=&sector=&gmlListLatLon=&featureType=&requestedTime=&startTime=&endTime=&compType=&propertyName=&product=time-series&begin=2004-01-01T00%3A00%3A00&end=2016-08-18T00%3A00%3A00&Unit=e&maxt=maxt&wspd=wspd&Submit=Submit"
		webfile = urlfetch.fetch(windurl, deadline=60)
		tree = ElementTree.parse(in_file)
		timelayouts = tree.findall(".//time-layout")
		windspeeds = tree.find(".//wind-speed")
		times = None
		windtimelayout = windspeeds.attrib['time-layout']
		winddict = {}

		for tl in timelayouts:
			if tl.find('.//layout-key').text == windtimelayout:
				times = tl.findall('start-valid-time')
		i = 0
		for w in windspeeds.findall('.//value'):
			if int(w.text) > 9 :
				winddict[times[i].text] = int(w.text)
			i += 1
app = webapp2.WSGIApplication([('/', MainPage)],
							  debug=True)