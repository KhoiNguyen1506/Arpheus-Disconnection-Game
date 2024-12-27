import pygame
import sys
import random


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Arpheus Game")
game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)


#Classes
class Orpheus(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position):
        super().__init__()
        self.x = x_position
        self.y = y_position

        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Orpheus on a cart.png"), (100, 120)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Orpheus ducking.png"), (140, 60)))

        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        

        self.velocity_y = 0  # Vertical velocity for jumping
        self.gravity = 0.1  # Gravity strength (adjust for slower descent)
        self.jump_strength = -6.2  # Initial jump velocity (adjust for lower jump)
        self.ducking = False
        self.on_ground = True  # Check if Orpheus is on the ground

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= len(self.running_sprites):
            self.current_image = 0

        if self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.image = self.running_sprites[int(self.current_image)]

    def duck(self):
        self.ducking = True
        self.image = self.ducking_sprites[0]
        self.rect.centery = 380

    def unduck(self):
        self.ducking = False
        self.image = self.running_sprites[0]
        self.rect.centery = 360

    def apply_gravity(self):
        # Apply gravity and update position
        self.velocity_y += self.gravity
        self.rect.centery += self.velocity_y

        # Stop movement if Orpheus hits the ground
        if self.rect.centery >= 360:  # Ground level
            self.rect.centery = 360
            self.velocity_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            jump_sfx.play()
            self.velocity_y = self.jump_strength  # Apply initial upward velocity
            self.on_ground = False
class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position):
        super().__init__()
        self.x_position = x_position
        self.y_position = y_position
        self.sprites = []
        for i in range(1,7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/cacti/cactus{i}.png"),(60,60))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def update(self):
        self.x_position -= game_Speed
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))
class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_position = 1300
        self.y_position = random.choice([280, 295, 350])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Ptero1.png"), (42, 31)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Ptero2.png"), (42, 31)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def update(self):
        self.animate()
        self.x_position -= game_Speed
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]
class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_position, y_position):
        super().__init__()
        self.image = image
        self.x_position = x_position
        self.y_position = y_position
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def update(self):
        self.rect.x -= 1


#Variables
game_Speed = 2
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000


#Sounds
death_sfx = pygame.mixer.Sound("assets/sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("assets/sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("assets/sfx/jump.mp3")


#Surfaces and backgrounds
ground = pygame.image.load("assets/ground.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640,400))
cloud = pygame.image.load("assets/cloud.png")
cloud = pygame.transform.scale(cloud, (200,80))


#Groups
Orphe_group = pygame.sprite.GroupSingle()
cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
ptero_group = pygame.sprite.Group()


#Objects
Orphe = Orpheus(50, 360)
Orphe_group.add(Orphe)


#Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

#Functions

def end_game():
    global player_score, game_Speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_Speed = 2
    cloud_group.empty()
    obstacle_group.empty()


while True:
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_DOWN]:
        Orphe.duck()
    else:
        if Orphe.ducking:
            Orphe.unduck()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                Orphe.jump()
                if game_over:
                    game_over = False
                    game_Speed = 2
                    player_score = 0
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50,300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)

    screen.fill("white")

    #Collisons
    if pygame.sprite.spritecollide(Orphe_group.sprite, obstacle_group, False):
        game_over = True
        death_sfx.play()
    if game_over:
        end_game()

    if not game_over:
        game_Speed += 0.001
        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play()

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            if player_score < 200:
                obstacle_random = random.randint(1,1500)
                if obstacle_random in range(1,7):
                    new_obstacle = Cactus(1280,340)
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                    obstacle_spawn = False
                elif obstacle_random in range(7,10):
                    new_obstacle = Ptero()
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                    obstacle_spawn = False
            else:
                obstacle_random = random.randint(1,200)
                if obstacle_random in range(1,7):
                    new_obstacle = Cactus(1280,340)
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                    obstacle_spawn = False
                elif obstacle_random in range(7,10):
                    new_obstacle = Ptero()
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                    obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(
            str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150,10))
        
        cloud_group.update()
        cloud_group.draw(screen)

        ptero_group.update()
        ptero_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        Orphe_group.draw(screen)
        Orphe_group.update()

        ground_x -= game_Speed

        screen.blit(ground, (ground_x, 360))
        screen.blit(ground, (ground_x + 1280, 360))

        if ground_x <= -1280:
            ground_x = 0




    pygame.display.update()
    clock.tick(120)



    
