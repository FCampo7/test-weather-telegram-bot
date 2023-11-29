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

	message_s: str # Mensaje que retorna, puede ser de error o de respuesta
	wit_intent = [] # Lista de intents
	wit_temp = [] # Lista de temperaturas
	wit_entities = dict() # Diccionario de entidades
	wit_location = [] # Lista de ubicaciones
	unidades_d = dict(k='standard', c='metric', f='imperial') # Diccionario de unidades
	unidad = unidades_d['c'] # Unidad por defecto

	try:
		# Realizo la petición a Wit.ai
		wit_r = apiCalls.witRequest(str(message)).json()

		print("wit response: "+str(wit_r)) # Para debuggueo

		# Obtengo los intents
		for i in wit_r['intents']:
			wit_intent.append(i['name'])

		wit_entities = wit_r['entities']

		# Obtengo las temperaturas y ubicaciones
		if 'wit$location:location' in wit_entities:
			for i in wit_entities['wit$location:location']:
				wit_location.append(i['body'])

		# Obtengo las temperaturas
		if 'wit$temperature:temperature' in wit_entities:
			for t in wit_entities['wit$temperature:temperature']:
				wit_temp.append(dict(valor = t['value'], unidad = t['unit']))

		# Obtengo las unidades
		if 'units:units' in wit_entities:
			unidad = unidades_d[str(wit_entities['units:units'][0]['value']).lower()[0]]

		# Obtengo la respuesta
		if(wit_intent[0] in ['temperature_get', 'wit$get_temperature']):
			message_s = apiCalls.get_weather(wit_location[0], unidad)
		elif(wit_intent[0] in ['temperature_set', 'wit$set_temperature']):
			message_s = apiCalls.set_weather(wit_location[0], wit_temp[0])
	
	# Si no se pudo interpretar el mensaje
	except Exception as e:
		message_s = f"{apiCalls.lang['es']['error']}"
		# message_s = f"Disculpas, no entendí\\. Por favor intenta de nuevo probando algo como \"¿Cual es el clima en Buenos Aires, Argentina?\"\\. Gracias\\!"
		raise Exception(message_s)
	
	return message_s

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/bot', methods=['POST'])
def main():
	message_s: str
	
	try:
		# Obtengo el JSON del mensaje
		telegramBot_r = request.json

		# Para debuggueo
		print("Telegram response: "+str(telegramBot_r))
		jsonMessage = 'message' # Por defecto es message

		# Si el mensaje es editado, se cambia el jsonMessage
		if('edited_message' in telegramBot_r):
			jsonMessage='edited_message'

		# Obtengo el ID del chat
		chat_id = telegramBot_r[jsonMessage]['chat']['id']

		# Envia señal de Escribiendo... al chat
		apiCalls.telegramAPI('sendChatAction', data={'chat_id': str(chat_id), 'action': 'typing'})

		# Geolocalización
		if('location' in telegramBot_r[jsonMessage]):
			message = telegramBot_r[jsonMessage]['location']
			print(message) #Para debuggueo
			message_s=apiCalls.get_open_weather_gps(str(message['latitude']), str(message['longitude']))
		# Mensaje de texto
		else:
			message = telegramBot_r[jsonMessage]['text']
			message_s=witInterpreter(message)

	# Si no se pudo interpretar el mensaje
	except Exception as e:
		print("Exception: " + str(e.__str__()))
		message_s=e

	print(message_s) # Para debuggueo
	
	# Envio el mensaje
	apiCalls.telegramAPI('sendMessage', dict(chat_id = chat_id, text = message_s, parse_mode='MarkdownV2'))

	return ''


if __name__ == '__main__':
	app.run()
