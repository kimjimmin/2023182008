from pico2d import load_image


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        # grass.png is 802 x 62: the actual grass is the inner 800 x 60 area.
        self.image.clip_draw(1, 1, 800, 60, 400, 30)

    def update(self):
        pass
