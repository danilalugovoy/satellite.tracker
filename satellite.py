import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timezone
import sqlite3
import errors

def getTle(name):
	db = sqlite3.connect('idnr.db')
	cursor = db.cursor()

	cursor.execute(f'SELECT name FROM info WHERE name = "{name}"')
	if not cursor.fetchone():
		raise errors.SatelliteNotFoundError(f'Satellite {name} not found!')
	else:
		for i in cursor.execute(f'SELECT noardid FROM info WHERE name = "{name}"'):
			tle = i[0]
		return tle

def getCoordinates(city):
	data = requests.get(f'http://search.maps.sputnik.ru/search?q={city}').json()
	if not data['result']:
		raise errors.SatelliteNotFoundError(f'City {city} not found!')
	else:
		return data['result'][0]['position']['lat'], data['result'][0]['position']['lon']

class Tracker:

	def __init__(self, city, satname):
		self.city = city
		self.satname = satname
		self.tle = getTle(satname)
		self.cityCoord = getCoordinates(city)
		self.soup = BeautifulSoup(requests.get(f'https://www.n2yo.com/satellite/?s={self.tle}', headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.6.2.169 Yowser/2.5 Yptp/1.23 Safari/537.36'}).content, 'html.parser')

	# С токеном

	def getSatCoord(self):
		resp = requests.get(f'https://www.n2yo.com/rest/v1/satellite/positions/{self.tle}/{self.cityCoord[0]}/{self.cityCoord[1]}/0/2/&apiKey=8WVXGF-K6LA8P-EDM43D-4HK3').json()
		return resp["positions"][0]["satlatitude"], resp["positions"][0]["satlongitude"]

	def getSatAzimuth(self):
		resp = requests.get(f'https://www.n2yo.com/rest/v1/satellite/positions/{self.tle}/{self.cityCoord[0]}/{self.cityCoord[1]}/0/2/&apiKey=8WVXGF-K6LA8P-EDM43D-4HK3').json()
		return resp["positions"][0]["azimuth"]

	def getSatAltitude(self):
		resp = requests.get(f'https://www.n2yo.com/rest/v1/satellite/positions/{self.tle}/{self.cityCoord[0]}/{self.cityCoord[1]}/0/2/&apiKey=8WVXGF-K6LA8P-EDM43D-4HK3').json()
		return resp["positions"][0]["sataltitude"]

	# Без токена

	def getSatInterCode(self):
		return self.soup.find("b", text=re.compile("Int'l Code")).next_sibling.strip()[2:]

	def getSatPerigee(self):
		return self.soup.find("b", text=re.compile("Perigee")).next_sibling.strip()[2:][0:-3]

	def getSatApogee(self):
		return self.soup.find("b", text=re.compile("Apogee")).next_sibling.strip()[2:][0:-3]

	def getSatIncl(self):
		return self.soup.find("b", text=re.compile("Inclination")).next_sibling.strip()[2:][0:-5]

	def getSatPeriod(self):
		return self.soup.find("b", text=re.compile("Period")).next_sibling.strip()[2:][0:-8]

	def getSatSource(self):
		return self.soup.find("b", text=re.compile("Source")).next_sibling.strip()[2:]

	def getSatLaunchSite(self):
		return self.soup.find("b", text=re.compile("Launch site")).next_sibling.strip()[2:]

	# С токеном

	def getSatVisual(self):
		resp = requests.get(f'https://www.n2yo.com/rest/v1/satellite/visualpasses/{self.tle}/{self.cityCoord[0]}/{self.cityCoord[1]}/0/2/300/&apiKey=8WVXGF-K6LA8P-EDM43D-4HK3').json()
		try:
			return time.strftime("%d:%m:%Y в %H:%M:%S", time.localtime(int(resp['passes'][0]['startUTC']))), time.strftime("%d:%m:%Y в %H:%M:%S", time.localtime(int(resp['passes'][0]['endUTC'])))
		except KeyError:
			return None

	def getSatRadio(self):
		resp = requests.get(f'https://www.n2yo.com/rest/v1/satellite/radiopasses/{self.tle}/{self.cityCoord[0]}/{self.cityCoord[1]}/0/2/300/&apiKey=8WVXGF-K6LA8P-EDM43D-4HK3').json()
		try:
			return time.strftime("%d:%m:%Y в %H:%M:%S", time.localtime(int(resp['passes'][0]['startUTC']))), time.strftime("%d:%m:%Y в %H:%M:%S", time.localtime(int(resp['passes'][0]['endUTC'])))
		except KeyError:
			return None