import os
import apiCalls
from flask import Flask, request, render_template


app = Flask(__name__)

def witInterpreter(message: str) -> str:
	"""Función que utilizando la API de Wit.ai interpreta el mensaje recibido por el bot de Telegram y devuelve una respuesta.

	Args:
		message (str): Mensaje recibido por el bot de Telegram.

	Raises:
		Exception: Lanza una excepción si no se pudo interpretar el mensaje.

	Returns:
		str: Resultado de la interpretación del mensaje.
	"""

	message_s: str
	wit_intent = []
	wit_temp = []
	wit_entities = dict()
	wit_location = []
	unidades_d = dict(k='standard', c='metric', f='imperial')
	unidad = unidades_d['c']

	try:
		wit_r = apiCalls.witRequest(str(message)).json()

		print(wit_r)

		for i in wit_r['intents']:
			wit_intent.append(i['name'])

		wit_entities = wit_r['entities']

		if 'wit$location:location' in wit_entities:
			for i in wit_entities['wit$location:location']:
				wit_location.append(i['body'])

		if 'wit$temperature:temperature' in wit_entities:
			for t in wit_entities['wit$temperature:temperature']:
				wit_temp.append(dict(valor = t['value'], unidad = t['unit']))

		if 'units:units' in wit_entities:
			unidad = unidades_d[str(wit_entities['units:units'][0]['value']).lower()[0]]

		if(wit_intent[0] in ['temperature_get', 'wit$get_temperature']):
			message_s = apiCalls.get_weather(wit_location[0], unidad)

		elif(wit_intent[0] in ['temperature_set', 'wit$set_temperature']):
			message_s = apiCalls.set_weather(wit_location[0], wit_temp[0])
	
	except Exception as e:
		message_s = f"Disculpas, no entendí\\. Por favor intenta de nuevo probando algo como \"¿Cual es el clima en Buenos Aires, Argentina?\"\\. Gracias\\!"
		raise Exception(message_s)
	
	return message_s

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/bot', methods=['POST'])
def main():
	message_s: str
	
	try:
		telegramBot_r = request.json

		print(telegramBot_r)

		if('message' in telegramBot_r):
			chat_id = telegramBot_r['message']['chat']['id']
			message = telegramBot_r['message']['text']
		else:
			chat_id = telegramBot_r['edited_message']['chat']['id']
			message = telegramBot_r['edited_message']['text']

		action_r = apiCalls.telegramAPI('sendChatAction', data={'chat_id': str(chat_id), 'action': 'typing'})

		print(action_r.json)

		message_s=witInterpreter(message)

	except Exception as e:
		print(e)
		message_s=e.args[0]

	print(message_s)
	r1 = apiCalls.telegramAPI('sendMessage', dict(chat_id = chat_id, text = message_s, parse_mode='MarkdownV2'))
	print(r1.content)

	return ''


if __name__ == '__main__':
	app.run()