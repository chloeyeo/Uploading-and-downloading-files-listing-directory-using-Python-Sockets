import socket
import sys
import os
from AE1_common import send_file, recv_file, recv_listing

# Create the socket with which we will connect to the server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The server's address is a tuple, comprising the server's IP address or hostname, and port number
srv_addr = (sys.argv[1], int(sys.argv[2])) # sys.argv[x] is the x'th argument on the command line

request = sys.argv[3] # request type: "put","get",or "list" (for uploading file, downloading file, listing files in root directory).

""" 
 Enclose the connect() call in a try-except block to catch
 exceptions related to invalid/missing command-line arguments, 
 port number out of range, etc. Ideally, these errors should 
 have been handled separately.
"""
try:
    """
     Connect our socket to the server. This will actually bind our socket to
     a port on our side; the port number will most probably be in the
     ephemeral port number range and may or may not be chosen at random
     (depends on the OS). The connect() call will initiate TCP's 3-way
     handshake procedure. On successful return, said procedure will have
     finished successfully, and a TCP connection to the server will have been
     established.
    """
    cli_sock.connect(srv_addr)
    
except Exception as e:
    # Print the exception message
    print(e)
    # Exit with a non-zero value, to indicate an error condition
    exit(1)

"""
 Surround the following code in a try-except block to account for
 socket errors as well as errors related to user input. Ideally
 these error conditions should be handled separately.
"""
try:
    
    cli_sock.sendall(str.encode(request))
    
    #raise ConnectionResetError # uncomment to TEST that IF there is connection error caused by the server what would the client do (print out msg: connection dropped).
    
    confirmation = cli_sock.recv(1024).decode('utf-8')
    
    if (request == "put") and (confirmation == "server received request"):
        filename = sys.argv[4] # for "put" and "get requests only. 
        cli_sock.sendall(filename.encode('utf-8'))
        confirmation2 = cli_sock.recv(1024).decode('utf-8') # receive confirmation msg telling whether server received filename.
        
        if confirmation2 == "server received filename":
            confirm_f_notInDirectory = cli_sock.recv(1024).decode('utf-8') # receive confirmation msg telling whether file in server directory.
            
            if confirm_f_notInDirectory == "file not in server directory":
                send_file(cli_sock, filename) # only send file to server when file not already in server's directory.
            
            else:
                print("server:",srv_addr,"type of request:",request, "filename:", filename, "status: failure",
                "reason of failure: The file already exists in server's directory, so file won't be sent to server.")
        
                
    elif (request == "get") and (confirmation == "server received request"):
        filename = sys.argv[4] # for "put" and "get requests only.
        directory_list_string = str(os.listdir())
        
        if filename not in directory_list_string:
            
            cli_sock.sendall(str.encode("file not in client directory")) # send confirmation msg to server: file not in client's directory.
        
            cli_sock.sendall(filename.encode('utf-8'))
            confirmation2 = cli_sock.recv(1024).decode('utf-8') # confirmation msg received telling whether server received filename.
            
            if confirmation2 == "server received filename":
                bytes_received = recv_file(cli_sock, filename)
                while bytes_received > 0:
                    bytes_received = recv_file(cli_sock, filename)
        
        elif filename in directory_list_string:
            
            cli_sock.sendall(str.encode("file in client directory"))
            print("server:",srv_addr,"type of request:",request, "filename:", filename, "status: failure",
                "reason of failure: This file already exists in client directory.")
                
    elif (request == "list") and (confirmation == "server received request"):
        recv_listing(cli_sock)
    
    """
    Report(print on console) containing IP address and port no. of server, type of request,
    filename for put/get request, status(in the case of success).
    """
    if ((request == "put") and (confirm_f_notInDirectory == "file not in server directory")) or ((request == "get") and (filename not in directory_list_string)):
        print("server:",srv_addr,"type of request:",request, "filename:", filename, "status: success")
    elif request == "list":
        print("server:",srv_addr,"type of request:",request, "status: success")

except ConnectionError:
    print("The connection to server has dropped.")
    
except Exception as e:
    """
    Report(print on console) containing IP address and port no. of server, type of request,
    filename for put/get request, status(in the case of failure), type of error that caused failure.
    """
    if (request == "put") or (request == "get"):
        print("server:",srv_addr,"type of request:",request, "filename:", filename, "status: failure",
        "reason of failure: error",e,"occured.")
    elif request == "list":
        print("server:",srv_addr,"type of request:",request, "status: failure", "reason of failure: error",
        e,"occured.")
        
finally:
    """
     Call close() on the connected socket to release the resources allocated to it by the OS.
    """
    cli_sock.close()

# Exit with a zero value, to indicate success
exit(0)
