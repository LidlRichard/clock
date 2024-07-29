# webapp.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader
import os, datetime as dt

LOG = "clock.log"

class ClockWebServer(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        logs = self.load_logs(LOG)
        
        if self.path == "/":
            # if no GET param then create initial page using HTML template and initial 'clocking in' log entry
            logs.append(self.add_timestamp("Clocked in"))
            # write logs back to log file
            self.write_logs(logs)
            # respond to user
            self.update_task_page(logs)
        else:
            # if param check correct param name, append log entry and send updated page in response
            query_components = parse_qs(urlparse(self.path).query)
            log_msg = query_components.get("log_msg")
            if log_msg and len(log_msg) > 0:
                print(log_msg[0])
                # Add timestamp to new log entry
                msg = self.add_timestamp(log_msg[0])
                # Add task entry to logs list
                logs.append(msg)
                # write logs back to log file
                self.write_logs(logs)
                # respond to user
                self.update_task_page(logs)

    def write_logs(self, logs)->None:
        """
        writes log list back to file
        """
        with open(LOG, "w") as log_file:
            for entry in logs:
                log_file.writelines(f"{entry}\n")

    def update_task_page(self, logs):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            jinja_environment = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
            page_template = jinja_environment.get_template("index.html")
            page_rendered = bytes(page_template.render({"logs": logs}), "utf-8")
            self.wfile.write(page_rendered)

    def add_timestamp(self,msg:str)->str:
        """
        prepends iso8601 timestamp to log entry
        """
        timestamp = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {msg}"

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