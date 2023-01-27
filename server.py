#  coding: utf-8 
import socketserver
import os

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
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))
        request = self.data.decode().split("\r\n")
        print(request)
        file_requested = request[0].split(" ")[1]

        # get the file path
        file_path = os.path.abspath("./www" + file_requested)

        # if the requested path not in .www
        if not file_path.startswith(os.path.abspath("./www")):
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type:text/html" + "\n\n" + "", "utf-8"))
            return

        # Must use 301 to correct path ending.

       # if (os.path.isdir('./www' + file_requested + '/')):
           # self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:text/html" + "\n\n" + str(content), "utf-8"))
           # return

        if (os.path.isdir('./www' + file_requested )):
            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:text/html" + "\n\n" + content, "utf-8"))
            return
        # Must use 301 to correct path ending.
        if (os.path.isdir('./www' + file_requested + '/')):
            self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + "/" + file_path + "/\n\n", "utf-8"))
            return

        # if exists
        if not os.path.isfile(file_path):
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type:text/html" + "\n\n" + "", "utf-8"))
            return
        
        with open(file_path, 'rb') as file:
            content = file.read()
        
        # get content type
        if file_path.endswith(".html"):
            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:text/html" + "\n\n" + str(content), "utf-8"))
            return
            #self.send_header("Content-Type", "text/html")
        elif file_path.endswith(".css"):
            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:text/css" + "\n\n" + str(content), "utf-8"))
            return
            #self.send_header("Content-Type", "text/css")

        # send the content
        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type:text/html" + "\n\n" + str(content), "utf-8"))
        #self.send_response(200)
        #self.end_headers()
        self.wfile.write(content)

        # Return a status code of “405 Method Not Allowed” for any method you cannot handle (POST/PUT/DELETE).
        if self.request != "GET":
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\nContent-Type:text/html" + "\n\n" + "", "utf-8"))
            return
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nContent-Type:text/html" + "\n\n" + "", "utf-8"))
            return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
