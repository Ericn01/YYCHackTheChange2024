import pygame
import sys
import os
import subprocess

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu - Character Model")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NPC_COLOR = (180, 100, 50)
HUD_COLOR = (0, 0, 0, 180)  # Semi-transparent black for HUD background

# Player settings
player_pos = [100, HEIGHT // 1.4]  # Fixed y-position at HEIGHT // 1.4
player_speed = 0.1
player_size = (50, 50)
HORIZONTAL_SPEED = 0.1  # Horizontal movement speed

# Load Sprites for each direction
player_sprite_right_1 = pygame.image.load('./images/walk_right_1.png').convert_alpha()
player_sprite_right_2 = pygame.image.load('./images/walk_right_2.png').convert_alpha()
player_sprite_left_1 = pygame.image.load('./images/walk_left_1.png').convert_alpha()
player_sprite_left_2 = pygame.image.load('./images/walk_left_2.png').convert_alpha()

# Scale the images to the size of the player
player_sprite_right_1 = pygame.transform.scale(player_sprite_right_1, player_size)
player_sprite_right_2 = pygame.transform.scale(player_sprite_right_2, player_size)
player_sprite_left_1 = pygame.transform.scale(player_sprite_left_1, player_size)
player_sprite_left_2 = pygame.transform.scale(player_sprite_left_2, player_size)

# Load the background image and scale it to fit the screen size
background_image = pygame.image.load("./images/main_menu_background2.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale the background

# NPC settings (transparent NPC)
npc_sprite = pygame.Surface((50, 50), pygame.SRCALPHA)  # Transparent surface
npc_sprite.fill((0, 0, 0, 0))  # Fully transparent (RGBA: 0, 0, 0, 0)

# Define NPC positions with 50 pixels spacing
npc_positions = [
    (170, HEIGHT // 1.4),  # First NPC at x = 170
    (330, HEIGHT // 1.4),  # Second NPC at x = 220 (50 pixels to the right of the first)
    (580, HEIGHT // 1.4),  # Third NPC at x = 270 (50 pixels to the right of the second)
]

# Map NPCs to their corresponding files
npc_files = {
    "tutorial": "tutorial.py",
    "police": "police.py",
    "office": "office.py",
}

# Create the player class
class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y  # Fixed at HEIGHT // 1.4
        self.size = player_size
        self.speed = player_speed
        self.sprite = player_sprite_right_1  # Default to facing right
        self.frame_counter = 0  # To control animation frames
        self.walking_speed = 300  # Set to a very high number to slow down sprite switching
        self.animation_timer = 0  # Timer to control sprite switching speed

    def move(self, dx: float):
        self.x += dx

    def update_sprite(self, keys):
        self.animation_timer += 1  # Increment the animation timer

        # Right movement
        if keys[pygame.K_RIGHT]:
            if self.animation_timer >= self.walking_speed:  # After every 'walking_speed' frames
                self.sprite = player_sprite_right_1 if self.frame_counter % 2 == 0 else player_sprite_right_2
                self.frame_counter += 1
                self.animation_timer = 0  # Reset the timer after switching the sprite
            self.move(HORIZONTAL_SPEED)  # Move right

        # Left movement
        elif keys[pygame.K_LEFT]:
            if self.animation_timer >= self.walking_speed:  # After every 'walking_speed' frames
                self.sprite = player_sprite_left_1 if self.frame_counter % 2 == 0 else player_sprite_left_2
                self.frame_counter += 1
                self.animation_timer = 0  # Reset the timer after switching the sprite
            self.move(-HORIZONTAL_SPEED)  # Move left

    def draw(self, surface: pygame.Surface):
        surface.blit(self.sprite, (self.x, self.y))

# Check if player is close enough to interact with NPC
def check_npc_interaction(player_x: float, player_y: float, npc_x: float, npc_y: float) -> bool:
    distance = ((player_x - npc_x) ** 2 + (player_y - npc_y) ** 2) ** 0.5
    return distance < 60

# Function to open the corresponding Python file for the NPC
def open_npc_file(npc_name: str):
    npc_file = npc_files.get(npc_name)
    if npc_file:
        npc_path = os.path.join("C:/Users/Ho_Ti/Documents/GitHub/YYCHackTheChange2024/scenarios", npc_file)
        
        # Use the full path to the Python executable
        python_executable = "C:/Users/Ho_Ti/AppData/Local/Programs/Python/Python313/python.exe"
        
        try:
            subprocess.run([python_executable, npc_path])  # Run the NPC file using the specified Python executable
        except Exception as e:
            print(f"Error running NPC file: {e}")

# Create a function to handle menu interactions
def main_menu():
    player = Player(player_pos[0], player_pos[1])

    # Main loop for the menu
    running = True
    while running:
        screen.fill(WHITE)

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Update player sprite and movement
        player.update_sprite(keys)

        # Draw the player
        player.draw(screen)

        # Draw and handle all NPCs (now transparent)
        for i, (npc_x, npc_y) in enumerate(npc_positions):
            if check_npc_interaction(player.x, player.y, npc_x, npc_y):
                # Show interaction message with HUD
                font = pygame.font.Font(None, 36)
                prompt_text = font.render("Press SPACE to interact", True, WHITE)  # Text color changed to white

                # Create a background HUD for the text
                text_width = prompt_text.get_width()
                text_height = prompt_text.get_height()
                hud_width = text_width + 30  # Add more padding around the text
                hud_height = text_height + 30  # Increase padding to cover the bottom part of the text

                # Draw HUD background (semi-transparent black)
                pygame.draw.rect(screen, HUD_COLOR, (WIDTH // 2 - hud_width // 2, HEIGHT - 50 - hud_height // 2, hud_width, hud_height))

                # Draw the text
                screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT - 63))

                # Handle interaction when SPACE is pressed
                if keys[pygame.K_SPACE]:
                    npc_name = list(npc_files.keys())[i]
                    open_npc_file(npc_name)

            # Draw the transparent NPC (no visible color, still interacts)
            screen.blit(npc_sprite, (npc_x, npc_y))

        pygame.display.flip()

# Run the main menu
if __name__ == "__main__":
    main_menu()
