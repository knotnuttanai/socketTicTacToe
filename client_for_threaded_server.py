import socket
import sys

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    # replace the host ip with your server's ip when playing online
    port = 8888

    try:
        s.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    print("\n===============================")
    print("input play or bye")
    while True:
        message = input(' -> ').strip()
        if message in ('play', 'bye'):
            break
        print('Please Enter play or bye')

    while message.lower().strip() != 'bye':
        s.send(message.encode())
        data = s.recv(1024).decode()
        while True:
            print("\n" + data)
            player = input().strip()
            if player.upper() in ('O', 'X'):
                break
            print('Please Enter O or X')
        s.send(player.encode())
        data = s.recv(1024).decode()
        while "Win" not in data:
            print("\nBoard:\n" + data)
            while True:
                message = input('Enter index <0-9> or <r> to display board -> ').strip()
                if message in [str(i+1) for i in range(9)] + ['r']:
                    break
                print('Please Enter number 1-9 for index, or enter <r> to display board')
            s.send(message.encode())
            data = s.recv(1024).decode()
        print(data)

        print("\n===============================")
        print("input play or bye")
        message = input(" -> ")

if __name__ == "__main__":
    main()