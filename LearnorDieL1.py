import pygame
import sys
import io
import contextlib
from code import InteractiveInterpreter
import mysql.connector
from tkinter import messagebox
global level
level=1
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="papa0042",
        database="gameverse"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")

gameid=3

if len(sys.argv) > 1:
        userid = sys.argv[1]
else:
        userid = ""
# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 1250, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learn or Die")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
HOVER_BLUE = (100, 149, 237)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Character attributes
char_x, char_y = 50, 350
char_width, char_height = 50, 50
char_velocity = 70
wrong_attempts = 0

# Font setup
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 28)

# Interpreter desired output
DESIRED_OUTPUT = "Hello"

# User input storage
user_input = ""
cursor_position = 0  # Cursor position in the input string

# Interpreter dimensions
interpreter_x, interpreter_y = 780, 50
interpreter_width, interpreter_height = 450, 500
interpreter_padding = 10

# Button dimensions
button_width, button_height = 100, 50
button_x, button_y = interpreter_x + (interpreter_width - button_width) // 2, interpreter_y + interpreter_height - button_height - 10

# Python interactive interpreter setup
interpreter = InteractiveInterpreter()

# Background image and character image
background_image = pygame.image.load('C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/backgroundgame.png')
background_image = pygame.transform.scale(background_image, (750, 500))
Rabbit = pygame.image.load('C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/rabbit2.jpg')
Rabbit = pygame.transform.scale(Rabbit, (70, 70))
Bridge = pygame.image.load('C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/bridge.png')
Bridge = pygame.transform.scale(Bridge, (150, 10))

wronganswer_sound = pygame.mixer.Sound('C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/wronganswersound.mp3')
gameover_sound = pygame.mixer.Sound('C:/Users/jhasa/OneDrive/Desktop/GameVerse/GameVerse/assets/Gameover.mp3')


def draw_game(cursor_visible, hover=False, click=False):
    """Draws the game screen."""
    screen.fill(WHITE)

    # Draw background
    screen.blit(background_image, (1, 130))

    # Draw character
    Rabbit.set_colorkey((255, 255, 255))
    screen.blit(Rabbit, (char_x, char_y))

    # Draw interpreter background
    pygame.draw.rect(screen, GRAY, (interpreter_x, interpreter_y, interpreter_width, interpreter_height))

    # Draw execute button with background effect
    button_color = DARK_BLUE if click else HOVER_BLUE if hover else BLUE
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    button_text = font.render("Run", True, WHITE)
    screen.blit(button_text, (button_x + 20, button_y + 10))

    # Display instructions and attempts left
    instructions = font.render(f"Write Python code to print '{DESIRED_OUTPUT}'", True, BLACK)
    attempts_left = font.render(f"Attempts left: {3 - wrong_attempts}", True, BLACK)

    # Render user input
    lines = user_input.split("\n")
    for i, line in enumerate(lines):
        user_text_display = input_font.render(line, True, BLACK)
        screen.blit(user_text_display, (interpreter_x + interpreter_padding, interpreter_y + interpreter_padding + i * 30))

    # Draw cursor
    if cursor_visible:
        line_index = user_input[:cursor_position].count("\n")
        line_start = sum(len(line) + 1 for line in user_input.split("\n")[:line_index])
        cursor_x = input_font.size(user_input[line_start:cursor_position])[0] + interpreter_padding
        cursor_y = interpreter_y + interpreter_padding + line_index * 30
        pygame.draw.line(screen, BLACK, (interpreter_x + cursor_x, cursor_y),
                         (interpreter_x + cursor_x, cursor_y + input_font.get_height()))

    screen.blit(instructions, (20, 20))
    screen.blit(attempts_left, (20, 60))
    pygame.display.flip()


def custom_interpreter(user_code):
    """Executes user code and checks if it generates the desired output."""
    try:
        fake_output = io.StringIO()  # Redirect stdout
        with contextlib.redirect_stdout(fake_output):
            interpreter.runsource(user_code, "<stdin>", "exec")
        result = fake_output.getvalue()
        return result.strip() == DESIRED_OUTPUT.strip()
    except Exception as e:
        print(f"Error executing user code: {e}")
        return False


def game_over():
    """Displays the game over screen with character animation."""
    global char_y
    while char_y < HEIGHT:
        screen.fill(WHITE)
        screen.blit(background_image, (1, 130))
        Rabbit.set_colorkey((255, 255, 255))
        screen.blit(Rabbit, (char_x, char_y))
        char_y += 10
        pygame.display.flip()
        clock.tick(30)

    game_over_text = font.render("Game Over!", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(2000)


def level_completed():
    """Displays the level completed screen."""
    cursor.execute(f"select level from scores where user_id={userid} and game_id={gameid}")
    fetchedlevel=cursor.fetchone()
    if(fetchedlevel[0]>1):
      cursor.execute(f"update scores set level={level} where user_id={userid} and game_id={gameid} ")
      db.commit()
    else:
        print(f"Level:{level}")
    screen.fill(WHITE)
    level_completed_text = font.render("Level 1 Completed!", True, BLUE)
    screen.blit(level_completed_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(2000)


# Main game loop
running = True
cursor_visible = True
cursor_timer = 0
button_hover = False
button_click = False
pygame.key.set_repeat(200, 50)  # Set key repeat delay and interval

while running:
    cursor_timer += clock.get_time()
    if cursor_timer >= 500:  # Toggle cursor visibility every 500ms
        cursor_visible = not cursor_visible
        cursor_timer = 0

    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_hover = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

    draw_game(cursor_visible, hover=button_hover, click=button_click)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if cursor_position > 0:
                    user_input = user_input[:cursor_position - 1] + user_input[cursor_position:]
                    cursor_position -= 1
            elif event.key == pygame.K_RETURN:
                user_input = user_input[:cursor_position] + "\n" + user_input[cursor_position:]
                cursor_position += 1
            elif event.key == pygame.K_LEFT and cursor_position > 0:
                cursor_position -= 1
            elif event.key == pygame.K_RIGHT and cursor_position < len(user_input):
                cursor_position += 1
            else:
                user_input = user_input[:cursor_position] + event.unicode + user_input[cursor_position:]
                cursor_position += 1

        if event.type == pygame.MOUSEBUTTONDOWN and button_hover:
            button_click = True

        if event.type == pygame.MOUSEBUTTONUP:
            button_click = False
            if button_hover:
                if not custom_interpreter(user_input):
                    wrong_attempts += 1
                    if wrong_attempts < 3:
                        wronganswer_sound.play()
                    char_x += char_velocity
                    if wrong_attempts >= 3:
                        gameover_sound.play()
                        draw_game(cursor_visible)
                        game_over()
                        running = False
                else:
                    Bridge.set_colorkey((255, 255, 255))
                    screen.blit(Bridge, (276, 413))
                    level_completed()
                    running = False

                user_input = ""
                cursor_position = 0

    clock.tick(30)

pygame.quit()
sys.exit()
