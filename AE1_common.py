import os
import socket

def send_file(socket,filename):
    """
    Opens the file with the given filename and sends its data
    over the network through the provided socket.
    """

    f = open(filename,"rb") # opens and reads file in binary mode.
    content = f.read(1024) # reads 1024 bytes of content in file at a time.
    content_received = True
    
    while (len(content) > 0) and (content_received == True):
        socket.sendall(content)
        confirmation_msg = socket.recv(1024).decode('utf-8')
        if confirmation_msg != "received file content":
            content_received = False
            
        content = f.read(1024)
        
    f.close()
        
def recv_file(socket,filename):
    """
    Creates the file with the given filename and stores into
    it data provided from the provided socket.
    """
    f = open(filename,"ab") # opens and appends content to the file in binary mode. If file does not exist, it creates a new file for writing.
    data = socket.recv(1024) # Read up to 1024 bytes of data in file at a time.
    bytes_received = len(data)
    
    while len(data) > 0:
        socket.sendall(str.encode("received file content"))
        
        f.write(data)
        data = socket.recv(1024)
        bytes_received += len(data)
    f.close()
    return bytes_received
        
def send_listing(socket):
    """
    Generates and sends the directory(=folder) listing from
    the server to the client via the provided socket.
    """
    directory_list = os.listdir() # gets the list of names of all files and/or directories in the root/top-most directory.
    socket.sendall(str(directory_list).encode('utf-8'))
    
def recv_listing(socket):
    """
    Receives the listing from the server via the provided socket
    and prints it on screen.
    """
    
    list_received = socket.recv(1024).decode('utf-8')
    listing = list_received.split(",")
    
    string_for_listing2 = "".join(listing)
    listing2 = string_for_listing2.split("'")
    
    listing2.remove("[")
    listing2.remove("]")
    
    for item in listing2:
        if item == " ":
            listing2.remove(item)
    
    print("The list of files/directories in root directory:")
    for name in listing2:
        print(name)