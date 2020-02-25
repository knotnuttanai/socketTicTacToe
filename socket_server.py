import socket
import random

board = [[0,0,0],[0,0,0],[0,0,0]]
num2Eng = {0:' ',1:'O',4:'X'}
eng2Num = {' ':0,'O':1,'X':4}
avail = [(i,j) for i in range(3) for j in range(3)]
indexTo2D = {(i*3)+j+1:(i,j) for i in range(3) for j in range(3)}

def genBoardMessage():
    s = ''
    for i in range(5):
        s+=' '
        for j in range(3):
            if i%2==0:
                s += ' '+num2Eng[board[i//2][j]]+' '
                if j == 0 or j == 1: s+= '|'
            else:
                s += '--- '
        s += '\n'
    return s

def genBoardIndex():
    s = ''
    for i in range(5):
        s+=' '
        for j in range(3):
            if i%2==0:
                s += ' '+str(((i//2)*3)+j+1)+' '
                if j == 0 or j == 1: s+= '|'
            else:
                s += '--- '
        s += '\n'
    return s


def checkWin():
    if len(avail)==0:
        return "Draw"
    col=[0,0,0]
    diag=[0,0]
    for i in range(3):
        if sum(board[i])==3:
            return 'O Win!'
        elif sum(board[i])==12:
            return 'X Win!'
        for j in range(3):
            if i==j:
                diag[0]+=board[i][j]
            if i+j==2:
                diag[1]+=board[i][j]
            col[j]+=board[i][j]
    for i in range(3):
        if col[i]==3:
            return 'O Win!'
        elif col[i]==12:
            return 'X Win!'
    for i in range(2):
        if diag[i]==3:
            return 'O Win!'
        elif diag[i]==12:
            return 'X Win!'
    return 'No'
    
def serverTurn(conn,server):
    i,j = random.choice(avail)
    print('Server at',i,j)
    board[i][j] = server
    avail.pop(avail.index((i,j)))

def playerTurn(conn,player,data):
    i = int(data[0])
    j = int(data[1])
    print("User at",i,j)
    board[i][j] = player
    avail.pop(avail.index((i,j)))


def playGame(conn):
    message = genBoardIndex() + "\n\nDo you want to be O or X? [O/X]: "
    conn.send(message.encode())
    data = conn.recv(1024).decode()
    print("User is",data)
    if data.upper() == 'X':
        player = 4
        server = 1
        i,j = random.choice(avail)
        board[i][j] = server
        avail.pop(avail.index((i,j)))
    else:
        server = 4
        player = 1
    while checkWin() == 'No':
        s = genBoardMessage() + '\nYour Turn:'
        conn.send(s.encode())
        data = conn.recv(1024).decode()
        data = indexTo2D[int(data)]
        playerTurn(conn,player,data)
        if checkWin() != 'No':
            break
        serverTurn(conn,server)
    message = genBoardMessage() + '\n\n' + checkWin()
    conn.send(message.encode())
    
    
def server_program():
    host = socket.gethostname()
    port = 5000
    global board,num2Eng,eng2Num,avail
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
    s.bind((host, port)) 

    s.listen(2)
    conn, addr = s.accept() 
    print('Connected by', addr)
    while True:
        data = conn.recv(1024).decode()
        if not data:
            print('break')
            break
        print("from connected user: " + str(data))
        if(data=="play"):
            board = [[0,0,0],[0,0,0],[0,0,0]]
            num2Eng = {0:' ',1:'O',4:'X'}
            eng2Num = {' ':0,'O':1,'X':4}
            avail = [(i,j) for i in range(3) for j in range(3)]
            playGame(conn)
        elif(data == "bye"):
            break

    conn.close() 

if __name__ == '__main__':
    server_program()
