import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Load Assets
forest_bg = pygame.image.load("C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/tressurehuntassets/Background.jpeg")
forest_bg = pygame.transform.scale(forest_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

tree_img = pygame.image.load("C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/tressurehuntassets/Tree.png")
tree_img = pygame.transform.scale(tree_img, (90, 120))  # Resize if needed

rock_img = pygame.image.load("C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/tressurehuntassets/stone.png")
rock_img = pygame.transform.scale(rock_img, (50, 50))

player_img = pygame.image.load("C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/tressurehuntassets/dog.jpeg")
player_img = pygame.transform.scale(player_img, (60, 60))

enemy_img = pygame.image.load("C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/tressurehuntassets/skeleton.jpeg")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

treasure_img = pygame.image.load("C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/tressurehuntassets/diamond.jpeg")
treasure_img = pygame.transform.scale(treasure_img, (30, 30))

player_img.set_colorkey((255,255,255))
enemy_img.set_colorkey((255,255,255))
treasure_img.set_colorkey((255,255,255))
tree_img.set_colorkey((255,255,255))
rock_img.set_colorkey((255,255,255))
# Load Sounds
pygame.mixer.init()
background_music = "C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/tressurehuntassets/cotton-candy-children-puzzle-game-music-197733.mp3"
treasure_sound = pygame.mixer.Sound(
    "C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/tressurehuntassets/short-success-sound-glockenspiel-treasure-video-game-6346.mp3")
collision_sound = pygame.mixer.Sound("C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/tressurehuntassets/sword-slash-and-swing-185432.mp3")
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # Loop infinitely

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Forest Treasure Hunt")

# Player settings
player_pos = [100, 100]
player_vel = [0, 0]
player_acceleration = 0.5
player_max_speed = 15
player_friction = 0.1
player_lives = 3

# Enemy settings
enemy_pos = [random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)]
enemy_speed = 1


# Treasure settings
def generate_treasure():
    return [random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)]


treasure_pos = generate_treasure()


# Collision Detection
def detect_collision(pos1, size1, pos2, size2):
    if (pos1[0] < pos2[0] + size2 and pos1[0] + size1 > pos2[0] and
            pos1[1] < pos2[1] + size2 and pos1[1] + size1 > pos2[1]):
        return True
    return False


# Obstacle settings
obstacles = []


# Ensure obstacles don't spawn at game start
def generate_obstacles():
    global obstacles
    obstacles = [[random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)] for _ in range(5)]


def draw_game():
    screen.blit(forest_bg, (0, 0))  # Set Background

    # Draw Obstacles (Trees & Rocks)
    for i, obs in enumerate(obstacles):
        if i % 2 == 0:
            screen.blit(tree_img, obs)
        else:
            screen.blit(rock_img, obs)

    # Draw Enemy
    screen.blit(enemy_img, enemy_pos)

    # Draw Player
    screen.blit(player_img, player_pos)

    # Draw Treasure
    screen.blit(treasure_img, treasure_pos)

    # Display Player Lives
    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Lives: {player_lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    pygame.display.flip()


# Game Loop
running = True
obstacle_spawned = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not obstacle_spawned:
        generate_obstacles()
        obstacle_spawned = True

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_vel[0] -= player_acceleration
    if keys[pygame.K_RIGHT]:
        player_vel[0] += player_acceleration
    if keys[pygame.K_UP]:
        player_vel[1] -= player_acceleration
    if keys[pygame.K_DOWN]:
        player_vel[1] += player_acceleration

    # Apply Friction
    player_vel[0] *= (1 - player_friction)
    player_vel[1] *= (1 - player_friction)

    # Limit Speed
    player_vel[0] = max(-player_max_speed, min(player_vel[0], player_max_speed))
    player_vel[1] = max(-player_max_speed, min(player_vel[1], player_max_speed))

    # Calculate new position
    new_pos = [player_pos[0] + player_vel[0], player_pos[1] + player_vel[1]]

    # Check for collision with obstacles
    collision_with_obstacle = False
    for i, obs in enumerate(obstacles):
        if detect_collision(new_pos, 40, obs, 50):
            if i % 2 != 0:  # If collides with rock
                player_lives -= 1
                collision_sound.play()
                print(f"Hit a rock! Lives left: {player_lives}")
                if player_lives == 0:
                    print("Game Over! You lost all lives.")
                    running = False
            collision_with_obstacle = True
            break

    if not collision_with_obstacle:
        player_pos = new_pos  # Update position only if no collision

    # Keep player within bounds
    player_pos[0] = max(0, min(player_pos[0], SCREEN_WIDTH - 40))
    player_pos[1] = max(0, min(player_pos[1], SCREEN_HEIGHT - 40))

    # Check for collision with treasure
    if detect_collision(player_pos, 40, treasure_pos, 30):
        print("Congratulations! You collected the treasure!")
        treasure_sound.play()
        treasure_pos = generate_treasure()  # Generate new treasure

    # Enhanced Enemy AI - Moves towards player
    if enemy_pos[0] < player_pos[0]:
        enemy_pos[0] += enemy_speed
    elif enemy_pos[0] > player_pos[0]:
        enemy_pos[0] -= enemy_speed
    if enemy_pos[1] < player_pos[1]:
        enemy_pos[1] += enemy_speed
    elif enemy_pos[1] > player_pos[1]:
        enemy_pos[1] -= enemy_speed

    # Check for collision with enemy
    if detect_collision(player_pos, 40, enemy_pos, 40):
        player_lives -= 1
        collision_sound.play()
        print(f"You were hit! Lives left: {player_lives}")
        if player_lives == 0:
            print("Game Over! You lost all lives.")
            running = False

    draw_game()
    clock.tick(FPS)

pygame.quit()
sys.exit()