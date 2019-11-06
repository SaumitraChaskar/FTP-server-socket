import socket
import os
def Main():
    host = '172.16.31.106'
    port = '5000'
    s = socket.socket()
    s.connect((host,int(port)))
    filename = input('Filename? ')
    if filename != 'q':
        filename = bytes(filename, 'utf-8')
        s.send(filename)
        data = s.recv(1024)
        print(data)
        print(data[:6])
        check = b'EXISTS'
        if data[:6] == check:
            #statinfo = os.stat(filename)
            filesize = int(data[6:])
            message = input('File Exists,' + str(filesize)+ 'Bytes, downloaded(Y/N) ?')
            if message == 'Y' :
                ok = 'OK'
                ok = bytes(ok,'utf-8')
                s.send(ok)
                f = open('new_' + filename.decode() ,'wb')
                data = s.recv(1024)
                print(data)
                f.write(data)
                totalRecv = len(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print('{0:.2f}'.format((totalRecv/float(filesize)*100)) + '%Done')
                print('Download Complete')
        else:
            print('File does not exist')
        s.close()
if __name__ == '__main__':
    Main()        
