from pico2d import *
import random
from pathlib import Path

IMAGE_DIR = Path(__file__).resolve().parent

class Grass:
    def __init__(self):
        self.image = load_image(str(IMAGE_DIR / 'grass.png'))

    def draw(self):
        self.image.draw(400, 30)
    def update(self): pass

class Ball:
    def __init__(self):
        self.image = load_image(str(IMAGE_DIR / 'ball21x21.png'))
        self.x, self.y = random.randint(0, 800), 90
        self.up_speed = random.randint(3, 13)
        pass
    def draw(self):
        self.image.draw(self.x, self.y)
        pass
    def update(self):
        if(self.y < 600):
            self.y += self.up_speed
        else :
            self.y = 550
        pass

class Boy:
    def __init__(self):
        self.x, self.y = random.randint(0, 800), 90
        self.frame = random.randint(0, 7)
        self.image = load_image(str(IMAGE_DIR / 'run_animation.png'))

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)

class Zombie:
    def __init__(self):
        self.x, self.y = random.randint(0, 800), 300
        self.frame = random.randint(0, 9)
        self.image = load_image(str(IMAGE_DIR / 'zombie_run_animation.png'))

    def update(self):
        self.frame = (self.frame + 1) % 10
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 430, 0, 430, 519,
                             self.x, self.y)

def reset_world():
    global running
    global world

    running = True
    world = []
    
    grass = Grass()
    world.append(grass)
    zombie = Zombie()
    world.append(zombie)
    balls = [Ball() for i in range(20)]
    world += balls
    
    team = [Boy() for i in range(11)]
    world += team

    

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas()
reset_world()

while running:
    #handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()





