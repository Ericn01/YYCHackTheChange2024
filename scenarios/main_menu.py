import pygame
import sys
import os

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

# Player settings
player_pos = [100, HEIGHT // 2]
player_speed = 0.1
player_size = (50, 50)
VERTICAL_SPEED = 0.1  # Vertical movement speed
HORIZONTAL_SPEED = 0.1  # Horizontal movement speed

# Load Sprites for each direction
player_sprite_right_1 = pygame.image.load('./images/walk_right_1.png').convert_alpha()
player_sprite_right_2 = pygame.image.load('./images/walk_right_2.png').convert_alpha()
player_sprite_left_1 = pygame.image.load('./images/walk_left_1.png').convert_alpha()
player_sprite_left_2 = pygame.image.load('./images/walk_left_2.png').convert_alpha()
player_sprite_up_1 = pygame.image.load('./images/walk_up_1.png').convert_alpha()
player_sprite_up_2 = pygame.image.load('./images/walk_up_2.png').convert_alpha()
player_sprite_down_1 = pygame.image.load('./images/walk_down_1.png').convert_alpha()
player_sprite_down_2 = pygame.image.load('./images/walk_down_2.png').convert_alpha()

# Scale the images to the size of the player
player_sprite_right_1 = pygame.transform.scale(player_sprite_right_1, player_size)
player_sprite_right_2 = pygame.transform.scale(player_sprite_right_2, player_size)
player_sprite_left_1 = pygame.transform.scale(player_sprite_left_1, player_size)
player_sprite_left_2 = pygame.transform.scale(player_sprite_left_2, player_size)
player_sprite_up_1 = pygame.transform.scale(player_sprite_up_1, player_size)
player_sprite_up_2 = pygame.transform.scale(player_sprite_up_2, player_size)
player_sprite_down_1 = pygame.transform.scale(player_sprite_down_1, player_size)
player_sprite_down_2 = pygame.transform.scale(player_sprite_down_2, player_size)

# Load the background image and scale it to fit the screen size
background_image = pygame.image.load("./images/main_menu_background2.jpg").convert()

background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale the background

# NPC settings (for interactivity)
npc_sprite = pygame.Surface((50, 50))
npc_sprite.fill(NPC_COLOR)

# Define NPC positions
npc_positions = [
    (300, HEIGHT // 2 - 100),
    (500, HEIGHT // 2 + 100),
    (700, HEIGHT // 2 - 50),
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
        self.y = y
        self.size = player_size
        self.speed = player_speed
        self.sprite = player_sprite_right_1  # Default to facing right
        self.frame_counter = 0  # To control animation frames
        self.walking_speed = 300  # Set to a very high number to slow down sprite switching
        self.animation_timer = 0  # Timer to control sprite switching speed

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def update_sprite(self, keys):
        self.animation_timer += 1  # Increment the animation timer

        # Right movement
        if keys[pygame.K_RIGHT]:
            if self.animation_timer >= self.walking_speed:  # After every 'walking_speed' frames
                self.sprite = player_sprite_right_1 if self.frame_counter % 2 == 0 else player_sprite_right_2
                self.frame_counter += 1
                self.animation_timer = 0  # Reset the timer after switching the sprite
            self.move(HORIZONTAL_SPEED, 0)  # Move right

        # Left movement
        elif keys[pygame.K_LEFT]:
            if self.animation_timer >= self.walking_speed:  # After every 'walking_speed' frames
                self.sprite = player_sprite_left_1 if self.frame_counter % 2 == 0 else player_sprite_left_2
                self.frame_counter += 1
                self.animation_timer = 0  # Reset the timer after switching the sprite
            self.move(-HORIZONTAL_SPEED, 0)  # Move left

        # Upward movement
        elif keys[pygame.K_UP]:
            if self.animation_timer >= self.walking_speed:  # After every 'walking_speed' frames
                self.sprite = player_sprite_up_1 if self.frame_counter % 2 == 0 else player_sprite_up_2
                self.frame_counter += 1
                self.animation_timer = 0  # Reset the timer after switching the sprite
            self.move(0, -VERTICAL_SPEED)  # Move up

        # Downward movement
        elif keys[pygame.K_DOWN]:
            if self.animation_timer >= self.walking_speed:  # After every 'walking_speed' frames
                self.sprite = player_sprite_down_1 if self.frame_counter % 2 == 0 else player_sprite_down_2
                self.frame_counter += 1
                self.animation_timer = 0  # Reset the timer after switching the sprite
            self.move(0, VERTICAL_SPEED)  # Move down

    def draw(self, surface: pygame.Surface):
        surface.blit(self.sprite, (self.x, self.y))

# Check if player is close enough to interact with NPC
def check_npc_interaction(player_x: float, player_y: float, npc_x: float, npc_y: float) -> bool:
    distance = ((player_x - npc_x) ** 2 + (player_y - npc_y) ** 2) ** 0.5
    return distance < 60

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

        # Draw and handle all NPCs
        for i, (npc_x, npc_y) in enumerate(npc_positions):
            if check_npc_interaction(player.x, player.y, npc_x, npc_y):
                # Show interaction message
                font = pygame.font.Font(None, 36)
                prompt_text = font.render("Press SPACE to interact", True, BLACK)
                screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT - 50))

                # Handle interaction when SPACE is pressed
                if keys[pygame.K_SPACE]:
                    npc_name = list(npc_files.keys())[i]
                    open_npc_file(npc_name)

            screen.blit(npc_sprite, (npc_x, npc_y))

        pygame.display.flip()

# Function to open the corresponding Python file for the NPC
def open_npc_file(npc_name: str):
    npc_file = npc_files.get(npc_name)
    if npc_file:
        npc_path = os.path.join("C:/Users/Ho_Ti/Documents/GitHub/YYCHackTheChange2024/scenarios", npc_file)
        os.system(f"python {npc_path}")  # Opens the file associated with the NPC

# Run the main menu
if __name__ == "__main__":
    main_menu()
