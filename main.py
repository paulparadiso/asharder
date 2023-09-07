from filer import *
from socketer import *

def on_message(msg):
    print(msg)
    if(msg == 'get_random_file'):
    

def main():
    comms = Socketer(4445, 4446, on_message)
    comms.start()

if __name__ == "__main__":
    main()