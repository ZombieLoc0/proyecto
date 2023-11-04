from flask import Flask, render_template, request
from time import sleep
import socket

#region SOOCKET VARIABLES

HEADER = 64
PORT = 12345 
SERVER = '192.168.100.10'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#endregion

startTask = '00'
currentTask = startTask
turn = 'Caquita'

app = Flask(__name__)

@app.route("/cashier-page", methods = ["GET", "POST"])
def cashier_page():
    if request.method == "POST":
        start()
    
    return render_template("Cashier.html", Turn = turn)


def send_request(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)
    print('Mensaje Enviado')

def start():
    global currentTask
    global turn

    send_request(currentTask)
    
    task = client.recv(HEADER).decode(FORMAT)
    print(f'Se recibio la Task: {task}')

    if task[1] == 't':
        currentTask = '00'
    
    currentTask = currentTask.replace(currentTask[0], str(int(currentTask[0]) + 1))
    
    while task[0] == 'n':
        sleep(3)
        if task[1] == 't':
            currentTask = startTask
        currentTask = currentTask.replace(currentTask[0], str(int(currentTask[0]) + 1))
        send_request(currentTask)
        task = client.recv(HEADER).decode(FORMAT)
        print(f'Se recibio la Task: {task}')
    turn = task


if __name__ == "__main__":
    app.run(debug=True, port=5000)


start()