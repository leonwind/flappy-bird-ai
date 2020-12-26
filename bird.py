import pygame


class Bird:
    VELOCITY = -10
    GRAVITY = 5

    def __init__(self, pos_x, pos_y, bird_img):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity = 0
        self.time_since_jump = 0

        self.bird_img: pygame.Surface = bird_img

    def jump(self):
        self.time_since_jump = 0

    def move(self):
        self.time_since_jump += 1

        # formular for projectile motion
        displacement = self.VELOCITY * self.time_since_jump + \
            0.5 * self.GRAVITY * self.time_since_jump ** 2

        self.pos_y += displacement

    def get_mask(self) -> pygame.Mask:
        return self.bird_img.get_mask()

    def draw(self):
        pass