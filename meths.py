import sqlite3
import errors
import requests

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