from netmiko import ConnectHandler

dispositivo = {
    "device_type" :"cisco_ios",
    "host" : "Equipo1.uag",
    "username" : "Equipo1",
    "password" : "12345"
}

connection = ConnectHandler(**dispositivo)
connection.enable()

while True:
    comando = input("Ingresa el comando que quieres ejecutar: ")
    try:
        connection.send_command(comando)
    except:
        print("Comando Incorrecto")
