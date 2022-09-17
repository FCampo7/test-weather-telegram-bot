# Test weather telegram bot

### [@PTestWeatherBot](http://t.me/PTestWearherBot)

## Index:
- [Test weather telegram bot](#test-weather-telegram-bot)
		- [@PTestWeatherBot](#ptestweatherbot)
	- [Index:](#index)
- [English](#english)
	- [Description](#description)
	- [License](#license)
			- [License MIT](#license-mit)
	- [Project status](#project-status)
	- [Notes](#notes)
- [Español](#español)
	- [Descripción](#descripción)
	- [Licencia](#licencia)
			- [License MIT](#license-mit-1)
	- [Estado del proyecto](#estado-del-proyecto)
	- [Notas](#notas)

---
# English

## Description

Telegram bot that implements the [Wit.ai API](https://wit.ai/) to process the message sent by the user and reply with the weather of the desired location. Weather information provided by the [Open Weather Map API](https://openweathermap.org/api).

The webhook implementation is a fork from [RNogales94's project](https://github.com/RNogales94/Telegram-Bot-Heroku-Webhook-For-Medium-).

The bot is hosted on [pythonanywhere](https://www.pythonanywhere.com/) servers with a free plan.

## License

#### [License MIT](https://gitlab.com/FCampo/test-weather-telegram-bot/-/blob/main/LICENSE)

Please, if you are going to use it totally or partially, i will appreciate that reference my [GitLab profile](https://gitlab.com/FCampo), if is not too much inconvenience, Thanks!

## Project status

Under development.

## Notes

The folder "old" contains old files that are unnecessary, the only reason cause I keep it it's to use it as a guide for future projects. Can be deleted with no problem.

old/telegramBot.py was the bot first implementation, make use of schedules but didn't convince me, so decide to change it for a webhook.

---
# Español

## Descripción
Bot de Telegram que implementa la [API Wit.ai](https://wit.ai/) para procesar el mensaje enviado por el usuario y responder con el clima de la ubicación deseada. Información del clima proporcionada por la [API Open Weather Map](https://openweathermap.org/api).

La implementación del webhook es una bifurcación del [proyecto de RNogales94](https://github.com/RNogales94/Telegram-Bot-Heroku-Webhook-For-Medium-).

El bot está hosteado en los servers de [pythonanywhere](https://www.pythonanywhere.com/) con un plan gratuito.

## Licencia

#### [License MIT](https://gitlab.com/FCampo/test-weather-telegram-bot/-/blob/main/LICENSE)
Por favor, si lo va a utilizar total o parcialmente, agradeceré que haga referencia a mi [perfil de GitLab](https://gitlab.com/FCampo), si no es demasiada molestia, Gracias!

## Estado del proyecto

Bajo desarrollo.

## Notas

La carpeta "old" contiene archivos antiguos que no son necesarios, la única razón por la que la guardo es para usarla como guía para futuros proyectos. Se puede borrar sin problema.

old/telegramBot.py fue la primera implementación del bot, hacía uso de schedules pero no me convenció, así que decidí cambiarlo por un webhook.
