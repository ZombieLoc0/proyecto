from threading import Thread, activeCount
import socket

#region SOCKET VARIABLES
HEADER = 64
PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())   #Obtener direccion IP de la computadora
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
#endregion

#Shared Variables
item = 0
item_queues = []
daily_tasks = []
current_dt_indexes = []


def put_in_queue(item):
    for i, q in enumerate(item_queues):
        if len(q) > 0 and item == q[0]:
            q.append(item)
            daily_tasks[i].append(len(daily_tasks[i]))
            return
    item_queues.append([item, item])
    daily_tasks.append([0])
    current_dt_indexes.append(0)

def send_item(request):
    item = "xy"
    index = int(request[0])
    print(item_queues)
    if index >= len(item_queues):
        item = item.replace('y', 't')
        index = 0

    try:
        item = item.replace('x', item_queues[index].pop(1))
        item += str(daily_tasks[index][current_dt_indexes[index]])
        current_dt_indexes[index] += 1
    except:
        item = item.replace('x', 'n')
        
    print(item)
    return item
    
def client_handler(conn, addr):
    connected = True
    while connected:
        msg_lenght = conn.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)

            if msg_lenght == 1:             #Los mensajes de la terminal son tamano 1
                msg = conn.recv(msg_lenght).decode(FORMAT)
                print(f'[Se recibe: {addr}]El item: -{msg}')
                put_in_queue(msg)

            elif msg_lenght > 1:            #Es un request del cashier es tamano 2 (o mas)
                msg = conn.recv(msg_lenght).decode(FORMAT)
                print(f'Mensaje recibido: {msg}')
                item  = send_item(msg)
                conn.send(item.encode(FORMAT))
                print(f'[Se envia a: {addr}]-El item: {item}')
            
    conn.close()

def start_server():
    server.listen()

    while True:
        conn, addr = server.accept()
        client_thread = Thread(target=client_handler, args=(conn, addr))
        client_thread.start()

        print('[NUEVA CONEXION]')
        print(f'[CONEXIONES ACTIVAS] - {activeCount()-1}')


start_server()