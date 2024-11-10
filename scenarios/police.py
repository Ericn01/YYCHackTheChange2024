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
# Initialize world offset for world movement simulation
world_offset = 0

# Load Images
background_image = pygame.image.load("../images/sample.png")
character_car_image = pygame.image.load("../images/car.png")
police_car_image = pygame.image.load("../images/car.png")
exclamation_image = pygame.image.load("../images/exclamation.png")
npc_image = pygame.image.load("../images/walk_down_1.png")

# Resize images if necessary
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
character_car_image = pygame.transform.scale(character_car_image, (100, 50))
police_car_image = pygame.transform.scale(police_car_image, (100, 50))
exclamation_image = pygame.transform.scale(exclamation_image, (30, 30))

# Initial positions
character_car_pos = [WIDTH - 150, HEIGHT // 2 + 65]
police_car_pos = [WIDTH - 500, HEIGHT // 2 + 65]
npc_pos = [1200, HEIGHT // 2 + 65]  # Adjust the y-position as needed

# Font settings
main_font = pygame.font.Font(None, 36)

# Flags to track interactions
interaction_occurred = False
npc_interaction_occurred = False  # New flag for NPC interaction

# Add the npc_spawned flag to track NPC spawning
npc_spawned = False

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

def show_exclamation(position):
    """Display an exclamation above the given position briefly."""
    exclamation_pos = (position[0] + 35, position[1] - 40)
    screen.blit(exclamation_image, exclamation_pos)
    pygame.display.flip()
    pygame.time.wait(500)  # Show the exclamation for half a second

def show_dialogue_and_options(dialogue_text, options, feedbacks):
    """Display the dialogue, options, and handle consequences in one dialogue box."""
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
    if not interaction_occurred:
        screen.blit(police_car_image, police_car_pos)  # Redraw the police car if needed
    if npc_spawned and not npc_interaction_occurred:
        screen.blit(npc_image, npc_pos)  # Redraw the NPC if needed
    dialogue_box.fill(DIALOGUE_BOX_COLOR)  # Clear and redraw the dialogue box
    screen.blit(dialogue_box, (0, HEIGHT - 150))

    # Display options in the same dialogue box
    options_text = "How would you respond?"
    
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
                    option_selected = 1
                elif event.key == pygame.K_2:
                    option_selected = 2

    # Refresh the screen and clear options text before displaying feedback
    screen.blit(background_image, (0, 0))
    screen.blit(character_car_image, character_car_pos)
    if not interaction_occurred:
        screen.blit(police_car_image, police_car_pos)
    if npc_spawned and not npc_interaction_occurred:
        screen.blit(npc_image, npc_pos)
    dialogue_box.fill(DIALOGUE_BOX_COLOR)
    screen.blit(dialogue_box, (0, HEIGHT - 150))

    # Display consequences based on selected option
    feedback = feedbacks[option_selected - 1]

    draw_text_wrapped(screen, feedback, main_font, WHITE, 20, HEIGHT - 130, WIDTH - 40)
    pygame.display.flip()
    pygame.time.wait(5000)  # Display the feedback for a few seconds

def main():
    global interaction_occurred, npc_interaction_occurred, world_offset, npc_spawned, character_car_pos

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

        # Draw the NPC character if it has been spawned and interaction hasn't occurred
        if npc_spawned and not npc_interaction_occurred:
            screen.blit(npc_image, npc_pos)

        # Move the world if character reaches the left edge
        if character_car_pos[0] < 0:
            world_offset -= 5  # Shift world to simulate movement
            character_car_pos = [WIDTH - 150, HEIGHT // 2 + 65]  # Reset character to initial position

            # Spawn the NPC the first time the character crosses the left edge
            if not npc_spawned:
                npc_pos[0] = WIDTH // 2  # Set the initial position of the NPC
                npc_spawned = True  # Mark NPC as spawned

        # Check for collision to start interaction with police car
        character_rect = pygame.Rect(
            character_car_pos[0],
            character_car_pos[1],
            character_car_image.get_width(),
            character_car_image.get_height()
        )
        police_rect = pygame.Rect(
            police_car_pos[0],
            police_car_pos[1],
            police_car_image.get_width(),
            police_car_image.get_height()
        )

        if character_rect.colliderect(police_rect) and not interaction_occurred:
            interaction_occurred = True
            show_exclamation(police_car_pos)
            # Dialogue and options for police interaction
            dialogue_text = (
                "The officer has stopped you and asked for identification. Under Canadian law, "
                "you generally have the right to ask why you're being stopped. In specific cases, "
                "like driving, you may need to show ID."
            )
            options = [
                "Press 1 to Comply and politely ask why.",
                "Press 2 to Refuse to show ID and walk away."
            ]
            feedbacks = [
                "Good choice! You have the right to know why you're being stopped. "
                "Interacting respectfully can help de-escalate the situation.",
                "This may not be the best option. Refusing to comply can lead to further questioning. "
                "In some cases, such as traffic stops, you are legally required to show ID."
            ]
            show_dialogue_and_options(dialogue_text, options, feedbacks)

        # Check for collision to start interaction with NPC
        if npc_spawned and not npc_interaction_occurred:
            npc_rect = pygame.Rect(
                npc_pos[0],
                npc_pos[1],
                npc_image.get_width(),
                npc_image.get_height()
            )
            if character_rect.colliderect(npc_rect):
                npc_interaction_occurred = True
                show_exclamation(npc_pos)
                # Dialogue and options for NPC interaction
                dialogue_text = (
                    "You encounter a pedestrian who seems to need assistance crossing the road. "
                    "Under Canadian law, drivers should yield to pedestrians at crosswalks."
                )
                options = [
                    "Press 1 to Stop and help the pedestrian cross.",
                    "Press 2 to Ignore and drive past."
                ]
                feedbacks = [
                    "Well done! Helping pedestrians ensures safety for everyone.",
                    "Not the best choice. Ignoring pedestrians can be dangerous and may violate traffic laws."
                ]
                show_dialogue_and_options(dialogue_text, options, feedbacks)

        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
