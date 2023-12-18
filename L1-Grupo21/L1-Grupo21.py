# socket: La libreria a utilizar

import socket

# definicion de host y puerto: Indicarán hacia donde nos estaremos conectando inicialmente

ME = "Mensaje enviado a {0}:{1} por {2}: {3}"
MR = "Mensaje recibido de {0}:{1} por {2}: {3}"

host = 'jdiaz.inf.santiago.usm.cl'
port = 50007
contador = 1
flag = True
while(flag):

    print("\n** Nuevo intento numero", contador,"**\n")
    contador += 1
    # Un ejemplo en UDP
    # Paso 1 - Definir el socket: el segundo argumento permite definir el tipo de conexión
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Paso 2 - Definir el mensaje a enviar: Debemos establecer un mensaje a enviar al servidor, recuerde codificarlo
    msj = "GET NEW IMG DATA".encode()

    # Paso 3 - Enviar el mensaje: Teniendo el mensaje y el socket basta con enviar el mensaje deseado
    # se adjunta a la funcion el mensaje y una tupla con el host y puerto a comunicar
    s.sendto(msj, (host, port))

    #print("Mensaje enviado a"+host+":"+str(port+"por UDP: GET NEW IMG DATA"))
    print(ME.format(host, str(port), "UPD", "GET NEW IMG DATA"))

    # Paso 4 - Obtener la respuesta: Enviado el mensaje quead recibir la respuesta desde el servidor, siendo una lista con información,
    # aunque solo usaremos el primer dato que se obtiene que contiene el mensaje que llega de vuelta, recordar decodificarlo.
    # el valor dentro de recvfrom es el buffer que va a leer de lo recibido.
    respuesta = s.recvfrom(1024)[0].decode()

    # Ejemplo para sacar y leer bytes de una foto
    '''
    Es el clásico de ejemplo de abrir y cerrar un archivo, solo que en vez de leer o escribir realizarlo con el comando read bytes y write bytes

    open("nombre.txt", "w") -> open("nombre.txt", "wb") 

    '''
    print(MR.format(host, str(port), "UDP", respuesta))
    ## NOTA: Mucho ojo con lo que hace encode y decode, recuerden que la codificación con .encode() transforma un texto a bytes. [para cuando escriban la foto por ejemplo]
    lista = respuesta.split(" ")

    #Con 3 puertos
    if(len(lista) == 7 ):
        ID, W, H, P1, P2, P3, PV = lista
        _, ID = ID.split(":")
        _, W = W.split(":")
        _, H = H.split(":")
        _, P1 = P1.split(":")
        _, P2 = P2.split(":")
        _, P3 = P3.split(":")
        _, PV = PV.split(":")

        buffer = int(W)*int(H)*3

        #Obtener primera parte de la imagen.
        print("\nObteniendo primera parte de la imagen")
        s_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_TCP.connect((host, int(P1)))
        msj = ("GET 1/3 IMG ID:"+ID).encode()
        s_TCP.send(msj)
        print(ME.format(ID, P1, "TCP", msj.decode()))
        respuesta_TCP = s_TCP.recv(buffer)
        print(MR.format(ID, P1, "TCP", "Bytes 1/3 de la Imagen"))
        s_TCP.close()

        #Obtener segunda parte de la imagen.
        print("\nObteniedo segunda parte de la imagen")
        s_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msj = ("GET 2/3 IMG ID:"+ID).encode()
        s_UDP.sendto(msj, (host, int(P2)))
        print(ME.format(ID, P2, "UDP", msj.decode()))
        respuesta_UDP_1 = s_UDP.recvfrom(buffer)[0]
        print(MR.format(ID, P2, "UDP", "Bytes 2/3 de la Imagen"))

        #Obtener tercera parte de la imagen.
        print("\nObteniedo tercera parte de la imagen")
        s_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msj = ("GET 3/3 IMG ID:"+ID).encode()
        s_UDP.sendto(msj, (host, int(P3)))
        print(ME.format(ID, P3, "UDP", msj.decode()))
        respuesta_UDP_2 = s_UDP.recvfrom(buffer)[0]
        print(MR.format(ID, P3, "UDP", "Bytes 3/3 de la Imagen"))

        #Verificando bytes.
        print("\nComenzando verificación de bytes")
        s_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_TCP.connect((host, int(PV))) 
        imagen_bytes = respuesta_TCP+respuesta_UDP_1+respuesta_UDP_2
        s_TCP.send(imagen_bytes)
        print(ME.format(ID, PV, "TCP", "Bytes de imagen completa"))
        
        #Respuesta de la verificacion
        respuesta_TCP = s_TCP.recv(buffer)
        print(MR.format(ID, PV, "TCP", respuesta_TCP.decode()))
        s_TCP.close()

    #Con 2 puertos
    elif(len(lista) == 6):
        ID, W, H, P1, P2, PV = lista
        _, ID = ID.split(":")
        _, W = W.split(":")
        _, H = H.split(":")
        _, P1 = P1.split(":")
        _, P2 = P2.split(":")
        _, PV = PV.split(":")

        #Calculo Buffer
        buffer = int(W)*int(H)*3

        #Obtener primera parte de la imagen.
        print("\nObteniendo primera parte de la imagen")
        s_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_TCP.connect((host, int(P1)))
        msj = ("GET 1/2 IMG ID:"+ID).encode()
        s_TCP.send(msj)
        print(ME.format(ID, P1, "TCP", msj.decode()))
        respuesta_TCP = s_TCP.recv(buffer)
        print(MR.format(ID, P1, "TCP", "Bytes 1/2 de la Imagen"))
        s_TCP.close()

        #Obtener segunda parte de la imagen.
        print("\nObteniedo segunda parte de la imagen")
        s_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msj = ("GET 2/2 IMG ID:"+ID).encode()
        s_UDP.sendto(msj, (host, int(P2)))
        print(ME.format(ID, P2, "UDP", msj.decode()))
        respuesta_UDP = s_UDP.recvfrom(buffer)[0]
        print(MR.format(ID, P2, "UDP", "Bytes 2/2 de la Imagen"))

        #Verificar bytes.
        print("\nComenzando verificación de bytes")
        s_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_TCP.connect((host, int(PV))) 
        imagen_bytes = respuesta_TCP+respuesta_UDP
        s_TCP.send(imagen_bytes)
        print(ME.format(ID, PV, "TCP", "Bytes de imagen completa"))
        
        #Respuesta de la verificacion
        respuesta_TCP = s_TCP.recv(buffer)
        print(MR.format(ID, PV, "TCP", respuesta_TCP.decode()))
        s_TCP.close()

    #Verificación de bytes.
    if "200" in respuesta_TCP.decode():
            print("Verificación exitosa de bytes:", respuesta_TCP)
            flag = False

            print("\nComenzando escritura de imagen")
            imagen = ID+".png"

            build = open(imagen, "wb")
            build.write(imagen_bytes)
            build.close()

            print("Escritura de imagen finalizada")
    else:
            print("Verificación fallida:", respuesta_TCP)

    print("\n**FIN**\n")