import socket
import os

def Main():
    host = '127.0.0.1'
    port = '5000'

    # create a socket 
    s = socket.socket()

    # connect the socket to the Server socket
    s.connect((host,int(port)))

    # ask for filename
    filename = input('Filename? ')
    if filename != 'q':
        filename = bytes(filename, 'utf-8')

        # send file name over to the Server socket
        s.send(filename)

        # Start recieving data
        data = s.recv(1024)
        
        # check if file EXISTS
        check = b'EXISTS'
        if data[:6] == check:
            filesize = int(data[6:])

            # ask for download
            message = input('File Exists,' + str(filesize)+ 'Bytes, downloaded(Y/N) ?')
            if message == 'Y' :
                ok = 'OK'
                ok = bytes(ok,'utf-8')

                # send message over the socket
                s.send(ok)

                # create new file to store the downloaded file
                f = open('new_' + filename.decode() ,'wb')
                data = s.recv(1024)
                f.write(data)
                totalRecv = len(data)
                print("****" + str(totalRecv) + "****")

    			# recieve file
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print('{0:.2f}'.format((totalRecv/float(filesize)*100)) + '%Done')
                print('Download Complete')
                
                done = "Done"
                s.send(bytes(done,'utf-8'))
        else:
        	# if file is not found
            print('File does not exist')

        # close the socket
        s.close()

if __name__ == '__main__':
    Main()