from socket import *
import sys
import hashlib
import random
import string

def Main(argv):
	#check arguments
	if len(sys.argv) != 2 and len(sys.argv) !=3:
		print "Check your arguments.\n\teg. python bank-serverUDP.py 8591 or\
		\n\tpython bank-serverUDP.py 8591 -d for debug mode" 
		sys.exit()

	#check if port input is right
	try:
		port = int(sys.argv[1])
	except:
		print 'Invalid port number argument, please enter in the number format such as\
		\n\t eg. python bank-serverUDP.py 8591'
		sys.exit()

	#check debug mode input
	debug = False
	if len(sys.argv) == 3 and str(sys.argv[2])!='-d':
		print "Check your input argument for debug mode."
		sys.exit()
	if (len(sys.argv) == 3 and str(sys.argv[2]) == '-d'):
			debug = True
			print "Debug is mode on"

	#static arguments
	host = "127.0.0.1" 
	userID = ["DrEvil", "Jimmie", "Yolanda"]
	userPass = ["minime123", "right?", "beCool"]
	userBal = [366.0, 2000.0, 150.0]

	#setting up server
	s = socket(AF_INET,SOCK_DGRAM)
	s.settimeout(1)
	if debug:
		print "\t*debug:Created socket"
	s.bind((host,port))
	if debug:
		"\t*debug:Server Started"

	#server is on	
	while True:
		connect = False
		gotMessage = False
		req = "req"

		#get authentication message
		while (not gotMessage):
			try:
				received, addr = s.recvfrom(1024)
				tag,req = str(received.decode()).split(":")
				p, auth = tag.split("@")
				user = ""
				#check user existence
				for ind in range(len(userID)) :
					if(p==userID[ind]):
						user = userID[ind]
						break;
					else:
						user = "invalid"
				if(user == "invalid"):
					s.sendto((p+"@chal:Failed to authenticate user."),addr)
				
				if(tag == (user+"@auth")):
					if debug:
						print "\t*debug:Received message:",req
					gotMessage = True
			except timeout:
				if debug:
					print "\t*debug:Waiting for message"

		#when authentication is requested
		if(req == "authentication request"):
			#send the challenge value to authenticate
			chalValue = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(64))
			chalValueMessage = user+'@chal:'+chalValue
			s.sendto(chalValueMessage.encode(),addr)
			if debug:
				print "\t*debug:Sending Challenge Value"
			
			#wait for client to reply with hash
			gotMessage = False
			while (not gotMessage):
				try:
					if debug:
						print "\t*debug:Waiting for Hash message"
					received, addr = s.recvfrom(1024)
					if debug:
						print "\t*debug:"+received.decode()
					tag, r = str(received.decode()).split(":")
					
					if(tag == (user+"@Hash")):
						if debug:
							print "\t*debug:Received Hash message"
						gotMessage = True
				except timeout:
					if debug:
						print "\t*debug:Resending Challenge Value"
					s.sendto(chalValueMessage.encode(),addr)

			# if received reply:
			username, Hash = r.split(',')
			if (username in userID):
				ind = userID.index(username)
				password = username + userPass[ind] + chalValue
				password = hashlib.md5(password.encode('utf-8')).hexdigest()
				
				#check hash
				if (password == Hash) :
					if debug:
						print "\t*debug:Hash matched"
					connect = True
				else:
					if debug:
						print "\t*debug:Hash mismatched"
					s.sendto((user+"@welcome:Failed to authenticate user."),addr)

				#when authenticated send welcome message 
				if connect:
					if debug:
						print "\t*debug:Connection establised."
					s.sendto((user+"@welcome:Welcome "+username).encode(),addr)
					if debug:
						print "\t*debug:Sent Message:","Welcome "+username
					#receive transaction message
					while connect:
						try:
							received, addr = s.recvfrom(1024)
							tag, r = str(received.decode()).split(":")
							if (tag==(user+"@trans")):
								if debug:
									print "\t*debug:Received message:",r.decode()
								try:
									#check transaction argument and amount
									transType, amt = r.decode().split(',')
									if(transType =='deposit'):
										userBal[ind] = userBal[ind] + float(amt)
										confirmation = user+"@trans:Your " +transType+ " of "+ amt+ " is successfully recorded.\
											\nYour new account balance is "+ str(userBal[ind]) +\
											"\nThank you for banking with us."
										if debug:
											"\t*debug:Sent Message:",confirmation
										s.sendto(confirmation,addr)
										break;
									elif(transType == 'withdrawal'):
										userBal[ind] = userBal[ind] - float(amt)
										confirmation = user+"@trans:Your " +transType+ " of "+ amt+ " is successfully recorded.\
											\nYour new account balance is "+ str(userBal[ind]) +\
											"\nThank you for banking with us."
										if debug:
											"\t*debug:Sent Message:",confirmation
										s.sendto(confirmation,addr)
										break;
									else:
										try:
											float(amt)
										except:
											if debug:
												print "\t*debug:Invalid amount received disconnecting"
											connect = False
								except:
									if debug:
										print "\t*debug:Sending message: Transaction Error"
									s.sendto(user+"@trans:Transaction Error",addr)
									connect = False
						except:
							if debug: 
								print "\t*debug:Need transaction message"
							connect = False

				else:
					#when authentication fails
					s.sendto(user+"@auth:Failed to authenticate user.".encode(),addr)
					if debug:
						print "\t*debug:Sent message:","Failed to authenticate user."
				connect = False
	s.close()

if __name__ == '__main__':
	Main(sys.argv)
