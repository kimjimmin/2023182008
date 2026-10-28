from pico2d import *
import boy
import grass


INPUT_EVENT_TYPES = (
    SDL_KEYDOWN,
    SDL_KEYUP,
    SDL_MOUSEMOTION,
    SDL_MOUSEBUTTONDOWN,
    SDL_MOUSEBUTTONUP,
    SDL_MOUSEWHEEL,
)


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

        if event.type in INPUT_EVENT_TYPES:
            boy_obj.handle_event(event)


def reset_world():
    global world, boy_obj

    world = []

    grass_obj = grass.Grass()
    world.append(grass_obj)

    boy_obj = boy.Boy()
    world.append(boy_obj)


def update_world():
    for game_object in world:
        game_object.update()


def render_world():
    clear_canvas()
    for game_object in world:
        game_object.draw()
    update_canvas()


running = True
open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
