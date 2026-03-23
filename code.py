
import termios
import tty
import sys
import select

lives = 3
block = ["x"]
up = [0,0]
down = [0,11]
left = [0,0]
right = [0,2]
bocktowerID = [-1,-1]
path = []
money = 40
round = 1
speed = 1.0
turn = 0
enemypath = []
enemyhealth = []
towerblock = []
towerdmgbase = []
towerdmg = []
towerrange = []
towerrangetype = [] #di,sq, str, money, boost

class1 = "farm" #farm, castle, church, mage
class2 = "castle"
ctower = []
ctowercost = []
ctowerdmg = []
ctowerrange = []
ctowerrangetype = []

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
    string = "  0 1 2 3 4 5 6 7 8 9"
    count = 1
    with open("map.txt", "w") as f:
        for i in range(10):
            string = string + "\n" + str(i) + " "
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
        string = string + "Press 'p' to stop.\nPress '1' to place a farmer's hut for 15 money.\nPress '2' to place a archer tower for 25 money.\n"
        f.write(string)

def boost_update():
    for i in range(len(towerdmg)):
        towerdmg[i] = towerdmgbase[i]
    for i in range(len(towerblock)):
        if towerrangetype[i] == "boost":
            if block[towerblock[i]] == "A":
                hitarea = diamondrange(towerblock[i], towerrange[i])
                for j in range(len(towerblock)):
                    if towerblock[j] in hitarea and towerrangetype[j] != "money" and towerrangetype[j] != "boost":
                        towerdmg[j] = towerdmg[j]+towerdmg[i]
            if block[towerblock[i]] == "C":
                for j in range(len(towerblock)):
                    if towerrangetype[j] != "money":
                        towerdmg[j] = towerdmg[j]+towerdmg[i]

def place(x,cost,dmg,range,rangetype):
    global money
    if money < cost:
        return
    map()
    with open("map.txt", "a") as f:
        if x == "C":
            string = "Name a column from 0 to 9 to place the top left corner of the cathedral.\n"
        else:
            string = "Name a column from 0 to 9 to place the tower.\n"
        f.write(string)
    column = ainput()
    map()
    with open("map.txt", "a") as f:
        if x == "C":
            string = "Name a row from 0 to 9 to place the top left corner of the cathedral.\n"
        else:
            string = "Name a row from 0 to 9 to place the tower.\n"
        f.write(string)
    row = ainput()
    if column.isdigit() and row.isdigit():
        n = int(row)*10 + int(column) + 1
        if x == "C":
            if block[n] != "□" or block[n+1] != "□" or block[n+10] != "□" or block[n+11] != "□":
                return
            block[n+1] = x
            block[n+10] = x
            block[n+11] = x
        elif block[n] != "□":
            return
        block[n] = x
        money -= cost
        bocktowerID[n] = len(bocktowerID) - 1
        towerblock.append(n)
        towerdmgbase.append(dmg)
        towerdmg.append(dmg)
        towerrange.append(range)
        towerrangetype.append(rangetype)
        boost_update()

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
        bocktowerID.append(-1)
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

for i in [class1, class2]:
    if i == "farm":
        ctower.append("H")
        ctowercost.append(15)
        ctowerdmg.append(12)
        ctowerrange.append(1)
        ctowerrangetype.append("di")
        ctower.append("F")
        ctowercost.append(40)
        ctowerdmg.append(0)
        ctowerrange.append(0)
        ctowerrangetype.append("money")
        ctower.append("W")
        ctowercost.append(55)
        ctowerdmg.append(15)
        ctowerrange.append(3)
        ctowerrangetype.append("str")
    elif i == "castle":
        ctower.append("T")
        ctowercost.append(25)
        ctowerdmg.append(6)
        ctowerrange.append(2)
        ctowerrangetype.append("di")
        ctower.append("A")
        ctowercost.append(30)
        ctowerdmg.append(2)
        ctowerrange.append(2)
        ctowerrangetype.append("boost")
        ctower.append("B")
        ctowercost.append(35)
        ctowerdmg.append(15)
        ctowerrange.append(3)
        ctowerrangetype.append("str")
    elif i == "church":
        ctower.append("+")
        ctowercost.append(10)
        ctowerdmg.append(6)
        ctowerrange.append(2)
        ctowerrangetype.append("str")
        ctower.append("C")
        ctowercost.append(75)
        ctowerdmg.append(0)
        ctowerrange.append(0)
        ctowerrangetype.append("boost")
        ctower.append("Ʌ")
        ctowercost.append(30)
        ctowerdmg.append(12) 
        ctowerrange.append(1)
        ctowerrangetype.append("sq")

with open("map.txt", "w") as f:
    f.write("Welcome to Tower Defense!\nYou can place a farmer's hut with the '1' key.\nYou can place a archer tower with the '2' key.\nPress 'p' to stop.\nPress any button to continue.")

ainput()

while True:
    update()
    action = secinput(speed)
    if action == "p":
        exit()
    elif action == "1":
        place(ctower[0], ctowercost[0], ctowerdmg[0], ctowerrange[0], ctowerrangetype[0])
    elif action == "2":
        place(ctower[3], ctowercost[3], ctowerdmg[3], ctowerrange[3], ctowerrangetype[3])
    elif action == "3":
        if round > 3:
            place(ctower[1], ctowercost[1], ctowerdmg[1], ctowerrange[1], ctowerrangetype[1])
    elif action == "4":
        if round > 3:
            place(ctower[4], ctowercost[4], ctowerdmg[4], ctowerrange[4], ctowerrangetype[4])
    elif action == "5":
        if round > 7:
            place(ctower[2], ctowercost[2], ctowerdmg[2], ctowerrange[2], ctowerrangetype[2])
    elif action == "6":
        if round > 7:
            place(ctower[5], ctowercost[5], ctowerdmg[5], ctowerrange[5], ctowerrangetype[5])
    elif action == "n":
        round += 1
        turn = 0
        for i in range(len(towerblock)):
            if towerrangetype[i] == "money":
                money += towerdmg[i]
        if round == 4:
            layout(path2, x2)
        elif round == 11:
            layout(path3, x3)
    elif action is None:
        turn += 1
        for i in range(len(enemypath)-1,-1,-1):
            block[path[enemypath[i]]] = "■"
            if enemyhealth[i] <= 0:
                enemypath.pop(i)
                enemyhealth.pop(i)
                money += 2
            elif enemypath[i] < len(path)-1:
                enemypath[i] += 1
                block[path[enemypath[i]]] = "▼"
            else:
                lives -= 1
                if lives == 0:
                    with open("map.txt", "w") as f:
                        f.write("Game Over! You survived until round " + str(round) + ".")
                    exit()
                enemypath.pop(i)
                enemyhealth.pop(i)
        if turn % 3 == 0 and turn <= 15*round:
            enemypath.append(0)
            enemyhealth.append(36+round*2)
            block[path[0]] = "▼"
        for i in range(len(towerblock)):
            if towerrangetype[i] == "money"or towerrangetype[i] == "boost":
                continue
            elif towerrangetype[i] == "di":
                hitarea = diamondrange(towerblock[i], towerrange[i])
            elif towerrangetype[i] == "sq":
                hitarea = squarerange(towerblock[i], towerrange[i])
            elif towerrangetype[i] == "str":
                hitarea = straightrange(towerblock[i], towerrange[i])
            for j in range(len(enemypath)):
                if path[enemypath[j]] in hitarea:
                    enemyhealth[j] -= towerdmg[i]
