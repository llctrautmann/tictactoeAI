from IPython.display import clear_output
import copy 
import random
import numpy as np

class XOGame:
    def __init__(self):
        self.board = []
        self.player = None
        self.optimal_move = None
        self.token_human = None
        self.token_ai = None
        self.create_board()
        self.starting_player()
        self.rounds = 0

    def main(self):
        if self.player == 'human':
            while self.rounds < 9:
                self.display_board()
                self.human_move(token='x')
                self.rounds += 1

                if self.check_win():
                    clear_output()
                    self.display_board()
                    self.rounds += 10
                    break

                self.optimal_move = self.best_move(board=self.board,maxi=False)
                self.ai_move(token='o')
                self.rounds += 1


                if self.check_win():
                    clear_output()
                    self.display_board()
                    self.rounds += 10
                    break
            
                clear_output()
            self.display_board()
            return None
        else:
            while self.rounds < 9:
                self.display_board()
                self.optimal_move = self.best_move(board=self.board,maxi=True)
                self.ai_move(token = 'x')
                self.rounds += 1

                if self.check_win():
                    clear_output()
                    self.display_board()
                    self.rounds += 10
                    break

                clear_output()
                self.display_board()
                self.human_move(token='o')
                self.rounds += 1

                if self.check_win():
                    clear_output()
                    self.display_board()
                    self.rounds += 10
                    break

                clear_output()
            self.display_board()
            return None


            
    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)
        return None


    def display_board2(self):
        print('-----')
        for s in self.board:
            print(*s)
        print('-----')

    def display_board(self):
        displayed_board = copy.deepcopy(self.board)

        for i in range(len(displayed_board)):
            displayed_board[i] = [i] + displayed_board[i]
        displayed_board.append([' ','0','1','2'])

        print('--------')
        for s in displayed_board:
            print(*s)
        print('--------')

    def starting_player(self):
        if random.random() < 0.5:
            self.player = 'ai'
        else:
            self.player = 'human'


    def human_move(self,token):
        my_tuple = tuple(input('Enter space-separated x and y coords: ').split())        

        x = int(my_tuple[0])
        y = int(my_tuple[1])

        self.board[x][y] = token

    def ai_move(self,token):
        self.board[self.optimal_move[0]][self.optimal_move[1]] = token


    def check_win(self):
        end_game = False

        if self.board[0][0] == 'x' and self.board[1][1] == 'x' and self.board[2][2] == 'x':
            end_game = True
        if self.board[0][0] == 'o' and self.board[1][1] == 'o' and self.board[2][2] == 'o':
            end_game = True
        if self.board[0][2] == 'x' and self.board[1][1] == 'x' and self.board[2][0] == 'x':
            end_game = True
        if self.board[0][2] == 'o' and self.board[1][1] == 'o' and self.board[2][0] == 'o':
            end_game = True

        for row in self.board:
            if row.count('x') == 3 or row.count('o') == 3:
                end_game = True

        transposed_board = self.transpose(copy.deepcopy(self.board))
        for row in transposed_board:
            if row.count('x') == 3 or row.count('o') == 3:
                end_game = True

        return end_game


    def best_move(self, board, maxi=True):
        evals = []

        if maxi:
            token = 'x'
        else:
            token = 'o'

        new_boards, moves = self.create_new_board_positions(board,token=token)

        if maxi == True:
            maximise = False
        if maxi == False:
            maximise = True


        for new_board in new_boards:
            evals.append(self.minmax(board=new_board, depth = 6, alpha=-np.inf, beta=np.inf, maximise=maximise))


        if maxi:
            if len(evals) == 0:
                self.rounds += 10
                return (1,1)
            elif 1 in evals:
                indices = self.find_indices(evals, 1)
                return moves[random.choice(indices)]
            elif 0 in evals:
                indices = self.find_indices(evals, 0)
                return moves[random.choice(indices)]
            else:
                indices = self.find_indices(evals, -1)
                return moves[random.choice(indices)]
        else:
            if len(evals) == 0:
                self.rounds += 10
                return (1,1)
            elif -1 in evals:
                indices = self.find_indices(evals, -1)
                return moves[random.choice(indices)]
            elif 0 in evals:
                indices = self.find_indices(evals, 0)
                return moves[random.choice(indices)]
            else:
                indices = self.find_indices(evals, 1)
                return moves[random.choice(indices)]
            


    def create_new_board_positions(self, board, token):
        possible_board_positions = []
        moves_coords = []

        rows = len(board)
        cols = len(board[0])

        for i in range(rows):
            for j in range(cols):
                if board[i][j] == '-':
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = token

                    possible_board_positions.append(new_board)
                    moves_coords.append((i,j))

        return possible_board_positions, moves_coords



    def minmax(self,board,depth=1,alpha= -np.inf, beta = np.inf, maximise = True):
        if self.board_evaluation(board) == 1:
            return 1
        elif self.board_evaluation(board) == -1:
            return -1
        elif self.check_leaf_node(board) == True:
            return 0
        elif depth == 0:
            return self.board_evaluation(board)
        
        else:

            if maximise:
                token = 'x'
            else:
                token = 'o'

            new_boards, moves = self.create_new_board_positions(board,token)


            if maximise:
                maxEval = -np.inf

                for new_board in new_boards:
                    eval = self.minmax(new_board, depth-1, alpha=alpha, beta=beta, maximise=False)
                    maxEval = max(maxEval, eval)

                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break

                return maxEval
            
            else:
                minEval = np.inf

                for new_board in new_boards:
                    eval = self.minmax(new_board, depth-1, alpha=alpha, beta=beta, maximise=True)
                    minEval = min(minEval, eval)

                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

                return minEval

    def board_evaluation(self,board):
        '''
        evaluates the board position
        +1: X is the winner
        -1: O is the winner
        0: No winner
        '''
        eval = 0

        if board[0][0] == 'x' and board[1][1] == 'x' and board[2][2] == 'x':
            eval = 1
        if board[0][0] == 'o' and board[1][1] == 'o' and board[2][2] == 'o':
            eval = -1
        if board[0][2] == 'x' and board[1][1] == 'x' and board[2][0] == 'x':
            eval = 1
        if board[0][2] == 'o' and board[1][1] == 'o' and board[2][0] == 'o':
            eval = -1

        for row in board:
            if row.count('x') == 3 or row.count('o') == 3:
                if row[0] == 'x':
                    eval = 1
                else:
                    eval = -1

        transposed_board = self.transpose(copy.deepcopy(board))
        for row in transposed_board:
            if row.count('x') == 3 or row.count('o') == 3:
                if row[0] == 'x':
                    eval = 1
                else:
                    eval = -1

        return eval

    @staticmethod
    def find_indices(list_to_check, item_to_find):
        return [idx for idx, value in enumerate(list_to_check) if value == item_to_find]   
    
    @staticmethod
    def transpose(ll: list):
        ref = copy.deepcopy(ll)
        ll[0][1] = ref[1][0]
        ll[1][0] = ref[0][1]
        ll[0][2] = ref[2][0]
        ll[2][0] = ref[0][2]
        ll[1][2] = ref[2][1]
        ll[2][1] = ref[1][2]
        return ll

    @staticmethod
    def check_leaf_node(board):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    return False
        return True




if __name__ == '__main__':
    game = XOGame()
    game.main()