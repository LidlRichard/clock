from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader
import os, datetime as dt
from clock import Clock, LOG


class ClockWebServer(BaseHTTPRequestHandler):

    def __init__(self, clock:Clock, *args):
        self.clock:Clock = clock
        self.config:dict = clock.config
        BaseHTTPRequestHandler.__init__(self, *args)


    def do_GET(self):
        print(self.path)
        logs = self.clock.load_logs(self.config.get("log") or LOG)
        
        if self.path == "/":
            # respond to user
            self.update_task_page(logs)
        else:
            # if param check correct param name, append log entry and send updated page in response
            query_components = parse_qs(urlparse(self.path).query)
            log_msg = query_components.get("log_msg")
            if log_msg and len(log_msg) > 0:
                print(log_msg[0])
                # Add timestamp to new log entry
                msg = self.clock.add_timestamp(log_msg[0])
                # Add task entry to logs list
                logs.append(msg)
                # write logs back to log file
                self.clock.write_logs(logs)
                # respond to user
                self.update_task_page(logs)

    def update_task_page(self, logs):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            jinja_environment = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
            page_template = jinja_environment.get_template("index.html")
            page_rendered = bytes(page_template.render({"logs": logs}), "utf-8")
            self.wfile.write(page_rendered)


def start_http_server(clock:Clock)->None:
    """
    
    """
    def handler(*args):
        """
        Function required to inject config
        dict into HTTP Request Handler
        """
        ClockWebServer(clock, *args)

    config = clock.config

    HOST = config.get("HOST", "localhost")
    PORT = config.get("PORT", 8000)

    web_server = HTTPServer((HOST,PORT), handler)

    print(f"Server at http://{HOST}:{PORT}")
    print("Use CTR+C to stop it")

    if config.get("clock_in_upon_web_server_initialisation"):
        # write direct to log with initial 'Clock In' entry
        clock.clock_in()

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped")


if __name__ == "__main__":
    start_http_server()