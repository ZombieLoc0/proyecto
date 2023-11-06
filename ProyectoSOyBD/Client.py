from flask import Flask, render_template, request
from time import sleep
import socket
#region SOOCKET VARIABLES

HEADER = 64
PORT = 12345 
SERVER = '192.168.1.67'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#endregion

startTask = '00'
currentTask = startTask
turn = 'Sin turno'

app = Flask(__name__)

@app.route("/cashier-page", methods = ["GET", "POST"])
def cashier_page():
    if request.method == "POST":
        cahiser_handler()
    
    return render_template("Cashier.html", Turn = turn)

@app.route("/terminal-page", methods=["GET", "POST"])
def terminal_page():
    if request.method == "POST":
        send_msg(request.form["send"])
        return render_template("Terminal.html")
    else:
        return render_template("Terminal.html")

def send_msg(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)

def cahiser_handler():
    global currentTask
    global turn

    send_msg(currentTask)
    
    task = client.recv(HEADER).decode(FORMAT)
    print(f'Se recibio la Task: {task}')

    if task.find('t') >= 0:
        currentTask = '00'
    
    currentTask = currentTask.replace(currentTask[0], str(int(currentTask[0]) + 1))
    
    print(task.find('n'))
    
    while task.find('n') >= 0:
        sleep(3)
        if task.find('t') >= 0:
            currentTask = startTask

        currentTask = currentTask.replace(currentTask[0], str(int(currentTask[0]) + 1))
        send_msg(currentTask) 
        task = client.recv(HEADER).decode(FORMAT)
        print(f'Se recibio la Task: {task}')
    
    turn = task

if __name__ == "__main__":
    app.run(debug=True, port=5000)