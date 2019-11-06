import socket 
import threading
import os

def RetrFile(name,sock):
	# recieve filename
    filename = sock.recv(1024)
    print("****** filename ******")
    print(filename)

    # check if file exists
    if os.path.isfile(filename):
    	# send 'EXISTS' message and file size
        stringSend = 'EXISTS' + str(os.path.getsize(filename))
        stringSend = bytes(stringSend,'utf-8')
        sock.send(stringSend)

        # get User response
        userResponse = sock.recv(1024)
        print(userResponse)
        check = b'OK'

        # if OK response send File via socket
        if userResponse[:2] == check:
            with open(filename,'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != '':
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
        else:
        	# send ERROR message if Not 
            sock.send(bytes('ERR','utf-8'))

        # close socket connection
        status = sock.recv(1024)
        print(status)
        sock.close()


def Main():
	# Host address and Port
    host = '127.0.0.1'
    port = '5000'

    # create socket object and bind IP and PORT
    s = socket.socket()
    s.bind((host,int(port)))

    # maximum backlogged requests not yet accepted by the server
    s.listen(5)
    print('Server Started.')
    while True:
    	# connection and adress are returned 
        c, addr = s.accept()
        print('Client connected ip:<' + str(addr)+ '>')
        # new thread for every connection
        t = threading.Thread(target = RetrFile,args = ('retrThread',c))
        t.start()

    # close the socket connection
    s.close()

if __name__ == '__main__':
    Main()