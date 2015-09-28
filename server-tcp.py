import socket
import sys
import hashlib
import random
import string

def Main(argv):
	#check command line arguments
	if len(sys.argv) != 2 and len(sys.argv) !=3:
		print "Check your arguments.\n\teg. python bank-serverTCP.py 8591 or\
		\n\tpython bank-serverTCP.py 8591 -d for debug mode" 
		sys.exit()
	#check port argument input
	try:
		port = int(sys.argv[1])
	except:
		print 'Invalid port number argument, please enter in the number format such as\n\t eg. python bank-serverTCP.py 8591'
		sys.exit()

	#check debug argument
	debug = False
	if len(sys.argv) == 3 and str(sys.argv[2])!='-d':
		print "Check your input argument for debug mode."
		sys.exit()
	if (len(sys.argv) == 3 and str(sys.argv[2]) == '-d'):
			debug = True
			print "Debug is mode on"

	#static argument
	host = "127.0.0.1" 
	userID = ["DrEvil", "Jimmie", "Yolanda"]
	userPass = ["minime123", "right?", "beCool"]
	userBal = [366.0, 2000.0, 150.0]

	#create socket
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	if debug:
		print "Created socket"
	s.bind((host,port))
	
	#server started
	while True:
		#listen to one client a time
		s.listen(1)
		connect = False
		conn, addr = s.accept()
		received = conn.recv(1024)
		req = str(received.decode())
		if debug:
			print "Received message:",req

		#when authentication is requested
		if(req == "authentication request"):
			chalValue = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(64))
			conn.send(chalValue.encode())
			if debug:
				print "Sent message:",chalValue
			received = conn.recv(1024)
			if debug:
				print "Received message:",received.decode('utf-8')
			#when Hash is received, check validity
			if received:
				username, Hash = str(received.decode()).split(',')
				if (username in userID):
					ind = userID.index(username)
					password = username + userPass[ind] + chalValue
					password = hashlib.md5(password.encode('utf-8')).hexdigest()
					#check validity of hash by user
					if (password == Hash) :
						if debug:
							print "Hash matched"
						connect = True
					else:
						if debug:
							print "Hash mismatched"
				#Connected if hash was correct
				if connect:
					if debug:
						print "Connection establised."
					conn.send(("Welcome "+username).encode())
					if debug:
						print "Sent Message:","Welcome "+username
					#Receive transaction message
					while connect:
						received = conn.recv(1024)
						if received:
							if debug:
								print "Received Message:",received.decode()
							try :
								transType, amt = received.decode().split(',')
								#check transaction type
								if(transType =='deposit'):
									userBal[ind] = userBal[ind] + float(amt)
									confirmation = "Your " +transType+ " of "+ amt+ " is successfully recorded.\
										\nYour new account balance is "+ str(userBal[ind])
									conn.send(confirmation)
									if debug:
										"Sent Message:",confirmation
									break;
								elif(transType == 'withdrawal'):
									userBal[ind] = userBal[ind] - float(amt)
									confirmation = "Your " +transType+ " of "+ amt+ " is successfully recorded.\
										\nYour new account balance is "+ str(userBal[ind])
									conn.send(confirmation)
									if debug:
										"Sent Message:",confirmation
								else:
									#check amt type
									try:
										float(amt)
									except:
										if debug:
											print "Invalid amount"
										connect = False
							except:
								#when the input was invalid
								if debug:
									print "Transaction Error" 
								connect = False
				else:
					#when authentication fails send failure message
					conn.send("Failed to authenticate user.".encode())
					if debug:
						print "Sent message:","Failed to authenticate user."
				#final message
				conn.send("\nThank you for banking with us.".encode())
				if debug:
					print "Sent message:","Thank you for banking with us."
				connect = False
	conn.close()

if __name__ == '__main__':
	Main(sys.argv)
