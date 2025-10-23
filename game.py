import pygame
from board import Board
from grid import Grid

pygame.init()

screen = pygame.display.set_mode((720, 900))
pygame.display.set_caption("Fruit digging")

board = Board(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.handle_click(event.pos)

    board.drawBoard()

pygame.quit()