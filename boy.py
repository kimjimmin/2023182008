from math import pi
from pico2d import (
    SDL_KEYDOWN,
    SDL_KEYUP,
    SDLK_a,
    SDLK_LEFT,
    SDLK_RIGHT,
    get_time,
    load_image,
)


# Both sprite sheets have a one-pixel border around 100 x 100 frames.
# pico2d uses the bottom-left corner as the origin when clipping an image.
FRAME_SIZE = 100
FRAME_COUNT = 8
SHEET_BORDER = 1
RUN_SPEED = 4
AUTO_RUN_SPEED = 8
AUTO_RUN_SIZE = 150
AUTO_RUN_DURATION = 5.0


def frame_left(frame):
    return SHEET_BORDER + frame * FRAME_SIZE


class Idle:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        boy.animation_time = get_time()
        boy.last_input_time = get_time()

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        now = get_time()
        if now - boy.last_input_time >= 5.0:
            boy.change_state(Sleep)
            return

        if now - boy.animation_time >= 0.12:
            boy.frame = (boy.frame + 1) % FRAME_COUNT
            boy.animation_time = now

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_draw(
                frame_left(boy.frame), 301,
                FRAME_SIZE, FRAME_SIZE, boy.x, boy.y
            )
        else:
            boy.image.clip_draw(
                frame_left(boy.frame), 201,
                FRAME_SIZE, FRAME_SIZE, boy.x, boy.y
            )


class Run:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        boy.animation_time = get_time()

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * RUN_SPEED
        boy.x = max(50, min(750, boy.x))

        now = get_time()
        if now - boy.animation_time >= 0.08:
            boy.frame = (boy.frame + 1) % FRAME_COUNT
            boy.animation_time = now

    @staticmethod
    def draw(boy):
        flip = '' if boy.face_dir == 1 else 'h'
        boy.run_image.clip_composite_draw(
            frame_left(boy.frame), SHEET_BORDER, FRAME_SIZE, FRAME_SIZE,
            0, flip,
            boy.x, boy.y, FRAME_SIZE, FRAME_SIZE
        )


class AutoRun:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        boy.dir = boy.face_dir
        boy.animation_time = get_time()
        boy.auto_run_start_time = get_time()

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        now = get_time()

        if now - boy.auto_run_start_time >= AUTO_RUN_DURATION:
            boy.dir = 0
            boy.change_state(Idle)
            return

        boy.x += boy.dir * AUTO_RUN_SPEED

        half_size = AUTO_RUN_SIZE // 2
        if boy.x <= half_size:
            boy.x = half_size
            boy.dir = 1
            boy.face_dir = 1
        elif boy.x >= 800 - half_size:
            boy.x = 800 - half_size
            boy.dir = -1
            boy.face_dir = -1

        if now - boy.animation_time >= 0.06:
            boy.frame = (boy.frame + 1) % FRAME_COUNT
            boy.animation_time = now

    @staticmethod
    def draw(boy):
        flip = '' if boy.face_dir == 1 else 'h'
        boy.run_image.clip_composite_draw(
            frame_left(boy.frame), SHEET_BORDER, FRAME_SIZE, FRAME_SIZE,
            0, flip,
            boy.x, boy.y + 25, AUTO_RUN_SIZE, AUTO_RUN_SIZE
        )


class Sleep:
    @staticmethod
    def enter(boy):
        boy.frame = 0

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        sprite_y = 301 if boy.face_dir == 1 else 201
        boy.image.clip_composite_draw(
            frame_left(0), sprite_y, FRAME_SIZE, FRAME_SIZE,
            pi / 2, '',
            boy.x, boy.y - 20, FRAME_SIZE, FRAME_SIZE
        )


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.left_pressed = False
        self.right_pressed = False
        self.image = load_image('animation_sheet.png')
        self.run_image = load_image('run_animation.png')
        self.state = Idle
        self.last_input_time = get_time()
        self.animation_time = get_time()
        self.state.enter(self)

    def change_state(self, next_state):
        self.state.exit(self)
        self.state = next_state
        self.state.enter(self)

    def handle_event(self, event):
        self.last_input_time = get_time()

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a and self.state is Idle:
                self.change_state(AutoRun)
                return

            if event.key == SDLK_LEFT:
                self.left_pressed = True
            elif event.key == SDLK_RIGHT:
                self.right_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.left_pressed = False
            elif event.key == SDLK_RIGHT:
                self.right_pressed = False

        input_dir = int(self.right_pressed) - int(self.left_pressed)

        if input_dir != 0:
            self.dir = input_dir
            self.face_dir = 1 if input_dir > 0 else -1
            if self.state is not Run:
                self.change_state(Run)
        elif self.state is Run:
            self.dir = 0
            self.change_state(Idle)
        elif self.state is Sleep:
            self.dir = 0
            self.change_state(Idle)

    def update(self):
        self.state.do(self)

    def draw(self):
        self.state.draw(self)
