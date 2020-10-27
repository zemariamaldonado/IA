# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 76:
# 89474 Joao Silva
# 89489 Jose Lopes
from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys

#TODO meter elifes nas funcoes onde eu quero que so se leia 1 if
#TODO apagar prints em comentarios

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
        self.initial = board
        
    def boundary_collision(self,pos, size, a_array, color):
        if pos[0] == 1:
            a_array.remove((color, 'u'))
        elif pos[0] == size:
            a_array.remove((color, 'd'))
        elif pos[1] == 1:
            a_array.remove((color, 'l'))
        elif pos[1] == size:
            a_array.remove((color, 'r'))

    def wall_collision(self, wall_pos_lst, pos, walls, color, a_array):
        d = ' '
        left = (color, 'l')
        right = (color, 'r')
        up = (color, 'u')
        down = (color, 'd')
        for i in range(len(wall_pos_lst)):
            if wall_pos_lst[i] == pos:
                d = self.initial.get_wall_direction(walls[i])
                
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
                if self.initial.get_wall_direction(walls[j]) == 'l':
                    if right in a_array:
                        a_array.remove(right)
            if wall_pos_lst[j] == self.move_1_square(pos,'l'):
                if self.initial.get_wall_direction(walls[j]) == 'r':
                    if left in a_array:
                        a_array.remove(left)
            if wall_pos_lst[j] == self.move_1_square(pos,'u'):
                if self.initial.get_wall_direction(walls[j]) == 'd':
                    if up in a_array:
                        a_array.remove(up)
            if wall_pos_lst[j] == self.move_1_square(pos,'d'):
                if self.initial.get_wall_direction(walls[j]) == 'u':
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
     
    def boundary(self, l, size, rd):
        #esquerda
        if rd == 'l':
            if (l[1] == 0):
                l[1] = l[1]+1
            if (l[1] == -1):
                l[1] = l[1]+2
            if (l[1] == -2):
                l[1] = l[1]+3
            new_move = l
        #direita
        if rd == 'r':
            if (l[1] == size+1):
                l[1] = l[1]-1
            if (l[1] == size+2):
                l[1] = l[1]-2
            if (l[1] == size+3):
                l[1] = l[1]-3
            new_move = l
        #cima
        if rd == 'u':
            if (l[0] == 0):
                l[0] = l[0]+1
            if (l[0] == -1):
                l[0] = l[0]+2
            if (l[0] == -2):
                l[0] = l[0]+3
            new_move = l
        #baixo
        if rd == 'd':
            if (l[0] == size+1):
                l[0] = l[0]-1
            if (l[0] == size+2):
                l[0] = l[0]-2
            if (l[0] == size+3):
                l[0] = l[0]-3
            new_move = l
        else:
            new_move = l
        
        
        return new_move
    

    def robot_bump(self, l, robot_pos_list, rob_direction):
        isRobot = 0
        tup_input = tuple(l)
        l_tup = (tup_input[0], tup_input[1]-1)
        r_tup = (tup_input[0], tup_input[1]+1)
        u_tup = (tup_input[0]-1, tup_input[1])
        d_tup = (tup_input[0]+1, tup_input[1])

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
                isRobot = 1
        if isRobot == 1:
            return True
        return False
        
    def wall_bump(self, l, wall_pos_list, rob_direction, walls):
        isWall = 0
        wall_direction = ' '
        tup_input = tuple(l)
        l_tup = (tup_input[0], tup_input[1]-1)
        r_tup = (tup_input[0], tup_input[1]+1)
        u_tup = (tup_input[0]-1, tup_input[1])
        d_tup = (tup_input[0]+1, tup_input[1])
         
         #TODO fix its ugly
        for i in range(len(wall_pos_list)):
            if wall_pos_list[i] == tup_input:
                wall_direction = self.initial.get_wall_direction(walls[i])
            elif wall_pos_list[i] == l_tup:
                wall_direction = self.initial.get_wall_direction(walls[i])
            elif wall_pos_list[i] == r_tup:
                wall_direction = self.initial.get_wall_direction(walls[i])
            elif wall_pos_list[i] == u_tup:
                wall_direction = self.initial.get_wall_direction(walls[i])
            elif wall_pos_list[i] == d_tup:
                wall_direction = self.initial.get_wall_direction(walls[i])
            
            if rob_direction == 'l':
                if tup_input == wall_pos_list[i]:
                    if wall_direction == 'l':
                        isWall = 1
                    #else:
                        #print("wallz")
                        #isWall = 0

                if l_tup == wall_pos_list[i]:
                    if wall_direction == 'r':
                        #print("tresdoisparede")
                        isWall = 1 
                    #else:
                        #isWall = 0
            if rob_direction == 'r':
                if tup_input == wall_pos_list[i]:
                    #print("setedoisparede")
                    if wall_direction == 'r':
                        #print("setedoisparededirecao")
                        isWall = 1
                    #else:
                        #isWall = 0

                elif r_tup == wall_pos_list[i]:
                    if wall_direction == 'l':
                        isWall = 1 
                    #else:
                        #isWall = 0
            if rob_direction == 'u':
                if tup_input == wall_pos_list[i]:
                    if wall_direction == 'u':
                        isWall = 1
                    #else:
                        #isWall = 0
                if u_tup == wall_pos_list[i]:
                    if wall_direction == 'd':
                        isWall = 1 
                    #else:
                        #isWall = 0
            if rob_direction == 'd':
                if tup_input == wall_pos_list[i]:
                    if wall_direction == 'd':
                        isWall = 1
                    #else:
                        #isWall = 0
                if d_tup == wall_pos_list[i]:
                    if wall_direction == 'u':
                        isWall = 1 
                    #else:
                        #isWall = 0
        #print(isWall)
        if isWall == 1:
            l = l
            return True
        
        return False

    def final_movement(self, size, l, wall_pos_list, robot_pos_list, rob_direction, walls):
        l_aux = l 

        for _ in range(0, size-1):
            #print("-->",l_aux)
            #print(self.wall_bump(l_aux, wall_pos_list, rob_direction, walls))
            
            if self.wall_bump(l_aux, wall_pos_list, rob_direction, walls) == False:
                if self.robot_bump(l_aux, robot_pos_list, rob_direction) == False:
                    if rob_direction == 'l':
                        l_aux[1] = l_aux[1]-1 
                        if self.boundary(l_aux, size, rob_direction) == l_aux:
                            l = l_aux

                        else:
                            l = self.boundary(l_aux, size, rob_direction)

                    if rob_direction == 'r':
                        l_aux[1] = l_aux[1]+1 
                        if self.boundary(l_aux, size, rob_direction) == l_aux:
                            l = l_aux
                        else:
                            l = self.boundary(l_aux, size, rob_direction)
                    if rob_direction == 'u':
                        l_aux[0] = l_aux[0]-1 
                        if self.boundary(l_aux, size, rob_direction) == l_aux:
                            l = l_aux
                        else:
                            l = self.boundary(l_aux, size, rob_direction)
                    if rob_direction == 'd':
                        l_aux[0] = l_aux[0]+1 
                        if self.boundary(l_aux, size, rob_direction) == l_aux:
                            l = l_aux
                        else:
                            l = self.boundary(l_aux, size, rob_direction)
                else:
                    l = l_aux
            else:
                l = l_aux

    def move_robot(self, pos, rob_direction, wall_pos_list, walls, size, robot_pos_list):
        res_tup = ( )
        l = list(pos)

        #l_to_tup = l 
        if rob_direction == 'l' or rob_direction == 'r' or rob_direction == 'u' or rob_direction == 'd':
            self.final_movement(size, l, wall_pos_list, robot_pos_list, rob_direction, walls)

        res_tup = tuple(l)
        return res_tup
        
    
    
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
          
                   
    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        
        color = action[0]
        direction = action[1]


        y_pos = state.board.robot_position('Y')
        g_pos = state.board.robot_position('G')
        b_pos = state.board.robot_position('B')
        r_pos = state.board.robot_position('R')

        size = int(state.board.size)
        walls = state.board.walls
        wall_pos_list = state.board.wall_coordinate_list(walls)
        robot_pos_lst = [y_pos, g_pos, b_pos, r_pos]
        
        r_positions = -1
        
        if color == 'Y':
            if state.board.get_robot_color(state.board.r1) == color:
                y_pos = self.move_robot(y_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(y_pos[0]) + ' ' + str(y_pos[1])
                r_positions = 1
            elif state.board.get_robot_color(state.board.r2) == color:
                y_pos = self.move_robot(y_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(y_pos[0]) + ' ' + str(y_pos[1])
                r_positions = 2
            elif state.board.get_robot_color(state.board.r3) == color:
                y_pos = self.move_robot(y_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(y_pos[0]) + ' ' + str(y_pos[1])
                r_positions = 3
            elif state.board.get_robot_color(state.board.r4) == color:
                y_pos = self.move_robot(y_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(y_pos[0]) + ' ' + str(y_pos[1])
                r_positions = 4
        if color == 'G':
            if state.board.get_robot_color(state.board.r1) == color:
                g_pos = self.move_robot(g_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(g_pos[0]) + ' ' + str(g_pos[1])
                r_positions = 1
            elif state.board.get_robot_color(state.board.r2) == color:
                g_pos = self.move_robot(g_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(g_pos[0]) + ' ' + str(g_pos[1])
                r_positions = 2
            elif state.board.get_robot_color(state.board.r3) == color:
                g_pos = self.move_robot(g_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(g_pos[0]) + ' ' + str(g_pos[1])
                r_positions = 3
            elif state.board.get_robot_color(state.board.r4) == color:
                g_pos = self.move_robot(g_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(g_pos[0]) + ' ' + str(g_pos[1])
                r_positions = 4
        if color == 'B':
            if state.board.get_robot_color(state.board.r1) == color:
                b_pos = self.move_robot(b_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(b_pos[0]) + ' ' + str(b_pos[1])
                r_positions = 1
            elif state.board.get_robot_color(state.board.r2) == color:
                b_pos = self.move_robot(b_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(b_pos[0]) + ' ' + str(b_pos[1])
                r_positions = 2
            elif state.board.get_robot_color(state.board.r3) == color:
                b_pos = self.move_robot(b_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(b_pos[0]) + ' ' + str(b_pos[1])
                r_positions = 3
            elif state.board.get_robot_color(state.board.r4) == color:
                b_pos = self.move_robot(b_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(b_pos[0]) + ' ' + str(b_pos[1])
                r_positions = 4
        if color == 'R':
            if state.board.get_robot_color(state.board.r1) == color:
                r_pos = self.move_robot(r_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(r_pos[0]) + ' ' + str(r_pos[1])
                r_positions = 1
            elif state.board.get_robot_color(state.board.r2) == color:
                r_pos = self.move_robot(r_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(r_pos[0]) + ' ' + str(r_pos[1])
                r_positions = 2
            elif state.board.get_robot_color(state.board.r3) == color:
                r_pos = self.move_robot(r_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(r_pos[0]) + ' ' + str(r_pos[1])
                r_positions = 3
            elif state.board.get_robot_color(state.board.r4) == color:
                r_pos = self.move_robot(r_pos, direction, wall_pos_list, walls, size, robot_pos_lst)
                state_change_string = color + ' ' + str(r_pos[0]) + ' ' + str(r_pos[1])
                r_positions = 4


        r = [0,0,0,0]

        if r_positions == 1 :
            r[0] = state_change_string
        elif r_positions == 2 :
            r[1] = state_change_string
        elif r_positions == 3:
            r[2] = state_change_string
        elif r_positions == 4 :
            r[3] = state_change_string
        

        if r[0] != 0 :
            board = Board(state.board.size, r[0] ,state.board.r2, state.board.r3 ,state.board.r4, state.board.target, state.board.wall_num, state.board.walls )
        elif r[1] != 0 :
            board = Board(state.board.size,state.board.r1 ,r[1], state.board.r3 ,state.board.r4, state.board.target, state.board.wall_num, state.board.walls )

        elif r[2] != 0 :
            board = Board(state.board.size, state.board.r1 ,state.board.r2, r[2] ,state.board.r4, state.board.target, state.board.wall_num, state.board.walls )

        elif r[3] != 0 :
            board = Board(state.board.size, state.board.r1 ,state.board.r2, state.board.r3 ,r[3], state.board.target, state.board.wall_num, state.board.walls )


        new_state = RRState(board)


        return new_state

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        # TODO
        print(type(state.board.target))
        target =state.board.target
        
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
        # TODO
        new_state = node.state

        goal = self.initial.string_to_robot_coord(new_state.target)#devolve as coordenadas do target

        start_robot = self.initial.string_to_robot_coord(self.initial.get_initial_robot(new_state.target))

        x1, y1 = start_robot
        x2, y2 = goal 
        return abs(x2 - x1) + abs(y2 - y1) 
      

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass


'''
# Ler tabuleiro do ficheiro "i1.txt":
board = parse_instance("instances/i1.txt")
problem = RicochetRobots(board)
s0 = RRState(board)
print(problem.actions(s0))
# Aplicar as ações que resolvem a instância
#print(('B', 'l') in problem.actions(s0))
s1 = problem.result(s0, ('B', 'l'))
print(problem.actions(s1))
#print(('Y', 'u') in problem.actions(s1))
s2 = problem.result(s1, ('Y', 'u'))
print(problem.actions(s2))
#print(('R', 'r') in problem.actions(s2))
s3 = problem.result(s2, ('R', 'r'))
print(problem.actions(s3))
#print(('R', 'u') in problem.actions(s3))
s4 = problem.result(s3, ('R', 'u'))
print(problem.actions(s4))
'''

