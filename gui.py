import tkinter as tk
import numpy as np
import copy
import time


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


# basic colors
WHITE = rgb_to_hex((255, 255, 255))
GREY = rgb_to_hex((128, 128, 128))
YELLOW = rgb_to_hex((204, 204, 0))
BLUE = rgb_to_hex((50, 255, 255))
BLACK = rgb_to_hex((0, 0, 0))


class Gui:
    def __init__(self, board, mcts, debug_mode=False):
        # initialise display
        self.window = tk.Tk()
        self.window.title('Chess')
        self.window.geometry('800x600')
        self.window.resizable(False, False)
        self.__pieces = self.load_pieces()
        self.game = board
        self.mcts = mcts
        self.selected_piece = None
        self.left_frame = tk.Frame(
            self.window, width=200, height=600, bg='grey')
        self.left_frame.pack(side=tk.LEFT)
        self.right_frame = tk.Frame(
            self.window, width=600, height=600, bg='white')
        self.right_frame.pack(side=tk.RIGHT)
        self.pixel = tk.PhotoImage(width=0, height=0)
        self.__button_board = [[None for file in range(
            board.size)] for rank in range(board.size)]
        self.init_complete = False
        self.debug_mode = debug_mode
        self.init_gui()

    def init_gui(self):
        text = 'Play as White'
        button_white = tk.Button(
            self.left_frame, bg='white', text=text)
        button_white.config(borderwidth=0)
        button_white.config(command=self.play_white)
        button_white.bind('<Button-1>')
        button_white.pack(side=tk.TOP, pady=10)

        text = 'Play as Black'
        button_black = tk.Button(
            self.left_frame, bg='white', text=text)
        button_black.config(borderwidth=0)
        button_black.config(command=self.play_black)
        button_black.bind('<Button-1>')
        button_black.pack(side=tk.TOP, pady=10)

        self.left_frame.pack(side=tk.LEFT)
        self.window.mainloop()

    def play_white(self):
        self.init_complete = False
        self.game.setup()
        self.game.player_color = 'White'
        self.init_board(self.game)
        self.redraw_board()
        self.mcts.game = copy.deepcopy(self.game)
        self.init_complete = True

    def play_black(self):
        self.init_complete = False
        self.game.setup()
        self.game.player_color = 'Black'
        self.init_board(self.game)
        self.redraw_board()
        self.mcts.game = copy.deepcopy(self.game)
        self.init_complete = True

        if self.game.win_state == 'None' and self.debug_mode is False:
            self.mcts_move()

    def init_board(self, board):
        for rank in range(board.size):
            for file in range(board.size):
                if (rank + file) % 2 == 0:
                    color = WHITE
                else:
                    color = GREY
                square = board.square(file, rank)
                text = str(file) + str(' ') + str(rank)
                if square is 0:
                    button = tk.Button(
                        self.right_frame, image=self.pixel, width=98, height=98, bg=color, text=text)
                    button.config(borderwidth=0)
                    button.config(command=lambda file=file,
                                  rank=rank: self.click(file, rank))
                    self.__button_board[rank][file] = button # type: ignore
                else:
                    image = self.__pieces[square.color][square.piece_type]
                    button = tk.Button(
                        self.right_frame, image=image, width=98, height=98, bg=color, text=text)
                    button.config(borderwidth=0)
                    button.config(command=lambda file=file,
                                  rank=rank: self.click(file, rank))
                    self.__button_board[rank][file] = button # type: ignore
                if board.player_color == 'White':
                    button.grid(column=file, row=board.size - rank - 1)
                else:
                    button.grid(column=board.size - file - 1, row=rank)
                button.bind('<Button-1>', self.click(file, rank))
        self.right_frame.pack(side=tk.RIGHT)
        self.color_board()
        self.selected_piece = None

    def color_board(self):
        for rank in range(self.game.size):
            for file in range(self.game.size):
                if (rank + file) % 2 == 0:
                    color = WHITE
                else:
                    color = GREY
                self.__button_board[rank][file].config(bg=color) # type: ignore

    def redraw_board(self):
        for rank in range(self.game.size):
            for file in range(self.game.size):
                square = self.game.square(file, rank)
                if square == 0:
                    image = self.pixel
                else:
                    image = self.__pieces[square.color][square.piece_type]
                self.__button_board[rank][file].config(image=image) # type: ignore

    def click(self, file, rank):
        if not self.init_complete:
            return
        if self.game.win_state != 'None':
            return
        square = self.game.square(file, rank)
        if self.selected_piece is None:
            if self.debug_mode is True:
                if square != 0:
                    self.selected_piece = (file, rank)
                    print(self.selected_piece)
                    self.highlight_moves(file, rank)
                elif self.selected_piece == (file, rank):
                    # deselect piece
                    print('deselect piece' + str(self.selected_piece))
                    self.selected_piece = None
                    self.unhighlight_moves(file, rank)
            else:
                if square != 0 and square.color == self.game.state.player_turn:
                    self.selected_piece = (file, rank)
                    print(self.selected_piece)
                    self.highlight_moves(file, rank)
                elif self.selected_piece == (file, rank):
                    # deselect piece
                    print('deselect piece' + str(self.selected_piece))
                    self.selected_piece = None
                    self.unhighlight_moves(file, rank)
        else:
            # move piece
            self.unhighlight_moves(
                self.selected_piece[0], self.selected_piece[1]) # type: ignore
            moved = self.move_piece(file, rank)
            self.selected_piece = None

            if self.game.win_state == 'None' and moved:
                tic = time.perf_counter()
                self.mcts_move()
                toc = time.perf_counter()
                print(f"Time taken by mcts to move: {toc - tic:0.4f} seconds")

    def mcts_move(self):
        mcts_probs = self.mcts.search(self.game.state)
        best_action = np.argmax(mcts_probs)
        self.game.push(best_action, self.game.state)
        self.redraw_board()

    def move_piece(self, file, rank):
        move_list = self.game.square(
            self.selected_piece[0], self.selected_piece[1]).moves # type: ignore
        move = list(filter(lambda move: (move.dest_file,
                    move.dest_rank) == (file, rank), move_list))
        if len(move) == 0:
            return False
        move_id = self.game.action_space.encode(move[0])
        self.game.push(move_id, self.game.state)
        self.redraw_board()
        return True

    def highlight_moves(self, file, rank):
        self.game.square(file, rank).generate_moves(self.game.state.board)
        for move in self.game.square(file, rank).moves:
            self.highlight_square(move.dest_file, move.dest_rank)

    def highlight_square(self, file, rank):
        self.__button_board[rank][file].config(bg=BLUE)

    def unhighlight_moves(self, file, rank):
        for move in self.game.square(file, rank).moves:
            self.unhighlight_square(move.dest_file, move.dest_rank)

    def unhighlight_square(self, file, rank):
        if (file + rank) % 2 == 0:
            color = WHITE
        else:
            color = GREY
        self.__button_board[rank][file].config(bg=color)

    def load_pieces(self):
        pieces = {}
        pieces['White'] = {}
        pieces['Black'] = {}
        pieces['White']['Pawn'] = tk.PhotoImage(file='assets/white_pawn.png')
        pieces['White']['Rook'] = tk.PhotoImage(file='assets/white_rook.png')
        pieces['White']['Knight'] = tk.PhotoImage(
            file='assets/white_knight.png')
        pieces['White']['Queen'] = tk.PhotoImage(file='assets/white_queen.png')
        pieces['White']['King'] = tk.PhotoImage(file='assets/white_king.png')
        pieces['Black']['Pawn'] = tk.PhotoImage(file='assets/black_pawn.png')
        pieces['Black']['Rook'] = tk.PhotoImage(file='assets/black_rook.png')
        pieces['Black']['Knight'] = tk.PhotoImage(
            file='assets/black_knight.png')
        pieces['Black']['Queen'] = tk.PhotoImage(file='assets/black_queen.png')
        pieces['Black']['King'] = tk.PhotoImage(file='assets/black_king.png')
        return pieces
