import pygame, time, math, random, sys, neat, os
#https://www.youtube.com/watch?v=wQWWzBHUJWM&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&index=6

background = pygame.Surface((640, 400))
background.fill((250, 250, 250))

WIDTH, HEIGHT = 500, 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Ground():
    def __init__(self):
        self.image_1 = pygame.image.load("ground.png")

    def draw(self):
        screen.blit(self.image_1, (0,350))

GRAVITY = .25

class Birb():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_y = 0
        self.height = 40
        self.width = 30
        self.alive = True
        self.isJump = False
        self.jumpCount = 10
        self.front = self.x + self.width
        self.image_1 = pygame.image.load("flappy1.png")
        self.image_2 = pygame.image.load("flappy2.png")

    def draw(self, falling=0):
        if self.isJump:
            screen.blit(self.image_2, (self.x, self.y))
        else:
            screen.blit(self.image_1, (self.x, self.y))
        # pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.width, self.height))

    def fall(self):
        self.speed_y += GRAVITY
        self.y += self.speed_y

    def jump(self):
        # Check if Player is jumping and then execute the
        # jumping code.
        if self.isJump:
            if self.jumpCount >= 0:
                neg = 1
                if self.jumpCount < 0:
                    neg = 1
                self.y -= self.jumpCount**2 * 0.20 * neg
                self.jumpCount -= 1
            else:
                self.speed_y = 0
                self.isJump = False
                self.jumpCount = 10

class PipePair():
    def __init__(self, offset=0):
        offset = offset * random.choice([-1, 1]) # UP/DOWN
        self.x = 500
        self.y = 250 + offset
        self.speed = 2
        self.offset = offset
        self.image_1 = pygame.image.load("Pipeup.png")
        self.image_2 = pygame.image.load(" pipedown.png")

    def draw(self):
        self.x-=self.speed
        screen.blit(self.image_1, (self.x, self.y))
        screen.blit(self.image_2, (self.x, self.y - 310))

    def colission(self, birb):
        if birb.y > 350 or birb.y < -20:
            return 1

        if self.x < birb.x < (self.x + 75): # 75 is the width of the pipe - not changed with offset 
            # (birb.y > self.y)
            if (birb.y > self.y) or (birb.y < self.y-120):
                return 1
        return 0

def get_nearest_pipe_location(pipes, target_area):
    differences = [pipe.x - target_area if pipe.x - target_area > 0 else 1000 for pipe in pipes]
    closest_pipe = pipes[differences.index(min(differences))]
    return closest_pipe.y, closest_pipe.y-120 # 120 is the distane between the pipes

def main(genomes, config):
    nets, ge, birbs = [], [], []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birbs.append(Birb(WIDTH/2, HEIGHT/2))
        genome.fitness = 0
        ge.append(genome)

    ground = Ground()
    pipes = []
    score = 0

    while True:
        score += 1

        # make the first pipe TODO -> test moving it to init pipes declaration
        if not pipes:
            pipes.append(PipePair())

        # Add a pipe if it's time to!
        if pipes and pipes[-1].x < 300:
            pipes.append(PipePair(random.randint(25, 50)))

        # remove pipes from pipes[]
        if pipes and pipes[0].x < -40:
            pipes.pop(0)

        # get the position of the proper pipes
        pipe_position = get_nearest_pipe_location(pipes, birbs[0].x)
        for idx, birb in enumerate(birbs):
            decision = nets[idx].activate((birb.y, birb.y-pipe_position[0], pipe_position[1]-birb.y))
            if decision[0] >= 0.5:
                birb.isJump = True

        for birb in birbs:
            if not birb.isJump:
                birb.fall()
            birb.jump()

        clock.tick(FPS)
        screen.blit(background, (0,0))

        for pipe in pipes:
            for idx, birb in enumerate(birbs):
                if pipe.colission(birb):
                    ge[idx].fitness = score
                    birb.alive = False
            pipe.draw()
        
        ground.draw()

        for birb in birbs:
            if birb.alive:
                birb.draw()

        ground.draw()
        pygame.display.flip()

        if not any([birb.alive for birb in birbs]):
            #pygame.quit()
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

