#!/usr/bin/python

"""
Alarm clock script

Checks time and plays random music from a predefined folder.

Usage: jumpstart.py hour minutes full_path_to_folder|file &

"""

import threading
import os
import time
import sys
import random
from subprocess import call


class jumpstart(threading.Thread):
	
	def __init__(self, hour, minute, music_source):
		threading.Thread.__init__(self)
		self.hour = hour
		self.minute = minute
		self.music_source = music_source

	#Check to see if its time to alarm every 30 seconds
	def run(self):

		while(True):

			ticks = time.localtime()
			self.current_hour = ticks[3]
			self.current_minute = ticks[4]

			self.alarm()
			time.sleep(60)
			
	#If current hour matches alarm hour take an action
	def alarm(self):
		if (self.current_hour == self.hour and 
			(self.current_minute == self.minute or
			self.current_minute == self.minute+1 or 
			self.current_minute == self.minute+2)):

			print "Time to wake up!"

			if os.path.isdir(self.music_source):
				self.play_random(self.music_source)
			
			elif os.path.isfile(self.music_source):
				self.play_music(self.music_source)
			
			else:
				print "Not a valid file or folder"
			
			sys.exit()			

	#When given a folder, search the folder for .mp3
	# and play at random
	def play_random(self, music_source):
		
		music_files = []

		#check if the directory has been ended with slash
		#for easy appending
		if music_source[-1] != '/':
			music_source = music_source + '/'

		for file in os.listdir(music_source):
			if file.endswith(".mp3"):
				music_files.append(file)

		randomized = random.randint(0, len(music_files)-1)

		randomized_file = music_source + music_files[randomized]
		self.play_music(randomized_file)

	#When file is given call local mac player and play 
	def play_music(self, music_file):
		print "Playing: " + music_file
		call(["afplay", music_file])


def main():

	#Sanity checks
	if len(sys.argv) == 1:
		print "Usage: jumpstart.py hour minutes full_path_to_folder|file &"
		print "\n"
	else:
		if ((str(sys.argv[1]).isdigit()) and 
			str(sys.argv[2]).isdigit()): 
		
			hours = int(str(sys.argv[1]))
			minutes = int(str(sys.argv[2]))
			music_source = str(sys.argv[3])

		else:
			print "\033[1;31mError: Digits only\033[0m" 
			print "Usage: jumpstart.py hour minutes full_path_to_folder|file &"
			print "\n"
			sys.exit()

		if (0 <= hours <= 23 and 
			0 <= minutes <= 59):

			alarmclock = jumpstart(hours,minutes,music_source)

			print "Your Alarm has been set for " + str(hours) + ":" + str(minutes).zfill(2)

			alarmclock.start()
		

		else:
			print "\033[1;31mError: Time out of range\033[0m" 
			print "Usage: jumpstart.py hour minutes full_path_to_folder|file &"	
			print "Usage ex: jumpstart.py 14 55 ~/Music/mymusic.mp3"



main() 