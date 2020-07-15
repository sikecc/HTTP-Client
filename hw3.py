import logging
import socket
import sys
import ssl

def parse_url(url):
    """
    Parse the url for host, path, & port
    """
    if(len(url) == 1):
        #parsed = url[0].split('/', 1)
        path = "/"
    else:
        parsed = url[1].split('/', 1)
        path = "/" + parsed[0]
    
    host_name = url[0]

    # # host_name = url[0]
    # print(parsed)
    # if parsed[0] == '':
    #     path = "/"
    # else:
        
	# set port number to default
    if host_name.find(":") == -1:
        port = 80
    else:
        # path = "/" + parsed[0]
        parsed = host_name.split(":")
        host_name = parsed[0]
        port = int(parsed[1])
    
    

    full_list = [host_name, path, port]
	# # return get statment
	# http_Request = "GET " + path + " HTTP/1.1\r\nHost: " + hostname + ":" + port + "\r\nConnection: Close\r\n\r\n"
    return full_list

    
def retrieve_url(url):
    """
    Parse the url
    """

    ssl_version = None
    certfile = None
    keyfile = "./ssl/key.pem"
    ciphers = None


    path_list = []
    url_length = len(url)

    
    if url.find("http://", 0, 7) != -1:
        path_list = (url[7:url_length].split("/", 1))
    elif url.find("https://", 0, 8) != -1:
        path_list = (url[8:url_length].split("/",1))
    

    client_path = parse_url(path_list)

    # """
    # Connect to the host & port to get path
    # """
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.load_default_certs()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientSocket = context.wrap_socket(s)

    try:
        clientSocket.connect((client_path[0], client_path[2]))
    except socket.error:
        return None
    
    
    client_request = ("GET " + client_path[1] + " HTTP/1.1\r\nHost:" + client_path[0] + "\r\nConnection: close\r\n\r\n")
    clientSocket.send(client_request.encode('utf-8'))
    data = clientSocket.recv(4096)

    # check if its not a 404 page
    if data.find(b"200 OK") == -1:
        return None
	
    # iterate thru the data to send
    newData = data
    while True:
        data = clientSocket.recv(4096)
        if not data:
            break
        newData += data

    parsed = newData.split(b"\r\n\r\n",2)
    finalData = parsed[1]

    return finalData


# print(retrieve_url('http://www.fieggen.com/shoelace'))
# print(retrieve_url('http://www.example.com'))
# print(retrieve_url('http://i.imgur.com/fyxDric.jpg'))
# print(retrieve_url('http://go.com/doesnotexist'))
# print(retrieve_url('http://www.ifyouregisterthisforclassyouareoutofcontrol.com/'))
# print(retrieve_url('http://www.asnt.org:8080/Test.html'))
# print(retrieve_url('http://www.httpwatch.com/httpgallery/chunked/chunkedimage.aspx'))
# print(retrieve_url('https://www.cs.uic.edu/~ckanich/'))
print(retrieve_url('https://😻🍕.ws'))
# print(retrieve_url('http://www.uic.edu/'))
# print(retrieve_url('http://www.google.com'))