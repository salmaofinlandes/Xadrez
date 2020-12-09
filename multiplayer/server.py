# Python program to implement server side of chat room. 
import socket 
import sys 
from _thread import *

i = 0


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# verifica se foram dados o numero de argumentos corretos 
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number") 
	exit() 

# 1º argumento - IP
IP_address = str(sys.argv[1]) 

# 2º argumento - Porta
Port = int(sys.argv[2]) 


server.bind((IP_address, Port)) # inicia o servidor nos parametros dados


server.listen(100) 

list_of_clients = [] # lista das sockets de cada cliente



def clientthread(conn, addr): # thread de cada cliente individual

	# recebe a mensagem de um cliente e envia para o outro

	while True: 
			try: 
				message = conn.recv(2048).decode() 
				if message: 

					print ("<" + addr[0] + "> " + message) 

					# Calls broadcast function to send message to all 
					message_to_send = message.encode() 
					broadcast(message_to_send, conn) 

				else:
					# se a conexao cair a mensagem nao tera conteudo
					# nesse caso encerra-se a conexao 
					remove(conn) 

			except Exception as e:
				print(e)
				print("Thread error") 
				continue

# funcao que envia a mensagem para todos os clientes (neste caso apenas 1) exceto o que envia
def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients!=connection: 
			try: 
				clients.send(message) 
			except:
				print("Broadcast error") 
				clients.close() 

				# remover cliente em caso de erro
				remove(clients) 

# funcao para remover clientes
def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection) 

while True: 

	#thread principal onde o servidor espera por novas conexoes
	conn, addr = server.accept() # enquanto nao ha conexoes a execucao para aqui (por isso é que é necessario usar threads)
	
	
	if i == 0: # se o cliente for o primeiro a conectar-se o servidor envia-lhe a mensagem "0" para ele saber que joga com as brancas
		f = "0"
		conn.send(f.encode())
		i+=1
	elif i == 1: # a mesma coisa para as peças pretas
		f = "1"
		conn.send(f.encode())	
	
	# adiciona o cliente à lista
	list_of_clients.append(conn)
	 
	print (addr[0] + " connected") 

	# inicia uma thread individual para cada cliente que se conecta 
	start_new_thread(clientthread,(conn,addr)) 


conn.close() 
server.close() 

