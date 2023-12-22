import pygame
import random

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: str, text: str = None, font: pygame.font.Font = None, color: tuple = (255, 255, 255)):
        super().__init__()
        self._image = image
        self._text = text
        self._font = font
        self._color = color
        self._rect = None

        # if no image is provided, create a blank surface
        if not self._image:
            self._image = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # if no font is provided, use the default pygame font
        if not self._font:
            self._font = pygame.font.Font(pygame.font.get_default_font(), 20)

        # if no text is provided, use the default text
        if not self._text:
            self._text = "Hello World!"

        # create the image
        self._image = self._font.render(self._text, True, self._color)
        self._rect = self._image.get_rect()

        # set it's position to a random place on the screen
        self._rect.x = random.randint(0, DISPLAY_WIDTH - self._rect.width)
        self._rect.y = random.randint(0, DISPLAY_HEIGHT - self._rect.height)

        # movement variables
        self._move_direction = random.randint(-4, 4)
        self._move_speed_x = random.choice([-1, 1])
        self._move_speed_y = random.choice([-1, 1])

    @property
    def move_direction(self):
        return self._move_direction

    @move_direction.setter
    def move_direction(self, value):
        self._move_direction = value

    @property
    def image_rect(self):
        return self._image.get_rect()

    @image_rect.setter
    def image_rect(self, value):
        self._image = pygame.transform.scale(self._image, value)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value

    def draw(self, surface: pygame.Surface):
        surface.blit(self._image, self._rect)

    def move(self, x: int, y: int):
        self._rect.move_ip(x, y)

    def update(self):
        self._rect.x += self._move_speed_x
        self._rect.y += self._move_speed_y
        if self._rect.left < 0 or self._rect.right > DISPLAY_WIDTH:
            self._move_speed_x *= -1
        if self._rect.top < 0 or self._rect.bottom > DISPLAY_HEIGHT:
            self._move_speed_y *= -1

    def check_collision(self, sprite: pygame.sprite.Sprite):
        return self._rect.colliderect(sprite.rect)


class RPSGame:
    def __init__(self):
        self._screen = None
        self._clock = None

        self._ui_running = True

        self.all_sprites = pygame.sprite.Group()

        self.init()
        # test sprite
        self.test_sprite = Sprite(
            pygame.Surface((self.screen_width, self.screen_height)), "Hello World!"
        )
        self.all_sprites.add(self.test_sprite)

        for i in range(10):
            self.all_sprites.add(
                Sprite(
                    pygame.Surface((self.screen_width, self.screen_height)),
                    "Hello World!",
                )
            )

        self.coll_sprites = pygame.sprite.Group()
        # collision test
        self.collision_sprite = Sprite(
            pygame.Surface((self.screen_width, self.screen_height)), "Boom!"
        )
        self.collision_sprite.rect.x = 100
        self.collision_sprite.rect.y = 100
        self.all_sprites.add(self.collision_sprite)
        self.coll_sprites.add(self.collision_sprite)

    @property
    def screen(self):
        return self._screen

    @property
    def clock(self):
        return self._clock

    def init(self):
        """Initialize the game."""
        pygame.init()
        pygame.display.set_caption("Pygame window")
        self._screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self._clock = pygame.time.Clock()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

    def quit(self):
        """Quit the game."""
        pygame.quit()

    def update(self):
        """Update the game."""
        pass

    def show(self):
        """Show the game screen."""
        self._screen.fill((0, 0, 0))
        pygame.display.update()
        self._clock.tick(60)

        while self._ui_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._ui_running = False

            self._screen.fill((0, 0, 0))

            for i in self.all_sprites:
                i: Sprite  # type hinting
                i.draw(self._screen)
                i.update()
                print(i.check_collision(self.collision_sprite))
                if i in self.coll_sprites:
                    i.color = (255, 0, 0)

            self.update()
            pygame.display.update()
            self._clock.tick(60)
