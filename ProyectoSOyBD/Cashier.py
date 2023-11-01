from threading import Thread
from queue import Queue
from time import sleep
import socket



#region SOOCKET VARIABLES

HEADER = 64
PORT = 5050 
SERVER = '148.239.124.112'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#endregion

def send_request(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)
    print('Mensaje Enviado')


def start():
    startTask = '00'
    currentTask = startTask
    while(True):
        input('Get new task: (Press R) ')    #El request que hace la caja para obtener otra tarea
        send_request(currentTask)

        task = client.recv(HEADER).decode(FORMAT)
        print(f'Se recivio la Task: {task}')

        if task[1] == 't':
            currentTask = startTask
        
        currentTask = currentTask.replace(currentTask[0], str(int(currentTask[0]) + 1))
        
        while task[0] == 'n':
            sleep(3)
            if task[1] == 't':
                currentTask = startTask
            currentTask = currentTask.replace(currentTask[0], str(int(currentTask[0]) + 1))

            send_request(currentTask)
            task = client.recv(HEADER).decode(FORMAT)
            print(f'Se recivio la Task: {task}')


start()