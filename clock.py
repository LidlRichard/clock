import datetime as dt
import yaml
from yaml.error import YAMLError

LOG = "clock.log"

class Clock():
    
    """
    Class for reading and writing to the Clock
    app's log file.
    """
    
    def __init__(self) -> None:
        try:
            with open("config.yaml", "r") as config_file:
                self.config:dict = yaml.safe_load(config_file)
                self.log_location = self.config["log"]
        except FileNotFoundError:
            print(f"\nCannot find Clock config file: config.yaml\n")
            exit()
        except YAMLError:
            print(f"\nError loading config.yaml file: config.yaml\n")
            exit()
        except KeyError:
            print(f"\nKeyError when attempting to access log file in config.yaml\n")
            exit()
        except Exception as err:
            print(f"\nUnexpected {err=}, {type(err)=}")
            exit()
    
    
    def clock_in(self)-> str:
        self._write_log("Clocked in")

    
    def user_msg(self, msg:str, timestamp:str=None)-> str:
        msg = "Clocked in" if msg == "in" else msg
        self._write_log(msg, timestamp)

    
    def _write_log(self, msg:str, timestamp=None) -> None:
        
        if timestamp is None:
            timestamp = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
        
        try:
            timestamp = dt.datetime.fromisoformat(str(timestamp))
        except ValueError:
            print(f"\nTypeError when converting timestamp {timestamp} - use iso format 8601 e.g. 2024-07-22 15:30\n")
            exit()
        except Exception as err:
            print(f"\nUnexpected {err=}, {type(err)=}\n")
            exit()
        
        try:
            with open(self.log_location, "a") as log:
                log.write(f"[{timestamp}] {msg}\n")
        except Exception as err:
            print(f"\nUnexpected {err=}, {type(err)=}\n")
            exit()

    def load_logs(self, log)->list:
        """
        load into server memory the entries from the log file
        as a list, so these can be written to the html template
        and served as a http response page to the user
        """
        log_entries = []
        with open(log, "r") as log_file:
            for line in log_file:
#                print(line)
                log_entries.append(str(line).replace("\n",""))
        return log_entries
    
    def write_logs(self, logs)->None:
        """
        writes log list back to file
        """
        with open(LOG, "w") as log_file:
            for entry in logs:
                log_file.writelines(f"{entry}\n")

    def add_timestamp(self,msg:str)->str:
        """
        prepends iso8601 timestamp to log entry
        """
        timestamp = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {msg}"