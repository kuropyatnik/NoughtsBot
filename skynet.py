import numpy as np
import random
#Checker for same elements in winning combination
def is_same(data):
    return all(x == data[0] for x in data)
#Make row from column
def column(list, pos):
    return [row[pos] for row in list]
#Win-checking method
def is_win(f):
    #Rows checking
    for i in range(len(f)):
        if (is_same(f[i]) and f[i][0]!='-'):
            # print("Game Over! Winner: ", field[i][0])
            return (True, f[i][0])

    #Column checking
    for i in range(len(f[0])):
        if (is_same(column(f, i)) and column(f, i)[0]!='-'):
            # print("Game Over! Winner: ", column(field, i)[0])
            return (True, column(f, i)[0])

    #Main diagonal
    if (is_same(np.diagonal(f)) and np.diagonal(f)[0]!='-'):
        # print("Game Over! Winner: ", np.diagonal(field)[0])
        return (True, np.diagonal(f)[0])

    #Collateral diagonal
    if (is_same(np.fliplr(f).diagonal()) and np.fliplr(f).diagonal()[0]!='-'):
        # print("Game Over! Winner: ", np.fliplr(field).diagonal()[0])
        return (True, np.fliplr(f).diagonal()[0])

    #print("Nope!")
    return (False, "")
#Find empty cell
def empty_indices(f):
    empty = []
    for i in range(len(f)):
        for j in range(len(f[i])):
            if (f[i][j] == '-'):
                empty.append([i, j])
    return empty
#Minimax function for finding best cell
def minimax (f, curr_pl, c, h):
    answer = []
    score = 0
    #looking for empty cell
    emp_ind = empty_indices(f)
    #Rating position
    res = is_win(f)
    if (res[0] and res[1] == h):
        score = -10
        return ([answer, score])
    elif (res[0] and res[1] == c):
        score = 10
        return ([answer, score])
    elif (len(emp_ind) == 0):
        score = 0
        return ([answer, score])

    cells = [] #Values of each cell in current situation
    #Recursionally calling minimax for all varitations
    for i in range (len(emp_ind)):
        cell = [emp_ind[i], 0]
        f[emp_ind[i][0]][emp_ind[i][1]] = curr_pl
        if (curr_pl == c):
            sub_res = minimax(f, h, c, h)
            cell[1] = sub_res[1]
        else:
            sub_res = minimax(f, c, c, h)
            cell[1] = sub_res[1]

        f[cell[0][0]][cell[0][1]] = '-'
        cells.append(cell)

    #Find the best cell from all
    index = 0 #Position of best cell in list
    if (curr_pl == c):
        max_score = -100000
        for i in range(len(cells)):
            if (cells[i][1] > max_score):
                max_score = cells[i][1]
                index = i
    else:
        min_score = 100000
        for i in range(len(cells)):
            if (cells[i][1] < min_score):
                min_score = cells[i][1]
                index = i

    return cells[index]
# Random pick
def jun(f, c):
    crds = random.choice(empty_indices(f))
    f[crds[0]][crds[1]] = c
# Minimax pick
def sen(f, cpt, side, counter):
    if (counter == 0):
        f[1][1] = cpt
    else:
        crds = minimax(f, cpt, cpt, side)
        f[crds[0][0]][crds[0][1]] = cpt