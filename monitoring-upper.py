from tkinter import *
from random import *
import time;
import random;

# Sensing radius
rs = 1
# Communication radius
rc = 3
# Weight
M = 1

# Total number of nodes 15*15= 225
total_nodes = 15
# Total number of objects 10*10= 100
total_objects = 10
# Grid size
row_size = 200
col_size = 200

# Position of node before a time step
pos_row = [[0 for y in range(total_nodes)] for x in range(total_nodes)]
pos_col = [[0 for y in range(total_nodes)] for x in range(total_nodes)]

# Position of object before a time step
obj_row = [0 for y in range(total_nodes**2)]
obj_col = [0 for y in range(total_nodes**2)]

# Position of node after a time step
new_pos_row = [[0 for y in range(total_nodes)] for x in range(total_nodes)]
new_pos_col = [[0 for y in range(total_nodes)] for x in range(total_nodes)]

# Movement direction previous time step
sx = [[0 for y in range(total_nodes)] for x in range(total_nodes)]
sy = [[0 for y in range(total_nodes)] for x in range(total_nodes)]

# Number of nodes in each grid position before a time step
nodes_in_pos = [[0 for y in range(col_size)] for x in range(row_size)]
# Number of nodes in each grid position after a time step
new_nodes_in_pos = [[0 for y in range(col_size)] for x in range(row_size)]

# Number of objects in each grid position before a time step
objs_in_pos = [[0 for y in range(col_size)] for x in range(row_size)]
# Count if this positions object is taken or not
objs_cnt = [[0 for y in range(col_size)] for x in range(row_size)]

# Different weights for each node
weightX_left = [[[0 for k in range(2)] for j in range(total_nodes)] for i in range(total_nodes)]
weightY_left = [[[0 for k in range(2)] for j in range(total_nodes)] for i in range(total_nodes)]
weightX_right = [[[0 for k in range(2)] for j in range(total_nodes)] for i in range(total_nodes)]
weightY_right = [[[0 for k in range(2)] for j in range(total_nodes)] for i in range(total_nodes)]

#Movement of each node
movement = [[0 for y in range(total_nodes)] for x in range(total_nodes)]

# Graph of the largest component
graph = dict()

# For connectivity
adj_matrix = [[0 for y in range(total_nodes**2)] for x in range(total_nodes**2)]

# Show the positions that are covered
sensed = [[0 for y in range(col_size)] for x in range(row_size)]





# Nodes are considered to begin at the center                                                                           joss
r = 93
c = 87
for i in range(total_nodes):
    for j in range(total_nodes):
        pos_row[i][j] = r
        pos_col[i][j] = c
        nodes_in_pos[r][c] += 1
        new_pos_row[i][j] = r
        new_pos_col[i][j] = c
        new_nodes_in_pos[r][c] += 1
        c += 2
        if c > 115:
            r += 1
            if r % 2 == 0:
                c = 86
            else:
                c = 87





# Nodes are considered to begin at the center                                                                           joss
r = 85
c = 91
for i in range(total_objects**2):
        obj_row[i] = r
        obj_col[i] = c
        objs_in_pos[r][c] += 1
        c += 2
        if c > 109:
            r += 1
            if r % 2 == 0:
                c = 90
            else:
                c = 91





# Calculate the number of cells for hex grid
cells = 0
for i in range(row_size):
    for j in range(col_size):
        if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
            cells += 1

root = Tk()
canvas = Canvas(root, height=1000, width=1000)
canvas.pack()





def draw(pixels):
    box = [0, 0, pixels * col_size, pixels * row_size]
    canvas.create_rectangle(box, fill='black')

    for i in range(row_size):
        for j in range(col_size):
            box = [j * pixels, i * pixels, (j * pixels) + pixels, (i * pixels) + pixels]
            canvas.create_rectangle(box, fill='white')

    for i in range(row_size):
        for j in range(col_size):
            if (i % 2 != 0 and j % 2 == 0) or (i % 2 == 0 and j % 2 != 0) or (i % 2 != 1 and j % 2 == 1) or (i % 2 == 1 and j % 2 != 1):
                box = [j * pixels, i * pixels, (j * pixels) + pixels, (i * pixels) + pixels]
                canvas.create_rectangle(box, fill='grey')

    for i in range(row_size):
        for j in range(col_size):
            if(sensed[i][j]==1):
                box = [j * pixels, i * pixels, (j * pixels) + pixels, (i * pixels) + pixels]
                canvas.create_rectangle(box, fill='black')

    for a in range(total_nodes ** 2):
        box = [pos_col[int(a / total_nodes)][a % total_nodes] * pixels,
               pos_row[int(a / total_nodes)][a % total_nodes] * pixels,
               (pos_col[int(a / total_nodes)][a % total_nodes] * pixels) + pixels,
               (pos_row[int(a / total_nodes)][a % total_nodes] * pixels) + pixels]
        canvas.create_rectangle(box, fill='red')

    for a in range(total_objects ** 2):
        box = [obj_col[a]* pixels,
               obj_row[a] * pixels,
               (obj_col[a] * pixels) + pixels,
               (obj_row[a] * pixels) + pixels]
        canvas.create_rectangle(box, fill='blue')

    root.update()





def updateNeihgbors():

    for a in range(total_nodes**2):
        for b in range(total_nodes**2):

            if adj_matrix[a][b] == 0 and a != b:

                row_diff = abs(pos_row[int(a / total_nodes)][a % total_nodes] - pos_row[int(b / total_nodes)][b % total_nodes])
                col_diff = abs(pos_col[int(a / total_nodes)][a % total_nodes] - pos_col[int(b / total_nodes)][b % total_nodes])

                if (row_diff == 0 and col_diff <= 2 * rc) or (row_diff == 1 and col_diff <= (2 * rc) - 1) or (row_diff == 2 and col_diff <= (2 * rc) - 2) or (row_diff == 3 and col_diff <= (2 * rc) - 3):
                    adj_matrix[a][b] = 1
                    adj_matrix[b][a] = 1





def checkConnection(row, col, new_row, new_col):

    if row == new_row:
        if nodes_in_pos[row - 3][col - 3] > 0 and nodes_in_pos[row - 3][col - 1] == 0 and nodes_in_pos[row - 3][col + 1] == 0 and nodes_in_pos[row - 3][col + 3] == 0 and nodes_in_pos[row - 2][col - 2] == 0 and nodes_in_pos[row - 2][col] == 0 and nodes_in_pos[row - 2][col + 2] == 0 and nodes_in_pos[row - 1][col - 3] == 0 and nodes_in_pos[row - 1][col - 1] == 0 and nodes_in_pos[row - 1][col + 1] == 0 and nodes_in_pos[row][col - 4] == 0 and nodes_in_pos[row][col - 2] == 0:
            return 0
        else:
            return 1
    else:
        if nodes_in_pos[row][col - 6] > 0 and nodes_in_pos[row - 3][col - 3] == 0 and nodes_in_pos[row - 2][col - 4] == 0 and nodes_in_pos[row - 2][col - 2] == 0 and nodes_in_pos[row - 1][col - 5] == 0 and nodes_in_pos[row - 1][col - 3] == 0 and nodes_in_pos[row - 1][col - 1] == 0 and nodes_in_pos[row][col - 4] == 0 and nodes_in_pos[row][col - 2] == 0 and nodes_in_pos[row + 1][col - 3] == 0 and nodes_in_pos[row + 1][col - 1] == 0 and nodes_in_pos[row + 2][col - 2] == 0:
            return 0
        else:
            return 1





def calculateObject(row,col):

    temp = 0

    if row - 1 >= 0:
        if col - 1 >= 0:
            if objs_cnt[row - 1][col - 1] == 0:
                temp += objs_in_pos[row - 1][col -1]
                objs_cnt[row - 1][col - 1] = 1

        if col + 1 >= 0:
            if objs_cnt[row - 1][col + 1] == 0:
                temp += objs_in_pos[row - 1][col + 1]
                objs_cnt[row - 1][col + 1] = 1

    if row + 1 < row_size:
        if col - 1 >= 0:
            if objs_cnt[row + 1][col - 1] == 0:
                temp += objs_in_pos[row + 1][col - 1]
                objs_cnt[row + 1][col - 1] = 1
        if col + 1 >= 0:
            if objs_cnt[row + 1][col + 1] == 0:
                temp += objs_in_pos[row + 1][col + 1]
                objs_cnt[row + 1][col + 1] = 1

    if row - 2 >= 0:
        if objs_cnt[row - 2][col] == 0:
            temp += objs_in_pos[row - 2][col]
            objs_cnt[row - 2][col] = 1

    if row + 2 < row_size:
        if objs_cnt[row + 2][col] == 0:
            temp += objs_in_pos[row + 2][col]
            objs_cnt[row + 2][col] = 1

    if objs_cnt[row][col] == 0:
        temp += objs_in_pos[row][col]
        objs_cnt[row][col] = 1

    return temp





def calculateYLeftNeighbours(row, col):
    # total weight
    weight = []

    temp1 = 0  # Rc neighbors
    temp2 = 0

    if objs_cnt[row - 1][col - 1] == 0:
        temp2 += objs_in_pos[row - 1][col - 1]
        objs_cnt[row - 1][col - 1] = 1

    if objs_cnt[row + 1][col - 1] == 0:
        temp2 += objs_in_pos[row + 1][col - 1]
        objs_cnt[row + 1][col - 1] = 1

    if col - 1 >= 0:
        if row + 5 < row_size:
            temp1 += nodes_in_pos[row + 5][col - 1]
            if nodes_in_pos[row + 5][col - 1] > 0:
                temp2 += calculateObject(row + 5,col - 1)
        if row + 3 < row_size:
            temp1 += nodes_in_pos[row + 3][col - 1]
            if nodes_in_pos[row + 3][col - 1] > 0:
                temp2 += calculateObject(row + 3,col - 1)
        if row + 1 < row_size:
            temp1 += nodes_in_pos[row + 1][col - 1]
            if nodes_in_pos[row + 1][col - 1] > 0:
                temp2 += calculateObject(row + 1,col - 1)

        if row - 5 >= 0:
            temp1 += nodes_in_pos[row - 5][col - 1]
            if nodes_in_pos[row - 5][col - 1] > 0:
                temp2 += calculateObject(row - 5,col - 1)
        if row - 3 >= 0:
            temp1 += nodes_in_pos[row - 3][col - 1]
            if nodes_in_pos[row - 3][col - 1] > 0:
                temp2 += calculateObject(row - 3,col - 1)
        if row - 1 >= 0:
            temp1 += nodes_in_pos[row - 1][col - 1]
            if nodes_in_pos[row - 1][col - 1] > 0:
                temp2 += calculateObject(row - 1,col - 1)

    if col - 2 >= 0:
        if row + 4 < row_size:
            temp1 += nodes_in_pos[row + 4][col - 2]
            if nodes_in_pos[row + 4][col - 2] > 0:
                temp2 += calculateObject(row + 4,col - 2)
        if row + 2 < row_size:
            temp1 += nodes_in_pos[row + 2][col - 2]
            if nodes_in_pos[row + 2][col - 2] > 0:
                temp2 += calculateObject(row + 2,col - 2)

        if row - 4 >= 0:
            temp1 += nodes_in_pos[row - 4][col - 2]
            if nodes_in_pos[row - 4][col - 2] > 0:
                temp2 += calculateObject(row - 4,col - 2)
        if row - 2 >= 0:
            temp1 += nodes_in_pos[row - 2][col - 2]
            if nodes_in_pos[row - 2][col - 2] > 0:
                temp2 += calculateObject(row - 2,col - 2)

        temp1 += nodes_in_pos[row][col - 2]
        if nodes_in_pos[row][col - 2] > 0:
            temp2 += calculateObject(row, col - 2)

    if col - 3 >= 0:
        if row + 3 < row_size:
            temp1 += nodes_in_pos[row + 3][col - 3]
            if nodes_in_pos[row + 3][col - 3] > 0:
                temp2 += calculateObject(row + 3,col - 3)
        if row + 1 < row_size:
            temp1 += nodes_in_pos[row + 1][col - 3]
            if nodes_in_pos[row + 1][col - 3] > 0:
                temp2 += calculateObject(row + 1,col - 3)

        if row - 3 >= 0:
            temp1 += nodes_in_pos[row - 3][col - 3]
            if nodes_in_pos[row - 3][col - 3] > 0:
                temp2 += calculateObject(row - 3,col - 3)
        if row - 1 >= 0:
            temp1 += nodes_in_pos[row - 1][col - 3]
            if nodes_in_pos[row - 1][col - 3] > 0:
                temp2 += calculateObject(row - 1,col - 3)

    weight.append(temp1)
    weight.append(temp2)

    return weight





def calculateYRightNeighbours(row, col):
    # total weight
    weight = []

    temp1 = 0  # Rc neighbors
    temp2 = 0

    if objs_cnt[row - 1][col + 1] == 0:
        temp2 += objs_in_pos[row - 1][col + 1]
        objs_cnt[row - 1][col + 1] = 1

    if objs_cnt[row + 1][col + 1] == 0:
        temp2 += objs_in_pos[row + 1][col + 1]
        objs_cnt[row + 1][col + 1] = 1

    if col + 1 < col_size:
        if row + 5 < row_size:
            temp1 += nodes_in_pos[row + 5][col + 1]
            if nodes_in_pos[row + 5][col + 1] > 0:
                temp2 += calculateObject(row + 5,col + 1)
        if row + 3 < row_size:
            temp1 += nodes_in_pos[row + 3][col + 1]
            if nodes_in_pos[row + 3][col + 1] > 0:
                temp2 += calculateObject(row + 3,col + 1)
        if row + 1 < row_size:
            temp1 += nodes_in_pos[row + 1][col + 1]
            if nodes_in_pos[row + 1][col + 1] > 0:
                temp2 += calculateObject(row + 1,col + 1)

        if row - 5 >= 0:
            temp1 += nodes_in_pos[row - 5][col + 1]
            if nodes_in_pos[row - 5][col + 1] > 0:
                temp2 += calculateObject(row - 5,col + 1)
        if row - 3 >= 0:
            temp1 += nodes_in_pos[row - 3][col + 1]
            if nodes_in_pos[row - 3][col + 1] > 0:
                temp2 += calculateObject(row - 3,col + 1)
        if row - 1 >= 0:
            temp1 += nodes_in_pos[row - 1][col + 1]
            if nodes_in_pos[row - 1][col + 1] > 0:
                temp2 += calculateObject(row - 1,col + 1)

    if col + 2 < col_size:
        if row + 4 < row_size:
            temp1 += nodes_in_pos[row + 4][col + 2]
            if nodes_in_pos[row + 4][col + 2] > 0:
                temp2 += calculateObject(row + 4,col + 2)
        if row + 2 < row_size:
            temp1 += nodes_in_pos[row + 2][col + 2]
            if nodes_in_pos[row + 2][col + 2] > 0:
                temp2 += calculateObject(row + 2,col + 2)

        if row - 4 >= 0:
            temp1 += nodes_in_pos[row - 4][col + 2]
            if nodes_in_pos[row - 4][col + 2] > 0:
                temp2 += calculateObject(row - 4,col + 2)
        if row - 2 >= 0:
            temp1 += nodes_in_pos[row - 2][col + 2]
            if nodes_in_pos[row - 2][col + 2] > 0:
                temp2 += calculateObject(row - 2,col + 2)

        temp1 += nodes_in_pos[row][col + 2]
        if nodes_in_pos[row][col + 2] > 0:
            temp2 += calculateObject(row,col + 2)

    if col + 3 < col_size:
        if row + 3 < row_size:
            temp1 += nodes_in_pos[row + 3][col + 3]
            if nodes_in_pos[row + 3][col + 3] > 0:
                temp2 += calculateObject(row + 3,col + 3)
        if row + 1 < row_size:
            temp1 += nodes_in_pos[row + 1][col + 3]
            if nodes_in_pos[row + 1][col + 3] > 0:
                temp2 += calculateObject(row + 1,col + 3)

        if row - 3 >= 0:
            temp1 += nodes_in_pos[row - 3][col + 3]
            if nodes_in_pos[row - 3][col + 3] > 0:
                temp2 += calculateObject(row - 3,col + 3)
        if row - 1 >= 0:
            temp1 += nodes_in_pos[row - 1][col + 3]
            if nodes_in_pos[row - 1][col + 3] > 0:
                temp2 += calculateObject(row - 1,col + 3)

    weight.append(temp1)
    weight.append(temp2)

    return weight





def calculateXLeftNeighbours(row, col):
    # total weight
    weight = []

    temp1 = 0  # Rc neighbors
    temp2 = 0

    if objs_cnt[row - 1][col + 1] == 0:
        temp2 += objs_in_pos[row - 1][col + 1]
        objs_cnt[row - 1][col + 1] = 1

    if objs_cnt[row - 1][col - 1] == 0:
        temp2 += objs_in_pos[row - 1][col - 1]
        objs_cnt[row - 1][col - 1] = 1

    if objs_cnt[row - 2][col] == 0:
        temp2 += objs_in_pos[row - 2][col]
        objs_cnt[row - 2][col] = 1

    if row - 1 >= 0:
        if col - 3 >= 0:
            temp1 += nodes_in_pos[row - 1][col - 3]
            if nodes_in_pos[row - 1][col - 3] > 0:
                temp2 += calculateObject(row - 1,col - 3)
        if col - 1 >= 0:
            temp1 += nodes_in_pos[row - 1][col - 1]
            if nodes_in_pos[row - 1][col - 1] > 0:
                temp2 += calculateObject(row - 1,col - 1)

        if col + 3 < col_size:
            temp1 += nodes_in_pos[row - 1][col + 3]
            if nodes_in_pos[row - 1][col + 3] > 0:
                temp2 += calculateObject(row - 1,col + 3)
        if col + 1 < col_size:
            temp1 += nodes_in_pos[row - 1][col + 1]
            if nodes_in_pos[row - 1][col + 1] > 0:
                temp2 += calculateObject(row - 1,col + 1)

    if row - 2 >= 0:
        if col - 2 >= 0:
            temp1 += nodes_in_pos[row - 2][col - 2]
            if nodes_in_pos[row - 2][col - 2] > 0:
                temp2 += calculateObject(row - 2,col - 2)

        if col + 2 < col_size:
            temp1 += nodes_in_pos[row - 2][col + 2]
            if nodes_in_pos[row - 2][col + 2] > 0:
                temp2 += calculateObject(row - 2,col + 2)

        temp1 += nodes_in_pos[row - 2][col]
        if nodes_in_pos[row - 2][col] > 0:
            temp2 += calculateObject(row - 2, col)

    if row - 3 >= 0:
        if col - 3 >= 0:
            temp1 += nodes_in_pos[row - 3][col - 3]
            if nodes_in_pos[row - 3][col - 3] > 0:
                temp2 += calculateObject(row - 3,col - 3)
        if col - 1 >= 0:
            temp1 += nodes_in_pos[row - 3][col - 1]
            if nodes_in_pos[row - 3][col - 1] > 0:
                temp2 += calculateObject(row - 3,col - 1)

        if col + 3 < col_size:
            temp1 += nodes_in_pos[row - 3][col + 3]
            if nodes_in_pos[row - 3][col + 3] > 0:
                temp2 += calculateObject(row - 3,col + 3)
        if col + 1 < col_size:
            temp1 += nodes_in_pos[row - 3][col + 1]
            if nodes_in_pos[row - 3][col + 1] > 0:
                temp2 += calculateObject(row - 3,col + 1)

    if row - 4 >= 0:
        if col - 2 >= 0:
            temp1 += nodes_in_pos[row - 4][col - 2]
            if nodes_in_pos[row - 4][col - 2] > 0:
                temp2 += calculateObject(row - 4,col - 2)

        if col + 2 < col_size:
            temp1 += nodes_in_pos[row - 4][col + 2]
            if nodes_in_pos[row - 4][col + 2] > 0:
                temp2 += calculateObject(row - 4,col + 2)

        temp1 += nodes_in_pos[row - 4][col]
        if nodes_in_pos[row - 4][col] > 0:
            temp2 += calculateObject(row - 4, col)

    if row - 5 >= 0:
        if col - 1 >= 0:
            temp1 += nodes_in_pos[row - 5][col - 1]
            if nodes_in_pos[row - 5][col - 1] > 0:
                temp2 += calculateObject(row - 5,col - 1)

        if col + 1 < col_size:
            temp1 += nodes_in_pos[row - 5][col + 1]
            if nodes_in_pos[row - 5][col + 1] > 0:
                temp2 += calculateObject(row - 5,col + 1)

    if row - 6 >= 0:
        temp1 += nodes_in_pos[row - 6][col]
        if nodes_in_pos[row - 6][col] > 0:
            temp2 += calculateObject(row - 6, col)

    weight.append(temp1)
    weight.append(temp2)

    return weight





def calculateXRightNeighbours(row, col):
    # total weight
    weight = []

    temp1 = 0  # Rc neighbors
    temp2 = 0

    if objs_cnt[row + 1][col + 1] == 0:
        temp2 += objs_in_pos[row + 1][col + 1]
        objs_cnt[row + 1][col + 1] = 1

    if objs_cnt[row + 1][col - 1] == 0:
        temp2 += objs_in_pos[row + 1][col - 1]
        objs_cnt[row + 1][col - 1] = 1

    if objs_cnt[row + 2][col] == 0:
        temp2 += objs_in_pos[row + 2][col]
        objs_cnt[row + 2][col] = 1

    if row + 1 < row_size:
        if col - 3 >= 0:
            temp1 += nodes_in_pos[row + 1][col - 3]
            if nodes_in_pos[row + 1][col - 3] > 0:
                temp2 += calculateObject(row + 1,col - 3)
        if col - 1 >= 0:
            temp1 += nodes_in_pos[row + 1][col - 1]
            if nodes_in_pos[row + 1][col - 1] > 0:
                temp2 += calculateObject(row + 1,col - 1)

        if col + 3 < col_size:
            temp1 += nodes_in_pos[row + 1][col + 3]
            if nodes_in_pos[row + 1][col + 3] > 0:
                temp2 += calculateObject(row + 1,col + 3)
        if col + 1 < col_size:
            temp1 += nodes_in_pos[row + 1][col + 1]
            if nodes_in_pos[row + 1][col + 1] > 0:
                temp2 += calculateObject(row + 1,col + 1)

    if row + 2 < row_size:
        if col - 2 >= 0:
            temp1 += nodes_in_pos[row + 2][col - 2]
            if nodes_in_pos[row + 2][col - 2] > 0:
                temp2 += calculateObject(row + 2,col - 2)

        if col + 2 < col_size:
            temp1 += nodes_in_pos[row + 2][col + 2]
            if nodes_in_pos[row + 2][col + 2] > 0:
                temp2 += calculateObject(row + 2,col + 2)

        temp1 += nodes_in_pos[row + 2][col]
        if nodes_in_pos[row + 2][col] > 0:
            temp2 += calculateObject(row + 2, col)

    if row + 3 < row_size:
        if col - 3 >= 0:
            temp1 += nodes_in_pos[row + 3][col - 3]
            if nodes_in_pos[row + 3][col - 3] > 0:
                temp2 += calculateObject(row + 3,col - 3)
        if col - 1 >= 0:
            temp1 += nodes_in_pos[row + 3][col - 1]
            if nodes_in_pos[row + 3][col - 1] > 0:
                temp2 += calculateObject(row + 3,col - 1)

        if col + 3 < col_size:
            temp1 += nodes_in_pos[row + 3][col + 3]
            if nodes_in_pos[row + 3][col + 3] > 0:
                temp2 += calculateObject(row + 3,col + 3)
        if col + 1 < col_size:
            temp1 += nodes_in_pos[row + 3][col + 1]
            if nodes_in_pos[row + 3][col + 1] > 0:
                temp2 += calculateObject(row + 3,col + 1)

    if row + 4 < row_size:
        if col - 2 >= 0:
            temp1 += nodes_in_pos[row + 4][col - 2]
            if nodes_in_pos[row + 4][col - 2] > 0:
                temp2 += calculateObject(row + 4,col - 2)

        if col + 2 < col_size:
            temp1 += nodes_in_pos[row + 4][col + 2]
            if nodes_in_pos[row + 4][col + 2] > 0:
                temp2 += calculateObject(row + 4,col + 2)

        temp1 += nodes_in_pos[row + 4][col]
        if nodes_in_pos[row + 4][col] > 0:
            temp2 += calculateObject(row + 4, col)

    if row + 5 < row_size:
        if col - 1 >= 0:
            temp1 += nodes_in_pos[row + 5][col - 1]
            if nodes_in_pos[row + 5][col - 1] > 0:
                temp2 += calculateObject(row + 5,col - 1)

        if col + 1 < col_size:
            temp1 += nodes_in_pos[row + 5][col + 1]
            if nodes_in_pos[row + 5][col + 1] > 0:
                temp2 += calculateObject(row + 5,col + 1)

    if row + 6 < row_size:
        temp1 += nodes_in_pos[row + 6][col]
        if nodes_in_pos[row + 6][col] > 0:
            temp2 += calculateObject(row + 6, col)

    weight.append(temp1)
    weight.append(temp2)

    return weight





node_move = 1
time_step = 1

while 1:
    draw(5)
    new_time=time.time()

    node_move = 0
    if time_step > 2000:
        break

    time_step += 1

    # Calculate the direction each node wants to move and number of nodes moving in a certain direction                 joss
    for i in range(total_nodes):
        for j in range(total_nodes):

            for x in range(row_size):
                for y in range(col_size):
                    objs_cnt[x][y] = 0
            weightX_left[i][j] = calculateXLeftNeighbours(pos_row[i][j], pos_col[i][j])
            weightX_right[i][j] = calculateXRightNeighbours(pos_row[i][j], pos_col[i][j])

            for x in range(row_size):
                for y in range(col_size):
                    objs_cnt[x][y] = 0
            weightY_left[i][j] = calculateYLeftNeighbours(pos_row[i][j], pos_col[i][j])
            weightY_right[i][j] = calculateYRightNeighbours(pos_row[i][j], pos_col[i][j])

            #Calculate col_moves for no object in both side
            if weightY_left[i][j][1] == 0 and weightY_right[i][j][1] == 0:
                col_move = weightY_right[i][j][0] - weightY_left[i][j][0]

            # Calculate row_moves for no object in both side
            if weightX_left[i][j][1] == 0 and weightX_right[i][j][1] == 0:
                row_move = weightX_right[i][j][0] - weightX_left[i][j][0]

            # Calculate col_moves for no object in one side
            if weightY_left[i][j][1] == 0 and weightY_right[i][j][1] >= 1:
                col_move = -1
            if weightY_left[i][j][1] >= 1 and weightY_right[i][j][1] == 0:
                col_move = 1

            # Calculate row_moves for no object in one side
            if weightX_left[i][j][1] == 0 and weightX_right[i][j][1] >= 1:
                row_move = -1
            if weightX_left[i][j][1] >= 1 and weightX_right[i][j][1] == 0:
                row_move = 1

            #Calculate col_moves for at least one object in both side
            if weightY_left[i][j][1] >= 1 and weightY_right[i][j][1] >= 1:
                ratioYleft = weightY_left[i][j][0]/weightY_left[i][j][1]
                ratioYright = weightY_right[i][j][0]/weightY_right[i][j][1]
                col_move = ratioYright - ratioYleft

            # Calculate row_moves for at least one object in both side
            if weightX_left[i][j][1] >= 1 and weightX_right[i][j][1] >= 1:
                ratioXleft = weightX_left[i][j][0] / weightX_left[i][j][1]
                ratioXright = weightX_right[i][j][0] / weightX_right[i][j][1]
                row_move = ratioXright - ratioXleft

            # Calculate sx
            if col_move == 0:
                sx[i][j] = 0
            elif col_move > 0:
                sx[i][j] = -1
            else:
                sx[i][j] = 1

            # Calculate sy
            if row_move == 0:
                sy[i][j] = 0
            elif row_move > 0:
                sy[i][j] = 1
            else:
                sy[i][j] = -1


    # Calculate actual movement                                                                                         joss
    for i in range(total_nodes):
        for j in range(total_nodes):

            # Move the nodes                                                                                            joss
            if sx[i][j] == 0 and sy[i][j] == 1:
                new_pos_row[i][j] -= 2
                node_move = 1
                movement[i][j] += 1

            elif sx[i][j] == 0 and sy[i][j] == -1:
                new_pos_row[i][j] += 2
                node_move = 1
                movement[i][j] += 1

            elif sx[i][j] == 1 and sy[i][j] == 0:
                new_pos_col[i][j] += 1
                new_pos_row[i][j] += 1
                node_move = 1
                movement[i][j] += 1

            elif sx[i][j] == -1 and sy[i][j] == 0:
                new_pos_col[i][j] -= 1
                new_pos_row[i][j] -= 1
                node_move = 1
                movement[i][j] += 1

            elif sx[i][j] == 1 and sy[i][j] == 1:
                new_pos_row[i][j] -= 1
                new_pos_col[i][j] += 1
                node_move = 1
                movement[i][j] += 1

            elif sx[i][j] == 1 and sy[i][j] == -1:
                new_pos_row[i][j] += 1
                new_pos_col[i][j] += 1
                node_move = 1
                movement[i][j] += 1

            elif sx[i][j] == -1 and sy[i][j] == 1:
                new_pos_row[i][j] -= 1
                new_pos_col[i][j] -= 1
                node_move = 1
                movement[i][j] += 1

            elif sx[i][j] == -1 and sy[i][j] == -1:
                new_pos_row[i][j] += 1
                new_pos_col[i][j] -= 1
                node_move = 1
                movement[i][j] += 1

            if  new_nodes_in_pos[new_pos_row[i][j]][new_pos_col[i][j]] > 0:
                new_pos_row[i][j] = pos_row[i][j]
                new_pos_col[i][j] = pos_col[i][j]
                node_move = 0
                movement[i][j] -= 1

            else:
                new_nodes_in_pos[new_pos_row[i][j]][new_pos_col[i][j]] += 1
                new_nodes_in_pos[pos_row[i][j]][pos_col[i][j]] -= 1


    for x in range(total_objects**2):
        probability = random.randint(1,12)

        print(probability)

        if probability == 1:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] -= 2
            obj_col[x] -= 2
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 2:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] -= 3
            obj_col[x] -= 1
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 3:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] -= 4
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 4:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] -= 3
            obj_col[x] += 1
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 5:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] -= 2
            obj_col[x] += 2
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 6:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] += 2
            obj_col[x] += 2
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 7:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] += 3
            obj_col[x] += 1
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 8:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] += 4
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 9:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] += 3
            obj_col[x] -= 1
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 10:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_row[x] += 2
            obj_col[x] -= 2
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 11:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_col[x] += 2
            objs_in_pos[obj_row[x]][obj_col[x]] += 1

        if probability == 12:
            objs_in_pos[obj_row[x]][obj_col[x]] -= 1
            obj_col[x] -= 2
            objs_in_pos[obj_row[x]][obj_col[x]] += 1


    pos_row = [t[:] for t in new_pos_row]
    pos_col = [t[:] for t in new_pos_col]
    nodes_in_pos = [t[:] for t in new_nodes_in_pos]

updateNeihgbors()