# webapp.py

from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

class ClockWebServer(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def get_log_entry(self, path):
        param_value = self.form_data
        return param_value

    def do_GET(self):
        print(self.path)
        log_entry = self.get_log_entry(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


    def do_POST(self):
        pass

def start_http_server(config={}):
    """
    
    """
    HOST = config.get("HOST", "localhost")
    PORT = config.get("PORT", 8000)
    
    web_server = HTTPServer((HOST,PORT), ClockWebServer)

    print(f"Server at htt://{HOST}:{PORT}")
    print("Use CTR+C to stop it")


if __name__ == "__main__":
    start_http_server()