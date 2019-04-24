#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################
### Grabs the selected proof photos
### Written by: Dylan Clark (dbhclark@gmail.com) (Narcosia)
### Version          Date        Changes
### 1.0              20/09/18    Initial Version
###########################################

import re
import urllib.request
import argparse
from bs4 import BeautifulSoup

###########################################
###	CONFIG
###########################################

search="selected"
attribute='data-photoid'

###########################################
###	FUNCTIONS
###########################################

def ascii_art():
	print(r"""____________ _____  ___________   _____ ______  ___  ____________ ___________ 
| ___ \ ___ \  _  ||  _  |  ___| |  __ \| ___ \/ _ \ | ___ \ ___ \  ___| ___ \
| |_/ / |_/ / | | || | | | |_    | |  \/| |_/ / /_\ \| |_/ / |_/ / |__ | |_/ /
|  __/|    /| | | || | | |  _|   | | __ |    /|  _  || ___ \ ___ \  __||    / 
| |   | |\ \\ \_/ /\ \_/ / |     | |_\ \| |\ \| | | || |_/ / |_/ / |___| |\ \ 
\_|   \_| \_|\___/  \___/\_|      \____/\_| \_\_| |_/\____/\____/\____/\_| \_|
""")                                                                              
                                                                              
def fancy_line():
	print("\n######################################################################################\n")

# Human Readable Sorting
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def html_requester(link):
	response = urllib.request.urlopen(link)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup

def html_parser(soup, link):
	pics = []
	for div in soup.find_all("div", class_=search):
		a = div.find('a')
		pics.append(a.attrs[attribute])
	print("Proof Gallery:\n")
	for tag in soup.find_all("meta"):
	    if tag.get("property", None) == "og:title":
	        print("%s" % tag.get("content", None))
	return pics

def printer(pics):
	pics.sort(key=natural_keys)
	print ("Selected Proofs: \n")
	for pic in pics:
		print("%s" % pic[5:])

def printer_search_format(pics):
	# search_regx = re.compile('-[0-9]+$')
	select_list=[]
	pics.sort(key=natural_keys)
	for pic in pics:
		# file_number = search_regx.search(pic)
		file_number = re.search(r'-[0-9]+$',pic,re.M) # regex oneliner
		pic = pic[5::]
		try:
			select_list.append(file_number.group())
		except:
			select_list.append(pic)
	print("Lightroom Search Format: \n")
	print("%s" % ','.join(select_list))
	fancy_line()
	print("Total Proofs: %d" % len(pics))


def arg_input():
	parser = argparse.ArgumentParser(description='Proof Grabber')
	parser.add_argument('-u', '--url',
						required = False,
						metavar = "STRING",
						help='URL of Proof Gallery')

	args = parser.parse_args()
	if args.url == None:
		link=user_input()
	else:
		link=args.url
	return link

def user_input():
	link = input("Enter Proof Gallery Link: ")
	return link


###########################################
###	MAIN
###########################################

fancy_line()
ascii_art()
fancy_line()
link=arg_input()
soup=html_requester(link)
pics=html_parser(soup, link)
fancy_line()
printer(pics)
fancy_line()
printer_search_format(pics)
fancy_line()

