import pygame
import sys
import json
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HALF_X = SCREEN_WIDTH / 2
HALF_Y = SCREEN_HEIGHT / 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 20

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Who Wants to Be a Millionaire")

# Fonts
font = pygame.font.SysFont("Arial", FONT_SIZE)

# Load background image
background_image = pygame.image.load(r'Images\bg02.jpg')

# Load background music
pygame.mixer.music.load('Music\music.mp3')
pygame.mixer.music.play(-1)  # Play the music in a loop

# Questions and answers
def load_questions_from_json(filename):
    with open(filename, 'r') as file:
        questions = json.load(file)
    questions_dict = {}
    for i, q in enumerate(questions):
        questions_dict[i] = {
            "question": q["question"],
            "options": q["options"],
            "answer": q["answer"]
        }
    return questions_dict

def draw_text(text, position, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_money(position=(HALF_X-75, 50)):
    global money, score
    dlls = str(money[score])
    text = f"Total money: ${dlls}"
    draw_text(text, position)

def display_question():
    global random_questions
    counter = [(50, 425), (350, 425), (50, 512), (350, 512)]
    question = random_questions[current_question]
    draw_text(question["question"], (50, 100))
    draw_money()
    # Draws options
    for i, option in enumerate(question["options"]):
        draw_text(option, counter[i])

def check_answer(answer):
    global current_question, score, game_over, random_questions

    correct_answer = random_questions[current_question]["answer"]

    if answer == correct_answer:
        score += 1
        current_question += 1
        if current_question >= 10:
            game_over = True  # Player wins
    else:
        game_over = True  # Player loses

def get_random_questions(questions_dict, num_questions=10):
    all_keys = list(questions_dict.keys())
    random.shuffle(all_keys)
    selected_keys = all_keys[:num_questions]
    random_questions = {new_key: questions_dict[old_key] for new_key, old_key in enumerate(selected_keys)}
    return random_questions

def reset_game():
    global current_question, score, game_over, random_questions
    current_question = 0
    score = 0
    game_over = False
    random_questions = get_random_questions(questions, 10)

def draw_semi_transparent_rect(surface, color, alpha):
    global score 

    #(25, 75, 750, 450)

    # const
    x = 643
    width = 150
    height = 28

    # y var
    y = 580  - (46 * score)
    
    if score != 0: 
        rect = (x, y, width, height)
        # Create a temporary surface with per-pixel alpha
        temp_surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        temp_surface.fill(color + (alpha,))
        surface.blit(temp_surface, rect)
    




# Variables
current_question = 0
score = 0
money = [0, 100, 200, 400, 800, 1600, 3200, 5000, 25000, 100000, 1000000]
game_over = False
questions = load_questions_from_json("questions.json")
random_questions = get_random_questions(questions, 10)

def main():
    global game_over

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_a:
                        check_answer("A")
                    elif event.key == pygame.K_b:
                        check_answer("B")
                    elif event.key == pygame.K_c:
                        check_answer("C")
                    elif event.key == pygame.K_d:
                        check_answer("D")
                else:
                    if event.key == pygame.K_r:
                        reset_game()

        # Draw background image
        screen.blit(background_image, (0, 0))

                                 # surface, rgb        ,     sqr dims,      alpha
        draw_semi_transparent_rect(screen, (0, 128, 128), 128)

        
        if game_over:
            if current_question >= 10:
                draw_text("Congratulations! You've won!", (50, 100))
            else:
                draw_text(f"Game Over! Your score: {score}", (50, 100))
            draw_text("Press 'R' to Restart", (50, 200))
        else:
            display_question()

        pygame.display.flip()

if __name__ == "__main__":
    main()


