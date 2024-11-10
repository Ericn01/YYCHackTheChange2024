import pygame
import sys
from typing import Dict, List, Tuple

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Canadian Law Tutorial")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (200, 50, 50)
NPC_COLOR = (180, 100, 50)
GREEN = (34, 139, 34)

# Player settings
player_pos = [100, HEIGHT // 2]
player_speed = 0.25
player_size = (50, 50)
VERTICAL_SPEED = 0.25  # Added vertical speed

# Load Sprites
player_sprite = pygame.Surface(player_size)
player_sprite.fill(BLUE)

npc_sprite = pygame.Surface((50, 50))
npc_sprite.fill(NPC_COLOR)

# Law NPCs with detailed information
laws_info = [
    {
        "title": "Freedom of Expression",
        "description": "Freedom of expression is protected under the Canadian Charter of Rights and Freedoms.",
        "details": [
            "Includes freedom of speech, press, and other forms of communication",
            "Has reasonable limits to prevent hate speech",
            "Protects peaceful protests and demonstrations",
            "Applies to various forms of expression including art and music"
        ]
    },
    {
        "title": "Privacy Rights",
        "description": "Personal information is protected under Canadian privacy laws.",
        "details": [
            "Organizations must get consent to collect personal data",
            "Individuals have the right to access their personal information",
            "Companies must protect stored personal information",
            "Privacy breaches must be reported to affected individuals"
        ]
    },
    {
        "title": "Property Laws",
        "description": "Canadian law protects property rights and establishes ownership rules.",
        "details": [
            "Defines ownership and transfer of property",
            "Protects against theft and damage",
            "Establishes rules for landlords and tenants",
            "Covers both physical and intellectual property"
        ]
    },
    {
        "title": "Anti-Discrimination",
        "description": "The Canadian Human Rights Act prohibits discrimination based on protected grounds.",
        "details": [
            "Protects against discrimination in employment",
            "Covers housing and public services",
            "Includes multiple protected grounds like race, gender, and disability",
            "Requires reasonable accommodation"
        ]
    },
    {
        "title": "Right to Assembly",
        "description": "Canadians have the right to peaceful assembly and association.",
        "details": [
            "Allows for peaceful protests and demonstrations",
            "Protects formation of unions and associations",
            "Must be conducted peacefully and lawfully",
            "May require permits for large gatherings"
        ]
    }
]

# NPC positions with varied y positions
npc_positions = [
    (400, HEIGHT // 2 - 100),
    (1200, HEIGHT // 2 + 50),
    (2000, HEIGHT // 2 - 50),
    (2800, HEIGHT // 2 + 100),
    (3600, HEIGHT // 2 - 75)
]

# Scenario-based quiz questions
scenarios = [
    {
        "scenario": "Sarah wants to organize a peaceful protest against climate change at a public park. The protest will include speeches and signs.",
        "question": "Is Sarah's planned protest protected under Canadian law?",
        "answer": "yes",
        "explanation": "Yes, peaceful protests are protected under freedom of expression and right to assembly, though permits may be required."
    },
    {
        "scenario": "A company wants to share its customer database with partners without getting permission from customers.",
        "question": "Is this practice allowed under privacy laws?",
        "answer": "no",
        "explanation": "No, companies must obtain consent before sharing personal information with third parties."
    },
    {
        "scenario": "Alex borrowed their neighbor's lawn mower and decided to keep it without permission.",
        "question": "Is this action legal under property laws?",
        "answer": "no",
        "explanation": "No, this would be considered theft and violates property laws."
    },
    {
        "scenario": "An employer refuses to hire qualified candidates based on their religion.",
        "question": "Is this practice legal under Canadian law?",
        "answer": "no",
        "explanation": "No, this is discrimination based on religion and is prohibited under the Human Rights Act."
    },
    {
        "scenario": "Workers at a factory want to form a union to negotiate better working conditions.",
        "question": "Do they have the right to form a union?",
        "answer": "yes",
        "explanation": "Yes, the right to form unions is protected under freedom of association."
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

def tutorial_level():
    in_tutorial = True
    showing_details = False
    current_details = None
    player_x_offset = 0
    visited_npcs = set()  # Track which NPCs have been visited

    # Loading in the background image
    background = pygame.image.load('images/main_menu_background2.jpg').convert()

    while in_tutorial:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_details is not None:
                    showing_details = not showing_details
                elif event.key == pygame.K_ESCAPE:
                    showing_details = False

        # Movement controls with boundary checking
        if not showing_details:
            keys = pygame.key.get_pressed()
            # Horizontal movement
            if keys[pygame.K_RIGHT]:
                if player_pos[0] < WIDTH // 2 or player_x_offset <= -npc_positions[-1][0] + WIDTH - 200:
                    player_pos[0] += player_speed
                else:
                    player_x_offset -= player_speed
            elif keys[pygame.K_LEFT]:
                if player_pos[0] > WIDTH // 2 or player_x_offset >= 0:
                    player_pos[0] -= player_speed
                else:
                    player_x_offset += player_speed
            
            # Vertical movement
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= VERTICAL_SPEED
            elif keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size[1]:
                player_pos[1] += VERTICAL_SPEED

        # Draw player
        screen.blit(player_sprite, (player_pos[0], player_pos[1]))

        # Reset current_details if no NPC is nearby
        current_details = None

        # Draw and handle all NPCs
        for i, (npc_x, npc_y) in enumerate(npc_positions):
            adjusted_x = npc_x + player_x_offset
            if 0 < adjusted_x < WIDTH:  # Only draw NPCs on screen
                screen.blit(npc_sprite, (adjusted_x, npc_y))
                
                # Check for interaction with this NPC
                if check_npc_interaction(player_pos[0], player_pos[1], adjusted_x, npc_y):
                    current_details = laws_info[i]
                    if not showing_details:
                        prompt_text = main_font.render("Press SPACE to learn more", True, BLACK)
                        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT - 50))
                    visited_npcs.add(i)

        # Show detailed information when activated
        if showing_details and current_details is not None:
            # Draw semi-transparent background
            s = pygame.Surface((WIDTH, HEIGHT))
            s.set_alpha(128)
            s.fill(WHITE)
            screen.blit(s, (0, 0))
            
            # Draw information panel
            info_surface = pygame.Surface((WIDTH - 100, HEIGHT - 100))
            info_surface.fill(WHITE)
            pygame.draw.rect(info_surface, BLACK, info_surface.get_rect(), 2)
            
            # Title
            title_surface = title_font.render(current_details["title"], True, BLACK)
            info_surface.blit(title_surface, (20, 20))
            
            # Description
            y_offset = draw_text_wrapped(info_surface, current_details["description"], main_font, BLACK, 20, 80, WIDTH - 140)
            
            # Details
            y_offset += 20
            for detail in current_details["details"]:
                y_offset = draw_text_wrapped(info_surface, "• " + detail, detail_font, BLACK, 20, y_offset, WIDTH - 140)
            
            # Draw close instruction
            close_text = main_font.render("Press SPACE or ESC to close", True, BLACK)
            info_surface.blit(close_text, (20, HEIGHT - 160))
            
            screen.blit(info_surface, (50, 50))

        # Draw exit
        exit_x = npc_positions[-1][0] + player_x_offset
        exit_rect = pygame.Rect(exit_x, HEIGHT // 2, 50, 50)
        
        # Only allow exit if all NPCs have been visited
        if len(visited_npcs) == len(npc_positions):
            pygame.draw.rect(screen, GREEN, exit_rect)  # Green exit means it's available
            if exit_rect.collidepoint(player_pos[0], player_pos[1]):
                quiz()
                return
        else:
            pygame.draw.rect(screen, RED, exit_rect)  # Red exit means player needs to visit more NPCs
            # Draw instruction about visiting all NPCs
            remaining_text = main_font.render(f"Visit all {len(npc_positions) - len(visited_npcs)} remaining NPCs", True, RED)
            screen.blit(remaining_text, (WIDTH // 2 - remaining_text.get_width() // 2, 20))

        pygame.display.flip()

def quiz():
    current_scenario = 0
    showing_explanation = False
    
    yes_button = Button(WIDTH // 4 - 100, HEIGHT - 100, 200, 50, "YES", GREEN)
    no_button = Button(3 * WIDTH // 4 - 100, HEIGHT - 100, 200, 50, "NO", RED)

    while current_scenario < len(scenarios):
        screen.fill(WHITE)
        
        scenario = scenarios[current_scenario]
        
        if not showing_explanation:
            # Draw scenario
            y_offset = draw_text_wrapped(screen, "Scenario:", title_font, BLACK, 50, 50, WIDTH - 100)
            y_offset = draw_text_wrapped(screen, scenario["scenario"], main_font, BLACK, 50, y_offset + 20, WIDTH - 100)
            
            # Draw question
            y_offset = draw_text_wrapped(screen, "Question:", title_font, BLACK, 50, y_offset + 40, WIDTH - 100)
            y_offset = draw_text_wrapped(screen, scenario["question"], main_font, BLACK, 50, y_offset + 20, WIDTH - 100)
            
            # Draw buttons
            yes_button.draw(screen)
            no_button.draw(screen)
        else:
            # Draw explanation
            y_offset = draw_text_wrapped(screen, "Explanation:", title_font, BLACK, 50, 50, WIDTH - 100)
            y_offset = draw_text_wrapped(screen, scenario["explanation"], main_font, BLACK, 50, y_offset + 20, WIDTH - 100)
            
            # Draw continue instruction
            continue_text = main_font.render("Press SPACE to continue", True, BLACK)
            screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT - 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and showing_explanation:
                if event.key == pygame.K_SPACE:
                    showing_explanation = False
                    current_scenario += 1
            elif not showing_explanation:
                if yes_button.handle_event(event):
                    if scenario["answer"] == "yes":
                        showing_explanation = True
                elif no_button.handle_event(event):
                    if scenario["answer"] == "no":
                        showing_explanation = True

        pygame.display.flip()

    # Show completion screen
    screen.fill(WHITE)
    completion_text = title_font.render("Congratulations! Tutorial Complete!", True, BLACK)
    screen.blit(completion_text, (WIDTH // 2 - completion_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    
    # Wait for a moment
    pygame.time.wait(3000)

if __name__ == "__main__":
    tutorial_level()
    pygame.quit()