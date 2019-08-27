#!/usr/bin/env python3.6

import re,sys
#from lxml import html
import requests

def main():
	if len(sys.argv) > 2:
		print("Please Enter Only One Command At A Time")
	elif sys.argv[1] == '-w':
		#write new db from form file
		inputLoc = "form.idx"
		outputLoc = "Def14AFormsLink.db"
	
		print("Input File: {}\nOutput File: {}\n".format(inputLoc,outputLoc))


		print("Creating Dictionary")
		addressDict = createAddressDictionary(inputLoc)	

		print("Writing To New File")
		writeNewDB(outputLoc,addressDict)

		print("Writing Complete")

	elif sys.argv[1] == '-fs':
		#get fullScrape
		linkLocation = "Def14AFormsLink.db"
		edgarFullScrape(linkLocation)

	else:
		print("Please Enter a Valid Arg")

def edgarFullScrape(linkLocation):
	f = open(linkLocation, "r")
	# db format: "CIKNum|||Company Name|||DatedFile|||Link\n"
	counter = 0
	
	for line in f:
		if counter == 0:
			counter+=1

			continue
		splitLine = line.split("|||")
		page = requests.get(splitLine[3])
		counter+=1
		
		print("Scraping {}".format(splitLine[1]))
		newFileOutput = "./WebScrapes/HTML/"+splitLine[0]+"_"+splitLine[2]+".html"

		newFile = open(newFileOutput,"w")
		newFile.write(page.text)
		newFile.close
	

	print("Files Scraped: {}".format(counter-1))

def createAddressDictionary(inputLoc): 
	f = open(inputLoc)

	addressDict = {}

	for line in f:
		regex = re.search(r"(DEF 14A)\ {2,}(.+?)\ {2,}(.+?)\ {2,}(.+?)\ {2,}(.+?)\ {2,}", line)
		if regex == None:
			continue
		
		#print(regex)

		formType = regex.group(1)
		companyName = regex.group(2)
		cikNum = regex.group(3)
		dateFiled = regex.group(4)
		link = "https://www.sec.gov/Archives/"+regex.group(5)
		
		
		if cikNum in addressDict:
			print("Dupe Found At {}. Keeping Original".format(cikNum))
		else:
			addressDict[cikNum]=[]
			addressDict[cikNum].append(formType)
			addressDict[cikNum].append(companyName)
			addressDict[cikNum].append(dateFiled)
			addressDict[cikNum].append(link)

	return addressDict

def writeNewDB(outLoc,addressDict):
	open(outLoc, "w").close() #clears file
	
	f = open(outLoc,"w")
	f.write("CIKNum|||Company Name|||DatedFile|||Link\n")
	f.close()

	f = open(outLoc,"a")

	for key in addressDict.keys():
		f.write("{}|||{}|||{}|||{}\n".format(key,addressDict[key][1],addressDict[key][2],addressDict[key][3]))
	
	f.close()


main()
