# -*- coding: utf-8 -*-
import re,sys
from optparse import OptionParser
import mailbox

#GLOBAL VARIABLES
emails_arr = []
excluded = ["reply","amazon","facebook","google","twitter","instagram","linkedin","youtube","tripadvisor"] #FILTERS

def usage():
	print "thisfile.py --write outputfile --exclude your@email.com"
	sys.exit(1)

def save(file,fromto):
	fo = open(file,"a")
	for message in mailbox.mbox("mailbox.mbox"):
		try:
			if "@" in message[fromto]:
				if "<" in message[fromto] and ">" in message[fromto]:
					email = message[fromto].split("<")[1].split(">")[0].lower()
				else:
					email = message[fromto].lower()
				#IF MULTIPLE EMAILS
				if "," in email:
					emails = email.split(",")
					for e in emails:
						e = re.sub("\s+"," ",e).strip()
						if (e not in emails_arr) and (any(ex in e for ex in excluded)==False):
							emails_arr.append(e)
							print "[+] added {}".format(e)
							fo.write(e+"\n")	
				else:
					if (email not in emails_arr) and (any(ex in email for ex in excluded)==False):
						emails_arr.append(email)
						print "[+] added {}".format(email)
						fo.write(email+"\n")
		except:
			print "[-] Error.. Split to next email"
	fo.close()

def main():
	# ARGPARSER
	parser = OptionParser()
	parser.add_option("-w", "--write", dest="filename")
	parser.add_option("-e", "--exclude", dest="myemail")
	(options, args) = parser.parse_args()
	filename = options.filename
	# CONTROL ARGUMENTS NEEDED
	if not filename:
		usage()
	# ADD YOUR EMAIL TO FILTERS
	if re.match(r"[^@]+@[^@]+\.[^@]+", options.myemail):
		excluded.append(options.myemail)
	else:
		usage()
	# CLEAN FILE
	fo = open(filename,"w")
	fo.close()
	# LAUNCH
	save(filename,"from")
	save(filename,"to")

if __name__ == "__main__":
	main()
