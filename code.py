
import termios
import tty
import sys
import select

block = ["x"]
up = [0,0]
down = [0,11]
left = [0,0]
right = [0,2]
path = []
money = 15
round = 1
speed = 1.0
turn = 0
enemypath = []
enemyhealth = []

path1 = [2,12,22,32,42,43,44,34,24,14,15,16,17,27,28,38,39,49,59,69,68,78,77,87,86,85,84,74,64,63,62,72,82,92]
path2 = [2,12,22,23,24,14,15,16,17,27,28,38,39,49,59,69,68,78,77,87,86,85,84,83,82,92]
path3 = [2,12,22,23,24,34,35,36,46,56,66,65,64,74,84,83,82,92]
x1 = [9,10,20,23,35,36,46,56,66,65,83,90,99,100]
x2 = [9,10,20,34,35,36,46,56,66,65,64,74,90,99,100]
x3 = [9,10,20,90,99,100]

def diamondrange(index, radius):
    result = [index]
    new = [index]
    for i in range(radius):
        oldnew = new.copy()
        new = []
        for j in oldnew:
            if up[j] != 0 and up[j] not in result:
                result.append(up[j])
                new.append(up[j])
            if right[j] != 0 and right[j] not in result:
                result.append(right[j])
                new.append(right[j])
            if down[j] != 0 and down[j] not in result:
                result.append(down[j])
                new.append(down[j])
            if left[j] != 0 and left[j] not in result:
                result.append(left[j])
                new.append(left[j])
    result.pop(0)
    return result

def squarerange(index, radius):
    result = [index]
    a = index
    for i in range(1, radius+1):
        if right[a] != 0:
            a = right[a]
            result.append(a)
        else:
            break
    a = index
    for i in range(1, radius+1):
        if left[a] != 0:
            a = left[a]
            result.append(a)
        else:
            break
    horizontal = result.copy()
    for i in horizontal:
        a = i
        for j in range(1, radius+1):
            if up[a] != 0:
                a = up[a]
                result.append(a)
            else:
                break
        a = i
        for j in range(1, radius+1):
            if down[a] != 0:
                a = down[a]
                result.append(a)
            else:
                break
    result.pop(0)
    return result

def straightrange(index, radius):
    result = []
    a = index
    for i in range(1, radius+1):
        if up[a] != 0:
            a = up[a]
            result.append(a)
        else:
            break
    a = index
    for i in range(1, radius+1):
        if right[a] != 0:
            a = right[a]
            result.append(a)
        else:
            break
    a = index
    for i in range(1, radius+1):
        if down[a] != 0:
            a = down[a]
            result.append(a)
        else:
            break
    a = index
    for i in range(1, radius+1):
        if left[a] != 0:
            a = left[a]
            result.append(a)
        else:
            break
    return result

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
    elif action == "n":
        round += 1
        if round == 4:
            layout(path2, x2)
        elif round == 11:
            layout(path3, x3)
    elif action is None:
        turn += 1
        for i in range(len(enemypath)-1,0,-1): #bug first enemy not moving
            block[path[enemypath[i]]] = "■"
            if enemypath[i] < len(path)-1 and enemyhealth[i] > 0:
                enemypath[i] += 1
                block[path[enemypath[i]]] = "▼"
            else:
                enemypath.pop(i)
                enemyhealth.pop(i)
        if turn % 3 == 0 and turn <= 15*round:
            enemypath.append(0)
            enemyhealth.append(8+round*2)
            block[path[0]] = "▼"

