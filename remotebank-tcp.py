import socket
import hashlib
import sys

def Main(argv):
	args = sys.argv
	if len(args) != 6 and len(args) != 7:
		print "Check your input arguments."
		sys.exit()
	if len(args) == 7 and str(args[6])!='-d':
		print "Check your input argument for debug mode."
		sys.exit()
	ip,port= args[1].split(':')
	if ip!="127.0.0.1" :
		print "Check your IP. It should be 127.0.0.1"
		sys.exit()
	username = args[2].decode('utf-8')
	password = args[3].decode('utf-8')
	transaction = args[4].decode('utf-8')
	amt = args[5].decode('utf-8')

	debug = False
	if (len(args) == 7 and args[6] == '-d'):
			debug = True

	s = socket.socket()


	try:
		if debug:
			print "\t*debug:Connecting to <"+ip+"><"+port+">"
		s.connect((ip,int(port)))
		if debug:
			print "\t*debug:Connected."
	except:
		print "Connection failure. Please check your input of IP address and Port number.\
		\n\teg.\"python remotebankTCP.py 127.0.0.1:8591 username password\" or\
		 \n\t eg.\"python remotebankTCP.py 127.0.0.1:8591 username password -d\" for debug mode."
		sys.exit()

	# auth request
	s.send("authentication request".encode())
	if debug:
		print "\t*debug:Sending authentication request to server <"+ip+"><"+port+">"

	#receive challenge value
	received = s.recv(1024)
	chalValue = str(received.decode())
	# print chalValue

	#creating Hash message = username, (username + password + challenge value)
	Hash = (username+','+hashlib.md5((username + password + chalValue).encode('utf-8')).hexdigest()).encode()
	
	# print Hash + " asdfasdasfd"
	#send Hash
	s.send(Hash)
	if debug:
		print "\t*debug:Sending username, hash <"+str(Hash.decode())+"> to server"
	
	#wait for response
	while True:
		if debug:
			print "\t*debug:Waiting for response."
		received = s.recv(1024)
		if received and str(received.decode()) == "Welcome "+username :
			if debug:
				print "\t*debug:Authenticated."
			break
		else:
			print "Check user credentials"
			s.send("Invalid user credentials".encode())
			s.close()
			sys.exit()

	#when successfully authenticated do send transaction info
	if str(received.decode()) != "Failed to authenticate user.":
		# print str(received.decode())
		if debug:
			print "\t*debug:Sending transaction information <" + str(transaction+","+amt) +">"
		if str(transaction)!='deposit' and str(transaction)!='withdrawal':
			print "Invalid trasaction. Choose either deposit or withdrawal"
			s.send("Invalid transaction".encode())
			s.close()
			sys.exit()
		try:
			float(amt)
		except:
			print "Check your amount. It should be in number format\n\teg.100.00"
			s.send("Invalid Amount".encode())
			s.close()
			sys.exit()
		s.send(str(transaction+","+amt).encode())
		if debug:
			print "\t*debug:Receiving transaction comfirmation and updated account information"
		received = s.recv(1024)
		print str(received.decode())
		s.close()
	else:
		print str(received.decode())
	s.close()

if __name__ == "__main__":
	Main(sys.argv)
