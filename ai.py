import pygame

class AI:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 75

    def reset_positions(self,screen):
        self.y = 400/3
        
    def move(self,ball):
        if ball.y > self.y:
            # Move the AI to the right towards the ball
            self.y += 5
        #If ball is abovethe AI
        elif ball.x < self.x :
            # Move the AI up towards the ball
            self.y -= 5
            
    def update(self,screen):
        
        # Check if the paddle hits the bottom of the screen
        if self.y >= 325:
            self.y = 325 

        # Check if the ball hits the top of the screen
        if self.y <= 0:
            self.y = 0
            
        pygame.draw.rect(screen, (255,255,255),(self.x, self.y, self.width, self.height))
            
