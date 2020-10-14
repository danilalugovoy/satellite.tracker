class CityNotFoundError(Exception):
	def __init__(self, text):
		self.txt = text

class SatelliteNotFoundError(Exception):
	def __init__(self, text):
		self.txt = text