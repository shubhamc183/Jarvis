import speech_recognition as sr
import pyttsx
import random
import os
import threading
import time
import requests
from bs4 import BeautifulSoup
engine=pyttsx.init()
engine.setProperty('rate',140)
r=sr.Recognizer()
m=sr.Microphone()
playing=[]
jobs=[]
change=0
f=open('details','r')
s=f.read()
SONGS=s.split('\n')
songs=(s.lower()).split('\n')
f.close()
t=len(songs)
#----------------------------------------------------------------------------------------------------------
def speak(s):
	engine.say(s)
	engine.runAndWait()
#-----------------------------------------------------------------------------------------------------------
def play():					#TO play randomly any songs from your songs directory
	global change
	change=1
	selected=SONGS[random.randint(0,t-1)]
	print(selected)
	selected="'"+selected+"'"
	prompt='cvlc --play-and-exit /root/Shubham/Music/'+selected		#direct this to your songs folder
	playing.append(selected)
	os.system(prompt)
	print("Song is over")
	playing.remove(selected)
	#play()
	#Uncomment play() if u want diff. songs to be played infinetly ,coz pkill vlc will kill song n again will pe played by 'play()' function
def player():
	t=threading.Thread(target=play)
	t.start()
#--------------------------------------------------------------------------------------------------------------
def play1(*q):								#To play a particular song
	global change
	change=1
	print('play1 also got')
	hits=[0 for x in range(len(songs))]
	for item in q:
		for i in range(len(songs)):
			if item in songs[i]:
				hits[i]+=1
	print(hits)
	m=max(hits)
	same=[]
	for i in range(len(hits)):
		if m==hits[i] and m!=0:
			same.append(i)
	if len(same)==1:
		q=SONGS[same[0]]
		q="'"+q+"'"
		playing.append(q)
		selected='cvlc --play-and-exit /root/Shubham/Music/'+q
		os.system(selected)
		playing.remove(q)
	elif len(same)>1:						#if song match is more than 1
		speak('Sir did you meant')
		for i in range(len(same)):
			speak(SONGS[same[i]])
			if i<len(same)-1:
				speak("or")
			time.sleep(.3)
		change=1
		speak("Choose your option")
	elif m>0:
		q=SONGS[hits.index(max)]
		q="'"+q+"'"
		playing.append(q)
		selected='cvlc --play-and-exit /root/Shubham/Music/'+q
		os.system(selected)
		playing.remove(q)
	else:
		s=''
		for i in q:
			s+=i
		tospeak='cannot find'+s
		speak(tospeak)
def player1(q):
	print('got q')
	print(q)
	t=threading.Thread(target=play1,args=q)
	t.start()
#---------------------------------------------------------------------------------------
def news():
	print('Getting news...!')						#to get top 5 news from Google News
	q=requests.get('https://news.google.co.in/')
	soup=BeautifulSoup(q.text)
	l=[i.text for i in soup.findAll("span","titletext")]
	for i in range(5):
		print(l[i])
		speak(l[i])
		time.sleep(.2)
#--------------------------------------------------------------------------------------
def  brain(s):
	global change								#works only when 'jarvis' is said..!
	change=0
	s=s.lower()								#lowers all the word
	l=s.split()
	if 'jarvis' in l:
		change=0
		if l[1]=='play':
			if(len(playing)>0):
				q='Already '+playing[0]+' playing'
				speak(q)
				change=1
			elif l[2]=='song' or l[2]=='music':
					if(len(playing)==0):
						player()
					else:
						q='Already '+playing[0]+' playing'
						speak(q)
						change=1
			else:
					player1(l[2:])
		if l[1]=='open':						#open website
				websites=['google','facebook','youtube','github','amazon','flipkart','spandeal','paytm','wikipedia','w3schools','edx','codecademy','codechef','hackerrank','gmail','fossbytes','tvfplay']
				asked=l[2:]
				if len(asked)==1:
					if asked[0] in l:
						speak('opening '+asked[0])
						os.system('firefox www.'+asked[0]+'.com')
						change=1
				else:
					q=''
					for i in asked:
						q+=i+' n '
					q=q[:len(q)-2]		# so dat not 'and' is said at last :p Grammatically correct..! 
					speak('opening '+q)
					for i in asked:
						os.system('firefox www.'+i+'.com')
					change=1
		if l[1]=='search':						#to search google
				if len(l)>2:
					change=1
					q=l[2:]
					query,speakable='',''
					for i in range(len(q)):
						query+=q[i]+'+'
						speakable+=q[i]+' '
					query=query[:len(query)-1]
					speak('searching '+speakable)
					os.system('firefox https://www.google.co.in/?#q='+query)
		if l[1]=='stop':						#to stop the playing music
			if l[2]=='song' or l[2]=='music':
				if(len(playing)>0):
					os.system('pkill vlc')				
					print("killing")
					change=1
				else:
					speak('Not playing anything')
		if l[1]=='what':			
			if l[3]=='playing':					#to tell what is playing
				change=1
				if(len(playing)>0):
					speak(playing[0])
				else:
					speak('nothing sir')
			if l[3]=='time':					#to tell time
				q=time.ctime()
				t=''
				t+=q[11:13]+' hours '+q[14:16]+' mins'
				print(t)
				speak(t)
				change=1 
		if l[1]=='read':
			if l[2]=='fortune':					#to read fortune
				change=1					#fortune is a package in linux which tells a randomfortune
				os.system('fortune -s > f') 
				f=open('f','r')
				t=f.read()
				f.close()
				print(t)
				os.system('rm f')
				speak(t) 
			if l[2]=='news' or l=='new':
				news()
				change=1
		if change==0:
			speak('sorry sir I can\'t understand you ')
#--------------------------------------------------------------------------------------------------------
def callback(r,audio):
	try:
		s=r.recognize_google(audio)
		print(s)
		brain(s)
	except sr.UnknownValueError:
		print("~~~~~~~~~~~~~~~~~~~")
	except sr.RequestError as e:
		print('Internet Error......!')
with m as source:
        r.adjust_for_ambient_noise(source)
print("			Welcome Sir......!")
stop_listening=r.listen_in_background(m,callback)		
speak('Jarvis at your command sir')
while(True):								#Always running to listen
        pass                                  
