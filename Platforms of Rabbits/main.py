import pygame
import sys

#boss fight, falling enemy boss projectiles, coins, shop, secret room with chester who has a gun.

# Game settings
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPEED = 5

# Visual and collision dimensions
IMAGE_HEIGHT = 100         # visual height of sprite
HITBOX_HEIGHT = 68         # smaller hitbox height (feet area)
JUMP_POWER = 15
GRAVITY = 1

# Colors
PLATFORM_COLOR = (0, 0, 0)
BG_COLOR = (200, 220, 255)
GRID_SPACING = 50
GRID_COLOR = (180, 200, 230)  # Light blue-gray for visibility on BG

#LEVEL2 = [pygame.Rect(100, 220, 500, 20), pygame.Rect(100, 120, 700, 20), pygame.Rect(-100, 320, 200, 20)] #medium -> big -> small = final level

# Platform layout
Wall = pygame.Rect(-20, 0, 10, 600)
Wallb = pygame.Rect(810, 100, 100000000, 500)
LEVEL1 = [Wall, Wallb, pygame.Rect(0, 500, 800, 40), pygame.Rect(500, 400, 200, 20), pygame.Rect(700, 320, 100, 20)] #big -> medium -> small
LEVEL2 = [pygame.Rect(-50, 0, 10, 600), Wallb, pygame.Rect(100, 220, 100, 20), pygame.Rect(120, 120, 700, 20), pygame.Rect(-150, 320, 250, 20)] #medium -> big -> small
LEVEL3 = [pygame.Rect(-50, 0, 10, 600), Wallb, pygame.Rect(-75, 500, 375, 40), pygame.Rect(500, 250, 700, 20)] #yea
LEVEL4 = [pygame.Rect(-50, 0, 10, 600), Wallb, pygame.Rect(-250, 500, 325, 40)]
LEVEL678 = [pygame.Rect(-50, 0, 10, 600), Wallb, pygame.Rect(500, 400, 200, 20)]
LEVELS = [LEVEL1, LEVEL2, LEVEL3, LEVEL4]


class Springs:
    def __init__(self, x, y):
        image_original = pygame.image.load("spring.png").convert_alpha()
        self.image = pygame.transform.scale(image_original, (75, 63))
        self.rect = self.image.get_rect(topleft = (x, y))
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Springsv:
    def __init__(self, x, y, direction = 1):
        image_original = pygame.image.load("pixil-frame-0 (76).png").convert_alpha()
        self.image = pygame.transform.scale(image_original, (24, 63))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.direction = direction
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
class Spikes:
    def __init__(self, x, y, direction = 1):
        image_original = pygame.image.load("tophatspike.png").convert_alpha()
        self.image = pygame.transform.scale(image_original, (50, 50))
        self.rect = self.image.get_rect(topleft = (x, y))
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
#portal goobers
class Portals:
    def __init__(self, x, y):
        image_original = pygame.image.load("portal.png").convert_alpha()
        self.image = pygame.transform.scale(image_original, (74, 55))
        self.rect = self.image.get_rect(topleft = (x, y))
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
class Player:
    def __init__(self, x, y):
        # Load and scale image
        image_original = pygame.image.load("goober.png").convert_alpha()
        scale_factor = IMAGE_HEIGHT / image_original.get_height()
        new_width = int(image_original.get_width() * scale_factor)
        self.image = pygame.transform.scale(image_original, (new_width, IMAGE_HEIGHT))

        # The visible image is drawn *above* the collision box (hitbox)
        self.image_offset_y = -(IMAGE_HEIGHT - HITBOX_HEIGHT)

        # Hitbox (placed so feet match visual feet)
        self.rect = pygame.Rect(x, y, new_width, HITBOX_HEIGHT)

        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False

    def handle_input(self, keys):
        if keys[pygame.K_a]:
            self.vel_x = -SPEED
        if keys[pygame.K_d]:
            self.vel_x = SPEED
        if keys[pygame.K_LEFT]:
            self.vel_x = -SPEED
        if keys[pygame.K_RIGHT]:
            self.vel_x = SPEED
        if keys[pygame.K_q]:
            self.vel_x = SPEED * -2
        if keys[pygame.K_e]:
            self.vel_x = SPEED * 2
        self.rect.x += self.vel_x


        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_POWER
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.rect.x += int(self.vel_x)
        self.vel_x *= 0.8
        if abs(self.vel_x) < 0.2:
            self.vel_x = 0
    def check_collisions(self, platforms):
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0 and self.rect.bottom - self.vel_y <= plat.top:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0 and self.rect.top - self.vel_y >= plat.bottom:
                    self.rect.top = plat.bottom
                    self.vel_y = 0
                else:
                    if self.rect.centerx < plat.centerx:
                        self.rect.right = plat.left
                    else:
                        self.rect.left = plat.right
    def spring_collisions(self, springs, springsv):
        for spring in springs:
            if self.rect.colliderect(spring):
                if self.vel_y > 0 and self.rect.bottom <= spring.rect.top + self.vel_y:
                    self.vel_y = -JUMP_POWER * 1.5
        for sprin in springsv:
            if self.rect.colliderect(sprin):
                #if self.vel_x > 0 and self.rect.left <= sprin.rect.right + self.vel_x:
                self.vel_x += sprin.direction * SPEED * 2
    def spike_collisions(self, spikes):
        for spike in spikes:
            if self.rect.colliderect(spike):
                exit()

    def update(self, platforms, springs, springsv, spikes):
        self.apply_gravity()
        self.check_collisions(platforms)
        self.spring_collisions(springs, springsv)
        self.spike_collisions(spikes)
    def draw(self, surface):
        draw_x = self.rect.x
        draw_y = self.rect.y + -self.image_offset_y - 32  # draw image above the hitbox
        surface.blit(self.image, (draw_x, draw_y))
def leveldata(levelindex):
    # Spring layout
    SLEVEL3 = [Springs(250, 450)]
    SLEVEL4 = [Springs(100, 430), Springs(350, 220)]
    SLEVEL5 = [Springs(25, 500), Springs(100, 500), Springs(175, 500), Springs(250, 500), Springs(325, 500), Springs(400, 500), Springs(475, 500), Springs(550, 500), Springs(625, 500), Springs(700, 500)]
    SVLEVEL5 = [Springsv(5, 10, 1), Springsv(5, 75, 1), Springsv(5, 150, 1), Springsv(5, 225, 1), Springsv(5, 300, 1), Springsv(5, 375, 1), Springsv(5, 450, 1), Springsv(775, 10, -1), Springsv(775, 75, -1), Springsv(775, 150, -1), Springsv(775, 225, -1), Springsv(775, 300, -1), Springsv(775, 375, -1), Springsv(775, 450, -1)]
    SPLEVEL6 = [Spikes(250, 450)]
    #2 max jump, 5 max dash, 6 max spring, 1.10 height is max.
    if levelindex == 0:
        platforms = LEVEL4
        portal = Portals(730, 260)
        springs = SLEVEL5
        springsv = SVLEVEL5
        spikes = []
        x = 25
        y = 200
    elif levelindex == 1:
        platforms = LEVEL2
        portal = Portals(730, 50)
        springs = []
        springsv = []
        spikes = []
        x = 25
        y = 200
    elif levelindex == 2:
        platforms = LEVEL3
        portal = Portals(730, 200)
        springs = SLEVEL3
        springsv = []
        spikes = []
        x = 25
        y = 200
    elif levelindex == 3:
        platforms = LEVEL4
        portal = Portals(730, 260)
        springs = SLEVEL4
        springsv = []
        spikes = []
        x = 25
        y = 200
    elif levelindex == 4:
        platforms = LEVEL4
        portal = Portals(400, 150)
        springsv = SVLEVEL5
        springs = SLEVEL5
        x = 10
        y = 300
    elif levelindex == 5:
        platforms = LEVEL678
        portal = Portals(400, 150)
        springsv = []
        springs = []
        spikes = SPLEVEL6
        x = 10
        y = 300
    elif levelindex == 6:
        platforms = LEVEL678
        portal = Portals(400, 150)
        springsv = []
        springs = []
        spikes = SPLEVEL6
        x = 10
        y = 300
    elif levelindex == 7:
        platforms = LEVEL678
        portal = Portals(400, 150)
        springsv = []
        springs = []
        spikes = SPLEVEL6
        x = 10
        y = 300
    else:
        platforms = LEVEL1
        portal = None
        springs = []
        springsv = []
        spikes = []
        x = 25
        y = 200
    return platforms, portal, springs, springsv, x, y, spikes
def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, GRID_SPACING):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SPACING):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Forgiving Platformer Hitbox")
    clock = pygame.time.Clock()

    # Start player at correct grounded position

    indexlevel = 0
    platforms, portal, springs, springsv, x, y, spikes = leveldata(indexlevel)
    player = Player(x, y)



    running = True
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.handle_input(keys)
        player.update(platforms, springs, springsv, spikes)
        if portal and player.rect.colliderect(portal.rect):
            indexlevel += 1
            platforms, portal, springs, springsv, x, y, spikes = leveldata(indexlevel)
            player.vel_y = 0
            player.rect.x = x
            player.rect.y = y

        # Draw scene
        screen.fill(BG_COLOR)
        draw_grid(screen)
        for plat in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, plat)
        for spring in springs:
            spring.draw(screen)
        for sprin in springsv:
            sprin.draw(screen)
        for spike in spikes:
            spike.draw(screen)
        if portal:
            portal.draw(screen)
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
