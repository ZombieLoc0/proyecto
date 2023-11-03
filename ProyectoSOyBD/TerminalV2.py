from socket import socket, AF_INET, SOCK_STREAM
from flask import Flask, render_template, request

#region SOCKET VARIABLES

HEADER = 64
PORT = 12345
SERVER = '148.239.110.9'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

#endregion

#region WEB

app = Flask(__name__)

@app.route("/terminal-page", methods=["GET", "POST"])
def terminal_page():
    if request.method == "POST":
        send(request.form["send"])
        return render_template("web.html")
    else:
        return render_template("web.html")

#endregion

def send(msg):
    if msg == 0:
        return None
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    