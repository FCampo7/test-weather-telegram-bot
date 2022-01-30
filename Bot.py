import requests  
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request

# BOT_URL = f'https://api.telegram.org/bot{os.environ["TOKEN_TELEGRAM"]}/'  # <-- add your telegram token as environment variable


load_dotenv(find_dotenv())

def telegramAPI(method, data):
	return requests.post(f'https://api.telegram.org/bot{os.getenv("TOKEN_TELEGRAM")}/'+method, data = data)

def witRequest(texto):
	header = {'Authorization': os.getenv('TOKEN_WIT')}
	url_wit = 'https://api.wit.ai/message?v=20220128&q=' + requests.utils.requote_uri(texto)
	return requests.get(url_wit, headers=header)

def get_weather(location):
	return ("The temperature in "+str(location)+" is 16 degrees")

def set_weather(location, temp):
	return "Temperature of "+str(location)+" set to "+str(temp['valor'])+" "+str(temp['unidad'])


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():  
	# data = request.json

	# print(data)  # Comment to hide what Telegram is sending you
	# chat_id = data['message']['chat']['id']
	# message = data['message']['text']

	# json_data = {
	# 	"chat_id": chat_id,
	# 	"text": message,
	# }

	# message_url = BOT_URL + 'sendMessage'
	# requests.post(message_url, json=json_data)


	telegramBot_r = request.json

	print(telegramBot_r)

	wit_intent = []
	wit_temp = []
	wit_entities = dict()
	wit_location = []
	chat_id = telegramBot_r['message']['chat']['id']
	
	try:
		message = telegramBot_r['message']['text']
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



	return ''


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)