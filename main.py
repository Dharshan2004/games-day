import pusher #server
import pyrebase #firebase
import time #control timing for google sheets
from gsheets import Sheets #google sheets
#Pusher clients
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
#firebase configuration
config = {
    "apiKey": "AIzaSyAFQWHKQcfdZ0GmxwFzohjPjRm6vwcbREM",
    "authDomain": "mael-c2ed5.firebaseapp.com",
    "databaseURL": "https://mael-c2ed5.firebaseio.com",
    "storageBucket": "mael-c2ed5.appspot.com"
}

firebase = pyrebase.initialize_app(config) #firebase object
database = firebase.database() #database object
sheets = Sheets.from_files('credentials.json') #access credentials file
url = 'https://docs.google.com/spreadsheets/d/1v_qSadYXZzS0TFuQ-vbmQKR95kKzFxiAvt-DQLwXeX8' #google sheets url

def get_client():
	#retrieves current pusher id
	i = database.child('Id').get().val()
	pusher_client = pusher_clients[i]
	return pusher_client


def main(pusher_client):
	s = sheets.get(url) #retrieve google sheet from url
	scores = {'Alpha': 0, 'Beta': 0, 'Gamma': 0, 'Delta': 0} #dictionary of total scores
	for class_index in range(0, 22): #!! REMEMBER: Change range when JC Classes are ready in the google sheets
		student_index = 3 #starts from 3
		while True:
			ls = s.sheets[class_index][str(student_index)] #Individual student
			#print('ls',ls)
			try:
				#make sure that line is not empty
				x = ls[0]
				if x == '':
					break
			except:
				break
			house = ls[3] #4th element in individual student list is house
			if house == 'A':
				house = 'Alpha'
			elif house == 'B':
				house = 'Beta'
			elif house == 'G':
				house == 'Gamma'
			elif house == 'D':
				house = 'Delta'
			scores[house] = scores[house] + ls[25]  #total up the scores using the student's grand total
			student_index += 1

	print("Alpha:", scores['Alpha'])
	print("Beta:", scores['Beta'])
	print("Gamma:", scores['Gamma'])
	print("Delta:", scores['Delta'])
	pusher_client.trigger('games_day', 'main', scores) #send the scores to the pusher server in JSON format of {"Alpha": 0, "Beta": 0, "Gamma": 0, "Delta": 0}
	#pusher_client.trigger('games_day', 'alpha', scores['Alpha'])
	#pusher_client.trigger('games_day', 'beta', scores['Beta'])
	#pusher_client.trigger('games_day', 'gamma', scores['Gamma'])
	#pusher_client.trigger('games_day', 'delta', scores['Delta'])		
while True:
	time.sleep(0.5) #prevent overusage of google sheets api
	main(get_client()) #run main function with server id from firebase



