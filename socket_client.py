import socket


def client_program():
    host = socket.gethostname() 
    port = 5000 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((host, port))  

    print("\n===============================")
    print("input play or bye")
    while True:
        message = input(' -> ').strip()
        if message in ('play','bye'):
            break
        print('Please Enter play or bye')

    while message.lower().strip() != 'bye':
        s.send(message.encode())
        data = s.recv(1024).decode()
        while True:
            print("\n"+data)
            player = input().strip()
            if player.upper() in ('O','X'):
                break
            print('Please Enter O or X')
        s.send(player.encode())
        data = s.recv(1024).decode()
        while "Win" not in data:
            print("\nBoard:\n"+data)
            while True:
                message = input(' index -> ').strip()
                if message in [str(i) for i in range(10)]:
                    break
                print('Please Enter number 1-9')
            s.send(message.encode())
            data = s.recv(1024).decode()
        print(data)

        print("\n===============================")
        print("input play or bye")
        message = input(" -> ")  

    s.close() 


if __name__ == '__main__':
    client_program()
