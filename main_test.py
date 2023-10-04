#Portland State University
#Professor Nirupama Bulusu
#IRC Project

#This module contains the socket connection
import socket
import threading #for multiple process


host = socket.gethostname() #localhost
port_number = 55599  #do not use 0 to 40000, as they are reserved

#starting the server
#AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections
#AF_INET is for the type of addresses that makes connection (Internet) and SOCK_STREAM is for tcp connections
server_details = socket.socket()
server_details.bind((host, port_number)) #server is binding
server_details.listen() #now its in listening mode


commands = '\nList of commands:\n' \
               '1.$listroom to list all the rooms\n' \
               '2.$listusers to list all the users\n' \
               '3.$quit to quit\n' \
               '4.$help to list all the commands\n' \
               '5.$leave to leave the room \n' \
               '6.$join roomname to join or create the room\n' \
               '7.$switch roomname to switch room\n' \
               '8.$personal name message to send personal message'

#now create a empty list and dict for data storage
name_of_clients = []
bynames = []
details_of_room = {}
users = {}
in_room_users = {}

#to broadcast the message
def transmission(info_msg, room_num):
    for client in details_of_room[room_num].peoples:
        text = '['+room_num+'] '+info_msg
        client.send(text.encode('utf-8'))
