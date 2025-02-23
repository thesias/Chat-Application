from socket import *
from threading import Thread

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', 6969))
serverSocket.listen(1)

print("Ready to serve")

user_to_socket = {}
def new_client(user_name):
	while True:
		data = user_to_socket[user_name].recv(2048).decode()
		if (data == "!BREAK"):
			user_to_socket[user_name].close()
			user_to_socket.pop(user_name)
			print(user_name, "left!")
			break
		to_user = data.split()
		if (len(to_user) == 0 or to_user[0] not in user_to_socket):
			message = "!INVALID"
			user_to_socket[user_name].send(message.encode())
		else:
			message = user_name+" "+' '.join(data.split()[1:])
			user_to_socket[to_user[0]].send(message.encode())

while True:
	clientSocket, clientAddress = serverSocket.accept()
	cur_user = clientSocket.recv(2048).decode()
	while (cur_user in user_to_socket):
		message = "!INVALID"
		clientSocket.send(message.encode())
		cur_user = clientSocket.recv(2048).decode()
	message = "!CONNECTED"
	print(cur_user, "joined!")
	clientSocket.send(message.encode())
	user_to_socket[cur_user] = clientSocket
	thread = Thread(target=new_client, args=(cur_user,))
	thread.start()
	thread.join()
serverSocket.close()