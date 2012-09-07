#!/usr/bin/python
from Tkinter import *

master = None
window = None

def InitializeWindow():
  master = Tk();
  window = Canvas(master, width=200, height=200)
  window.pack()
  window.create_line(0,0,200,100)
  window.create_line(0,100,200,0, fill="red", dash=(4,4))
  window.create_rectangle(50,25,150,75, fill="blue")
  master.mainloop()

def main():
  InitializeWindow()
  print "Game loop."

if __name__ == "__main__":
  main()