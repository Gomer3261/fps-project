#!/usr/bin/python
import socket

def main():
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((socket.gethostbyname(socket.gethostname()), 5555))
  server.listen(1)
  client, address = server.accept()
  print "Connected by", address

  while 1:
    data = client.recv(1024)

    if data == "q":
      break
    else:
      print data

if __name__ == "__main__":
  main()
