import pygame
import main
import colors

class Button():
    def __init__(self, SCREEN, color, x, y, width, height, text=''):
        self.SCREEN = SCREEN;
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self):
        global clicked
        mouse_pos = pygame.mouse.get_pos()


        if self.button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.draw.rect(self.SCREEN,colors.WHITE, self.button_rect)
            else:
                pygame.draw.rect(self.SCREEN,self.color, self.button_rect)

        else:
            pygame.draw.rect(self.SCREEN,self.color, self.button_rect)

        pygame.draw.line(self.SCREEN, colors.WHITE, (self.x,self.y),(self.x + self.width,self.y),2)
        pygame.draw.line(self.SCREEN, colors.WHITE, (self.x, self.y), (self.x,  self.y + self.height), 2)
        pygame.draw.line(self.SCREEN, colors.BLACK, (self.x, self.y+self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(self.SCREEN, colors.BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y+self.height), 2)

        font = pygame.font.SysFont('Arial',20)
        text = font.render(self.text,True,colors.BLACK)
        self.SCREEN.blit(text,(self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
