import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

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
	url_ow = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units={unit}&appid={os.getenv("TOKEN_OPENWEATHER")}'
	
	return requests.get(url_ow)

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
	
	return f"**The weather in {str(location).capitalize()}: ** \
		** {icon} {response['weather'][0]['main']} ** \
		__Temperature:__ {int(response['main']['temp'])}°{unidad_d[unit]} \
		__Feels like:__ {int(response['main']['feels_like'])}°{unidad_d[unit]} \
		__Max:__ {int(response['main']['temp_max'])}°{unidad_d[unit]} \
		__Min:__ {int(response['main']['temp_min'])}°{unidad_d[unit]}"

def set_weather(location, temp):
	"""This function was only to try if the Wit.ai API was recognizig the intent well"""
	return f"Temperature of {str(location).capitalize()} set to {int(temp['valor'])} {temp['unidad']}"