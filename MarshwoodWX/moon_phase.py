from bottle import route, run, template, hook, response
import requests

# This gets the API key from key.txt, which is not uploaded to GitHub:
with open("key.txt") as file: key = file.read()

# This header allows the server to be used as an API:
@hook('after_request')
def enable_cors():
	response.headers['Access-Control-Allow-Origin'] = '*'

# This function is called whenever someone tries to access localhost:8080/
@route('/')
def index():
	# Get the moon phase data
	response = requests.get('https://api.darksky.net/forecast/' + key + '/43.200710,-70.797379,2017-01-11T12:59:00-0500')
	# We multiply by 100 and convert to int for exact comparisons:
	moon_phase = int(response.json()["daily"]["data"][0]["moonPhase"] * 100)
	# Based off the number, get a description:
	if moon_phase == 0:
		moon_str = "New Moon"
	elif moon_phase < 25:
		moon_str = "Waxing Crescent"
	elif moon_phase == 25:
		moon_str = "First Quarter"
	elif moon_phase < 50:
		moon_str = "Waxing Gibbous"
	elif moon_phase == 50:
		moon_str = "Full Moon"
	elif moon_phase < 75:
		moon_str = "Waning Gibbous"
	elif moon_phase == 75:
		moon_str = "Last Quarter"
	elif moon_phase < 100:
		moon_str = "Waning Crescent"
	# We should never reach this case and something has gone wrong if we do:
	else:
		moon_str = "Error"
	# Finally, return the description:
	return moon_str

# Run the server at localhost:8080
run(host='localhost', port=8080)
