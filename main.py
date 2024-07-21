import Visuallize
import pygame
import random
import sys
from Utils import createState, print_boards, generateNewState
from Board import Board
from Button import Button
from level1 import DFS, UCS, IDS, BFS, GBFS, Asearch
from level3 import A_star_search,gbfs
from level2 import Asearch2,UCS_2
from level4 import A_star_search_lv4
if __name__ == "__main__":

    matrix,time,fuel = Visuallize.read_file("input_1_level4_1.txt")
    board = Board(matrix, time, fuel)
    #Call search function here

    #Visualize map 
    #print(limit)
    vehicles = 3
    Boards = createState(board, vehicles) 
    # coordinate = (1,3)
    # new_board = generateNewState(Boards[1], 1,  coordinate)
    # new_board.print_board()
    print_boards(Boards)
    paths = A_star_search_lv4(Boards)
    print(paths)
    # for row in new_board.matrix:
    #     print(f"\t\t{row}")  # Print each row of the matrix with indentation


   # Visuallize.start_lv4()

    

