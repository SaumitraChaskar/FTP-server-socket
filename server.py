import socket 
import threading
import os
def RetrFile(name,sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        stringSend = 'EXISTS' + str(os.path.getsize(filename))
        stringSend = bytes(stringSend,'utf-8')
        sock.send(stringSend)
        userResponse = sock.recv(1024)
        print(userResponse)
        check = b'OK'
        if userResponse[:2] == check:
            with open(filename,'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != '':
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
        else:
            sock.send(bytes('ERR','utf-8'))
        sock.close()
def Main():
    host = '172.16.31.106'
    port = '5000'
    s = socket.socket()
    s.bind((host,int(port)))
    s.listen(5)
    print('Server Started.')
    while True:
        c, addr = s.accept()
        print('Client connected ip:<' + str(addr)+ '>')
        t = threading.Thread(target = RetrFile,args = ('retrThread',c))
        t.start()
    s.close()
if __name__ == '__main__':
    Main()
