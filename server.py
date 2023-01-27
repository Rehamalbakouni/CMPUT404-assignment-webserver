
#  coding: utf-8 
import socketserver
import os
import mimetypes


# You will need to create a class that inherits from BaseHTTPRequestHandler
# and override the do_GET method. You will also need to create a server
# that inherits from TCPServer and pass in your request handler class.


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % self.data)


        path = self.data.split()[1]

        file_path = os.path.abspath("www"+ path)
  
        if os.path.commonpath([file_path, os.path.abspath("www")]) != os.path.abspath("www"):
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n",'utf-8'))
            return

        if os.path.isfile(file_path):
            content = file = open(file_path).read()
            response = f"HTTP/1.1 200 OK\r\nContent-Length: " + str(len(content)) + "\r\n"
            response += f"Content-Type: {mimetypes.guess_type(file_path)[0]}; charset=utf-8\r\n"
            response += "\r\n"
            self.request.sendall(bytearray(response + content,'utf-8'))
            return

        if os.path.isdir(file_path) and path.endswith("/"):  
     
            content = file = open(file_path + "/index.html").read()
            if os.path.isfile(file_path + "/index.html"):
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Length: " + str(len(content)) + "\r\nContent-Type: text/html; charset=utf-8\r\n" + content,'utf-8'))   
                return
    

        if os.path.isdir(file_path) and not path.endswith("/") :
            self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + "/" + file_path + "/\n\n", "utf-8"))
            return

        if self.data.split()[0] != "GET":
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n",'utf-8'))
            return
        
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n",'utf-8'))
            return
        
        
    
    


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()