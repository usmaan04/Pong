import pygame,sys
import random
from button import Button
from paddles import Paddles
from ai import AI

#Initialise pygame
pygame.init()

# Set up the game window
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the scores for the players 
player1_score = 0
player2_score = 0

class Ball:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed_x = 1
        self.speed_y = 1
        self.radius = 10

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def reset_position(self):
        self.x = 300
        self.y = 200

    def update(self,screen,Player1,AI,Player2):
        # Check if the ball hits the bottom of the screen
        if self.y + self.radius >= 400:
            # Reverse the ball's direction and reduce its speed when it hits the ground
            self.speed_y = abs(self.speed_y) * -1;

        # Check if the ball hits the top of the screen
        if self.y - self.radius < 0:
            # Reverse the ball's direction and reduce its speed when it hits the ceiling
            self.speed_y = abs(self.speed_y) 

        # Check if the ball hits the left of the screen
        if self.x - self.radius <= 0:
            self.speed_x = abs(self.speed_x);
            global player2_score
            player2_score +=1
            self.reset_position()

        # Check if the ball hits the right of the screen
        if self.x + self.radius >= 600:
            self.speed_x = abs(self.speed_x) * -1;
            global player1_score
            player1_score +=1
            self.reset_position()

        # Check collision with Player1's paddle
        if (
            self.x - self.radius <= Player1.x + Player1.width
            and Player1.y <= self.y <= Player1.y + Player1.height
        ):
            self.speed_x = abs(random.randint(2, 4))

        # Check collision with Player2's paddle
        if (
            self.x + self.radius >= Player2.x
            and Player2.y <= self.y <= Player2.y + Player2.height
        ):
            self.speed_x = -abs(random.randint(2, 4))

        # Check collision with Player2's paddle
        if (
            self.x + self.radius >= AI.x
            and AI.y <= self.y <= AI.y + AI.height
        ):
            self.speed_x = -abs(random.randint(2, 4))
            
        pygame.draw.circle(screen, (255,255,255),(self.x,self.y),self.radius)
            
# Creates instances of the player and AI class for characters
Player1 = (Paddles(25, screen_height/3))
Player2 = (Paddles(screen_width - 50,screen_height/3))
AI = (AI(screen_width - 50,screen_height/3))
ball = (Ball(screen_width/2,screen_height/2))

def create_ball():
    global ball
    ball = (Ball(screen_width/2,screen_height/2))

# Return a font with a specified size
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Multi line paragraphing
def drawText(surface, text, colour, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    #gets the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside the created surface box
        if y + fontHeight > rect.bottom:
            break

        # determines the maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if the text has just been wrapped, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and displays it to the surface
        if bkg:
            image = font.render(text[:i], 1, colour, bkg)
            image.set_colourkey(bkg)
        else:
            image = font.render(text[:i], aa, colour)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text just blit
        text = text[i:]

    return text

def instructions():
    while True:
        # Get the current mouse position
        INSTRUCTIONS_POS = pygame.mouse.get_pos()
        
        # Set the window caption to "Instructions"
        pygame.display.set_caption("Instructions")
        
        screen.fill((0, 0, 0))

        # Create a game description text object, display it on a rectangle on the screen
        game_description = "The objective of Pong is to score points by successfully hitting a ball past your opponents paddle.                                                                                         1. The game begins with the ball in the center of the screen                                                                         2. The ball will start moving in a random direction towards one of the players.                                          3. Use your paddle to hit the ball and send it towards the opponent.                                   4. If you fail to hit the ball and it passes your paddle, the opposing player scores a point.                   5. The ball will bounce off the paddles, changing direction at a random speed with each impact."

        description_rect = pygame.draw.rect(screen, (0, 0, 00), pygame.Rect(5, 0, screen_width, screen_height- 50))
        drawText(screen, game_description, "White", description_rect, get_font(20))

        # Create a back button object and display it on the screen
        back_button = Button(image=pygame.image.load("assets/button.png"), pos=(screen_width - 300, screen_height - 50),     
                            text_input="Back", font=get_font(25), base_colour="White", hovering_colour="Green")
        back_button.changeColour(INSTRUCTIONS_POS)          
        back_button.update(screen)

       # Listen for events like button clicks and mouse movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Call function to switch screen if button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:                    
                if back_button.checkForInput(INSTRUCTIONS_POS):    
                    main_menu()
                    
        # Update the display to show any changes
        pygame.display.update()

def one_player():
    ball.x = screen_width/2
    ball.y = screen_height/2
    ball.speed_x = random.choice([-1, 1])
    ball.speed_y = random.choice([-1, 1])
    Player1.reset_positions(screen)
    Player2.reset_positions(screen)
    global player1_score
    player1_choice = 0
    global player2_score
    player2_score = 0
    while True:
        # Get the current mouse position
        ONE_PLAYER_POS = pygame.mouse.get_pos()
        
        # Set the window caption to "Two Player"
        pygame.display.set_caption("Two Player")

        # Display the background colour
        screen.fill((0, 0, 0))

        # Create a back button object and display it on the screen
        back_button = Button(image=pygame.image.load("assets/button.png"), pos=(screen_width/2, screen_height - 50),     
                            text_input="Back", font=get_font(30), base_colour="White", hovering_colour="Green")

        Player1.update(screen)
        AI.move(ball)
        AI.update(screen)
        ball.move()
        ball.update(screen,Player1,AI,Player2)

        scoreboard_player1 = get_font(40).render("{}".format(player1_score), True, (255, 255, 255))
        scoreboard_player2 = get_font(40).render("{}".format(player2_score), True, (255, 255, 255))
        screen.blit(scoreboard_player1, (screen_width/2 -50, 5 ))
        screen.blit(scoreboard_player2, (screen_width/2 + 25, 5))
        
        for y in range(0, screen_height, screen_height//13):
            pygame.draw.rect(screen, (255,255,255), (screen_width//2 - 5, y, 5, screen_height//20))

        back_button.changeColour(ONE_PLAYER_POS)
        back_button.update(screen)
        
        # Listen for events like button clicks and mouse movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Call function to allow draw choice or switch screen if button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(ONE_PLAYER_POS):
                    ball.x = screen_width/2
                    ball.y = screen_height/2
                    main_menu()

        # Listen for keyboard inputs to control the player character's movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            Player1.move_down()
        if keys[pygame.K_w]:
            Player1.move_up()
                    
        # Update the display to show any changes 
        pygame.display.update()
        
def two_player():
    ball.x = screen_width/2
    ball.y = screen_height/2
    ball.speed_x = random.choice([-1, 1])
    ball.speed_y = random.choice([-1, 1])
    Player1.reset_positions(screen)
    Player2.reset_positions(screen)
    global player1_score
    player1_choice = 0
    global player2_score
    player2_score = 0
    while True:
        # Get the current mouse position
        TWO_PLAYER_POS = pygame.mouse.get_pos()
        
        # Set the window caption to "Two Player"
        pygame.display.set_caption("Two Player")

        # Display the background colour
        screen.fill((0, 0, 0))

        # Create a back button object and display it on the screen
        back_button = Button(image=pygame.image.load("assets/button.png"), pos=(screen_width/2, screen_height - 50),     
                            text_input="Back", font=get_font(30), base_colour="White", hovering_colour="Green")
        Player1.update(screen)
        Player2.update(screen)
        ball.move()
        ball.update(screen,Player1,AI,Player2)

        scoreboard_player1 = get_font(40).render("{}".format(player1_score), True, (255, 255, 255))
        scoreboard_player2 = get_font(40).render("{}".format(player2_score), True, (255, 255, 255))
        screen.blit(scoreboard_player1, (screen_width/2 -50, 5 ))
        screen.blit(scoreboard_player2, (screen_width/2 + 25, 5))
        
        for y in range(0, screen_height, screen_height//13):
            pygame.draw.rect(screen, (255,255,255), (screen_width//2 - 5, y, 5, screen_height//20))

        back_button.changeColour(TWO_PLAYER_POS)
        back_button.update(screen)

        # Listen for events like button clicks and mouse movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Call function to allow draw choice or switch screen if button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(TWO_PLAYER_POS):
                    main_menu()

        # Listen for keyboard inputs to control the player character's movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            Player1.move_down()
        if keys[pygame.K_w]:
            Player1.move_up()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            Player2.move_down()
        if keys[pygame.K_UP]:
            Player2.move_up()
                    
        # Update the display to show any changes 
        pygame.display.update()
        
def main_menu():
    while True:
        # Get the current mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Set the window caption to "Main Main"
        pygame.display.set_caption("Main Menu")

        screen.fill((0, 0, 0))
        
        screen.blit(get_font(40).render('Pong', True, (255, 255, 255)),(screen_width/2 - 50 , screen_height/5))

        oneplayer_button = Button(image=pygame.image.load("assets/button.png"), pos=(screen_width - 400, screen_height - 170),     
                            text_input="One Player", font=get_font(25), base_colour="White", hovering_colour="Green")
        twoplayer_button = Button(image=pygame.image.load("assets/button.png"), pos=(screen_width - 200, screen_height - 170),     
                            text_input="Two Player", font=get_font(25), base_colour="White", hovering_colour="Green")
        instruction_button = Button(image=pygame.image.load("assets/button.png"), pos=(screen_width/2, screen_height - 100),     
                            text_input="Instructions", font=get_font(25), base_colour="White", hovering_colour="Green")
        
        # Update all buttons
        for button in [oneplayer_button, twoplayer_button, instruction_button]:                           
            button.changeColour(MENU_MOUSE_POS)          
            button.update(screen)

        # Listen for events like button clicks and mouse movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Call function to switch screen if button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:                    
                if instruction_button.checkForInput(MENU_MOUSE_POS):    
                    instructions()
                elif oneplayer_button.checkForInput(MENU_MOUSE_POS):
                    one_player()
                elif twoplayer_button.checkForInput(MENU_MOUSE_POS):
                    two_player()

        pygame.display.update()

main_menu()
