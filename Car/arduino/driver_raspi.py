import serial

arduino = serial.Serial('/dev/ttyACM0', 9600) #abrimos la conexion por el puerto serial.

print("Starting!")
print("Comandos:")
print("D --> Enciende motor derecho")
print("I --> Enciende motor Izquierdo")
print("S --> Apaga motores")
print("q --> Salir")

while True:
      comando = raw_input('Introduce un comando: ') #Input
      arduino.write(comando) #Mandar un comando hacia Arduino
	# Esta parte del codigo es prescindible, pero de momento la usaremos por tal de verificar el funcionamiento del mismo
      if comando == 'D':
            print('GIRO DERECHA')
      elif comando == 'A':
            print('GIRO IZQUIERDA')
      elif comando == 'S':
            print('APAGA MOTORES')
      elif comando == 'X':
            print('REVERSA')
      elif comando == 'W':
            print('HACIA DELANTE')
      elif comando == 'q':
	    print('SALIENDO DEL CONTROLADOR')
	    exit()

arduino.close() #Finalizamos la comunicacion
