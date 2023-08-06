# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 07:
# 99046 Afonso Ponces de Carvalho
# 99091 Joao Ponces de Carvalho

import time
from calendar import TUESDAY
from sys import stdin
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, board, size):
        self.board = board
        self.size = size

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO

        return int(self.board[row][col])


    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        # TODO

        if(row == 0):
            return (int(self.board[row + 1][col]), None)
        elif(row == self.size - 1):
            return (None, int(self.board[row - 1][col]))
        else:
            return (int(self.board[row + 1][col]), int(self.board[row - 1][col]))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO

        if(col == 0):
            return (None, int(self.board[row][col + 1]))
        elif(col == self.size - 1):
            return (int(self.board[row][col - 1]), None)
        else:
            return (int(self.board[row][col - 1]), int(self.board[row][col + 1]))


    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        # TODO

        size = int(stdin.readline())
        new_board = []
        
        for i in range(size):
            new_line = stdin.readline()
            row = []
            for j in new_line:
                if(j == '1' or j == '0' or j == '2'):
                    row.append(int(j))
            new_board.append(row)
        board = np.array(new_board)
        instance = Board(board, size)
        return instance

    def __repr__(self):
        result = ""
        for i in range(self.size):
            line = ""
            for j in range(self.size):
                if(j == self.size - 1):
                    line += str(self.board[i][j]) + '\n'
                    continue
                line += str(self.board[i][j]) + "\t"
            result += line
        return result

    def matrix_valid(self, rotated):
        for i in range(self.size):
            counter = 0
            counter_r = 0
            for j in range(self.size):
                if self.board[i][j] == 2 or rotated[i][j] == 2:
                    return False
                elif self.board[i][j] == 1:
                    counter += 1
                    if self.adjacent_horizontal_numbers(i,j) == (1,1) or self.adjacent_vertical_numbers(i,j) == (1,1):
                        return False
                elif self.board[i][j] == 0:
                    if self.adjacent_horizontal_numbers(i,j) == (0,0) or self.adjacent_vertical_numbers(i,j) == (0,0):
                        return False
                if rotated[i][j] == 1:
                    counter_r +=1
            if self.size % 2 == 0:
                if counter != self.size / 2 or counter_r != self.size / 2:
                    return False
            else:
                if counter > (self.size-1) / 2 + 1 or counter_r > (self.size-1) / 2 + 1:
                    return False
        return True   
    

    def is_valid(self):
        #if 2 in self.board:
        #   return False
        if not self.matrix_valid(np.rot90(self.board, 3)):
            return False
        if len(np.unique(self.board, axis = 0)) != self.size:
            return False
        if len(np.unique(np.rot90(self.board), axis = 0)) != self.size:
            return False
        return True


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        self.initial = TakuzuState(board)
    
        pass
    
    def actions(self, state: TakuzuState):
        actions = []

        two_positions = np.where(state.board.board == 2)
        length = np.size(two_positions[0])
        flag = 0
        x = -1
        y = -1

        for i in range(length):
            x = two_positions[0][i]
            y = two_positions[1][i]

            hor = state.board.adjacent_horizontal_numbers(x,y)
            ver = state.board.adjacent_vertical_numbers(x,y)

            if (hor == (1,1)) or (ver == (1,1)):
                flag = 2
                break
            elif (hor == (0,0)) or (ver == (0,0)):
                flag = 1
                break

            row_zeros = np.count_nonzero(state.board.board[x] == 0)
            row_ones = np.count_nonzero(state.board.board[x] == 1)

            rotated = np.rot90(state.board.board, 3)
            column_zeros = np.count_nonzero(rotated[y] == 0)
            column_ones = np.count_nonzero(rotated[y] == 1)

            if state.board.size % 2 == 0:
                if row_zeros > state.board.size / 2 or row_ones > state.board.size / 2 or column_zeros > state.board.size / 2 or column_ones > state.board.size / 2:
                    return []
                elif (row_zeros == state.board.size / 2) or (column_zeros == state.board.size / 2):
                    flag = 1
                    break
                elif (row_ones == state.board.size / 2) or (column_ones == state.board.size / 2):
                    flag = 2
                    break
            else:
                if row_zeros > (state.board.size-1)/2+1 or row_ones > (state.board.size-1)/2+1 or column_zeros > (state.board.size-1)/2+1 or column_ones > (state.board.size-1)/2+1:
                    return []
                elif (row_zeros == (state.board.size-1) / 2 + 1) or (column_zeros == (state.board.size-1) / 2 + 1):
                    flag = 1
                    break
                elif (row_ones == (state.board.size-1) / 2 + 1) or (column_ones == (state.board.size-1) / 2 + 1):
                    flag = 2
                    break
            
            if y != state.board.size - 1 and state.board.adjacent_horizontal_numbers(x,y+1)[1] == state.board.board[x][y+1]:
                if state.board.board[x][y+1] == 0:
                    flag = 1
                    break
                elif state.board.board[x][y+1] == 1:
                    flag = 2
                    break
            if y != 0 and state.board.adjacent_horizontal_numbers(x,y-1)[0] == state.board.board[x][y-1]:
                if state.board.board[x][y-1] == 0:
                    flag = 1
                    break
                elif state.board.board[x][y-1] == 1:
                    flag = 2
                    break
            
            if x != state.board.size - 1 and state.board.adjacent_vertical_numbers(x+1,y)[0] == state.board.board[x+1][y]:
                if state.board.board[x+1][y] == 0:
                    flag = 1
                    break
                elif state.board.board[x+1][y] == 1:
                    flag = 2
                    
                    break
            if x != 0 and state.board.adjacent_vertical_numbers(x-1,y)[1] == state.board.board[x-1][y]:
                if state.board.board[x-1][y] == 0:
                    flag = 1
                    break      
                elif state.board.board[x-1][y] == 1:
                    flag = 2  
                    break   

        if x != -1 and y != -1:        
            if flag == 1:
                actions.append((x, y, 1))
            elif flag == 2:
                actions.append((x, y, 0))
            elif flag == 0 and length > 0:
                actions.append((two_positions[0][0], two_positions[1][0], 1))
                actions.append((two_positions[0][0], two_positions[1][0], 0))
        return actions

        
    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        new_board_array = np.array(state.board.board)
        board = Board(new_board_array, state.board.size)
        new_state = TakuzuState(board)
        new_state.board.board[action[0]][action[1]] = action[2]
        return new_state

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        return state.board.is_valid()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance_from_stdin()

    problem = Takuzu(board)

    goal_node = depth_first_tree_search(problem)

    print(goal_node.state.board, end="")