
import termios
import tty
import sys
import select

block = ["x"]
up = [0]
down = [0]
left = [0]
right = [0]
path = []
money = 15
round = 0
speed = 1.0

path1 = [2,12,22,32,42,43,44,34,24,14,15,16,17,27,28,38,39,49,59,69,68,78,77,87,86,85,84,74,64,63,62,72,82,92]
path2 = [2,12,22,23,24,14,15,16,17,27,28,38,39,49,59,69,68,78,77,87,86,85,84,83,82,92]
x1 = [9,10,20,23,83,90,99,100]
x2 = [9,10,20,90,99,100]

def ainput():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)  # read exactly 1 character
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print()  # newline after key
    return ch

def secinput(timeout):
    sys.stdout.flush()
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            ch = sys.stdin.read(1)
            print()  # newline
            return ch
        else:
            return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def map():
    string = "1 2 3 4 5 6 7 8 9 10\n"
    count = 1
    with open("map.txt", "w") as f:
        for i in range(10):
            for j in range(10):
                string = string + block[count] + " "
                count += 1
            string = string + "\n"
        f.write(string)

def update():
    string = ""
    map()
    with open("map.txt", "a") as f:
        string = string + "Money: " + str(money) + "\n"
        string = string + "Round: " + str(round) + "\n"
        if round < 2:
            string = string + "Press 'p' to stop.\nPress 'e' to place a melee tower for 5 money.\nPress 'r' to place a ranged tower for 10 money.\n"
        f.write(string)

def place(x,cost):
    global money
    if money < cost:
        return
    map()
    with open("map.txt", "a") as f:
        string = "Name a column from 1 to 10 to place the tower.\n"
        f.write(string)
    column = ainput()
    map()
    with open("map.txt", "a") as f:
        string = "Name a row from 2 to 11 to place the tower.\n"
        f.write(string)
    row = ainput()
    if column.isdigit() and row.isdigit():
        column = int(column)
        row = int(row)
        if 1 <= column <= 10 and 2 <= row <= 11:
            if block[(row-2)*10+column] == "□":
                block[(row-2)*10+column] = x
                money -= cost

def layout(newpath, x):
    global path
    for i in path:
        block[i] = "□"
    path = []
    for i in newpath:
        block[i] = "■"
        path.append(i)
    for i in x:
        block[i] = "x"

for i in range(10):
    for j in range(10):
        block.append("□")
        index = len(block)
        if index < 11:
            up.append(0)
        else:
            up.append(index-10)
        if index % 10 == 0:
            right.append(0)
        else:
            right.append(index+1)
        if index > 90:
            down.append(0)
        else:
            down.append(index+10)
        if index % 10 == 1:
            left.append(0)
        else:
            left.append(index-1)

layout(path1, x1)

with open("map.txt", "w") as f:
    f.write("Welcome to Tower Defense!\nYou can place a melee tower with the 'e' key.\nYou can place a ranged tower with the 'r' key.\nPress 'p' to stop.\nPress any button to continue.")

ainput()

while True:
    update()
    action = secinput(speed)
    if action == "p":
        exit()
    elif action == "e":
        place("e", 5)
    elif action == "r":
        place("r", 10)
