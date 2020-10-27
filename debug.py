from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys
import itertools
import numpy as np

import sys



columns = []
grid = []

num_of_rows = 3
num_of_columns = 4
'''
#creates the matrix
for x in range(0, num_of_rows): # 3 rows by 4 columns
    for y in range(0, num_of_columns): 
        columns.append((x, y))
    grid.append(columns.copy())
    columns = []

#prints the grid in the matrix format
for x in range(0, len(grid)):
    print(grid[x])
    
'''

def string_to_wall_coord(string: str):
        x = int(string[0])
        y = int(string[2])
        tup = (x, y)
        return tup

def get_wall_pos(l,index):
        pos = ( )
        for _ in range(len(l)):
            pos = string_to_wall_coord(l[index])
        return pos


def wall_coordinate_list(walls):
        i = 0 
        h = [ ]
        while i < len(walls) :
            h.append(get_wall_pos(walls,i))
            i+=1
        return h
def get_wall_direction(string: str):
        direction = string[4]
        return direction

def boundary(l, size, rd):
    #esquerda
    if rd == 'l':
        if (l[1] == 0):
            l[1] = l[1]+1
        if (l[1] == -1):
            l[1] = l[1]+2
        if (l[1] == -2):
            l[1] = l[1]+3
    #direita
    if rd == 'r':
        if (l[1] == size+1):
            l[1] = l[1]-1
        if (l[1] == size+2):
            l[1] = l[1]-2
        if (l[1] == size+3):
            l[1] = l[1]-3
    #cima
    if rd == 'u':
        if (l[0] == 0):
            l[0] = l[0]+1
        if (l[0] == -1):
            l[0] = l[0]+2
        if (l[0] == -2):
            l[0] = l[0]+3
    #baixo
    if rd == 'd':
        if (l[0] == size+1):
            l[0] = l[0]-1
        if (l[0] == size+2):
            l[0] = l[0]-2
        if (l[0] == size+3):
            l[0] = l[0]-3
    else:
        return l
    

    
def move_1_square(pos, direction):
        new_move = ( )
        l = list(pos)
        if direction == 'l':
            l[1] = l[1]-1
            new_move = tuple(l)
        elif direction == 'r':
            l[1] = l[1]+1
            new_move = tuple(l)
        elif direction == 'u':
            l[0] = l[0]-1
            new_move = tuple(l)
        elif direction == 'd':
            l[0] = l[0]+1 
            new_move = tuple(l)
    
        return new_move
'''

size = 5
l_test_pos = (2,1)
r_test_pos = (1,5)
u_test_pos = (3,2)
d_test_pos = (4,2)
walls = ['3 1 r', '3 2 r', '4 4 r', '1 3 d']


robot_pos_list = [l_test_pos, r_test_pos, u_test_pos, d_test_pos]



string = 'Y 4 2'
tup = (4, 1)
v1,v2 = str(tup[0]), str(tup[1])

new_string = 'Y ' + v1 + ' ' + v2



wall_pos_list = wall_coordinate_list(walls)
def wall_bump(l, wall_pos_list, rob_direction, walls):
    isWall = 0
    wall_direction = ' '
    tup_input = tuple(l)
    l_tup = (tup_input[0], tup_input[1]-1)
    r_tup = (tup_input[0], tup_input[1]+1)
    u_tup = (tup_input[0]-1, tup_input[1])
    d_tup = (tup_input[0]+1, tup_input[1])
    
    for i in range(len(wall_pos_list)):
        if wall_pos_list[i] == tup_input:
            wall_direction = get_wall_direction(walls[i])
        if wall_pos_list[i] == l_tup:
            wall_direction = get_wall_direction(walls[i])
        if wall_pos_list[i] == r_tup:
            wall_direction = get_wall_direction(walls[i])
        if wall_pos_list[i] == u_tup:
            wall_direction = get_wall_direction(walls[i])
        if wall_pos_list[i] == d_tup:
            wall_direction = get_wall_direction(walls[i])

    print(wall_direction)
    if rob_direction == 'l':
        if tup_input in wall_pos_list:
            if wall_direction == 'l':
                
                isWall = 1
            else:
                isWall = 0
        if l_tup in wall_pos_list:
            if wall_direction == 'r':
                isWall = 1 
            else:
                isWall = 0
    
    if rob_direction == 'r':
        if tup_input in wall_pos_list:
            if wall_direction == 'r':
                isWall = 1
            else:
                isWall = 0
        if r_tup in wall_pos_list:
            if wall_direction == 'l':
                isWall = 1 
            else:
                isWall = 0
    
    if rob_direction == 'u':
        if tup_input in wall_pos_list:
            if wall_direction == 'u':
                isWall = 1
            else:
                isWall = 0
        if u_tup in wall_pos_list:
            if wall_direction == 'd':
                isWall = 1 
            else:
                isWall = 0
    
    if rob_direction == 'd':
        if tup_input in wall_pos_list:
            if wall_direction == 'd':
                isWall = 1
            else:
                isWall = 0
        if d_tup in wall_pos_list:
            if wall_direction == 'u':
                isWall = 1 
            else:
                isWall = 0
    
    if isWall == 1:
        l = l
        return True
    
    return False


def robot_bump(l, robot_pos_list, rob_direction):
    tup_input = tuple(l)
    l_tup = (tup_input[0], tup_input[1]-1)
    r_tup = (tup_input[0], tup_input[1]+1)
    u_tup = (tup_input[0]-1, tup_input[1])
    d_tup = (tup_input[0]+1, tup_input[1])
    isRobot = 0
    
    if rob_direction == 'l':
        if l_tup in robot_pos_list:
            isRobot = 1
    if rob_direction == 'r':
        if r_tup in robot_pos_list:
            isRobot = 1
    if rob_direction == 'u':
        if u_tup in robot_pos_list:
            isRobot = 1   
    if rob_direction == 'd':
        if d_tup in robot_pos_list:
            i
    if isRobot == 1:
        return True
    return False

def final_movement(size, l, wall_pos_list, robot_pos_list, rob_direction, walls):
    l_aux = l 

    for _ in range(0, size-1):
        if wall_bump(l_aux, wall_pos_list, rob_direction, walls) == False:
            print("parede")
            if robot_bump(l_aux, robot_pos_list, rob_direction) == False:
                print("robot")
                if rob_direction == 'l':
                    l_aux[1] = l_aux[1]-1 
                    if boundary(l_aux, size, rob_direction) == l_aux:
                        l = l_aux
                       
                    else:
                        l = boundary(l_aux, size, rob_direction)
                        
                if rob_direction == 'r':
                    l_aux[1] = l_aux[1]+1 
                    if boundary(l_aux, size, rob_direction) == l_aux:
                        l = l_aux
                    else:
                        l = boundary(l_aux, size, rob_direction)
                if rob_direction == 'u':
                    l_aux[0] = l_aux[0]-1 
                    if boundary(l_aux, size, rob_direction) == l_aux:
                        l = l_aux
                    else:
                        l = boundary(l_aux, size, rob_direction)
                if rob_direction == 'd':
                    l_aux[0] = l_aux[0]+1 
                    print("l_aux.->", l_aux)
                    if boundary(l_aux, size, rob_direction) == l_aux:
                        l = l_aux
                    else:
                        l = boundary(l_aux, size, rob_direction)
            else:
                l = l_aux
        else:
            l = l_aux

    return l
           

    

n = wall_bump([3,2], wall_pos_list, 'l', walls)
print("------wall bump----")
print(n)

h = robot_bump([1,4], robot_pos_list, 'd')
print("------robot bump----")
print(h)
'''
'''
#print("\n\n\n")

y = final_movement(size, [1,4], wall_pos_list, robot_pos_list, 'd', walls)
print("----final move----")
print(y)
#tup = move_robot((4,4), 'l', wall_pos_list, walls, size, robot_pos_list)
 d = ' '
        j = 0
        for i in range(len(wall_pos_lst)):
            if wall_pos_lst[i] == pos:
                
                d = get_wall_direction(walls[i])
    
            if d == 'l':
                a_array.remove((color, 'l'))
            if d == 'r':
                a_array.remove((color, 'r'))
            if d == 'u':
                a_array.remove((color, 'u'))
            if d == 'd':
                a_array.remove((color, 'd'))

            if wall_pos_lst[i] == move_1_square(pos,'r'):
                if get_wall_direction(walls[i]) == 'l':
                    a_array.remove((color, 'r'))
            if wall_pos_lst[i] == move_1_square(pos,'l'):
                if get_wall_direction(walls[i]) == 'r':
                    a_array.remove((color, 'l'))
            if wall_pos_lst[i] == move_1_square(pos,'u'):
                if get_wall_direction(walls[i]) == 'd':
                    a_array.remove((color, 'u'))
            if wall_pos_lst[i] == move_1_square(pos,'d'):
                if get_wall_direction(walls[i]) == 'u':
                    a_array.remove((color, 'd')) 
        print("JOAT-->",j)
'''

#new = move_robot((2,2), 'u', wall_pos_list, walls, size,  robot_pos_list)
#move_robot((4,4), 'l', wall_pos_list, walls, size,  robot_pos_list)
#moves_against_wall([4,4], wall_pos_list, 'l')

actions = [('Y','l'), ('Y','r'), ('Y','u'), ('Y','d'), ('G','l'), ('G','r'), ('G','u'), ('G','d'), ('B','l'), ('B','r'), ('B','u'), ('B','d'), ('R','l'), ('R','r'), ('R','u'), ('R','d')]
walls = ['1 1 d', '1 3 d', '1 4 d', '1 7 d', '2 2 d', '2 5 d', '2 7 d', '3 1 d', '3 2 d', '3 5 d', '3 6 d', '4 3 d', '4 5 d', '5 3 d', '5 4 d', '5 5 d', '5 6 d', '5 7 d', '6 3 d', '6 7 d', '1 1 r', '1 2 r', '1 5 r', '1 6 r', '2 1 r', '2 2 r', '2 3 r', '2 5 r', '3 2 r', '3 4 r', '3 6 r', '4 5 r', '5 1 r', '5 2 r', '5 4 r', '5 6 r', '6 1 r', '6 5 r', '7 2 r', '7 3 r', '7 6 r']
wall_pos_list = wall_coordinate_list(walls)
size = 7
y_pos = (4,5)
g_pos = (4,6)
b_pos = (4,1)
r_pos = (6,4)


def test(pos):
    lst = []
    wall_pos_c = 0

    for i in range(len(wall_pos_list)):
        if y_pos == wall_pos_list[i]:
            wall_pos_c+=1
            lst.append(i)
    
    return lst


def not_removed(color, direction, lst):
    return (color,direction) in lst




#def wall_collision(wall_pos_lst, pos, walls, color, actions):
pos = y_pos
l_tup = (pos[0], pos[1]-1)
r_tup = (pos[0], pos[1]+1)
u_tup = (pos[0]-1, pos[1])
d_tup = (pos[0]+1, pos[1]) 
curr_lst = []
l_lst = []
r_lst = []
u_lst = []
d_lst = []
wall_direction = ''
isWall = 0
color = 'Y'
for i in range(len(wall_pos_list)):
    if wall_pos_list[i] == pos:
        d = get_wall_direction(walls[i])
        print(d)



for i in range(len(wall_pos_list)):
    if pos == wall_pos_list[i]:
        curr_lst.append(i)
        isWall = 1
    if l_tup == wall_pos_list[i]:
        l_lst.append(i)
        isWall = -1 
    if r_tup == wall_pos_list[i]:
        r_lst.append(i)
        isWall = -1 
    if u_tup == wall_pos_list[i]:
        u_lst.append(i)
        isWall = -1 
    if d_tup == wall_pos_list[i]:
        d_lst.append(i)
        isWall = -1 

#verifica todas as paredes da posicao
if isWall == 1:
    for i in range(len(curr_lst)):
        j = curr_lst[i]
        wall_direction = get_wall_direction(walls[j])
        if wall_direction == 'r':
            if not_removed(color,'r',actions):
                actions.remove((color, 'r'))
        elif wall_direction == 'l':
            if not_removed(color,'l',actions):
                actions.remove((color, 'l'))
        elif wall_direction == 'u':
            if not_removed(color,'u',actions):
                actions.remove((color, 'u'))
        elif wall_direction == 'd':
            if not_removed(color,'d',actions):
                actions.remove((color, 'd'))

#if isWall == -1:
    
print(wall_pos_list)