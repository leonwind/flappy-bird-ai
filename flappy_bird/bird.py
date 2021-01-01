import pygame


class Bird:
    VELOCITY = -10.5
    GRAVITY = 3
    MAX_DISPLACEMENT = 20

    def __init__(self, pos_x, pos_y, bird_img):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.alive = True
        self.time_since_jump = 0

        self.bird_img: pygame.Surface = bird_img

    def jump(self):
        self.time_since_jump = 0

    def move(self):
        """
        Move the bird using the projectile motion formula
        Limit the maximum falling speed to let the bird glide 
        """
        self.time_since_jump += 1

        displacement = \
            self.VELOCITY * self.time_since_jump + 0.5 * self.GRAVITY * self.time_since_jump ** 2

        # limit falling speed
        displacement = min(displacement, self.MAX_DISPLACEMENT)

        self.pos_y += displacement

    def get_mask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.bird_img)

    def draw(self, window: pygame.Surface):
        window.blit(self.bird_img, (self.pos_x, self.pos_y))
