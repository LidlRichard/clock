import sys
from web.http_server import start_http_server
from clock import Clock


def start():

    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        display_help()
        exit()

    clock = Clock()
    

    if len(sys.argv) == 2:
        if sys.argv[1]=="--ui":
            print("\nstarting http server...")
            start_http_server(clock)
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