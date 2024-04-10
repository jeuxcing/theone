import socket

from os import getcwd, path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


WWW_DIRECTORY = path.join(getcwd(), "j5e/game/panelAdmin/www")

class MyRequestHandler(BaseHTTPRequestHandler):
    
    # Function to handle GET requests
    def do_GET(self):
        # Get the requested URL
        requested_url = self.path

        # Search for the file in the www directory
        filepath = self.get_file_path(requested_url)

        # If the file exists, serve it; otherwise, route the request
        if filepath:
            self.serve_file(filepath)
        else:
            self.route_request(requested_url)
    

     # Method to get the full path of the file in the www directory
    def get_file_path(self, url):
        # Extract the filename from the URL
        filename = url[1:]  # Remove the leading "/"
        filepath = path.join(WWW_DIRECTORY, filename)

        # Check if the file exists
        if path.exists(filepath) and path.isfile(filepath):
            return filepath
        else:
            return None

    # Method to serve a file
    def serve_file(self, filepath):
        # Read the content of the file
        with open(filepath, "rb") as file:
            content = file.read()

        # Send the response with code 200 (OK) and the appropriate MIME type for HTML
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    # Method to route requests
    def route_request(self, url):
        # Here you can add your routing logic for URLs
        # In this example, we simply send a response indicating that the URL is not found
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("404 Not Found: {}".format(url), "utf-8"))
    

def http_server_start():
    # Specify the IP address and port on which the server will listen
    address = ('', 8000)
    
    # Create an instance of the server using our custom request handler
    server = HTTPServer(address, MyRequestHandler)
    print('Server started on {}:{}'.format(*address))
    
    # Start the server and keep it running until manually stopped
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print('Server stopped.')