import pygame
import math
from typing import Tuple

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 900
HEX_RADIUS = 40
BOARD_SIZE = 6  # Hexagons per side

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
BACKGROUND = (240, 240, 240)
OUTLINE = (0, 0, 0)


class HexBoard:
    """Represents a hexagonal chess board using axial coordinates."""
    
    def __init__(self, size: int, hex_radius: float):
        self.size = size
        self.radius = hex_radius
        self.hexagons = self._generate_hexagons()
        
    def _generate_hexagons(self) -> dict:
        """Generate hexagon positions using axial coordinates (q, r)."""
        hexagons = {}
        
        # Generate hexagons in a hexagonal shape
        for q in range(-self.size + 1, self.size):
            r1 = max(-self.size + 1, -q - self.size + 1)
            r2 = min(self.size - 1, -q + self.size - 1)
            for r in range(r1, r2 + 1):
                color = self._get_hex_color(q, r)
                hexagons[(q, r)] = color
                
        return hexagons
    
    def _get_hex_color(self, q: int, r: int) -> Tuple[int, int, int]:
        """
        Determine hex color using 3-coloring algorithm.
        For hexagonal grids, we use: (q - r) mod 3
        This ensures no two adjacent hexagons have the same color.
        """
        s = -q - r  # s coordinate (q + r + s = 0)
        color_index = (q - r) % 3
        
        colors = [WHITE, BLACK, GREY]
        return colors[color_index]
    
    def axial_to_pixel(self, q: int, r: int, center_x: float, center_y: float) -> Tuple[float, float]:
        """Convert axial coordinates to pixel coordinates."""
        x = center_x + self.radius * (3/2 * q)
        y = center_y + self.radius * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
        return x, y
    
    def get_hex_corners(self, center_x: float, center_y: float) -> list:
        """Calculate the six corner points of a hexagon."""
        corners = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            x = center_x + self.radius * math.cos(angle_rad)
            y = center_y + self.radius * math.sin(angle_rad)
            corners.append((x, y))
        return corners


def draw_hexagon(surface: pygame.Surface, center: Tuple[float, float], 
                 radius: float, color: Tuple[int, int, int], outline_color: Tuple[int, int, int]):
    """Draw a single hexagon with outline."""
    corners = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        corners.append((x, y))
    
    # Draw filled hexagon
    pygame.draw.polygon(surface, color, corners)
    # Draw outline
    pygame.draw.polygon(surface, outline_color, corners, 2)


def main():
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Hexagonal Chess Board")
    clock = pygame.time.Clock()
    
    # Create the hex board
    board = HexBoard(BOARD_SIZE, HEX_RADIUS)
    
    # Calculate center of screen
    center_x = WINDOW_WIDTH // 2
    center_y = WINDOW_HEIGHT // 2
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen
        screen.fill(BACKGROUND)
        
        # Draw all hexagons
        for (q, r), color in board.hexagons.items():
            x, y = board.axial_to_pixel(q, r, center_x, center_y)
            draw_hexagon(screen, (x, y), board.radius, color, OUTLINE)
        
        # Draw info text
        # font = pygame.font.Font(None, 24)
        # text = font.render(f"Hexagonal Board: {BOARD_SIZE} per side", True, (0, 0, 0))
        # screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()