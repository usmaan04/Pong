import pygame

class Paddles:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 75

    def reset_positions(self,screen):
        self.y = 400/3
        
    def move_down(self):
        # Move the player left by subtracting from the x coordinate
        self.y += 5

    def move_up(self):
        # Move the player right by adding to the x coordinate
        self.y -= 5


    def update(self,screen):
        
        # Check if the paddle hits the bottom of the screen
        if self.y >= 325:
            self.y = 325 

        # Check if the ball hits the top of the screen
        if self.y <= 0:
            self.y = 0
            
        pygame.draw.rect(screen, (255,255,255),(self.x, self.y, self.width, self.height))
            
