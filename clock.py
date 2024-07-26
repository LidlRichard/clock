import datetime as dt
import http.server
import sys, yaml, http
from yaml.error import YAMLError
from web.http_server import start_http_server

class Clock():
    
    """
    
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
    
    
    def _clock_in(self)-> str:
        self._write_log("Clocked in")

    
    def user_msg(self, msg:str, timestamp:str=None)-> str:
        msg = "clocked in" if msg == "in" else msg
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



def start():

    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        display_help()
        exit()

    clock = Clock() 
    

    if len(sys.argv) == 2:
        if sys.argv[1]=="--ui":
            print("\nstarting http server...")
            start_http_server(clock.config)
        else:
            clock.user_msg(str(sys.argv[1]))

    if len(sys.argv) == 3:
        clock.user_msg(str(sys.argv[1]), str(sys.argv[2]))


def display_help():
    print("\n")
    print("clock.py in\n")
    print('clock.py "task description" "[yyyy-mm-dd H:M[:S]"]\n')
    print('Enter "clock.py in" to start the day. Thereafter always enter tasks upon completion.\n')

if __name__ == "__main__":
    start()