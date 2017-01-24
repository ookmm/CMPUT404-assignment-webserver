#  coding: utf-8 
import SocketServer
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


# Copyright 2017 Avery Tan, Gaylord Mbuyi Konji
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


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip() #grab the incoming data
        print ("Got a request of: %s\n" % self.data) 

        splitData = self.data.split()
        method = splitData[0] #the methods: GET, POST, PUT etc,..
        desiredPath = splitData[1] 
        fullUrl = os.path.abspath(os.getcwd()+'/www'+desiredPath) #get the full directory path
        # print 'fullUrl is ' + fullUrl
        # print 'desiredpath is ' + desiredPath
        # print 'method is ' + method

        try:
            if os.path.exists(fullUrl) and method == 'GET':
                if desiredPath[-1] != '/' and os.path.isdir(fullUrl): #the current directory contains no files
                    self.send301(fullUrl, desiredPath)
                else:
                    self.send200(fullUrl) #we are inside the directory
            else:
                self.send404(fullUrl)

        except IOError:
            self.send404(fullUrl)
            #print("ERROR###############################################\r\n\r\n")

    def send404(self, fullUrl):
        self.request.sendall('HTTP/1.1 404 Not Found\r\n')
        return
    
    def send301(self, fullUrl, desiredPath):
        self.request.sendall("HTTP/1.1 301 Moved Permanently\r\nLocation: " + fullUrl + "/\r\n")
        return

    def send200(self, fullUrl):
        header = 'HTTP/1.1 200 OK\r\n'
        try:
            if fullUrl.endswith('.html'):
                fileType = 'Content-Type: text/html\r\n' #set content type
            elif fullUrl.endswith('.css'):
                fileType = 'Content-Type: text/css\r\n'
            else: 
                fileType = 'Content-Type: text/html\r\n'
                fullUrl = fullUrl +'/index.html' #no content type specified, so serve them the index.html file
        except IOError:
            self.send404(fullUrl)

        file = open(fullUrl,'r').read()
        fileLen =  'Content-Length: ' + str(len(file)) + '\r\n\r\n'
        reply = header + fileType + fileLen+ file
        self.request.sendall(reply)
        return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
