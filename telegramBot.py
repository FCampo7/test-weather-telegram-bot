import requests
import json
import os
from dotenv import load_dotenv, find_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

load_dotenv(find_dotenv())

def telegramAPI(method, data):
	return requests.post('https://api.telegram.org/bot'+str(os.getenv('TOKEN_TELEGRAM'))+'/'+method, data = data)

def witRequest(texto):
	header = {'Authorization': str(os.getenv('TOKEN_WIT'))}
	url_wit = 'https://api.wit.ai/message?v=20220128&q=' + requests.utils.requote_uri(texto)
	return requests.get(url_wit, headers=header)

def get_weather(location):
	return ("The temperature in "+str(location)+" is 16 degrees")

def set_weather(location, temp):
	return "Temperature of "+str(location)+" set to "+str(temp['valor'])+" "+str(temp['unidad'])

offset = 0

@sched.scheduled_job('interval', seconds=1)
def Schedule():
	global offset
	data = dict(offset = str(offset))

	telegramBot_r = telegramAPI('getUpdates', data)

	if(telegramBot_r.status_code==200):
		resultado = json.loads(telegramBot_r.content)['result']

		for r in resultado:
			wit_intent = []
			wit_temp = []
			wit_entities = dict()
			wit_location = []
			offset = r['update_id']
			chat_id = r['message']['chat']['id']
			
			try:
				message = r['message']['text']
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
				except Exception as e:
					print(e)

				if(wit_intent[0] in ['temperature_get', 'wit$get_temperature']):
					r1 = telegramAPI('sendMessage', dict(chat_id = chat_id, text = get_weather(wit_location[0])))
					print(r1.content)
				elif(wit_intent[0] in ['temperature_set', 'wit$set_temperature']):
					r2 = telegramAPI('sendMessage', dict(chat_id = chat_id, text = set_weather(wit_location[0], wit_temp[0])))
					print(r2.content)
			except Exception as e:
				print(e)
				res = telegramAPI('sendMessage', dict(chat_id = chat_id, text = 'Sorry, I didn\'t understand.\nPlease try again adding a location or temperature value.'))
				print(res.content)
	offset += 1

sched.start()
