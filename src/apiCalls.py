import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

file=open("src/lang.json") # para debuguear
#file=open("lang.json") # para produccion

lang = json.load(file)

file.close()

def telegramAPI(method, data):
	"""Function to communicate with the [Telegram Bot](https://core.telegram.org/bots/api)
	
	> Look into the [available methods](https://core.telegram.org/bots/api#available-methods) section
	
	Args:
		method (str): String with the desired method to be executed by the bot\n
		data (json): json with the data required by the method

	Returns: 
		Response: HTTP Response from the bot
	"""
	return requests.post(f'https://api.telegram.org/bot{os.getenv("TOKEN_TELEGRAM")}/'+method, data = data)


def witRequest(texto):
	"""Call the [Wit.ai](https://wit.ai/) API to process the message received by the bot

	Args:
		texto (str): String with the message to be processed

	Returns:
		Response: HTTP Response with the processed information
	"""
	header = {'Authorization': 'Bearer '+os.getenv('TOKEN_WIT')}
	url_wit = 'https://api.wit.ai/message?v=20220128&q=' + requests.utils.requote_uri(texto)
	
	return requests.get(url_wit, headers=header)


def __get_open_weather(location, unit):
	"""Call the [Open Weather](https://openweathermap.org/api) API to get the current weather

	Args:
		location (str): String with the desired weather location (City, country)\n
		unit (str): String with the units system wanted (could be: metric (Celsius), standard (Kelvin) or imperial (Fahrenheit))

	Returns:
		Response: HTTP Response with the weather information
	"""
	url_ow = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units={unit}&lang=es&appid={os.getenv("TOKEN_OPENWEATHER")}'
	
	return requests.get(url_ow)


def get_open_weather_gps(lat, lon, unit='metric'):
	"""Call the [Open Weather](https://openweathermap.org/api) API to get the current weather

	Args:
		lat (str): String with the latitude from desired weather location (City, country)\n
		lon (str): String with the longitude from desired weather location (City, country)\n
		unit (str): String with the units system wanted (could be: metric (Celsius), standard (Kelvin) or imperial (Fahrenheit))

	Returns:
		Response: HTTP Response with the weather information
	"""
	unidad_d = dict(metric='ºC', imperial='ºF', standard='K')
	icons_d = dict([(2, '⛈'), (3, '🌦'), (5, '🌧'), (6, '🌨'), (7, '🌫'), (800, '☀️'), (8, '☁️')])
	
	response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={unit}&lang=es&appid={os.getenv("TOKEN_OPENWEATHER")}').json()
	
	if response["weather"][0]["id"] == 800:
		icon = icons_d[800]
	else:
		icon = icons_d[int(response["weather"][0]["id"]/100)]	

	return f"{lang['es']['geo']} {icon} {response['weather'][0]['main']} {lang['es']['temp']} {int(response['main']['temp'])}{unidad_d[unit]} {lang['es']['feels']} {int(response['main']['feels_like'])}{unidad_d[unit]} {lang['es']['max']} {int(response['main']['temp_max'])}{unidad_d[unit]} {lang['es']['min']} {int(response['main']['temp_min'])}{unidad_d[unit]}"
	# return f"*El clima en tu ubicación:*\n*{icon} {response['weather'][0]['main']}*\n*Temperatura:* {int(response['main']['temp'])}{unidad_d[unit]}\n*Sensación Térmica:* {int(response['main']['feels_like'])}{unidad_d[unit]}\n*Max:* {int(response['main']['temp_max'])}{unidad_d[unit]}\n*Min:* {int(response['main']['temp_min'])}{unidad_d[unit]}"


def get_weather(location, unit='metric'):
	"""Gets the weather and return it in a string ready to be sent by the bot

	Args:
		location (str): String with the desired weather location (City, country)\n
		unit (str): String with the units system wanted (could be: metric (Celsius), standard (Kelvin) or imperial (Fahrenheit)). Defaults to 'metric'.

	Returns:
		str: String with the weather information already formatted and ready to be sent by the bot
	"""	
	unidad_d = dict(metric='ºC', imperial='ºF', standard='K')
	icons_d = dict([(2, '⛈'), (3, '🌦'), (5, '🌧'), (6, '🌨'), (7, '🌫'), (800, '☀️'), (8, '☁️')])

	response = __get_open_weather(location, unit).json()
	
	if response["weather"][0]["id"] == 800:
		icon = icons_d[800]
	else:
		icon = icons_d[int(response["weather"][0]["id"]/100)]

	return f"{lang['es']['location']} {str(location).capitalize()}:*\n*{icon} {response['weather'][0]['main']} {lang['es']['temp']} {int(response['main']['temp'])}{unidad_d[unit]} {lang['es']['feels']} {int(response['main']['feels_like'])}{unidad_d[unit]} {lang['es']['max']} {int(response['main']['temp_max'])}{unidad_d[unit]} {lang['es']['min']} {int(response['main']['temp_min'])}{unidad_d[unit]}"
	# return f"*El clima en {str(location).capitalize()}:*\n*{icon} {response['weather'][0]['main']}*\n*Temperatura:* {int(response['main']['temp'])}{unidad_d[unit]}\n*Sensación Térmica:* {int(response['main']['feels_like'])}{unidad_d[unit]}\n*Max:* {int(response['main']['temp_max'])}{unidad_d[unit]}\n*Min:* {int(response['main']['temp_min'])}{unidad_d[unit]}"


def set_weather(location, temp):
	"""This function was only to try if the Wit.ai API was recognizig the intent well"""
	return f"Temperatura de {str(location).capitalize()} seteada en {int(temp['valor'])} {temp['unidad']}"
