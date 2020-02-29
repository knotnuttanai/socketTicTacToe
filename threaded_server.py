import socket
import sys
import traceback
import random
from _thread import *
from threading import Thread
import threading

board = [[0,0,0],[0,0,0],[0,0,0]]
num2Eng = {0:' ',1:'O',4:'X'}
eng2Num = {' ':0,'O':1,'X':4}
avail = [(i,j) for i in range(3) for j in range(3)]
indexTo2D = {(i*3)+j+1:(i,j) for i in range(3) for j in range(3)}
player_list = []

def main():
    start_server()


def start_server():
    host = "0.0.0.0"
    port = 8888

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)
    print("Socket now listening")

    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(c, ip, port):
    global board, num2Eng, eng2Num, avail
    player_list.append(port)
    print("Player " + str(len(player_list)) + " port: " + str(port))

    while True:
        data = c.recv(1024).decode()
        if not data:
            print('break')
            break
        print("from connected user: " + str(data))
        if (data == "play"):
            board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            num2Eng = {0: ' ', 1: 'O', 4: 'X'}
            eng2Num = {' ': 0, 'O': 1, 'X': 4}
            avail = [(i, j) for i in range(3) for j in range(3)]
            playGame(c, ip, port)
        elif (data == "bye"):
            break


def genBoardMessage():
    s = ''
    for i in range(5):
        s += ' '
        for j in range(3):
            if i % 2 == 0:
                s += ' ' + num2Eng[board[i // 2][j]] + ' '
                if j == 0 or j == 1: s += '|'
            else:
                s += '--- '
        s += '\n'
    return s


def genBoardIndex():
    s = ''
    for i in range(5):
        s += ' '
        for j in range(3):
            if i % 2 == 0:
                s += ' ' + str(((i // 2) * 3) + j + 1) + ' '
                if j == 0 or j == 1: s += '|'
            else:
                s += '--- '
        s += '\n'
    return s


def checkWin():
    if len(avail) == 0:
        return "Draw"
    col = [0, 0, 0]
    diag = [0, 0]
    for i in range(3):
        if sum(board[i]) == 3:
            return 'O Win!'
        elif sum(board[i]) == 12:
            return 'X Win!'
        for j in range(3):
            if i == j:
                diag[0] += board[i][j]
            if i + j == 2:
                diag[1] += board[i][j]
            col[j] += board[i][j]
    for i in range(3):
        if col[i] == 3:
            return 'O Win!'
        elif col[i] == 12:
            return 'X Win!'
    for i in range(2):
        if diag[i] == 3:
            return 'O Win!'
        elif diag[i] == 12:
            return 'X Win!'
    return 'No'


def serverTurn(conn, server):
    i, j = random.choice(avail)
    print('Server at', i, j)
    board[i][j] = server
    avail.pop(avail.index((i, j)))


def playerTurn(conn, player, data):
    i = int(data[0])
    j = int(data[1])

    if player == 4:
        print("X at", i, j)
    else:
        print("O at", i, j)
    board[i][j] = player
    avail.pop(avail.index((i, j)))

def getPlayerByPort(port):
    if port in player_list:
        return player_list.index(port) + 1
    else: return -1

def getPlayerStringByPort(port):
    return "Player " + str(getPlayerByPort(port))


def playGame(conn, ip, port):
    global turn
    message = genBoardIndex() + "\n\nDo you want to be O or X? [O/X]: "
    conn.send(message.encode())
    data = conn.recv(1024).decode()
    print(getPlayerStringByPort(port) + " is", data)
    if data.upper() == 'X':
        player1 = 4
        player2 = 1
    else:
        player2 = 4
        player1 = 1

    data = ""
    while checkWin() == 'No':
        if(data != 'r'):
            s = genBoardMessage() + '\nEnter index:'
            conn.send(s.encode())
        data = conn.recv(1024).decode()

        if data == 'r':
            conn.send(genBoardMessage().encode())
            if checkWin() != 'No':
                break
        else:
            data = indexTo2D[int(data)]
            playerTurn(conn, player1, data)
            if checkWin() != 'No':
                break

    message = genBoardMessage() + '\n\n' + checkWin()
    conn.send(message.encode())

if __name__ == "__main__":
    main()