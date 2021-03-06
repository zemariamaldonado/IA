# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 76:
# 89474 Joao Silva
# 89489 Jose Lopes
from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys, math

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
        if len(string) == 5:
            x = int(string[2])
            y = int(string[4])
        elif len(string) == 6:
            if string[3] != ' ':
                x = int(string[2] + string[3])
                y = int(string[5])
            else:
                x = int(string[2])
                y = int(string[4] + string[5])
        elif len(string) == 7:
            x = int(string[2] + string[3])
            y = int(string[5] + string[6])

        tup = (x, y)
        return tup
    
    def string_to_wall_coord(self, string: str):
        if len(string) == 5:
            x = int(string[0])
            y = int(string[2])
        elif len(string) == 6:
            if string[1] != ' ':
                x = int(string[0] + string[1])
                y = int(string[3])
            else:
                x = int(string[0])
                y = int(string[2] + string[3])
        elif len(string) == 7:
            x = int(string[0] + string[1])
            y = int(string[3] + string[4])
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
        self.stepList = []

    def boundary_collision(self, pos, size, a_array, color):
        left = (color, 'l')
        right = (color, 'r')
        up = (color, 'u')
        down = (color, 'd')

        if pos[0] == 1:
            if up in a_array:
                del self.stepList[a_array.index(up)]
                a_array.remove(up)
        elif pos[0] == size:
            if down in a_array:
                del self.stepList[a_array.index(down)]
                a_array.remove(down)
        
        if pos[1] == 1:
            if left in a_array:
                del self.stepList[a_array.index(left)]
                a_array.remove(left)
        elif pos[1] == size:
            if right in a_array:
                del self.stepList[a_array.index(right)]
                a_array.remove(right)

    def checkSteps(self, state: RRState, wall_pos_lst, walls, size, robot_pos_lst, a_array):
        i = 0

        while i < len(a_array):
            #print('--------START WHILE--------')
            #print('Actions: ', a_array)
            #print('Steps: ', self.stepList)
            #print('Index: ', i)
            steps = 0

            move = a_array[i]
            color = move[0]
            d = move[1]

            pos = state.board.robot_position(color)
            posAux = pos
            #print(posAux)

            #Se for andar pa esquerda
            if d == 'l':
                #Andar ate bater na boundary
                while posAux[1] > 1:

                    #Se a barreira estiver na mesma posiçao e a esquerda
                    if posAux in wall_pos_lst:
                        dAux = self.initial.board.get_wall_direction(walls[wall_pos_lst.index(posAux)])

                        if dAux == d:
                            if steps == 0:
                                del self.stepList[a_array.index(move)]
                                a_array.remove(move)
                                i -= 1
                            
                            break

                    #Calcular a proxima POSSIVEL posicao
                    aux = list(posAux)
                    aux[1] -= 1
                    nextPos = tuple(aux)

                    #Se houver barreira na proxima pos
                    if nextPos in wall_pos_lst:
                        dAux = self.initial.board.get_wall_direction(walls[wall_pos_lst.index(nextPos)])

                        if dAux == 'r':
                            if steps == 0:
                                del self.stepList[a_array.index(move)]
                                a_array.remove(move)
                                i -= 1

                            break
                    
                    #Se houver robot na proxima pos
                    if nextPos in robot_pos_lst:
                        if steps == 0:
                            del self.stepList[a_array.index(move)]
                            a_array.remove(move)
                            i -= 1

                        break

                    #Se passar tudo, igualar a posAux a proxima possivel
                    posAux = nextPos
                    steps += 1
            #Se for andar pa direita
            elif d == 'r':
                #Andar ate bater na boundary
                while posAux[1] < size:

                    #Se a barreira estiver na mesma posiçao e a direita
                    if posAux in wall_pos_lst:
                        dAux = self.initial.board.get_wall_direction(walls[wall_pos_lst.index(posAux)])

                        if dAux == d:
                            if steps == 0:
                                del self.stepList[a_array.index(move)]
                                a_array.remove(move)
                                i -= 1
                            
                            break

                    #Calcular a proxima POSSIVEL posicao
                    aux = list(posAux)
                    aux[1] += 1
                    nextPos = tuple(aux)

                    #Se houver barreira na proxima pos
                    if nextPos in wall_pos_lst:
                        dAux = self.initial.board.get_wall_direction(walls[wall_pos_lst.index(nextPos)])

                        if dAux == 'l':
                            if steps == 0:
                                del self.stepList[a_array.index(move)]
                                a_array.remove(move)
                                i -= 1

                            break
                    
                    #Se houver robot na proxima pos
                    if nextPos in robot_pos_lst:
                        if steps == 0:
                            del self.stepList[a_array.index(move)]
                            a_array.remove(move)
                            i -= 1
                            
                        break

                    #Se passar tudo, igualar a posAux a proxima possivel
                    posAux = nextPos
                    steps += 1
            #Se for andar pa cima
            elif d == 'u':
                #Andar ate bater na boundary
                while posAux[0] > 1:

                    #Se a barreira estiver na mesma posiçao
                    if posAux in wall_pos_lst:
                        dAux = self.initial.board.get_wall_direction(walls[wall_pos_lst.index(posAux)])

                        if dAux == d:
                            if steps == 0:
                                del self.stepList[a_array.index(move)]
                                a_array.remove(move)
                                i -= 1
                            
                            break

                    #Calcular a proxima POSSIVEL posicao
                    aux = list(posAux)
                    aux[0] -= 1
                    nextPos = tuple(aux)

                    #Se houver barreira na proxima pos
                    if nextPos in wall_pos_lst:
                        dAux = self.initial.board.get_wall_direction(walls[wall_pos_lst.index(nextPos)])

                        if dAux == 'd':
                            if steps == 0:
                                del self.stepList[a_array.index(move)]
                                a_array.remove(move)
                                i -= 1

                            break
                    
                    #Se houver robot na proxima pos
                    if nextPos in robot_pos_lst:
                        if steps == 0:
                            del self.stepList[a_array.index(move)]
                            a_array.remove(move)
                            i -= 1  

                        break

                    #Se passar tudo, igualar a posAux a proxima possivel
                    posAux = nextPos
                    steps += 1
            #Se for andar pa baixo
            elif d == 'd':
                #Andar ate bater na boundary
                while posAux[0] < size:

                    #Se a barreira estiver na mesma posiçao
                    if posAux in wall_pos_lst:
                        dAux = self.initial.board.get_wall_direction(walls[wall_pos_lst.index(posAux)])

                        if dAux == d:
                            if steps == 0:
                                del self.stepList[a_array.index(move)]
                                a_array.remove(move)
                                i -= 1
                            
                            break

                    #Calcular a proxima POSSIVEL posicao
                    aux = list(posAux)
                    aux[0] += 1
                    nextPos = tuple(aux)

                    #Se houver barreira na proxima pos
                    if nextPos in wall_pos_lst:
                        dAux = self.initial.board.get_wall_direction(walls[wall_pos_lst.index(nextPos)])

                        if dAux == 'u':
                            if steps == 0:
                                del self.stepList[a_array.index(move)]
                                a_array.remove(move)
                                i -= 1

                            break
                    
                    #Se houver robot na proxima pos
                    if nextPos in robot_pos_lst:
                        if steps == 0:
                            del self.stepList[a_array.index(move)]
                            a_array.remove(move)
                            i -= 1
                            
                        break

                    #Se passar tudo, igualar a posAux a proxima possivel
                    posAux = nextPos
                    steps += 1

            if steps > 0:
                self.stepList[i] = steps

            i += 1
         
    def moveRobot(self, state: RRState, action, actions):
        color = action[0]
        d = action[1]

        r1= state.board.r1
        r2= state.board.r2
        r3= state.board.r3
        r4= state.board.r4

        color1 = state.board.get_robot_color(r1)
        color2 = state.board.get_robot_color(r2)
        color3 = state.board.get_robot_color(r3)
        color4 = state.board.get_robot_color(r4)

        rPos = state.board.robot_position(color)

        new_state = state

        if action in actions:
            numSteps = self.stepList[actions.index(action)]

            if d == 'l':
                state_change_string = action[0] + ' ' + str(rPos[0]) + ' ' + str(rPos[1] - numSteps)
            elif d == 'r':
                state_change_string = action[0] + ' ' + str(rPos[0]) + ' ' + str(rPos[1] + numSteps)
            elif d == 'u':
                state_change_string = action[0] + ' ' + str(rPos[0] - numSteps) + ' ' + str(rPos[1])
            elif d == 'd':
                state_change_string = action[0] + ' ' + str(rPos[0] + numSteps) + ' ' + str(rPos[1])

            if color == color1:
                board = Board(state.board.size, state_change_string ,r2, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                new_state = RRState(board)
            elif color == color2:
                board = Board(state.board.size, r1 ,state_change_string, r3 ,r4, state.board.target, state.board.wall_num, state.board.walls )
                new_state = RRState(board)
            elif color == color3:
                board = Board(state.board.size, r1 ,r2, state_change_string ,r4, state.board.target, state.board.wall_num, state.board.walls )
                new_state = RRState(board)
            elif color == color4:
                board = Board(state.board.size, r1 ,r2, r3 ,state_change_string, state.board.target, state.board.wall_num, state.board.walls )
                new_state = RRState(board)

        return new_state

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
       
        actions = [('Y','l'), ('Y','r'), ('Y','u'), ('Y','d'), ('G','l'), ('G','r'), ('G','u'), ('G','d'), ('B','l'), ('B','r'), ('B','u'), ('B','d'), ('R','l'), ('R','r'), ('R','u'), ('R','d')]
        self.stepList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        y_pos = state.board.robot_position('Y')
        g_pos = state.board.robot_position('G')
        b_pos = state.board.robot_position('B')
        r_pos = state.board.robot_position('R')

        size = int(state.board.size)
        walls = state.board.walls
        wall_pos_lst = state.board.wall_coordinate_list(walls)
        robot_pos_lst = [y_pos, g_pos, b_pos, r_pos]

        self.boundary_collision(y_pos, size, actions, 'Y')
        self.boundary_collision(g_pos, size, actions, 'G')
        self.boundary_collision(b_pos, size, actions, 'B')
        self.boundary_collision(r_pos, size, actions, 'R')

        self.checkSteps(state, wall_pos_lst, walls, size, robot_pos_lst, actions)
        
        return actions
          
                   
    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        
        action_list  = self.actions(state)

        new_state = self.moveRobot(state, action, action_list)

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
        # TODO
        state = node.state

        size = int(state.board.size)

        goal = state.board.target
        target = state.board.string_to_robot_coord(goal)

        start_robot = self.initial.board.get_initial_robot(state.board.target)
        initialPos = state.board.string_to_robot_coord(start_robot)

        color = state.board.get_robot_color(goal)
        current = state.board.robot_position(color)

        verticalDistance = abs(current[0] - target[0])
        horizontalDistance = abs(current[1]- target[1])
        h = (verticalDistance + horizontalDistance)

        if node.parent != None:
            currentPosDistanceX = current[0] - target[0]
            currentPosDistanceY = current[1] - target[1]
            initialPosDistanceX = initialPos[0] - target[0]
            initialPosDistanceY = initialPos[1]- target[1]

            crossProduct = abs(currentPosDistanceX * initialPosDistanceY - initialPosDistanceX * currentPosDistanceY)
            h += crossProduct * 0.001

        return h

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