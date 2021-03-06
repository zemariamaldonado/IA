from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys
import itertools
import numpy as np

import sys



    
class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id


class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    

    def __init__(self, size, r1, r2, r3, r4, target, wall_num, walls):
        self.size = size
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4
        self.target = target
        self.wall_num = wall_num
        self.walls = walls


    def get_initial_robot(self, string):
        starting_color = self.get_robot_color(string)
        #print(starting_color)
        #print()
        if self.get_robot_color(self.r1) == starting_color:
            return self.r1
        elif self.get_robot_color(self.r2) == starting_color:
            return self.r2
        elif self.get_robot_color(self.r3) == starting_color:
            return self.r3
        elif self.get_robot_color(self.r4) == starting_color:
            return self.r4

    def get_robot_color(self, string):
        color = string[0]
        return color
    
    def string_to_robot_coord(self, string: str):
        #print(">>>>>>",string)
        x = int(string[2])
        y = int(string[4])
        tup = (x, y)
        return tup
    
    def string_to_wall_coord(self, string: str):
        x = int(string[0])
        y = int(string[2])
        tup = (x, y)
        return tup
    
    def get_wall_direction(self, string: str):
        direction = string[4]
        return direction
    
    def get_wall_pos(self,l,index):
        pos = ( )
        for _ in range(len(l)):
            pos = self.string_to_wall_coord(l[index])
        return pos

    def wall_coordinate_list(self,walls):
        i = 0 
        h = [ ]
        while i < len(walls) :
            h.append(self.get_wall_pos(walls,i))
            i+=1
        return h

    def aux_pos(self, string):
        r1_pos = self.r1
        r2_pos = self.r2
        r3_pos = self.r3
        r4_pos = self.r4
       
        if self.get_robot_color(r1_pos) == string:
            r1_pos = self.string_to_robot_coord(r1_pos)
            return r1_pos
        if self.get_robot_color(r2_pos) == string:
            r2_pos = self.string_to_robot_coord(r2_pos)
            return r2_pos
        if self.get_robot_color(r3_pos) == string:
            r3_pos = self.string_to_robot_coord(r3_pos)
            return r3_pos
        if self.get_robot_color(r4_pos) == string:
            r4_pos = self.string_to_robot_coord(r4_pos)
            return r4_pos
            
    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        # TODO
        if robot == 'Y' or robot == 'G' or robot == 'B' or robot == 'R':
            res = self.aux_pos(robot)
            return res

    
def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    #mudar para sys.argv[1]
    with open (filename,'r') as f:
        lines = f.read().splitlines()

    size = lines[0]
    r1 = lines[1]
    r2 = lines[2]
    r3 = lines[3]
    r4 = lines[4]
    target = lines[5]
    wall_num = lines[6]

    def n_wall_pos():
        number = int(wall_num) 
        i = 0
        index = 7
        w_pos = [ ]
    
        while i < number:
            w_pos.append(lines[index])
            index+=1
            i+=1
        return w_pos

    walls = n_wall_pos()

    return Board(size, r1, r2, r3, r4, target, wall_num, walls )
    
class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = RRState(board)
        
    def boundary_collision(self,pos, size, a_array, color):
        left = (color, 'l')
        right = (color, 'r')
        up = (color, 'u')
        down = (color, 'd')
        if pos[0] == 1:
            if up in a_array:
                a_array.remove((color, 'u'))
        elif pos[0] == size:
            if down in a_array:
                a_array.remove((color, 'd'))
        
        if pos[1] == 1:
            if left in a_array:
                a_array.remove((color, 'l'))
        elif pos[1] == size:
            if right in a_array:
                a_array.remove((color, 'r'))

    def wall_collision(self, wall_pos_lst, pos, walls, color, a_array):
        d = ' '
        left = (color, 'l')
        right = (color, 'r')
        up = (color, 'u')
        down = (color, 'd')
        for i in range(len(wall_pos_lst)):
            if wall_pos_lst[i] == pos:
                d = self.initial.board.get_wall_direction(walls[i])
                
            if d == 'l':
                if left in a_array:
                    a_array.remove(left)
            elif d == 'r':
                if right in a_array:
                    a_array.remove(right)
            elif d == 'u':
                if up in a_array:
                    a_array.remove(up)
            elif d == 'd':
                if down in a_array:
                    a_array.remove(down)
        
        for j in range(len(wall_pos_lst)):
            if wall_pos_lst[j] == self.move_1_square(pos,'r'):
                if self.initial.board.get_wall_direction(walls[j]) == 'l':
                    if right in a_array:
                        a_array.remove(right)
            if wall_pos_lst[j] == self.move_1_square(pos,'l'):
                if self.initial.board.get_wall_direction(walls[j]) == 'r':
                    if left in a_array:
                        a_array.remove(left)
            if wall_pos_lst[j] == self.move_1_square(pos,'u'):
                if self.initial.board.get_wall_direction(walls[j]) == 'd':
                    if up in a_array:
                        a_array.remove(up)
            if wall_pos_lst[j] == self.move_1_square(pos,'d'):
                if self.initial.board.get_wall_direction(walls[j]) == 'u':
                    if down in a_array:
                        a_array.remove(down) 
        

    def robot_collisions(self, robot_pos_lst, pos, color, a_array):
        left = (color, 'l')
        right = (color, 'r')
        up = (color, 'u')
        down = (color, 'd')

        for i in range(len(robot_pos_lst)):
            if robot_pos_lst[i] == self.move_1_square(pos,'l'):
                if left in a_array:
                    a_array.remove(left)
            if robot_pos_lst[i] == self.move_1_square(pos,'r'):
                if right in a_array:
                    a_array.remove(right)
            if robot_pos_lst[i] == self.move_1_square(pos,'u'):
                if up in a_array:
                    a_array.remove(up)
            if robot_pos_lst[i] == self.move_1_square(pos,'d'):
                if down in a_array:    
                    a_array.remove(down)

    def move_1_square(self, pos, direction):
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
     
    
    
    
    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
       
        actions = [('Y','l'), ('Y','r'), ('Y','u'), ('Y','d'), ('G','l'), ('G','r'), ('G','u'), ('G','d'), ('B','l'), ('B','r'), ('B','u'), ('B','d'), ('R','l'), ('R','r'), ('R','u'), ('R','d')]
        
        y_pos = state.board.robot_position('Y')
        g_pos = state.board.robot_position('G')
        b_pos = state.board.robot_position('B')
        r_pos = state.board.robot_position('R')

        size = int(state.board.size)
        walls = state.board.walls
        wall_pos_lst = state.board.wall_coordinate_list(walls)
        robot_pos_lst = [y_pos, g_pos, b_pos, r_pos]

        #-------yellow robot----------
        
        self.wall_collision(wall_pos_lst, y_pos, walls, 'Y', actions)
        self.robot_collisions(robot_pos_lst, y_pos, 'Y', actions)
        self.boundary_collision(y_pos, size, actions, 'Y')
         #-------green robot----------
        
        self.wall_collision(wall_pos_lst, g_pos, walls, 'G', actions)
        self.robot_collisions(robot_pos_lst, g_pos, 'G', actions)
        self.boundary_collision(g_pos, size, actions, 'G')
        #-------blue robot---------
        
        self.wall_collision(wall_pos_lst, b_pos, walls, 'B', actions)
        self.robot_collisions(robot_pos_lst, b_pos, 'B', actions)
        self.boundary_collision(b_pos, size, actions, 'B')
        #-------red robot----------
       
        self.wall_collision(wall_pos_lst, r_pos, walls, 'R', actions)
        self.robot_collisions(robot_pos_lst, r_pos, 'R', actions)
        self.boundary_collision(r_pos, size, actions, 'R')

        
        return actions
          
                   

    def dengue(self, r,colors, nextColor, state_string, state, new_state, action_list) :
        if colors[0] == nextColor:
            r[0] = state_string
            board = Board(state.board.size, r[0] ,state.board.r2, state.board.r3 ,state.board.r4, state.board.target, state.board.wall_num, state.board.walls )
            new_state = RRState(board)
            action_list = self.actions(new_state)   
        elif colors[1] == nextColor:            
            r[1] = state_string
            board = Board(state.board.size, state.board.r1 ,r[1], state.board.r3 ,state.board.r4, state.board.target, state.board.wall_num, state.board.walls ) 
            new_state = RRState(board)
            action_list = self.actions(new_state)        
        elif colors[2] == nextColor:            
            r[2] = state_string
            board = Board(state.board.size, state.board.r1,state.board.r2, r[2] ,state.board.r4, state.board.target, state.board.wall_num, state.board.walls )
            new_state = RRState(board)
            action_list = self.actions(new_state)                     
        elif colors[3] == nextColor:            
            r[3] = state_string
            board = Board(state.board.size, state.board.r1 ,state.board.r2, state.board.r3 ,r[3], state.board.target, state.board.wall_num, state.board.walls )
            new_state = RRState(board)
            action_list = self.actions(new_state)   

        


    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        
        action_list  = self.actions(state)
        y_pos = state.board.robot_position('Y')
        g_pos = state.board.robot_position('G')
        b_pos = state.board.robot_position('B')
        r_pos = state.board.robot_position('R')

        r = [state.board.r1,state.board.r2,state.board.r3,state.board.r4]
        colors = [state.board.get_robot_color(r[0]),state.board.get_robot_color(r[1]),state.board.get_robot_color(r[2]),state.board.get_robot_color(r[3])]

   
        new_state = state
        

        while action in action_list:
            if action[0] == 'Y':
                y_pos = self.move_1_square(y_pos, action[1])
                state_change_string = action[0] + ' ' + str(y_pos[0]) + ' ' + str(y_pos[1])
                self.dengue(r, colors, 'Y', state_change_string, state, new_state, action_list)
            
            elif action[0] == 'B':
                b_pos = self.move_1_square(b_pos, action[1])
                state_change_string = action[0] + ' ' + str(b_pos[0]) + ' ' + str(b_pos[1])
                self.dengue(r, colors, 'B', state_change_string, state, new_state, action_list)
            elif action[0] == 'G':
                g_pos = self.move_1_square(g_pos, action[1])
                state_change_string = action[0] + ' ' + str(g_pos[0]) + ' ' + str(g_pos[1])
                self.dengue(r, colors, 'G', state_change_string, state, new_state, action_list)
            elif action[0] == 'R':
                r_pos = self.move_1_square(r_pos, action[1])
                state_change_string = action[0] + ' ' + str(r_pos[0]) + ' ' + str(r_pos[1])
                self.dengue(r, colors, 'R', state_change_string, state, new_state, action_list)
              

        return new_state

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        # TODO
        #print(type(state))
        target = state.board.target
        
        color = state.board.get_robot_color(target)

        if color == 'Y':
            return state.board.robot_position('Y') == state.board.string_to_robot_coord(target)
                
        if color == 'G':
            return state.board.robot_position('G') == state.board.string_to_robot_coord(target)
        
        if color == 'B':
            return state.board.robot_position('B') == state.board.string_to_robot_coord(target)
        
        if color == 'R':
            return state.board.robot_position('R') == state.board.string_to_robot_coord(target)
                 

        return False

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        new_state = node.state
        
        goal = new_state.board.target    #devolve as coordenadas do target
        start_robot = self.initial.board.get_initial_robot(new_state.board.target)
        x1, y1 = int(start_robot[2]),int(start_robot[4])
        x2, y2 = int(goal[2]),int(goal[4])
        # xDif = x2-x1
        # yDif = y2-y1
        # print( xDif )
        # print(yDif)
        # print("total is")
        # print(xDif + yDif)

        #return  node.pathCost
        # TODO
        #print(type(node))



        return abs(x2 - x1) + abs(y2 - y1) 
      

if __name__ == "__main__":
    
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    board  =  parse_instance(sys.argv[1])
    # Usar uma técnica de procura para resolver a instância,
    problem = RicochetRobots(board)

    solution_node = astar_search(problem)
    # Retirar a solução a partir do nó resultante,
    action_list = []
    while solution_node.parent != None:
         action_list.append(solution_node.action)
         node_aux = solution_node
         solution_node = node_aux.parent
    # Imprimir para o standard output no formato indicado.
    size = len(action_list)
    print(size)
    
    for i in reversed(range(0, size)):

        print(action_list[i][0], action_list[i][1])



 #action_list  = self.actions(state)
        y_pos = state.board.robot_position('Y')
        g_pos = state.board.robot_position('G')
        b_pos = state.board.robot_position('B')
        r_pos = state.board.robot_position('R')

        r1= state.board.r1
        r2= state.board.r2
        r3= state.board.r3
        r4= state.board.r4

        color1 = state.board.get_robot_color(r1)
        color2 = state.board.get_robot_color(r2)
        color3 = state.board.get_robot_color(r3)
        color4 = state.board.get_robot_color(r4)

        new_state = state
        size = int( state.board.size)

        #por cada estado é feito um ciclo que verifica a acao
        #o movimento esta mal feito
        for _ in range (0,size-1):   
            if action[0] == 'Y':
                y_pos = self.move_1_square(y_pos, action[1])
                state_change_string = action[0] + ' ' + str(y_pos[0]) + ' ' + str(y_pos[1])

                if color1 == 'Y':
                    r1 = state_change_string
                    board = Board(state.board.size, r1 ,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)


                elif color2 == 'Y':
                    r2 = state_change_string
                    board = Board(state.board.size, r1 ,r2, r3, r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color3 == 'Y':
                    r3 = state_change_string
                    board = Board(state.board.size, r1,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color4 == 'Y':
                    r4 = state_change_string
                    board = Board(state.board.size, r1 ,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

            if action[0] == 'B':
                b_pos = self.move_1_square(b_pos, action[1])
                state_change_string = action[0] + ' ' + str(b_pos[0]) + ' ' + str(b_pos[1])
                r_positions = 2
                if color1 == 'B':
                    r1 = state_change_string
                    board = Board(state.board.size, r1 ,state.board.r2, state.board.r3 ,state.board.r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color2 == 'B':
                    r2 = state_change_string
                    board = Board(state.board.size, state.board.r1 ,r2, state.board.r3 ,state.board.r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color3 == 'B':
                    r3 = state_change_string
                    board = Board(state.board.size, state.board.r1,state.board.r2, r3 ,state.board.r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color4 == 'B':
                    r4 = state_change_string
                    board = Board(state.board.size, state.board.r1 ,state.board.r2, state.board.r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

            if action[0] == 'G':
                g_pos = self.move_1_square(g_pos, action[1])
                state_change_string = action[0] + ' ' + str(g_pos[0]) + ' ' + str(g_pos[1])

                if color1 == 'G':
                    r1 = state_change_string
                    board = Board(state.board.size, r1 ,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color2 == 'G':
                    r2 = state_change_string
                    board = Board(state.board.size, r1 ,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color3 == 'G':
                    r3 = state_change_string
                    board = Board(state.board.size,r1,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color4 == 'G':
                    r4 = state_change_string
                    board = Board(state.board.size, r1 ,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

            if action[0] == 'R':
                r_pos = self.move_1_square(r_pos, action[1])
                state_change_string = action[0] + ' ' + str(r_pos[0]) + ' ' + str(r_pos[1])

                if color1 == 'R':
                    r1 = state_change_string
                    board = Board(state.board.size, r1 ,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color2 == 'R':
                    r2 = state_change_string
                    board = Board(state.board.size, r1 ,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color3 == 'R':
                    r3 = state_change_string
                    board = Board(state.board.size, r1,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)

                elif color4 == 'R':
                    r4 = state_change_string
                    board = Board(state.board.size, r1 ,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                    new_state = RRState(board)
                    self.actions(new_state)
      
        return new_state
