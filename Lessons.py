#!/usr/bin/env python
#Python script to automagicly give information about lessons on a day
import datetime
import argparse
import sys
import math
##PARSING ARGUMENTS (BUT NOT STARTING THEM)
##TODO:COLOUR PARSER
parser = argparse.ArgumentParser(description='Gives information about lessons on a given day.', epilog='Tshadwell 2011')
parser.add_argument('-w', type=int, choices=[1, 2], required=True, dest='week', help='Week to handle.')
parser.add_argument('-d', type=int, choices=[1, 2, 3, 4, 5, 6, 7], dest='day',  help='Output a timetable for given day.')
parser.add_argument('-p', type=int, choices=[1, 2, 3, 4, 5], dest='period', help='This switch will output a lesson, given its period.')
parser.add_argument('--notes',  action='store_true', dest='notes',  help='Draw up a timetable of notes. --verbose makes the output \'fancier\'.')
parser.add_argument('--week', action='store_true', dest='wholeweek', help='Draw up a timetable for the whole week')
parser.add_argument('--verbose', action='store_true', dest='verbose',  help='Be somewhat more verbose with output.')
parser.add_argument('--colours', action='store_true', dest='colours',  help='Use some artistic licence with my console colours.\n [Linux Only!]')
args = parser.parse_args()
##Throw them out if they've not given us the week
if (args.week == None):
	sys.exit()



def OrdinalSuffix ( numeral ):
	ret= str(numeral)
	if ((int(str(numeral)[-1]) < 4) and not ((int(str(numeral)) > 10) and (int(str(numeral)) < 14))):
		lst = str(numeral)[-1]
		if lst == "1":
			ret=ret+"st"
		elif lst == "2":
			ret=ret+"nd"
		elif lst == "3":
			ret=ret+"rd"
		else:
			ret=ret+"?"
	else:
		ret=ret+"th"
	return ret


def DayNumToName ( num, IsZeroBased ):
	Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	if (IsZeroBased == True):
		return Days[num]
	else:
		return Days[num -1]
def EzList ( num, IsZeroBased ):
	descriminant = 1
	if (IsZeroBased == True):
		descriminant = 0
	if (int(num) > descriminant):
		return ","
	else:
		return ""
now = datetime.datetime.now()
today = now.weekday()
#Form schedule[w][d][p]= lesson (as string)
#Notes for extention: scedule is an array in the form currently [week1:[M[]T[]W[]T[]F[]]2:[M[]T[]W[]T[]F[]], adding lessons per day needs no code modification. Adding more weeks, however
#requires you to edit the -w argument to [1, 2, 3 ... n] to support your n-week rota.
schedule=[
#WEEK 1
[
#Monday
["Chemistry", + "Physics", "Physics","Maths", "Biology"],
#Tuesday
["Maths", "Biology", "Biology", None,  "Chemistry"],
#Wednesday
["Chemistry", None,   "Maths",  "Physics", "Liberal"],
#Thursday
["Chemistry", None,   "Maths",  "Biology",  "Physics"],
#Friday
[  "Maths", None,  "Chemistry",  "Physics", None],
#Saturday
[None, None, None, None, None],
#Sunday
[None, None, None, None, None]
],
#WEEK 2
[
#Monday
["Chemistry",   "Maths",  "Physics",  "Biology",   "Maths"],
#Tuesday
["Physics",  "Biology",  "Biology",  "Chemistry",  "Chemistry"],
#Wednesday
["Biology",   "Maths", None,  "Physics", "Liberal"],
#Thursday
["Biology",  "Physics",  "Biology",  "Chemistry",   "Maths"],
#Friday
["Chemistry",  "Physics",   "Maths", None, None],
#Saturday
[None, None, None, None, None],
#Sunday
[None, None, None, None, None]
]
]

verbose = bool(args.verbose)
verbstop=""
verbline=""
##Verbose output customisation step ("Today's lessons:", "(date)'s lessons" etc. etc.)
if (verbose == True):
	timetable_intro="Timetable for"
	lesson_intro= "Lesson in"
	notes_intro= ""
	verbstop="."
	verbline="\n"
##START DOING STUFF!
#What zero-based week is it?



week = int(args.week) -1
day = 1337
out = "SRS ERROR"
if ((args.notes != True) and (args.wholeweek != True)):
	#If they give us a lesson number, then we need to give them the lesson.
	if (args.period != None):
		#If they don't give us the day, we need to derive it.
		if (args.day  == None):
			day = today
			#Give them what they asked for
			out=""
			if (verbose == True):
				out = lesson_intro + " week " + str(args.week) +  ", "+ OrdinalSuffix(args.period) + " period on " + DayNumToName(day, True) + ": "
			
			out = out + schedule[week][day][args.period] + verbstop
		else: 
			#If they do, it becomes very simple.
			out=""
			if (verbose == True):
				out = lesson_intro + " week " + str(args.week) +  ", "+ OrdinalSuffix(args.period) + " period on " + DayNumToName(args.day, False) + ": "
			out = out + schedule[week][args.day-1][args.period] + verbstop
	else:
		#If they've not given the lesson number, they want the schedule for that day.
			#If they don't give us the day, we need to derive it.
		if (args.day  == None):
			day = today
			#START THE ITERATION!
			out = ""
			if (verbose == True):
				out = timetable_intro + " week " + str(week+1) + " " + DayNumToName(day, True) + "\n"
				count=1
			for i in schedule[week][day]:
				if (verbose == True):
					out = out + OrdinalSuffix(count) + " period:\n"
					count=count+1
				out = out + " " + str(i) + verbline
		else: 
			#If they do, it becomes very simple.
			out = ""
					#START THE ITERATION!
			out = ""
			if (verbose == True):
				out = timetable_intro + " week " + str(week+1) + " " + DayNumToName(args.day, False) + "\n"
				count=1
			for i in schedule[week][args.day -1]:
				if (verbose == True):
					out = out + OrdinalSuffix(count) + " period:\n"
					count=count+1
				out = out + " " + str(i) + verbline
elif ((args.notes == True) and (args.wholeweek == True)):
	print("You can't do both!")
	sys.exit()
elif ((args.notes == True) and (args.wholeweek != True)):
	out = ""

	##Handle args.
	if (args.day == None):
		day = today
	else:
		day = args.day
	##Date File.
	now = datetime.datetime.now();
	out = out + str(now.hour).lstrip("0") + now.strftime(":%M on %A, the ") + str(now.day).lstrip("0")
	#1st 2nd 3rd 4th 5th 6th 7th 8th 9th 10th 11th - 21st 22nd 23rd
	
	if ((int(str(now.day)[-1]) < 4) and not ((int(str(now.day)) > 10) and (int(str(now.day)) < 14))):
		lst = str(now.day)[-1]
		if lst == "1":
			out=out+"st"
		elif lst == "2":
			out=out+"nd"
		elif lst == "3":
			out=out+"rd"
		else:
			out=out+"?"
	else:
		out=out+"th"
	out = out + " of " + now.strftime("%B %Y") + "\n"
	out += "-" * len(out) + "\n\n"
	##Start writing out lessons
	iterationconst = 1
	for lessons in schedule[week][day]:
		
		line = OrdinalSuffix(iterationconst) + " period: " + str(lessons)
		if (verbose == True):
			out += " " + "_-" * math.ceil(len(line)/2) + "_" + "\n"+ "| " + line + "|" + "\n" + " " + "-_" * math.ceil(len(line)/2) + "-" + "\n\n"
		else:
			out += line + "\n" + "-" * len(line) + "\n\n"
		iterationconst += 1
elif ((args.notes != True) and (args.wholeweek == True)):
	out=""
	if (verbose == True):
		out = out + "Week " + str(week +1) + " Timetable\n"
	counter = 1
	for days in schedule[week]:
		out = out + "\n" + DayNumToName(counter, False) + "\n"
		counter=counter+1
		secondlevelcounter=1
		for lesson in days:
			if (verbose == True):
				out = out + "\nPeriod " + str(secondlevelcounter) + ":\n"
			else:
				out = out + EzList(secondlevelcounter, False) + " "
			secondlevelcounter=secondlevelcounter+1
			out = out + str(lesson)
		out = out +"\n"
else:
	print("Something has gone very wrong!")
print(out.strip())
