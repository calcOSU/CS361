import json
import socket
import sys

PORT = 5050
FORMAT = 'utf-8'
HOST = "127.0.0.12"
my_sock = (HOST,PORT)
HEADER = 1024

DISCONNECT_MESSAGE = "!DISCONNECT"
OPTION_MESSAGE = "!OPTIONS"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(my_sock)

def send(msg, client):
    json_msg = json.dumps(msg)
    message = json_msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    resp = client.recv(2048).decode(FORMAT)
    resp = json.loads(resp)
    return resp

def send_json(json_msg):
    try:
        sock = socket.socket()
    except socket.error as err:
        print(f'socket error because of {err}')

    msg = json_msg.encode(FORMAT)
    try:
        sock.connect((address,port))
        sock.send(msg) #TypeError: a bytes-like object is required, not 'str'
    except socket.gaierror:
        print('error resolving host')
        sys.exit()
    print(json_msg+' was sent')

# def send(msg, client):

#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     client.send(send_length)
#     client.send(message)
#     return client.recv(2048).decode(FORMAT)

def options():
    print('would you like to see the available options?')
    while True:
        ans = input().lower()[0]
        if ans == 'y':
            options = True
            print('Alright, one second while I find your options: ')
            return True
        elif ans =='n':
            options = False
            return False
        else:
            print("Sorry, I didn't get that")
            print("Please enter 'yes' if you want options, 'no' if you don't")

def user_prompt():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(my_sock)
    if options() == True:
        print('fetching available workout attributes...')
        resp = send(OPTION_MESSAGE, client)
        counter = 0
        for _ in resp:
            if counter == 0:
                print('\nFirst choose one of these attributes:')
                print(_)
                counter += 1
            else:
                print('\nThen choose one of these attributes:')
                print(_)
        
    print('\nplease input your workout attributes:')
    input_request = list()
    counter = 1
    send_request = False
    while send_request == False:
        print(f'\nExercise attribute #{counter}:')
        ans = input()
        input_request.append(ans)
        while True:
            print('do you want to enter another attribute?')
            ans2 = input()
            if ans2.lower()[0] == 'y':
                counter += 1
                break
            elif ans2.lower()[0] == 'n':
                print('alright, querying with the attributes you requested')
                send_request = True
                break
            else:
                print("I'm sorry, I didn't get that, please enter yes or no")
    print('\nHere are your suggested exercises:')
    resp = send(input_request, client)
    print(resp)
    print('closing now')
    client.close()

def send_list(my_list):
    """just sends the information in my_list"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(my_sock)
    resp = send(my_list, client)
    client.close()
    return resp



if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'demo':
            t1 = ['compound','upper','shoulders']
            t2 = ['shoulders', 'upper', 'compound']
            t3 = ['blank', 'blue']
            t4 = ['shoulders','upper', 'compound', 'orange']  # still returns data
            t5 = ['blank','','three',3,'four','orange']
            t6 = [5,3,'compound', 'orange', 2,'green', 1,'upper', 'four', 'five', 3, 'shoulders', 'hey']
            t7 = [_ for _ in t6[::-1]]
            res_list = list()
            for _ in t1,t2,t3,t4,t5,t6,t7:
                response = send_list(_)
                res_list.append(response)
                print(f'\nFor the input list of: {_}')
                print(f'The result is: {response}')
        else:
            params = sys.argv[1:]
            res = send_list(params)
            print(res)
    else:
        user_prompt()