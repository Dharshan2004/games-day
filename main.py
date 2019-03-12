import pusher
import pyrebase
import time 
from gsheets import Sheets 
import os
pusher_clients = [
#anirudhasaraf123t
pusher.Pusher(
  app_id='715707',
  key='c524437e1b5b7c5b2f78',
  secret='1f71d40dedf076e24767',
  cluster='ap1',
  ssl=True
),
#tjcgamesday
pusher.Pusher(
  app_id='715770',
  key='65686ca69e230fdeed5b',
  secret='884df68ad44dcf9032d7',
  cluster='ap1',
  ssl=True
),
#tjcgamesday2
pusher.Pusher(
  app_id='715775',
  key='ecc6c2bdbb1c7e33ded9',
  secret='e2799445dd43fcbdbfd5',
  cluster='ap1',
  ssl=True
),
#tjcgamesday3
pusher.Pusher(
  app_id='715784',
  key='a9118261807d47f13f0d',
  secret='3b4e9caf8f748d5b619e',
  cluster='ap1',
  ssl=True
),
#tjcgamesday4
pusher.Pusher(
  app_id='715785',
  key='8cc2eab2a8c546690f08',
  secret='1b1a0aeb5c8325d6b73d',
  cluster='ap1',
  ssl=True
),
#tjcgamesday5
pusher.Pusher(
  app_id='715786',
  key='110c3ad5eb59136927ac',
  secret='163db0137cbb07365aa6',
  cluster='ap1',
  ssl=True
),
#tjcgamesday6
pusher.Pusher(
  app_id='715787',
  key='a3edf1a5f488e9a9d6e2',
  secret='fdb899a8618614b64aa2',
  cluster='ap1',
  ssl=True
),
#tjcgamesday7
pusher.Pusher(
  app_id='715788',
  key='caa5e35d8be834b55364',
  secret='52d2bb645e3be00a574f',
  cluster='ap1',
  ssl=True
),
#tjcgamesday8
pusher.Pusher(
  app_id='715789',
  key='a287341e860a33a09c53',
  secret='06345e254960803cffe5',
  cluster='ap1',
  ssl=True
),
#tjcgamesday9
pusher.Pusher(
  app_id='715790',
  key='035f240c26134eae472e',
  secret='b0f4c7015ee1638bcbcf',
  cluster='ap1',
  ssl=True
)]

config = {
	"apiKey": "AIzaSyAFQWHKQcfdZ0GmxwFzohjPjRm6vwcbREM",
	"authDomain": "mael-c2ed5.firebaseapp.com",
	"databaseURL": "https://mael-c2ed5.firebaseio.com",
	"storageBucket": "mael-c2ed5.appspot.com"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
sheets = Sheets.from_files('credentials.json')
url = 'https://docs.google.com/spreadsheets/d/1v_qSadYXZzS0TFuQ-vbmQKR95kKzFxiAvt-DQLwXeX8'

def error():
	print("ERROR")
	try:
		database.child("Error").set(1)
	except:
		print ("DATABASE ERROR (CHECK INTERNET)")


def get_client():
	Id = database.child('Id').get().val()
	Terminate = database.child('Terminate').get().val()
	if Terminate == 1:
		database.child('Terminate').set(0)
		os._exit(0)
	pusher_client = pusher_clients[Id]
	return [pusher_client, Id]

def get_external_scores():
	alpha = database.child("Alpha").get().val()
	beta = database.child("Beta").get().val()
	gamma = database.child("Gamma").get().val()
	delta = database.child("Delta").get().val()
	return [alpha, beta, gamma, delta]
def main(pusher_client):
	external_scores = get_external_scores()
	sheet = sheets.get(url)
	scores = {'Alpha': external_scores[0], 'Beta': external_scores[1], 'Gamma': external_scores[2], 'Delta': external_scores[3]} 
	for class_index in range(0, 74): #!! REMEMBER: Change range when JC Classes are ready in the google sheets
		student_index = 3
		if class_index == 47:
			continue
		while True:
			student_list = sheet.sheets[class_index][str(student_index)]
			try:
				if student_list[1] == '':
					break
			except:
				break
			house = student_list[3]
			if house == 'A':
				house = 'Alpha'
			elif house == 'B':
				house = 'Beta'
			elif house == 'G':
				house = 'Gamma'
			elif house == 'D':
				house = 'Delta'
			scores[house] = scores[house] + student_list[25]
			student_index += 1
	os.system('cls')
	print("Alpha:", scores['Alpha'])
	print("Beta:", scores['Beta'])
	print("Gamma:", scores['Gamma'])
	print("Delta:", scores['Delta'])
	print("Server:", pusher_client[1] + 1)
	scores['Greatest'] = max(scores.values())
	pusher_client[0].trigger('games_day', 'main', scores)

def run():
	try:
		time.sleep(0.2) 
		main(get_client())
	except:
		error()

while True:

	main(get_client())




