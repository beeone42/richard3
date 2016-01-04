#!/usr/bin/python

import time, signal, sys, os, commands



def already_running():
	script_name = "omxplayer"
	l = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}' | awk '{print $2}'" % script_name)
	if l[1]:
		signal.signal(signal.SIGINT, signal_handler)		# ctr+c 
	else:
		print(chr(27) + "[2J") 					# Permet de faire un clean de l'ecran mais ne fonctionne au reboot
		os.system('omxplayer -o local -r -b --win "0 0" /home/pi/video.mp4 &')


while True:								#
	def signal_handler(signal, frame):				#
		sys.exit(0)						# CTRL + C 
	already_running()						#
	time.sleep(0.2) 						#

