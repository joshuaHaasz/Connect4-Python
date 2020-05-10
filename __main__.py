from connect4 import Connect4
from connect4_with_ai import Connect4AI
import pygame
import sys
class Game(object):
    def __init__(self):
        pygame.init()
        self.game = None
        self.menu = True
        self.playing = False
        self.screen = pygame.display.set_mode((700,700))
        self.myfont = pygame.font.SysFont("monospace", 50)
        self.exit = False
        self.create_menu()
        self.play()

    def create_menu(self):
        box1 = pygame.draw.rect(self.screen, (0,128,255), pygame.Rect(125,125,435,120))
        box1 = pygame.draw.rect(self.screen, (0, 128, 255), pygame.Rect(125, 425, 435, 120))
        label1 = self.myfont.render(f"2 Player Mode", 1, (255,0,0))
        label2 = self.myfont.render(f"Single player", 1, (255, 0, 0))
        self.screen.blit(label1, (150,150))
        self.screen.blit(label2, (150, 450))
        pygame.display.update()

    def return_to_menu(self):
        box = pygame.draw.rect(self.screen, (0,128,255), pygame.Rect(0,0,100,100))
        label = self.myfont.render(f"Quit", 1, (255, 0, 0))
        self.screen.blit(label, (10, 10))
        pygame.display.update()

    def play(self):
        while not self.exit:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        if 125 <= pos[0] <= 560:
                            if 125 <= pos[1] <= 245:
                                game = Connect4()
                                game.main_loop()
                            elif 425 <= pos[1] <= 545:
                                game = Connect4AI()
                                game.main_loop()
                    self.screen.fill((0,0,0))
                    self.create_menu()



        pygame.time.wait(3000)








if __name__ == "__main__":
    # Load main screen. Give option of playing against AI or amother play. When game over return to menu screen. Be able to quit
    Game()