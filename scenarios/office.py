import pygame
import sys
from typing import Dict, List, Tuple

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Canadian Law For Employees")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (200, 50, 50)
NPC_COLOR = (180, 100, 50)
GREEN = (34, 139, 34)
DIALOGUE_BOX_COLOR = (0, 0, 0, 128)

# Player settings
player_pos = [350, HEIGHT // 2]
player_speed = 0.1
player_size = (75,75)
VERTICAL_SPEED = 0.1  # Added vertical speed
npc_size = (25,25)

# Load Sprites
player_sprite_down = pygame.image.load('./images/look_down.png').convert_alpha()
player_sprite_left = pygame.image.load('./images/look_left.png').convert_alpha()
player_sprite_right = pygame.image.load('./images/look_right.png').convert_alpha()
player_sprite_up = pygame.image.load('./images/look_up.png').convert_alpha()

player_walk_down_1 = pygame.image.load('./images/walk_down_1.png').convert_alpha()
player_walk_down_2 = pygame.image.load('./images/walk_down_2.png').convert_alpha()
player_walk_left_1 = pygame.image.load('./images/walk_left_1.png').convert_alpha()
player_walk_left_2 = pygame.image.load('./images/walk_left_2.png').convert_alpha()
player_walk_right_1 = pygame.image.load('./images/walk_right_1.png').convert_alpha()
player_walk_right_2 = pygame.image.load('./images/walk_right_2.png').convert_alpha()
player_walk_up_1 = pygame.image.load('./images/walk_up_1.png').convert_alpha()
player_walk_up_2 = pygame.image.load('./images/walk_up_2.png').convert_alpha()

# Scale the images to the size of the player
player_sprite_down = pygame.transform.scale(player_sprite_down, player_size)
player_sprite_left = pygame.transform.scale(player_sprite_left, player_size)
player_sprite_right = pygame.transform.scale(player_sprite_right, player_size)
player_sprite_up = pygame.transform.scale(player_sprite_up, player_size)

player_walk_down_1 = pygame.transform.scale(player_walk_down_1, player_size)
player_walk_down_2 = pygame.transform.scale(player_walk_down_2, player_size)
player_walk_left_1 = pygame.transform.scale(player_walk_left_1, player_size)
player_walk_left_2 = pygame.transform.scale(player_walk_left_2, player_size)
player_walk_right_1 = pygame.transform.scale(player_walk_right_1, player_size)
player_walk_right_2 = pygame.transform.scale(player_walk_right_2, player_size)
player_walk_up_1 = pygame.transform.scale(player_walk_up_1, player_size)
player_walk_up_2 = pygame.transform.scale(player_walk_up_2, player_size)

npc_image = pygame.image.load('./images/document.png').convert_alpha()
npc_image = pygame.transform.scale(npc_image, npc_size)




npc_sprite = pygame.Surface((50, 50))
npc_sprite.fill(NPC_COLOR)

# Load the background and image and scale it to fit the screen size
background_image = pygame.image.load("./images/office.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale the background

# Law NPCs with detailed information
laws_info = [
    {
        "title": "Employment Standards",
        "description": "The Employment Standards Act sets out the basic rights of workers in the workplace, including hours of work, wages, and termination.",
        "details": [
            "• Employees are entitled to minimum wage and overtime pay for hours worked beyond the standard workweek.",
            "• Employers must provide notice or severance pay when terminating an employee without cause.",
            "• Employees are entitled to paid vacation and rest periods.",
            "• Termination and dismissal rules are outlined, and employees are entitled to written notice."
        ]
    },
    {
        "title": "Anti-Discrimination",
        "description": "The Canadian Human Rights Act prohibits discrimination in the workplace on the basis of various protected grounds, including race, age, gender, and disability.",
        "details": [
            "• Discrimination based on age, race, gender, or disability is prohibited in employment practices.",
            "• Employees are entitled to reasonable accommodation for disabilities or family responsibilities.",
            "• Employers cannot treat employees unfairly based on personal characteristics like gender, race, or sexual orientation.",
            "• Includes protection against harassment and bullying in the workplace."
        ]
    },
    {
        "title": "Occupational Health and Safety",
        "description": "The Occupational Health and Safety Act requires employers to provide a safe working environment and protect employees from workplace hazards.",
        "details": [
            "• Employees have the right to refuse unsafe work without fear of retaliation.",
            "• Employers must provide necessary safety equipment and conduct safety training.",
            "• Workplace incidents or injuries must be reported and investigated.",
            "• Employees are entitled to workers' compensation benefits in case of workplace injury or illness."
        ]
    },
    {
        "title": "Employment Insurance (EI)",
        "description": "Employment Insurance (EI) benefits provide temporary financial assistance to workers who lose their job or are unable to work due to illness or family responsibilities.",
        "details": [
            "• Employees who lose their job through no fault of their own are entitled to EI benefits.",
            "• Employees can receive EI benefits during maternity or parental leave.",
            "• Employees are eligible for sickness benefits under EI if they are unable to work due to illness.",
            "• EI benefits are based on a worker’s insurable earnings and the duration of employment."
        ]
    },
    {
        "title": "Union Rights",
        "description": "Employees in Canada have the right to join unions and engage in collective bargaining without fear of retaliation from employers.",
        "details": [
            "• Employees are legally protected if they form or join a union.",
            "• Employers cannot fire, demote, or discriminate against employees for union activities.",
            "• Unionized employees have the right to negotiate wages, benefits, and working conditions collectively.",
            "• sCollective agreements ensure better protection for union members in areas like dispute resolution."
        ]
    }
]


# NPC positions with varied y positions
npc_positions = [
    (190, HEIGHT // 2 - 140),
    (340, HEIGHT // 2 + 230),
    (600, HEIGHT // 2 - 130),
    (80, HEIGHT // 2 + 10),
    (710, HEIGHT // 2 + 115)
]

# Scenario-based quiz questions
scenarios = [
    {
        "scenario": "David has been working at a company for 5 years. One day, his manager informs him that his position is being eliminated due to 'restructuring,' even though David’s performance has been excellent. David is not given any severance pay or notice",
        "question": "Is David entitled to severance phoay or notice under Canadian law?",
        "answer": "yes",
        "explanation": "Under the Canadian Employment Standards, employees are generally entitled to notice or severance pay if terminated without cause, especially if they have been employed for a certain period (usually more than 3 months)."
    },
    {
        "scenario": "Emily is a qualified worker who has been with her company for over 10 years. Her employer begins promoting younger employees, and she is passed over for a promotion despite having more experience and qualifications. She suspects this is because of her age.",
        "question": "Is Emily’s situation considered workplace discrimination under Canadian law?",
        "answer": "yes",
        "explanation": "Discrimination based on age is prohibited under the Canadian Human Rights Act. Employees cannot be denied opportunities based on factors such as age, race, gender, or disability."
    },
    {
        "scenario": "John works overtime hours regularly at his job, but his employer never compensates him for the extra hours worked, despite him mentioning it multiple times.",
        "question": "Is this practice legal under Canadian labor law?",
        "answer": "no",
        "explanation": "Under Canadian law, employees must be paid for all hours worked, including overtime. If the employer does not pay for overtime hours, this constitutes wage theft and is against the law."
    },
    {
        "scenario": "Marie has been subjected to verbal harassment from a coworker. She feels uncomfortable and has reported the issue to HR, but no action has been taken. The harassment continues.",
        "question": "Is Marie’s employer legally required to address her harassment complaint?",
        "answer": "yes",
        "explanation": "Under Canadian law, employers have a legal duty to provide a safe workplace, free from harassment. They are required to take action to investigate and address harassment claims promptly."
    },
    {
        "scenario": "Employees at a manufacturing plant want to form a union to negotiate better wages and working conditions. The employer threatens to fire anyone who supports the union.",
        "question": "Is it legal for the employer to threaten employees for supporting unionization?",
        "answer": "no",
        "explanation": "Under Canadian law, employees have the right to join and form unions without fear of retaliation or discrimination. Employers cannot threaten or punish employees for union activities."
    }
]

# Font settings
title_font = pygame.font.Font(None, 48)
main_font = pygame.font.Font(None, 36)
detail_font = pygame.font.Font(None, 24)

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, surface: pygame.Surface):
        color = (min(self.color[0] + 20, 255), min(self.color[1] + 20, 255), min(self.color[2] + 20, 255)) if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = main_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

def draw_text_wrapped(surface: pygame.Surface, text: str, font: pygame.font.Font, color: Tuple[int, int, int], x: int, y: int, max_width: int) -> int:
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

def check_npc_interaction(player_x: float, player_y: float, npc_x: float, npc_y: float) -> bool:
    """Check if player is close enough to interact with NPC"""
    distance = ((player_x - npc_x) ** 2 + (player_y - npc_y) ** 2) ** 0.5
    return distance < 60

def office_level():
    in_office = True
    showing_details = False
    current_details = None
    player_x_offset = 0
    visited_npcs = set()  # Track which NPCs have been visited
    walking_animation_frame = 0
    last_update_time = pygame.time.get_ticks()
    space_pressed = False  # New flag to track space bar interaction

    while in_office:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_details is not None:
                    # Space pressed to show details
                    showing_details = not showing_details
                    if current_details is not None and not showing_details:
                        # The index of the NPC in the `laws_info` list
                        npc_index = laws_info.index(current_details)
                        if npc_index not in visited_npcs:
                            visited_npcs.add(npc_index)
                            space_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    showing_details = False

        # Movement controls with boundary checking
        if not showing_details:
            keys = pygame.key.get_pressed()
            # Horizontal movement
            if keys[pygame.K_RIGHT]:
                # Restrict movement based on background limits or screen boundary
                if player_pos[0] < WIDTH - player_size[0] // 2 or player_x_offset <= -npc_positions[-1][0] + WIDTH - 200:
                    player_pos[0] = min(player_pos[0] + player_speed, WIDTH - player_size[0])  # Limit to right screen boundary
                else:
                    player_x_offset = max(player_x_offset - player_speed, -npc_positions[-1][0] + WIDTH - 200)  # Limit background offset
                # Update animation for right walking
                walking_animation_frame = (walking_animation_frame + 1) % 2
                last_update_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]:
                # Restrict movement to the left boundary of the screen
                if player_pos[0] > player_size[0] // 2:
                    player_pos[0] = max(player_pos[0] - player_speed, 0)  # Limit to left screen boundary
                else:
                    player_x_offset = min(player_x_offset + player_speed, 0)  # Prevent background from going past starting point
                # Update animation for left walking
                walking_animation_frame = (walking_animation_frame + 1) % 2
                last_update_time = pygame.time.get_ticks()

            # Vertical movement
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= VERTICAL_SPEED
                # Update animation for up walking
                walking_animation_frame = (walking_animation_frame + 1) % 2
                last_update_time = pygame.time.get_ticks()
            elif keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size[1]:
                player_pos[1] += VERTICAL_SPEED
                # Update animation for down walking
                walking_animation_frame = (walking_animation_frame + 1) % 2
                last_update_time = pygame.time.get_ticks()

        # Draw player animation
        if keys[pygame.K_RIGHT]:
            if walking_animation_frame == 0:
                screen.blit(player_walk_right_1, (player_pos[0], player_pos[1]))
            else:
                screen.blit(player_walk_right_2, (player_pos[0], player_pos[1]))
        elif keys[pygame.K_LEFT]:
            if walking_animation_frame == 0:
                screen.blit(player_walk_left_1, (player_pos[0], player_pos[1]))
            else:
                screen.blit(player_walk_left_2, (player_pos[0], player_pos[1]))
        elif keys[pygame.K_UP]:
            if walking_animation_frame == 0:
                screen.blit(player_walk_up_1, (player_pos[0], player_pos[1]))
            else:
                screen.blit(player_walk_up_2, (player_pos[0], player_pos[1]))
        elif keys[pygame.K_DOWN]:
            if walking_animation_frame == 0:
                screen.blit(player_walk_down_1, (player_pos[0], player_pos[1]))
            else:
                screen.blit(player_walk_down_2, (player_pos[0], player_pos[1]))
        else:
            # When idle, use the "look" images
            screen.blit(player_sprite_right, (player_pos[0], player_pos[1]))  # Default to right-facing idle state

        # Reset current_details if no NPC is nearby
        current_details = None

        # Draw and handle all NPCs
        for i, (npc_x, npc_y) in enumerate(npc_positions):
            adjusted_x = npc_x + player_x_offset
            if 0 < adjusted_x < WIDTH:  # Only draw NPCs on screen
                # screen.blit(npc_sprite, (adjusted_x, npc_y))
                screen.blit(npc_image,(adjusted_x,npc_y))
                
                # Check for interaction with this NPC
                if check_npc_interaction(player_pos[0], player_pos[1], adjusted_x, npc_y):
                    current_details = laws_info[i]
                    if not showing_details:
                        prompt_text = main_font.render("Press SPACE to learn more", True, BLACK)
                        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT - 50))

        # Draw the legal info with white background if we are showing details
        if showing_details and current_details:
            info_width = WIDTH - 100  # Width of the info box
            info_height = 320  # Height of the info box
            info_x = 50
            info_y = HEIGHT // 4  # Center the box vertically

         
    
            info_box_surface = pygame.Surface((info_width, info_height), pygame.SRCALPHA)

            # Fill the surface with a semi-transparent black (you can adjust the alpha value for transparency)
            info_box_surface.fill((0, 0, 0, 128))  # (R, G, B, A), where A is the alpha (transparency)

            # Blit the surface onto the main screen
            screen.blit(info_box_surface, (info_x, info_y))

            # Draw the title and description with more space in between
            y_offset = draw_text_wrapped(screen, f"{current_details['title']}", title_font, WHITE, info_x + 10, info_y + 10, info_width - 20)
            
            # Add additional vertical space (increase this value for more spacing)
            y_offset += 20  # Space between title and description
            y_offset = draw_text_wrapped(screen, f"{current_details['description']}", main_font, WHITE, info_x + 10, y_offset, info_width - 20)

            # Add more space between the description and the details
            y_offset += 20  # Space between description and details

            # Draw detailed information with additional space between each point
            for detail in current_details["details"]:
                y_offset = draw_text_wrapped(screen, detail, detail_font, WHITE, info_x + 10, y_offset, info_width - 20)
                y_offset += 10  # Space between each detail

        # Update the remaining text only when space is pressed and an NPC is interacted with
        if space_pressed:
            remaining_text = main_font.render(f"Find all {len(npc_positions) - len(visited_npcs)} remaining legal documents", True, WHITE)
            screen.blit(remaining_text, (WIDTH // 2 - remaining_text.get_width() // 2, 20))
            space_pressed = False  # Reset space flag after updating

        # Draw exit logic
        exit_x = npc_positions[-1][0] + 400 + player_x_offset
        exit_rect = pygame.Rect(exit_x, HEIGHT // 2, 50, 50)
        
        # Only allow exit if all NPCs have been visited
        if len(visited_npcs) == len(npc_positions):
            pygame.draw.rect(screen, GREEN, exit_rect)  # Green exit means it's available
            if exit_rect.collidepoint(player_pos[0] - player_x_offset, player_pos[1]):
                quiz()
                return
        else:
            pygame.draw.rect(screen, RED, exit_rect)  # Red exit means player needs to visit more NPCs
            # Draw instruction about visiting all NPCs
            remaining_text = main_font.render(f"Find all {len(npc_positions) - len(visited_npcs)} remaining legal documents", True, WHITE)
            screen.blit(remaining_text, (WIDTH // 2 - remaining_text.get_width() // 2, 20))

        pygame.display.flip()



    # Show completion screen
    screen.fill(WHITE)
    completion_text = title_font.render("Congratulations! Tutorial Complete!", True, BLACK)
    screen.blit(completion_text, (WIDTH // 2 - completion_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    
    # Wait for a moment
    pygame.time.wait(3000)

if __name__ == "__main__":
    office_level()
    pygame.quit()