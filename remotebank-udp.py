from socket import *
import hashlib
import sys

def Main(argv):
	#checks arguments
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

	#check debug mode
	debug = False
	if (len(args) == 7 and args[6] == '-d'):
			debug = True

	#check if port is an integer
	try:
		port = int(port)
	except:
		if debug:
			print "\t*debug:port input",port
		print 'Invalid port number argument, please enter in the number format such as\n\t eg. python bank-serverTCP.py 8591'
		sys.exit()

	#create socket
	s = socket(AF_INET, SOCK_DGRAM)
	s.settimeout(1)
	

	#send authentication request
	if debug:
		print "\t*debug:Sending authentication request to server <"+ip+"><"+str(port)+">"
	s.sendto((username+"@auth:authentication request".encode()),(ip, port))
	
	time = 0
	gotMessage = False
	while (not gotMessage):
		try:
			if debug:
				print "\t*debug:Waiting to receive challenge value"
			received, addr = s.recvfrom(1024)
			tag,chalValue = str(received.decode()).split(":")
			if(tag == (username+"@chal")):
				if debug:
					print "\t*debug:Received challenge value"
				gotMessage = True
		except timeout:
			while(time < 10):
				print "Resending Authentication Request Message"
				s.sendto((username+"@auth:authentication request".encode()),(ip, port))
				time = time +1
			print "No reply from server after " + str(time) +" tries. Aborted "
			s.close()
			sys.exit()

	#when authentication is wrong the chal value message contains failure message
	if(chalValue=="Failed to authenticate user."):
		print chalValue
		s.close()
		sys.exit()
	
	#creating Hash message = username, (username + password + challenge value)
	Hash = (username+','+hashlib.md5((username + password + chalValue).encode('utf-8')).hexdigest()).encode()
	
	#sending Hash message
	if debug:
		print "\t*debug:Sending Hash Message"
	HashMessage = username+"@Hash:"+Hash
	s.sendto(HashMessage,(ip,port))
	time = 0
	gotMessage = False
	while (not gotMessage):
		try:
			received, addr = s.recvfrom(1024)
			tag, confirm = str(received.decode()).split(":")
			if(tag == (username+"@welcome")):
				if debug:
					print "\t*debug:Received Hash authentication message"
				gotMessage = True
		except timeout:
			while(time < 10):
				print "Resending username, hash <"+str(Hash.decode())+"> to server"
				s.sendto(HashMessage, addr)
				time=time+1
			print "No reply from server after " + str(time) +" secs. Aborted "
			s.close()
			sys.exit()

	#when successfully authenticated with hash, send transaction info
	if str(confirm.decode()) != "Failed to authenticate user.":
		if debug:
			print "\t*debug:Sending transaction information <" + str(transaction+","+amt) +">"
		if str(transaction)!='deposit' and str(transaction)!='withdrawal':
				print "Invalid trasaction. Choose either deposit or withdrawal"
				s.sendto((username+"@trans:Invalid transaction").encode(),addr)
				s.close()
				sys.exit()
		s.sendto((username+"@trans:"+str(transaction+","+amt).encode()),addr)
		
		time = 0
		gotMessage = False
		while (not gotMessage):
			try:
				received, addr = s.recvfrom(1024)
				tag, r = str(received.decode()).split(":")
				if(tag == (username+"@trans")):
					if debug:
						"\t*debug:Received transaction message"
				gotMessage = True
			except timeout:
				while(time<10):
					print "Resending Trasaction message"
					if str(transaction)!='deposit' and str(transaction)!='withdrawal':
						print "Invalid trasaction. Choose either deposit or withdrawal"
						s.sendto((username+"@trans:Invalid transaction").encode(),(ip,port))
						s.close()
						sys.exit()
					try:
						float(amt)
					except:
						print "Check your amount. It should be in number format\n\teg.100.00"
						s.sendto((username+"@trans:Invalid Amount").encode(),(ip,port))
						s.close()
						sys.exit()
					s.sendto((username+str("@trans:"+transaction+","+amt)).encode(),(ip,port))
					time= time +1
				print "No reply from server after " + str(time) +" secs. Aborted "
				s.close()
				sys.exit()
		if debug:
			print "\t*debug:Received transaction comfirmation message"
		print str(r.decode())
	else:
		#print Failed to authenticate user
		print str(confirm.decode())

	#finish connection
	s.close()

if __name__ == "__main__":
	Main(sys.argv)
