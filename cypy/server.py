#!/usr/bin/env python
# cypy - HTTP server.
# ===================================

# Built-in modules
import re
import time
import fcntl
import struct
import socket
import argparse
from urllib.parse import urlparse, parse_qsl
from http.server import BaseHTTPRequestHandler, HTTPServer
# Project specific modules
import ui
from data import Data
from cypher import encode, decode
from credentials import Credential


# Get port number from user input.
parser = argparse.ArgumentParser(prog="cypy", description="CyPy CLI")
parser.add_argument("port", help="Port in which CyPy listens.")
args = parser.parse_args()


def get_ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


HOSTNAME = get_ip_addr()
PORT = int(args.port)

username_pattern = re.compile(r"\busername=([^&]+)")
password_pattern = re.compile(r"\bpassword=([^&]+)")
keyword_pattern = re.compile(r"\bkeyword=(\w+)")

paths = {
    "/add": {"status": 200},
    "/get": {"status": 200},
    "/del": {"status": 200},
}


class CyPyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/favicon.ico":
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(ui.generate_form(parsed_url.path), "UTF-8"))

    def do_POST(self):
        parsed_url = urlparse(self.path)
        # Get POST body content.
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("UTF-8")
        try:
            # Get each key-value pair.
            data = {
                "username": username_pattern.findall(post_data)[0],
                "keyword": keyword_pattern.findall(post_data)[0]
            }
            if len(password_pattern.findall(post_data)) > 0:
                data["password"] = password_pattern.findall(post_data)[0]
        except IndexError:
            print("No valid values used in form or the form has empty"
                  " obligatory values.")
            raise

        if parsed_url.path in paths:
            self.handle_request(paths[parsed_url.path]["status"],
                                parsed_url, data)
        else:
            self.handle_request(500, parsed_url, data)

    def handle_request(self, status_code, parsed_url, query_str):
        d = Data()

        def add_credential(data):
            cred = Credential(data["username"], data["password"],
                              data["keyword"])
            d.add_credential(cred.username, cred.password)
            response = ("Successfully added '{}' to credentials DB.".format(
                data["username"]
            ))
            return "<body><p>{}</p></body>".format(response)

        def get_credential(data):
            try:
                password = d.get_credential(encode(data["keyword"],
                                                   data["username"]))
                response = decode(data["keyword"], password)
            except KeyError:
                response = "ERROR: No such user."
            return "<body><p>{}</p></body>".format(response)

        def delete_credential(data):
            try:
                username = encode(data["keyword"], data["username"])
                d.delete_credential(username)
                response = "Successfully deleted user '{}'.".format(
                    data["username"]
                )
            except KeyError:
                response = "ERROR: No such user."
            return "<body><p>{}</p></body>".format(response)

        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        methods = {
            "/add": add_credential,
            "/get": get_credential,
            "/del": delete_credential
        }

        response = "<html><title>CyPy</title>"
        if status_code == 200:
            response += methods[parsed_url.path](query_str)
        elif status_code == 500:
            response += "<body><h3>Internal Server Error</h3></body>"
        else:
            response += "Status code #{}".format(status_code)
        response += "</html>"
        self.wfile.write(bytes(response, "UTF-8"))


if __name__ == '__main__':
    server = HTTPServer
    httpd = server((HOSTNAME, PORT), CyPyServer)
    print(time.asctime(), "Server starts - {}:{}".format(HOSTNAME, PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
print(time.asctime(), "Server stops - {}:{}".format(HOSTNAME, PORT))
