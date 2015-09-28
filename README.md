Name:	YongHui Cho
Email: 	ycho46@gatech.edu
Date:	9/26/2015




Sockets Programming

Platform: Python 2.7.9

A.	Goals:
		Implement two complete separate versions of client and server using TCP and UDP

B.	List of all files:
	
	1.	remotebank-tcp.py	:	TCP client
	2.	server-tcp			:	TCP server
	3.	remotebank-udp.py	:	UDP client
	4.	server-udp.py			:	UDP server

C.	Detailed Instructions for compiling and running

	I. Server
		
		1.	Open a cmd window/terminal and go to the directory containing the server files
		2.	Type “python server-tcp 8951” to start TCP server in normal mode
	    		Type “python server-udp 8951” to start UDP server in normal mode
			(for debug mode simply add “-d” at the end of the command.	
				e.g.“python server-tcp 8951 -d”) 
	
		*Note that when running both TCP and UDP server at the same time you have to use a different port number.

	II. Client
		
		1.	Once server is up and running, open the cmd window/terminal and go to the the directory containing the client files
		2.	Type in to format of “python remotebank-tcp.py 127.0.0.1:8591 username password transaction amount”
			(eg.“python remotebank-tcp.py 127.0.0.1:8591 DrEvil minime123 deposit 100.0” or “python remotebank-udp.py 127.0.0.1:8591 DrEvil minime123 deposit 100.0” )
		
	III. Description of input parameters
		
		1.	IP address 				- 127.0.0.1 has to be exact for local host
		2.	Port						- within range 1024~65535
		3.	Username/Password 		- “DrEvil/minime123” or “Yolanda/beCool” or “Jimmie/right?”
		4.	Transaction				- “deposit” or “withdrawal”
		5.	Amount					- Should be in a number format. eg.”100” or “20.0”
		6.	Debug*					- “-d”
		
	IIII. Debug mode
		Debug mode is a mode where user gets to see what actions are being done by the server and the client as the program runs.
		It can be enabled by adding “-d” parameter at the commands

D.	Description of application protocol

	I. TCP application
	
		1.	Server
	
			a.	Checks command line arguments before initiation and set up static arguments (IP address, user credentials and info)
			b.	Creates the TCP socket, binds the IP address and port number from user input arguments
			c.	After TCP socket has been created, server runs and listens for client connection.
			d.	Socket accepts client’s connection, and waits for client’s “authentication request” message.
			e.	When message is confirmed, server sends challenge value to client and waits for computed MD5 Hash
			f.	When Hash message is verified on server, connection is established. 
				*(If Hash is wrong server sends client authentication fail message)
			g.	Server sends welcome message, and receives transaction information (Transaction type and amount) and checks validity. 
				*(if transaction information is invalid server sends transaction error message)
			h.	Server performs the transaction request to the client’s account and sends confirmation message
				*(Client disconnects after confirmation message)
			i.	goes back to d. (Socket accepts client’s connection, and waits for client’s “authentication request” message)

		2.	Client
			
			a.	Checks command line arguments before initiation.
			b.	Creates TCP socket, and connects to IP and port number from user input arguments.
			c.	Once connected, send “authentication request” message
			d.	Receive the challenge value, computes the MD5 hash and sends to server
				*(If server replies with authentication failure message, print failure message and client disconnects)
			e.	Receives confirmation welcome message from the server, and sends transaction information
				*(If server replies with authentication failure message, print failure message and client disconnects)
			f.	Client sends transaction information to server.
				*(If transaction information was invalid, client receives transaction error message and disconnects)
			e.	Client receives transaction confirmation message and disconnects.

	II. UDP application
		
		1.	Server

			a.	Checks command line arguments before initiation and set up static arguments (IP address, user credentials and info)
			b.	Creates the UDP socket, binds the IP address(127.0.0.1) and port number from user input port argument.
			c.	Server is up and running waiting to receive “authentication request” message from clients
			d.	When authentication message is received from client, check if user exists
				*(If authentication message does not arrive, server waits for authentication message)
			e.	Server send challenge value until user replies with an MD5 Hash message
				*(Until client sends an MD5 hash message, server sends challenge value again until server times out)
			e.	When server verifies MD5 hash, client is authenticated and server sends welcome message.
				*(If MD5 hash is invalid, send authentication failure message to client
			f.	Server waits from transaction message, 
				*(If transaction message is not received, server waits for the transaction message until server times out)	
			g.	Server receives transaction message, then server checks transaction message arguments and performs transaction and sends confirmation message
				*(If transaction message arguments, server responds to client and sends transaction error message)
			h.	Server goes back to c. (Server is up and running waiting to receive “authentication request” message from clients)

		2.	Client
			
			a.	Checks command line arguments before initiation.
			b.	Creates UDP socket and start sending authentication request
				*(if there is no reply from the server client disconnects after client times out)
			c.	Client receives a reply with a challenge value from the server, and sends the computed MD5 Hash
				*(If there is no reply from the server with a welcoming message, client  sends Hash until client times out )
			d.	Client receives a reply with a welcoming message, and sends the transaction message
				*(If there is no reply from the server with transaction confirmation message, client sends transaction message until client times out)
			e.	Client receives a reply with confirmation message, and disconnects

E.	Bugs 

	1.	UDP has timeout of 1 secs. UDP clients disconnects after sending 10 messages to get a reply from the server. 

F.	Limitations

	1.	TCP server only processes one connection at a time
	2.	UDP server accommodates all transactions from multiple clients but process one at a time.

G.	References

	1.	https://docs.python.org/2/library/socket.html
	2.	https://wiki.python.org/moin/UdpCommunication
	3.	http://rosettacode.org/wiki/MD5
	4.	https://en.wikipedia.org/wiki/MD5#Algorithm
	5.	Stackoverflow
	6.	Textbook







