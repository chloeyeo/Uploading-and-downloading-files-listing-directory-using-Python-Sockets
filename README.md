# Uploading-and-downloading-files-listing-directory-using-Python-Sockets
Created a server file, client file and a common code so that the client can upload files, download files, and see the list of files in the most recent directory via python sockets.

The server will be a Python script, named server.py, executed through the Windows
command line interface. The current working directory of the server (i.e., the directory
from where the server.py script is executed) will be used as the directory where files
will be stored and served from.

The server should receive, as its single command line argument, its port number; that
is, the server should be executed like so:
 python server.py <port number>
 
The server should be able to handle three types of requests:

• Uploading of a file: The client request should include, as a minimum, the
request type and the filename to be used on the server side, and the data of
the file. The server should then create the file (in exclusive creation, binary
mode) and copy the data sent by the client from the socket to the file. To avoid
accidents, the server should deny overwriting existing files.

• Downloading of a file: The client request should include, as a minimum, the
request type and the filename of the file to be downloaded. The server should
then open the file (in binary mode) and copy its data to the client through the
socket.

• Listing of 1st-level directory contents: The client request should indicate the
request type. The server should then construct a list of the names of
files/directories at the top level of its current working directory and return it to the client over the socket.

In every case, the server reports (i.e., prints on the console) information for every
request after its processing is over. This report is a single line including the IP address and port number of the client,
information on the request itself (type and filename) and its status (success/failure).
For failures, the report also includes an informative message indicating the type of error.
Lastly, the server also prints informative messages for any other types of errors
encountered throughout its execution.

The client will be a Python script, named client.py, executed through the Windows
command line interface and receiving its arguments as command line arguments. The
first argument should be the address of the server (hostname or IP address) and the
second argument should be the server’s port number. The next argument should be
one of “put”, “get” or “list”; these signify that the client wishes to send or receive
a file, or request a directory listing, respectively. For “put” and “get” there should
then be one more argument with the name of the file to upload/download
respectively. That is, the client should be executed like so:
 python client.py <hostname> <port> <put filename|get filename|list>
 
The client parses the command line arguments and decides what operation is
requested. The client then creates a client socket, connects to the server defined in the
command line, constructs and sends an appropriate request message, receives the
server’s response, process it, and finally closes the connection. The processing of
requests will depend on the request type:

• Upload (“put”) request: The client opens (in binary mode) the local file defined
on the command line, reads its data, sends it to the server through the socket, and finally closes the connection.

• Download (“get”) request: The client creates the local
file defined on the command line (in exclusive binary mode), reads the data sent
by the server, stores it in the file, and finally closes the connection. To avoid
accidents, the client denies overwriting existing files.

• Listing (“list”) request: the client sends an
appropriate request message, receives the listing from the server, prints it on
the screen one file per line, and finally closes the connection.

In every case, the client reports information for every request; this report
is a single line of text including the IP and port number of
the server, information on the request itself (type and filename), and
its status (success/failure). For failures, the report also includes an informative
message indicating the type of error (within the same single line).
