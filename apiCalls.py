import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def telegramAPI(method, data):
	return requests.post(f'https://api.telegram.org/bot{os.getenv("TOKEN_TELEGRAM")}/'+method, data = data)

def witRequest(texto):
	header = {'Authorization': os.getenv('TOKEN_WIT')}
	url_wit = 'https://api.wit.ai/message?v=20220128&q=' + requests.utils.requote_uri(texto)
	
	return requests.get(url_wit, headers=header)

def get_weather(location, unit='metric'):
	unidad_d = dict(metric='Celsius', imperial='Fahrenheit', standard='Kelvin')
	icons_d = dict([(2, '⛈'), (3, '🌦'), (5, '🌧'), (6, '🌨'), (7, '🌫'), (800, '☀️'), (8, '☁️')])

	response = get_open_weather(location, unit).json()
	
	if response["weather"][0]["id"] == 800:
		icon = icons_d[800]
	else:
		icon = icons_d[int(response["weather"][0]["id"]/100)]
	
	return f"*The weather in {str(location).capitalize()}: {icon} {response['weather'][0]['main']} & {int(response['main']['temp'])} {unidad_d[unit]}*"

def set_weather(location, temp):
	return f"Temperature of {str(location).capitalize()} set to {int(temp['valor'])} {temp['unidad']}"

def get_open_weather(location, unit):
	url_ow = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units={unit}&appid={os.getenv("TOKEN_OPENWEATHER")}'
	
	return requests.get(url_ow)