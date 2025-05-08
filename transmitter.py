

import sys
import os
import socket
import datetime
import time
import ipaddress

chunk_size = 512  #--file tx/rx size

def send_the_file(i_file, i_ip, i_port) :

    #--check file
    if not os.path.isfile(i_file) :
        print(' Error - {} file does not exist'.format(i_file))
        sys.exit()

    try :
        #- setup ip-v4 and tcp connection
        tx_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tx_socket.connect((i_ip,i_port))
        
        with open(i_file, 'rb') as f:
            chk_cnt=1
            while True:
                data = f.read(chunk_size) # Read in chunks
                if not data:
                    break
                tx_socket.sendall(data)
                print('  Tx - sending chunk # {}'.format(chk_cnt))
                chk_cnt += 1

        f.close()
        tx_socket.close()

    except Exception as e :
        print(e)
    
        

def recv_the_file(o_ip, o_port) :

    #- setup ip-v4 and tcp connection
    rx_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    rx_socket.bind((o_ip,o_port))
    

    nbr_of_files = 1
    rx_buf = []
    rx_socket.listen(nbr_of_files)
    file_nbr = 1
    rx_socket.settimeout(10)

    try :
        print(f' Listening at {o_ip} {o_port} for file - {file_nbr} for 10 secs') 
        for i in range(nbr_of_files) :  
            conn = rx_socket.accept() 
            rx_buf.append(conn) 
            print(f'Connected with: client - {file_nbr}')
            file_nbr += 1
            # Establishing Connections 
        
        wait_cnt = 0
        for buf in rx_buf:
            data = buf[0].recv(chunk_size)

            # Creating a new file with date suffix 
            f_suffix= datetime.datetime.now().strftime('%m%d_%H%M%S')
            filename = 'rcvd_file_' + f_suffix
            print(f' using {filename}')
            with open(filename, 'wb') as f :
                while data: 
                    if not data: 
                        break
                    else: 
                        f.write(data) 
                        data = buf[0].recv(chunk_size)
                print('Received successfully! New filename is: {}'.format(filename)) 
                f.close()
            if nbr_of_files > 1 :
                print('waiting for next file for 1 sec, if any')
                time.sleep(1) #force sleep to get next file with different name
        
        for buf in rx_buf : 
            buf[0].close()

    except Exception as e :
        print(e)
    

def display_usage() :
    print('Usage - ')
    print('  transmitter.py send <filename> <ip> <port>')
    print('  transmitter.py recv <ip> <port>')
    sys.exit()

def  chk_tcp_port(port) :
    try :
        port = int(port)
    except Exception as e:
        print(f'  Error - port must contain integers only, check further - {e}')
        return False

    # chk tcp port
    if 1 <= port <= 65535:
        return True
    else:
        return False

def chk_tcp_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def main():
    
    #--check arg usage
    args_nbr = len(sys.argv)
    print('{} arguments passed - {}'.format(args_nbr,sys.argv))

    if args_nbr == 5 and sys.argv[1] == 'send' :
        mode, tx_file, tx_ip, tx_port = sys.argv[1:5]
    elif args_nbr == 4 and sys.argv[1] == 'recv':
        mode, rx_ip, rx_port = sys.argv[1:4]
    else :
        display_usage()


    if mode == 'send' :
        if not chk_tcp_ip(tx_ip):
            print(f' Error send - {tx_ip} address is not valid, must be ip-v4/v6 address format')
            display_usage()  
        
        if not chk_tcp_port(tx_port):
            print(f' Error send - {tx_port} port is not valid, must be an integer 1-65535')
            display_usage()

        tx_port = int(tx_port)
        send_the_file(tx_file,tx_ip, tx_port)

    elif mode == 'recv' :
        if not chk_tcp_ip(rx_ip):
            print(f' Error recv - {rx_ip} address is not valid, must be ip-v4/v6 address format')
            display_usage()  
        
        if not chk_tcp_port(rx_port):
            print(f' Error recv - {rx_port} port is not valid, must be an integer 1-65535')
            display_usage()
        
        rx_port = int(rx_port)
        recv_the_file(rx_ip, rx_port) 

    else :
        print('  Error - Invalid mode specified')


if __name__ == '__main__' :
    main()


