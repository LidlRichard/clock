# webapp.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, FileSystemLoader
import os

LOG = "clock.log"

class ClockWebServer(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        logs = self.load_logs(LOG)
        
        if self.path == "/":
            # if no GET param then create initial page using HTML template
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            jinja_environment = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
            page_template = jinja_environment.get_template("index.html")
            page_rendered = bytes(page_template.render({"logs": logs}), "utf-8")
            self.wfile.write(page_rendered)

        else:
            # if param check correct param name, append log entry and send updated page in response
            pass


    def load_logs(self, log)->list:
        """
        load into server memory the entries from the log file
        as a list, so these can be written to the html template
        and served as a http response page to the user
        """
        log_entries = []
        with open(log, "r") as log_file:
            for line in log_file:
                print(line)
                log_entries.append(str(line).replace("\n",""))
        return log_entries


def start_http_server(config={})->None:
    """
    
    """
    HOST = config.get("HOST", "localhost")
    PORT = config.get("PORT", 8000)

    if config.get("log"):
        LOG = config["log"]

    web_server = HTTPServer((HOST,PORT), ClockWebServer)

    print(f"Server at http://{HOST}:{PORT}")
    print("Use CTR+C to stop it")

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped")


if __name__ == "__main__":
    start_http_server()