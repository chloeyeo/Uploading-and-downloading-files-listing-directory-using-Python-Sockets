import socket
import sys
import os
from AE1_common import send_file, recv_file, send_listing

# Create the socket on which the server will receive new connections
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

""" 
 Enclose the following two lines in a try-except block to catch
 exceptions related to already bound ports, invalid/missing
 command-line arguments, port number out of range, etc. Ideally,
 these errors should have been handled separately.
"""
try:
    """
     Register the socket with the OS kernel so that messages sent
     to the user-defined port number are delivered to this program.
     Using "0.0.0.0" as the IP address so as to bind to all available
     network interfaces. Alternatively, could have used "127.0.0.1"
     to bind only to the local (loopback) interface, or any other IP
     address on an interface of the computer where this program is
     running (use "ipconfig /all" to list all interfaces and their IP
     addresses).
    """
    srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) # sys.argv[1] is the 1st argument on the command line
    
    """
     Create a queue where new connection requests will be added by
     the OS kernel. This number should be small enough to not waste
     resources at the OS level, but also large enough so that the
     connections queue doesn't fill up. For this latter, one should
     ideally have an idea of how long it takes to serve a request
     and how frequently clients initiate new connections to the
     server.
    """
    srv_sock.listen(5)
except Exception as e:
    # Print the exception message
    print(e)
    # Exit with a non-zero value, to indicate an error condition
    exit(1)

# Loop forever (or at least for as long as no fatal errors occur) so that
# when one connection closes, server socket keeps on accepting another connection.
while True:
    print("Connecting to new client...")
    """
     Surround the following code in a try-except block to account for
     socket errors as well as errors related to user input. Ideally
     these error conditions should be handled separately.
    """
    
    try:
        """
         Dequeue a connection request from the queue created by listen() earlier.
         If no such request is in the queue yet, this will block until one comes
         in. Returns a new socket to use to communicate with the connected client
         plus the client-side socket's address (IP and port number).
        """
        
        cli_sock, cli_addr = srv_sock.accept()
        print("Connection made to client.")
        
        #raise ConnectionResetError # uncomment to TEST that IF there is connection error caused by the client, what would the server do.
        
        request = cli_sock.recv(1024).decode('utf-8')
        cli_sock.sendall(str.encode("server received request"))
        
        if request == "put":
            filename_str = ""
            filename_bytes = cli_sock.recv(1024)
            filename_str += filename_bytes.decode()
            cli_sock.sendall(str.encode("server received filename"))
            
            directory_list_string = str(os.listdir())
            
            if filename_str not in directory_list_string:
                cli_sock.sendall(str.encode("file not in server directory")) # send confirmation msg to client: file not in server's directory.
                
                bytes_received = recv_file(cli_sock, filename_str)
                while bytes_received > 0:
                    bytes_received = recv_file(cli_sock, filename_str)
            
            elif filename_str in directory_list_string:
                cli_sock.sendall(str.encode("file in server directory")) # send confirmation msg to client: file already in server's directory.
                print("client:", cli_addr, "type of request:",request, "filename:", filename_str, "status: failure",
                "reason of failure: This file already exists in server directory.")
           
                
        elif request == "get":
        
            confirm_f_notInDirectory = cli_sock.recv(1024).decode('utf-8')
            filename_str = ""
            filename_bytes = cli_sock.recv(1024) 
            filename_str += filename_bytes.decode()
            cli_sock.sendall(str.encode("server received filename"))
            
            if confirm_f_notInDirectory == "file not in client directory":     
                send_file(cli_sock, filename_str)   # only send file content once it's confirmed the file deosn't exist in client's directory.           
            else:
                print("client:", cli_addr, "type of request:",request, "filename:", filename_str, "status: failure",
                "reason of failure: The file already exists in client directory, so file won't be sent to client.")
                
        elif request == "list":
            send_listing(cli_sock)
        
        """
        Report(print on console) containing IP address and port no. of client, type of request,
        filename for put/get request, status(in the case of success).
        """
        if ((request == "put") and (filename_str not in directory_list_string)) or ((request == "get") and (confirm_f_notInDirectory == "file not in client directory")):
            print("client:", cli_addr,"type of request:",request, "filename:", filename_str, "status: success")
        elif request == "list":
            print("client:", cli_addr,"type of request:",request, "status: success")
    
    except ConnectionError: # if connection to client drops, server prints error msg then enters while loop again to connect to new client.
        print("The connection to this client has dropped.")
        
    except Exception as e:
        """
        Report(print on console) containing IP address and port no. of client, type of request,
        filename for put/get request, status(in the case of failure), type of error that caused failure.
        """
        if (request == "put") or (request == "get"):
            print("client:", cli_addr, "type of request:",request, "filename:", filename_str, "status: failure",
            "reason of failure: error",e,"occured.")
        elif request == "list":
            print("client:", cli_addr, "type of request:",request, "status: failure", "reason of failure: error",
            e,"occured.")
        
    finally:
        """
         Call close() on the connected socket to release the resources allocated to it by the OS.
        """
        cli_sock.close()

# Close the server socket as well to release its resources back to the OS
srv_sock.close()

# Exit with a zero value, to indicate success
exit(0)
