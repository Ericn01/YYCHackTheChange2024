import os
import pygame
import sys

# Set up working directory to the script’s location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Canadian Law Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DIALOGUE_BOX_COLOR = (0, 0, 0, 128)  # Semi-transparent black for the dialogue box

# Load Images
background_image = pygame.image.load("../images/sample.png")
character_car_image = pygame.image.load("../images/car.png")
police_car_image = pygame.image.load("../images/car.png")
exclamation_image = pygame.image.load("../images/exclamation.png")

# Resize images if necessary
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
character_car_image = pygame.transform.scale(character_car_image, (100, 50))
police_car_image = pygame.transform.scale(police_car_image, (100, 50))
exclamation_image = pygame.transform.scale(exclamation_image, (30, 30))

# Initial positions
character_car_pos = [WIDTH - 150, HEIGHT // 2 + 65]
police_car_pos = [WIDTH - 500, HEIGHT // 2 + 65]

# Font settings
main_font = pygame.font.Font(None, 36)

# Flag to track if interaction occurred
interaction_occurred = False

def draw_text_wrapped(surface, text, font, color, x, y, max_width):
    """Draw wrapped text."""
    words = text.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_surface = font.render(word + " ", True, color)
        word_width = word_surface.get_width()

        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width

    lines.append(" ".join(current_line))

    y_offset = y
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y_offset))
        y_offset += font.get_height()

    return y_offset

def show_exclamation():
    """Display an exclamation above the police car briefly."""
    exclamation_pos = (police_car_pos[0] + 35, police_car_pos[1] - 40)
    screen.blit(exclamation_image, exclamation_pos)
    pygame.display.flip()
    pygame.time.wait(500)  # Show the exclamation for half a second

def show_dialogue_and_options():
    """Display the dialogue, options, and handle consequences in one dialogue box."""

    # Display initial dialogue text
    dialogue_text = (
        "The officer has stopped you and asked for identification. Under Canadian law, "
        "you generally have the right to ask why you're being stopped. In specific cases, "
        "like driving, you may need to show ID."
    )

    # Draw the initial dialogue box and text
    dialogue_box = pygame.Surface((WIDTH, 150), pygame.SRCALPHA)
    dialogue_box.fill(DIALOGUE_BOX_COLOR)
    screen.blit(dialogue_box, (0, HEIGHT - 150))
    draw_text_wrapped(screen, dialogue_text, main_font, WHITE, 20, HEIGHT - 130, WIDTH - 40)
    pygame.display.flip()

    # Wait for Space key to proceed to options
    waiting_for_space = True
    while waiting_for_space:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_space = False

    # Clear previous dialogue text by refreshing the screen and background elements
    screen.blit(background_image, (0, 0))  # Redraw the background
    screen.blit(character_car_image, character_car_pos)  # Redraw the character car
    screen.blit(police_car_image, police_car_pos)  # Redraw the police car (if needed)
    dialogue_box.fill(DIALOGUE_BOX_COLOR)  # Clear and redraw the dialogue box
    screen.blit(dialogue_box, (0, HEIGHT - 150))

    # Display options in the same dialogue box
    options_text = "How would you respond?"
    options = [
        "Press 1 to Comply and politely ask why.",
        "Press 2 to Refuse to show ID and walk away."
    ]
    
    draw_text_wrapped(screen, options_text, main_font, WHITE, 20, HEIGHT - 130, WIDTH - 40)
    for i, option in enumerate(options):
        draw_text_wrapped(screen, option, main_font, WHITE, 20, HEIGHT - 90 + i * 30, WIDTH - 40)
    pygame.display.flip()

    # Handle option selection and display consequences
    option_selected = None
    while option_selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    option_selected = "Comply and politely ask why."
                elif event.key == pygame.K_2:
                    option_selected = "Refuse to show ID and walk away."

    # Refresh the screen and clear options text before displaying feedback
    screen.blit(background_image, (0, 0))
    screen.blit(character_car_image, character_car_pos)
    screen.blit(police_car_image, police_car_pos)
    dialogue_box.fill(DIALOGUE_BOX_COLOR)
    screen.blit(dialogue_box, (0, HEIGHT - 150))

    # Display consequences based on selected option
    feedback = ""
    if option_selected == "Comply and politely ask why.":
        feedback = (
            "Good choice! You have the right to know why you're being stopped. "
            "Interacting respectfully can help de-escalate the situation."
        )
    elif option_selected == "Refuse to show ID and walk away.":
        feedback = (
            "This may not be the best option. Refusing to comply can lead to further questioning. "
            "In some cases, such as traffic stops, you are legally required to show ID."
        )

    draw_text_wrapped(screen, feedback, main_font, WHITE, 20, HEIGHT - 130, WIDTH - 40)
    pygame.display.flip()
    pygame.time.wait(5000)  # Display the feedback for a few seconds



def main():
    global interaction_occurred

    while True:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_car_pos[0] -= 0.2
        if keys[pygame.K_RIGHT]:
            character_car_pos[0] += 0.2
        if keys[pygame.K_UP]:
            character_car_pos[1] -= 0.2
        if keys[pygame.K_DOWN]:
            character_car_pos[1] += 0.2

        # Draw the player's car
        screen.blit(character_car_image, character_car_pos)

        # Draw the police car only if interaction has not yet occurred
        if not interaction_occurred:
            screen.blit(police_car_image, police_car_pos)

        # Create rectangles for collision detection
        character_rect = pygame.Rect(character_car_pos[0], character_car_pos[1], character_car_image.get_width(), character_car_image.get_height())
        police_rect = pygame.Rect(police_car_pos[0], police_car_pos[1], police_car_image.get_width(), police_car_image.get_height())

        # Check for collision to start interaction
        if character_rect.colliderect(police_rect) and not interaction_occurred:
            interaction_occurred = True
            show_exclamation()
            show_dialogue_and_options()  # Show dialogue, options, and feedback all in the same box

        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
