from board import Board

board = Board(6)
# board.setup()
# board.fenn_decode('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R')
board.fenn_decode('rnqknr/pppppp///PPPPPP/RNQKNR')
board.print()