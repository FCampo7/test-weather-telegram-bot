import os
import requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request


load_dotenv(find_dotenv())

def telegramAPI(method, data):
	return requests.post(f'https://api.telegram.org/bot{os.getenv("TOKEN_TELEGRAM")}/'+method, data = data)

def witRequest(texto):
	header = {'Authorization': os.getenv('TOKEN_WIT')}
	url_wit = 'https://api.wit.ai/message?v=20220128&q=' + requests.utils.requote_uri(texto)
	return requests.get(url_wit, headers=header)

def get_weather(location, unit='metric'):
	unidad_d = dict(metric='Celsius', imperial='Fahrenheit', standard='Kelvin')
	icons_d = dict([(2, ':thunder_cloud_rain:'), (3, ':white_sun_rain_cloud:'), (5, ':cloud_rain:'), (6, ':cloud_snow:'), (7, ':fog:'), (800, ':sunny:'), (8, ':cloud:')])
	response = get_open_weather(location, unit).json()
	if response["weather"][0]["id"] == 800:
		icon = icons_d[800]
	else:
		icon = icons_d[int(response["weather"][0]["id"]/100)]
	return f'*The weather in {location}:*  \
		__Weather:__ {response["weather"][0]["main"]} {icon}  \
		__Temperature:__ {response["main"]["temp"]} {unidad_d[unit]}'

def set_weather(location, temp):
	return f"Temperature of {location} set to {temp['valor']} {temp['unidad']}"

def get_open_weather(location, unit):
	url_ow = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units={unit}&appid={os.getenv("TOKEN_OPENWEATHER")}'
	return requests.get(url_ow)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():

	unidades_d = dict(k='standard', c='metric', f='imperial') 
	telegramBot_r = request.json

	print(telegramBot_r)

	wit_intent = []
	wit_temp = []
	wit_entities = dict()
	wit_location = []
	unidad = unidades_d['c']
	
	try:
		if('message' in telegramBot_r):
			chat_id = telegramBot_r['message']['chat']['id']
			message = telegramBot_r['message']['text']
		else:
			chat_id = telegramBot_r['edited_message']['chat']['id']
			message = telegramBot_r['edited_message']['text']

		wit_r = witRequest(str(message)).json()

		print(wit_r)

		for i in wit_r['intents']:
			wit_intent.append(i['name'])

		wit_entities = wit_r['entities']

		try:
			if 'wit$location:location' in wit_entities:
				for i in wit_entities['wit$location:location']:
					wit_location.append(i['body'])
			if 'wit$temperature:temperature' in wit_entities:
				for t in wit_entities['wit$temperature:temperature']:
					wit_temp.append(dict(valor = t['value'], unidad = t['unit']))
			if 'units:units' in wit_entities:
				unidad = unidades_d[str(wit_entities['units:units'][0]['value']).lower()[0]]
		except Exception as e:
			print(e)

		if(wit_intent[0] in ['temperature_get', 'wit$get_temperature']):
			message_s = get_weather(wit_location[0], unidad)
			
		elif(wit_intent[0] in ['temperature_set', 'wit$set_temperature']):
			message_s = set_weather(wit_location[0], wit_temp[0])
	except Exception as e:
		print(e)
		message_s = "Sorry, I didn't understand.  \
			Please try again adding a location or temperature value."
	
	print(message_s)
	r1 = telegramAPI('sendMessage', dict(chat_id = chat_id, text = message_s, parse_mode='MarkdownV2'))
	print(r1.content)

	return ''


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)