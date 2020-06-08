""" Followed this guy https://www.youtube.com/watch?v=V_f07t570pA """
import pygame
import sys
import random
import time

class Snake():
    def __init__(self):
        self.position=[100, 60]
        self.body=[[100, 60], [80, 60], [60, 60]]
        self.direction = "Right"
        self.changeDirectionTo = self.direction

    def changeDirTo(self, direct):
        if direct=="Right" and not self.direction=="Left":
            self.direction="Right"
        elif direct=="Left" and not self.direction=="Right":
            self.direction="Left"
        elif direct=="Up" and not self.direction=="Down":
            self.direction="Up"
        elif direct=="Down" and not self.direction=="Up":
            self.direction="Down"
    
    def move(self, foodPosition):
        if self.direction == "Right":
            self.position[0]+=20 # if moving right -> update x cord of position
        if self.direction == "Left":
            self.position[0]-=20 # if moving right -> update x cord of position
        if self.direction == "Up":
            self.position[1]-=20 # if moving right -> update x cord of position
        if self.direction == "Down":
            self.position[1]+=20 # if moving right -> update x cord of position
        
        self.body.insert(0, list(self.position)) # Add a new body piece - remove tail isf we didnt hit a food piece

        if self.position == foodPosition: 
            return 1 # generate a new food 
        else:
            self.body.pop()
            return 0 # remove last element of the body
    
    # now check if the snake has hit the wall or itself
    def checkCollision(self):
        if self.position[0] > 500 or self.position[0] < 0: # extreme left and right
            return 1 # yes weve collided with wall 
        elif self.position[1] > 500 or self.position[1] < 0:
            return 1
       
       # we exclude the head - then check if the head has hit another body - part
        for bodyPart in self.body[1:]:
            if self.position == bodyPart:
                print("Fack")
                return 1
        
        return 0

    def getHeadPosition(self):
        return self.position
    
    def getBody(self):
        # proabbly wotn use this
        return self.body
    
class Food():
    def __init__(self):
        self.position = [random.randrange(1,25)*20, random.randrange(1,25)*20]
        self.isFoodOnScreen = True

    def spawnFood(self):
        if self.isFoodOnScreen == False: # change this with 'not'
            self.position = [random.randrange(1,25)*20, random.randrange(1,25)*20]
            self.isFoodOnScreen = True
        return self.position

    def setFoodOnScreen(self, b:bool):
        self.isFoodOnScreen=b
    

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("NICK MADE SNAKE")
fps = pygame.time.Clock()

score = 0
snake = Snake()
food = Food()

def gameOver():
    pygame.quit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                print("RIGHT")
                snake.changeDirTo("Right")
            elif event.key == pygame.K_LEFT:
                print("LEFt")
                snake.changeDirTo("Left")
            elif event.key == pygame.K_UP:
                print("UP")
                snake.changeDirTo("Up")
            elif event.key == pygame.K_DOWN:
                print("DOWN")
                snake.changeDirTo("Down")
        
    
    foodPosition = food.spawnFood()
    
    if snake.move(foodPosition)==1:
        score+=1
        food.setFoodOnScreen(False)

    window.fill([255,255,255])

    for part in snake.getBody():
        pygame.draw.rect(window, [0,0,0], [part[0], part[1], 20, 20], 0) # len width of 10 10
    
    # draw food
    pygame.draw.rect(window, pygame.Color(225, 0, 0), pygame.Rect(foodPosition[0], foodPosition[1], 20, 20)) # len width of 10 10

    pygame.display.update()

    if snake.checkCollision():
        gameOver()

    
    
    pygame.display.set_caption("Score: ", str(score))
    fps.tick(16)
