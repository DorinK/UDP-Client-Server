from socket import socket, AF_INET, SOCK_DGRAM
import sys

""""""""""""""""""""""""""
# Dorin Keshales 313298424
# Almog Lev 307900183
""""""""""""""""""""""""""


# This function adds a new user to the group and notify the other users in the group.
def new_user(name):

    # String which will hold the names of the other users in the group.
    names = ""

    # If the user is already in the group.
    if sender_info in users_names:
        s.sendto("Illegal request".encode(), sender_info)

    else:
        # For each user in the group add the joining notification to it's messages string.
        for user_info, name_info in zip(users_names.keys(), users_names.values()):
            users_messages[user_info] += (name + " has joined\n")
            #  Add the users name to the names string
            names += ", " + name_info

        # Adding the new user to the group.
        users_names[sender_info] = name
        users_messages[sender_info] = ""

        # Send to the new user the names of the users already in the group.
        s.sendto(names[2:].encode(), sender_info)


# This function sends a message from one user in the group to the others.
def send_msg(message):

    # If the user is in the group.
    if existence_validity():

        # For each user in the group, except the sender, add the message notification to it's messages string.
        for user_info in users_names.keys():
            if user_info != sender_info:
                users_messages[user_info] += (users_names[sender_info] + ": " + message + "\n")


# This function changes the name of the user and notify the other users in the group.
def change_name(new_name):

    # If the user is in the group.
    if existence_validity():

        # For each user in the group, except the sender, add the change name notification to it's messages string.
        for user_info in users_names.keys():
            if user_info != sender_info:
                users_messages[user_info] += ("" + users_names[sender_info] + " changed his name to " + new_name + "\n")

        # Update the new user's name
        users_names[sender_info] = new_name


# This function removes a user from the group following his request and notify the other users in the group.
def leave_group():

    # If the user is in the group.
    if existence_validity():

        # For each user in the group, except the sender, add the leaving notification to it's messages string.
        for user_info in users_names.keys():
            if user_info != sender_info:
                users_messages[user_info] += ("" + users_names[sender_info] + " has left the group\n")

        # Remove the sender from the group.
        del (users_names[sender_info])
        del (users_messages[sender_info])

        # Send an empty message to the client in order for him to be able to finish.
        s.sendto("".encode(), sender_info)

    else:  # Otherwise, notify the client about an Illegal request.
        s.sendto("Illegal request".encode(), sender_info)


# This function sends to one user all his waiting messages, he hasn't seen yet.
def receive_messages():

    # If the user is in the group, send him all of his unseen messages and after that clear it's string messages.
    if existence_validity():
        s.sendto((users_messages[sender_info])[:-1].encode(), sender_info)
        users_messages[sender_info] = ""

    else:  # Otherwise, notify the client about an Illegal request.
        s.sendto("Illegal request".encode(), sender_info)


# This function returns true if the user is already in the group. Otherwise, false.
def existence_validity():
    return False if sender_info not in users_names else True


# Receive number of port of the server from command line.
port = int(sys.argv[1])

s = socket(AF_INET, SOCK_DGRAM)
source_ip = '0.0.0.0'
source_port = port
s.bind((source_ip, source_port))

# Dictionary where the key is the sender info and the value is the user's name.
users_names = {}

# Dictionary where the key is the sender info and the value is a string of all messages that hasn't been sent yet.
users_messages = {}

data, sender_info = s.recvfrom(2048)

while True:

    # If data is empty.
    if len(data) == 0:
        s.sendto("Illegal request".encode(), sender_info)

    else:
        # The option the user chose to use.
        option = str(chr(data[0]))

        """ If the format is valid activate the method following the user's choice. """

        if option == '1' and len(data) > 2 and str(chr(data[1])) == ' ':
            new_user(data[2:].decode("utf-8"))

        elif option == '2' and len(data) > 2 and str(chr(data[1])) == ' ':
            send_msg(data[2:].decode("utf-8"))

            # Send the user all his waiting messages, he hasn't seen yet.
            receive_messages()

        elif option == '3' and len(data) > 2 and str(chr(data[1])) == ' ':
            change_name(data[2:].decode("utf-8"))

            # Send the user all his waiting messages, he hasn't seen yet.
            receive_messages()

        elif option == '4' and len(data) == 1:
            leave_group()

        elif option == '5' and len(data) == 1:
            receive_messages()

        else:  # Otherwise, notify the client about an Illegal request.
            s.sendto("Illegal request".encode(), sender_info)

    data, sender_info = s.recvfrom(2048)
