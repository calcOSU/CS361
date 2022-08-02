# https://mirdan.medium.com/send-json-with-python-socket-f1107876f50e
# https://www.youtube.com/watch?v=3QiPPX-KeSc

import threading
import json
import socket
import random

PORT = 5050
FORMAT = 'utf-8'
HOST = "127.0.0.12"
my_sock = (HOST,PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
OPTION_MESSAGE = "!OPTIONS"
HEADER = 1024


def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(my_sock)
    server.listen()
    print(f"[LISTENING] Server is listening on {my_sock}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print('message:')
            json_msg = json.loads(msg)
            print(json_msg)
            # 3 options: either disconnect, an options request, or request for exercises
            if json_msg == DISCONNECT_MESSAGE:
                connected = False
            elif json_msg == OPTION_MESSAGE:
                print('received option request')
                options = get_options()
                options_json = json.dumps(options)
                options_encode = options_json.encode(FORMAT)
                conn.send(options_encode)
            else:
                results = get_result(json_msg)
                json_results = json.dumps(results)
                json_results = json_results.encode(FORMAT)
                conn.send(json_results)

def get_options():
    with open('ex.json', 'r') as f:
        data = json.load(f)
    data_holder = data
    options_list = list()
    while type(data_holder) == type(dict()):
        layer_list = list()
        for _ in data_holder.keys():
            layer_list.append(_)
        options_list.append(layer_list)
        data_holder = data_holder[list(data_holder.keys())[0]]
    return options_list

def get_result(input_list):
    """given a list containing search values, return the list of matched results"""
    with open('ex.json', 'r') as f:
        data = json.load(f)
    data_holder = data
    check_later = list()
    results = list()
    lowest_level = False
    for request in input_list:
        try:
            if request not in data_holder.keys():
                check_later.append(request)
            else:  # go a layer down
                data_holder = data_holder[request]
        except AttributeError: # given more parameters than necessary -- already at the lowest level
            lowest_level = True
            break

    # consider that the requests may be out of order, check other orders
    if len(check_later) > 0 and lowest_level == False:
        checked_all = False
        check_index = len(check_later) - 1
        while len(check_later) > 0 and checked_all == False:
            examine_this = check_later[check_index]
            try:
                if type(examine_this) != type(''):
                    check_index -= 1
                else:
                    data_holder = data_holder[examine_this]
                    check_later.pop(check_index)
                    check_index = len(check_later) -1 # start back from the beginning
            except TypeError: # type error indicating that we've already arrived to the lowest level
                checked_all = True
            except KeyError: # key error indicating that the value we're searching for isn't a valid key
                check_index -= 1
            except IndexError:
                check_index -= 1
            finally:
                if check_index < 0:
                    checked_all = True
    if type(data_holder) == type(list()): # good query
        results.extend(data_holder)
    else: # we still haven't gotten to the 'floor' of the json file
        return False 
    return results[random.randint(0,len(results))]

if __name__ == "__main__":
    start()