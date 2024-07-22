import datetime as dt
import sys, yaml
from yaml.error import YAMLError

class Clock():
    
    """
    
    """
    
    def __init__(self) -> None:
        try:
            with open("config.yaml", "r") as config_file:
                config = yaml.safe_load(config_file)
                self.log_location = config["log"]
        except FileNotFoundError:
            print(f"Cannot find Clock config file: config.yaml")
            raise
        except YAMLError:
            print(f"Error loading config.yaml file: config.yaml")
            raise
        except KeyError:
            print(f"KeyError when attempting to access log file in config.yaml")
            raise
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
    
    
    def _clock_in(self)-> str:
        self._write_log("Clocked in")

    
    def user_msg(self, msg:str, timestamp:str=None)-> str:
        self._write_log(msg, timestamp)

    
    def _write_log(self, msg:str, timestamp=None) -> None:
        
        if timestamp is None:
            timestamp = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
        
        try:
            timestamp = dt.datetime.fromisoformat(str(timestamp))
        except ValueError:
            print(f"TypeError when converting timestamp {timestamp} - use iso format 8601 e.g. 2024-07-22 15:30")
            raise
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        
        try:
            with open(self.log_location, "a") as log:
                log.write(f"[{timestamp}] {msg}\n")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise



def start():

    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        display_help()
        exit()

    clock = Clock() 
    

    if len(sys.argv) == 2:
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