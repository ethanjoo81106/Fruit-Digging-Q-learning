import pygame
from Display.board import Board

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((720, 900))
pygame.display.set_caption("Fruit digging")

board = Board(screen)

running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.handle_click(event.pos)

    board.draw_board()

pygame.quit()