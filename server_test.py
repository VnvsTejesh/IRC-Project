#This module contains all the functionalities

from main_test import *

#now to instatiate
class User:
    def __init__(self, name):
        self.name = name
        self.details_of_room = []
        self.thisRoom = ''


class Room:
    def __init__(self, name):
        self.peoples = []
        self.bynames = []
        self.name = name


#now to listing the room and it's details
def room_details_list(codename,comm):
    name = users[codename]
    print(comm)
    print(len(details_of_room))
    print(codename)
    if len(details_of_room) == 0:
        name.send('There are no available room details.'.encode('utf-8'))
    else:
        reply1 = "List of available roomdetails: \n"
        reply2 = "List of available pepople: \n"
        for room in details_of_room:
            print(details_of_room[room].name)
            
            reply1 += details_of_room[room].name
            reply1+= "   "
            print(details_of_room[room].bynames)
            

            #if codename not in details_of_room[room].bynames:
            for people in details_of_room[room].bynames:
                reply2 += people
                reply2+= "   "
        if comm=='$listrooms':
            name.send(f'{reply1}'.encode('utf-8'))
        elif comm=='$listusers':
            name.send(f'{reply2}'.encode('utf-8'))


#now to join to other rooms
def room_joining(codename, room_name):
    name = users[codename]
    user = in_room_users[codename]
    if room_name not in details_of_room:
        room = Room(room_name)
        details_of_room[room_name] = room
        room.peoples.append(name)
        room.bynames.append(codename)

        user.thisRoom = room_name
        user.details_of_room.append(room)
        name.send(f'{room_name} created'.encode('utf-8'))
    else:
        room = details_of_room[room_name]
        if room_name in user.details_of_room:
            name.send('You are already within the space.'.encode('utf-8'))
        else:
            room.peoples.append(name)
            room.bynames.append(codename)
            user.thisRoom = room_name
            user.details_of_room.append(room)
            transmission(f'{codename} joined the room', room_name)
            #name.send('Joined room'.encode('utf-8'))

#now to switch to other room
def room_switching(codename, room_num):
    user = in_room_users[codename]
    name = users[codename]
    room = details_of_room[room_num]
    if room_num == user.thisRoom:
        name.send('You are already within the space.'.encode('utf-8'))
    elif room not in user.details_of_room:
        name.send('You are not a part of the room, there is no switch available.'.encode('utf-8'))
    else:
        user.thisRoom = room_num
        name.send(f'Switched to {room_num}'.encode('utf-8'))

#now to exit the room
def room_leaving(codename):
    user = in_room_users[codename]
    name = users[codename]
    if user.thisRoom == '':
        name.send('You are not part of any room'.encode('utf-8'))
    else:
        room_num = user.thisRoom
        room = details_of_room[room_num]
        user.thisRoom = ''
        user.details_of_room.remove(room)
        details_of_room[room_num].peoples.remove(name)
        details_of_room[room_num].bynames.remove(codename)
        transmission(f'{codename} left the room', room_num)
        name.send('You left the room'.encode('utf-8'))


#now to personally message
def message_to_individual(info_msg):
    args = info_msg.split(" ")
    user = args[2]
    sender = users[args[0]]
    if user not in users:
        sender.send('User not found'.encode('utf-8'))
    else:
        reciever = users[user]
        text = ' '.join(args[3:])
        reciever.send(f'[personal message] {args[0]}: {text}'.encode('utf-8'))
        sender.send(f'[personal message] {args[0]}: {text}'.encode('utf-8'))

#now to exit the server
def client_removing(codename):
    bynames.remove(codename)
    client = users[codename]
    user = in_room_users[codename]
    user.thisRoom = ''
    for room in user.details_of_room:
        print(room.name)
        room.peoples.remove(client)
        print(room.peoples)
        room.bynames.remove(codename)
        print(room.bynames)
        transmission(f'{codename} left the room', room.name)


#to handle
def client_handler(client):
    nick=''
    while True:
        try:
            info_msg = client.recv(1024).decode('utf-8')
            args = info_msg.split(" ")
            name = users[args[0]]
            nick = args[0]
            if '$help' in info_msg:
                name.send(commands.encode('utf-8'))
            elif '$listroom' in info_msg:
                room_details_list(args[0],args[1])
            elif '$listusers' in info_msg:
                room_details_list(args[0],args[1])
            elif '$join' in info_msg:
                room_joining(args[0], ' '.join(args[2:]))
            elif '$leave' in info_msg:
                room_leaving(args[0])
            elif '$switch' in info_msg:
                room_switching(args[0], args[2])
            elif '$personal' in info_msg:
                message_to_individual(info_msg)
            elif '$quit' in info_msg:
                client_removing(args[0])
                name.send('QUIT'.encode('utf-8'))
                name.close()
            else:
                if in_room_users[args[0]].thisRoom == '':
                    name.send(''.encode('utf-8'))
                else:
                    text = ' '.join(args[1:])
                    transmission(f'{args[0]}: {text}',in_room_users[args[0]].thisRoom)

            #transmission(info_msg)
        except Exception as e:
            print("exception occured ", e)
            index = name_of_clients.index(client)
            name_of_clients.remove(client)
            client.close()
            '''codename = bynames[index]
            print(f'{codename} left')
            user = in_room_users[codename]'''
            '''if user.thisRoom != '':
                room_num = user.thisRoom
                user.thisRoom = ''
                #user.details_of_room.remove(room_num)
                details_of_room[room_num].peoples.remove(name)
                details_of_room[room_num].bynames.remove(codename)
                transmission(f'{codename} left the room', room_num)'''
            print(f'nick name is {nick}')
            if nick in bynames:
                client_removing(nick)
            if nick in bynames:
                bynames.remove(nick)

            #transmission(f'{codename} left the room'.encode('utf-8'))

            break

#main
def recieve():
    while True:
        client, address = server_details.accept()
        print(f'connected with {str(address)}')
        print(client)
        client.send('NICK'.encode('utf-8'))
        codename = client.recv(1024).decode('utf-8')
        if codename not in bynames:
            bynames.append(codename)
            client.send('NICK'.encode('utf-8'))
            name_of_clients.append(client)
            user = User(codename)
            in_room_users[codename] = user
            users[codename] = client
            print(f'codename of the client is {codename}')
            #transmission(f'{codename} joined the chat'.encode('utf-8'))
            client.send('Connected to the server!'.encode('utf-8'))
            client.send(commands.encode('utf-8'))
            thread = threading.Thread(target=client_handler, args=(client,))
            thread.start()
        else:
            client.send('The username already Exists'.encode('utf-8'))

print('Server is active and listening...')
recieve()
