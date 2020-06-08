""" Followed this guy https://www.youtube.com/watch?v=V_f07t570pA """
import pygame
import sys
import random
import time
import numpy as np
import os, neat

window = pygame.display.set_mode((500, 500))
fps = pygame.time.Clock()
DIR_MAPPINGS = ["Left", "Right", "Up", "Down"]

class Snake():
    def __init__(self):
        self.alive = True
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
    def draw(self, window):
        for part in self.body:
            pygame.draw.rect(window, [0,0,0], [part[0], part[1], 20, 20], 0)
    
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
    
    def draw(self, window):
        pygame.draw.rect(window, pygame.Color(225, 0, 0), pygame.Rect(self.position[0], self.position[1], 20, 20)) # len width of 10 10
    
def get_space_encoding(snake: Snake, food: Food):
    #25 * 25 board, + direction + head location + food location
    snake_direction = [0] * 4
    snake_direction[DIR_MAPPINGS.index(snake.direction)] = 1

    # get the gameboard of where the body is
    mapps = np.zeros((25, 25))
    for body_part in snake.body:
        mapps[int(body_part[0]/20)-1][int(body_part[1]/20)-1] = 1

    encoding = list(mapps.flatten()) + snake.position + snake_direction + food.position
    return encoding

def main(genomes, config):
    nets, ge, snakes, foods = [], [], [], []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake())
        foods.append(Food())
        genome.fitness = 0
        ge.append(genome)

    score = 0

    while True:
        for idx, snake in enumerate(snakes):
            if snake.alive:
                decision = nets[idx].activate((get_space_encoding(snake, foods[idx])))
                direction = DIR_MAPPINGS[decision.index(max(decision))]
                snake.changeDirTo(direction)

        for food in foods:
            food.spawnFood()
        
        for food, snake, gene in zip(foods, snakes, ge):
            if snake.alive and snake.move(food.position)==1:
                # Give a lot of fitness for getting a food
                gene.fitness += 1000
                food.setFoodOnScreen(False)

        window.fill([255,255,255])

        for snake, food, gene in zip(snakes, foods, ge):
            if snake.alive:
                # give 1 fitness so its incentivised to survive
                gene.fitness += 1
                snake.draw(window)
                food.draw(window)
    
        pygame.display.update()

        for snake in snakes:
            if snake.checkCollision():
                snake.alive = False

        fps.tick(16)

        if not any([snake.alive for snake in snakes]):
            print("broke")
            break

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # run(fitness_function, generations) 
    # it passes main(genome, config)
    winner = pop.run(main, 50)

if __name__ == "__main__":
    config = "config_neat.txt"
    config_path = os.path.join("configs", config)
    run(config_path)
