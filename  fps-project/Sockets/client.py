#!usr/bin/python
import socket

HOST = "10.0.0.6"
PORT = 5555

def main():
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((HOST,PORT))
	
	while 1:
		usrInput = raw_input("")
		
		if usrInput == "q":
			client.send(usrInput)
			client.close()
			break;

if __name__ == "__main__":
	main()