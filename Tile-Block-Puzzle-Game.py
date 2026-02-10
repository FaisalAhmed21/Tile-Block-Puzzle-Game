import pygame
import random
import time
import asyncio

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Tile Block Puzzle Game")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 255, 0), # Yellow
    (0, 255, 255), # Cyan
    (255, 0, 255)  # Magenta
]

RAINBOW_COLORS = [
    (255, 0, 0),   # Red
    (255, 165, 0), # Orange
    (255, 255, 0), # Yellow
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (75, 0, 130),  # Indigo
    (238, 130, 238) # Violet
]

# Button settings
BUTTON_WIDTH = 30
BUTTON_HEIGHT = 30
BUTTON_MARGIN = 10
BUTTON_Y = 10

# Control Buttons class
class ControlButton:
    def __init__(self, x, y, width, height, color, hover_color, icon_func):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.icon_func = icon_func
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=5)
        self.icon_func(surface, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        return self.is_hovered and event.type == pygame.MOUSEBUTTONDOWN

def draw_cross(surface, rect):
    margin = 8
    pygame.draw.line(surface, WHITE, 
                    (rect.x + margin, rect.y + margin),
                    (rect.x + rect.width - margin, rect.y + rect.height - margin), 2)
    pygame.draw.line(surface, WHITE,
                    (rect.x + margin, rect.y + rect.height - margin),
                    (rect.x + rect.width - margin, rect.y + margin), 2)

def draw_pause_play(surface, rect, is_paused):
    margin = 8
    if is_paused:
        # Draw play triangle
        points = [(rect.x + margin, rect.y + margin),
                 (rect.x + margin, rect.y + rect.height - margin),
                 (rect.x + rect.width - margin, rect.y + rect.height//2)]
        pygame.draw.polygon(surface, WHITE, points)
    else:
        # Draw pause bars
        bar_width = 4
        pygame.draw.rect(surface, WHITE, 
                        (rect.x + margin, rect.y + margin, 
                         bar_width, rect.height - 2*margin))
        pygame.draw.rect(surface, WHITE,
                        (rect.x + rect.width - margin - bar_width, rect.y + margin,
                         bar_width, rect.height - 2*margin))

def draw_restart(surface, rect):
    margin = 6
    
    # Calculate arrow dimensions
    arrow_width = rect.width - (2 * margin)
    arrow_height = rect.height - (2 * margin)
    
    # Calculate points for a clean back arrow
    # Main arrow line
    start_x = rect.x + rect.width - margin
    end_x = rect.x + margin
    mid_y = rect.y + (rect.height // 2)
    
    # Arrow head points
    head_height = arrow_height // 2
    head_x = end_x
    head_top_y = mid_y - head_height // 2
    head_bottom_y = mid_y + head_height // 2
    
    # Draw the arrow line
    pygame.draw.line(surface, WHITE, 
                    (start_x, mid_y),
                    (end_x, mid_y), 2)
    
    # Draw arrow head
    arrow_head_points = [
        (head_x, mid_y),
        (head_x + head_height//2, head_top_y),
        (head_x + head_height//2, head_bottom_y)
    ]
    pygame.draw.polygon(surface, WHITE, arrow_head_points)

# Block shapes
SHAPES = [
    [[1, 1],
     [1, 1]],

    [[1, 0],
     [1, 0],
     [1, 1]],

    [[0, 1],
     [0, 1],
     [1, 1]],

    [[1, 1, 1],
     [0, 1, 0]]
]

# Grid settings
GRID_WIDTH = 10
GRID_HEIGHT = 15
TILE_SIZE = 40

# Initialize grid
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_cube(surface, color, rect):
    """Draw a single cube with grid lines"""
    pygame.draw.rect(surface, color, rect)
    # Draw outer border
    pygame.draw.rect(surface, (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40)), rect, 1)
    
    # Draw inner vertical lines
    for i in range(1, 3):
        x = rect.x + (rect.width * i) // 3
        pygame.draw.line(surface, (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40)),
                        (x, rect.y), (x, rect.y + rect.height))
    
    # Draw inner horizontal lines
    for i in range(1, 3):
        y = rect.y + (rect.height * i) // 3
        pygame.draw.line(surface, (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40)),
                        (rect.x, y), (rect.x + rect.width, y))

def draw_grid():
    """Draw the game grid and background grid lines"""
    # Draw background grid lines
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, (50, 50, 50), 
                        (x * TILE_SIZE, 0), 
                        (x * TILE_SIZE, GRID_HEIGHT * TILE_SIZE))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, (50, 50, 50), 
                        (0, y * TILE_SIZE), 
                        (GRID_WIDTH * TILE_SIZE, y * TILE_SIZE))
    
    # Draw filled blocks
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                draw_cube(screen, grid[y][x], rect)


    

def draw_block(block, pos, color):
    """Draw the current block"""
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (pos[0] + x) * TILE_SIZE, (pos[1] + y) * TILE_SIZE, TILE_SIZE, TILE_SIZE
                )
                draw_cube(screen, color, rect)

def check_collision(block, pos):
    """Check if block collides with boundaries or other blocks"""
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                grid_x = pos[0] + x
                grid_y = pos[1] + y
                # Check boundaries
                if (grid_x < 0 or grid_x >= GRID_WIDTH or 
                    grid_y >= GRID_HEIGHT or 
                    (grid_y >= 0 and grid[grid_y][grid_x] is not None)):
                    return True
    return False

def check_obstacle_collision(block, pos, obstacle_x, obstacle_y):
    """Check if block collides with obstacle"""
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                grid_x = pos[0] + x
                grid_y = pos[1] + y
                if grid_x == obstacle_x and grid_y == obstacle_y:
                    return True
    return False

def lock_block(block, pos, color):
    """Lock the block in place on the grid and award points"""
    global score
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell and 0 <= pos[1] + y < GRID_HEIGHT:
                grid[pos[1] + y][pos[0] + x] = color
    # Award exactly 10 points for locking a block (without obstacle collision)
    score += 10  # Only add 10 points, no more

def clear_rows():
    """Clear completed rows and return number of rows cleared"""
    global grid, score
    rows_cleared = 0
    y = GRID_HEIGHT - 1
    cleared_rows = []
    
    # First pass: identify completed rows
    while y >= 0:
        if all(cell is not None for cell in grid[y]):
            cleared_rows.append(y)
            rows_cleared += 1
        y -= 1
    
    # Second pass: clear the rows and shift blocks down
    if cleared_rows:
        # Remove the cleared rows
        for row in sorted(cleared_rows):
            del grid[row]
            # Add new empty row at the top
            grid.insert(0, [None for _ in range(GRID_WIDTH)])
        
        # Award points based on number of rows cleared
        if rows_cleared == 1:
            score += 10  # Extra 10 points for clearing one row
        elif rows_cleared > 1:
            score += 20  # Extra 20 points for clearing multiple rows
    
    return rows_cleared

def get_free_spaces():
    """Get list of all free spaces in the grid"""
    free_spaces = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] is None:  # If the cell is empty
                free_spaces.append((x, y))
    return free_spaces

def generate_obstacle():
    """Generate new obstacle position and color in free space"""
    free_spaces = get_free_spaces()
    
    # If there are no free spaces, return None values
    if not free_spaces:
        return None, None, None
    
    # Choose a random free position
    x_pos, y_pos = random.choice(free_spaces)
    obstacle_color = random.choice(RAINBOW_COLORS)
    return (x_pos, y_pos, obstacle_color)


def generate_new_block():
    """Generate new block with random shape and color"""
    new_block = random.choice(SHAPES)
    new_color = random.choice(COLORS)
    new_pos = [GRID_WIDTH // 2 - len(new_block[0]) // 2, 0]
    return new_block, new_color, new_pos


def reset_game():
    """Reset all game variables to initial state"""
    global grid, lives, score, current_block, current_color, current_pos, game_over
    global timer_start, timer_running, obstacle_x, obstacle_y, obstacle_color, collision_count, game_exited
    
    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    lives = 3
    score = 0
    current_block = random.choice(SHAPES)
    current_color = random.choice(COLORS)
    current_pos = [GRID_WIDTH // 2 - len(current_block[0]) // 2, 0]
    game_over = False
    timer_start = pygame.time.get_ticks()
    timer_running = True
    obstacle_x, obstacle_y, obstacle_color = generate_obstacle()
    collision_count = 0
    game_exited = False

# Initialize control buttons
close_button = ControlButton(400 - BUTTON_WIDTH - BUTTON_MARGIN, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, RED, (200, 0, 0), draw_cross)
pause_button = ControlButton(400 - 2*BUTTON_WIDTH - 2*BUTTON_MARGIN, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, GREEN, (0, 200, 0), lambda s, r: draw_pause_play(s, r, not timer_running))
restart_button = ControlButton(400 - 3*BUTTON_WIDTH - 3*BUTTON_MARGIN, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, (0, 0, 200), draw_restart)

# Main game variables
lives = 3
score = 0
current_block = random.choice(SHAPES)
current_color = random.choice(COLORS)
current_pos = [GRID_WIDTH // 2 - len(current_block[0]) // 2, 0]
game_over = False

fall_speed = 500  # Faster falling speed (milliseconds)
last_fall_time = pygame.time.get_ticks()

timer_start = pygame.time.get_ticks()
game_duration = 60000  # 1 minute
timer_running = True

obstacle_x, obstacle_y, obstacle_color = generate_obstacle()
collision_count = 0
running = True
elapsed_time = 0
game_exited = False

# Touch control variables
touch_start_pos = None
touch_start_time = 0
MIN_SWIPE_DISTANCE = 30  # Minimum distance for swipe detection
TAP_MAX_DURATION = 300  # Maximum time for tap (milliseconds)

async def main():
    """Main async game loop"""
    global running, screen, clock, game_over, current_block, current_color, current_pos
    global last_fall_time, timer_running, elapsed_time, lives, score, obstacle_x, obstacle_y, obstacle_color
    global collision_count, game_exited, touch_start_pos, touch_start_time
    
    while running:
        screen.fill(BLACK)
        
        # Draw game elements only if not game over
        if not game_over:
            draw_grid()
            draw_block(current_block, current_pos, current_color)
            
            # Draw obstacle
            obstacle_rect = pygame.Rect(obstacle_x * TILE_SIZE, obstacle_y * TILE_SIZE, 
                                      TILE_SIZE, TILE_SIZE)
            draw_cube(screen, obstacle_color, obstacle_rect)
            
            # Display stats
            elapsed_time = pygame.time.get_ticks() - timer_start if timer_running else elapsed_time
            time_left = max(0, (game_duration - elapsed_time) // 1000)
            font = pygame.font.SysFont(None, 36)
            time_text = font.render(f"Time: {time_left}s", True, WHITE)
            lives_text = font.render(f"Lives: {lives}", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(time_text, (10, 10))
            screen.blit(lives_text, (10, 50))
            screen.blit(score_text, (10, 90))

        # Draw control buttons
        close_button.draw(screen)
        pause_button.draw(screen)
        restart_button.draw(screen)

        if game_over:
            game_over_reason = ""
            if game_exited:
                game_over_reason = "Thanks for playing!"
            elif lives <= 0:
                game_over_reason = "Out of lives!"
            elif elapsed_time >= game_duration:
                game_over_reason = "Time's up!"
            else:
                game_over_reason = "Block collision!"
                
            restart_rect = display_game_over(screen, score, game_over_reason)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle button clicks in game over screen
                if close_button.handle_event(event):
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        reset_game()
                        game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Allow Enter key to restart
                        reset_game()
                        game_over = False
            
            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)  # Yield control to browser
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle button clicks
            if close_button.handle_event(event):
                game_over = True
                game_exited = True
            elif pause_button.handle_event(event):
                timer_running = not timer_running
            elif restart_button.handle_event(event):
                reset_game()

            # Touch controls for mobile
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and timer_running:
                # Check if touch is not on control buttons
                if not (close_button.rect.collidepoint(event.pos) or 
                       pause_button.rect.collidepoint(event.pos) or 
                       restart_button.rect.collidepoint(event.pos)):
                    touch_start_pos = event.pos
                    touch_start_time = pygame.time.get_ticks()
            
            elif event.type == pygame.MOUSEBUTTONUP and not game_over and timer_running:
                if touch_start_pos is not None:
                    touch_end_pos = event.pos
                    touch_duration = pygame.time.get_ticks() - touch_start_time
                    
                    dx = touch_end_pos[0] - touch_start_pos[0]
                    dy = touch_end_pos[1] - touch_start_pos[1]
                    distance = (dx**2 + dy**2)**0.5
                    
                    # Detect tap (short duration, small movement) - rotate
                    if touch_duration < TAP_MAX_DURATION and distance < MIN_SWIPE_DISTANCE:
                        rotated_block = list(zip(*current_block[::-1]))
                        if not check_collision(rotated_block, current_pos):
                            current_block = rotated_block
                    
                    # Detect swipe gestures
                    elif distance >= MIN_SWIPE_DISTANCE:
                        # Horizontal swipe is stronger
                        if abs(dx) > abs(dy):
                            if dx > 0:  # Swipe right
                                new_pos = [current_pos[0] + 1, current_pos[1]]
                                if not check_collision(current_block, new_pos):
                                    current_pos = new_pos
                            else:  # Swipe left
                                new_pos = [current_pos[0] - 1, current_pos[1]]
                                if not check_collision(current_block, new_pos):
                                    current_pos = new_pos
                        # Vertical swipe (down only)
                        else:
                            if dy > 0:  # Swipe down
                                new_pos = [current_pos[0], current_pos[1] + 1]
                                if not check_collision(current_block, new_pos):
                                    current_pos = new_pos
                    
                    touch_start_pos = None
            
            # Keyboard controls (still available)
            elif event.type == pygame.KEYDOWN and not game_over and timer_running:
                if event.key == pygame.K_LEFT:
                    new_pos = [current_pos[0] - 1, current_pos[1]]
                    if not check_collision(current_block, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = [current_pos[0] + 1, current_pos[1]]
                    if not check_collision(current_block, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = [current_pos[0], current_pos[1] + 1]
                    if not check_collision(current_block, new_pos):
                        current_pos = new_pos
                elif event.key == pygame.K_UP:
                    rotated_block = list(zip(*current_block[::-1]))
                    if not check_collision(rotated_block, current_pos):
                        current_block = rotated_block

        if timer_running and not game_over:
            # Check for obstacle collision during movement
            if check_obstacle_collision(current_block, current_pos, obstacle_x, obstacle_y):
                lives -= 1
                collision_count += 1
                
                # Generate new block and obstacle
                current_block, current_color, current_pos = generate_new_block()
                
                # Only generate new obstacle if there are free spaces
                new_obstacle = generate_obstacle()
                if new_obstacle[0] is not None:  # If a valid position was found
                    obstacle_x, obstacle_y, obstacle_color = new_obstacle
                
                if lives <= 0:
                    game_over = True
                    display_game_over(screen, score, "Out of lives!")

            # Handle block falling
            if pygame.time.get_ticks() - last_fall_time > fall_speed:
                last_fall_time = pygame.time.get_ticks()
                new_pos = [current_pos[0], current_pos[1] + 1]

                if not check_collision(current_block, new_pos):
                    current_pos = new_pos
                else:
                    lock_block(current_block, current_pos, current_color)
                    score += 10
                    clear_rows()
                    current_block = random.choice(SHAPES)
                    current_color = random.choice(COLORS)
                    current_pos = [GRID_WIDTH // 2 - len(current_block[0]) // 2, 0]
                    
                    if check_collision(current_block, current_pos):
                        game_over = True
                        display_game_over(screen, score, "Block collision!")
                    
                    # Generate new obstacle only in free space
                    new_obstacle = generate_obstacle()
                    if new_obstacle[0] is not None:  # If a valid position was found
                        obstacle_x, obstacle_y, obstacle_color = new_obstacle

            # Check if time is over
            if elapsed_time >= game_duration:
                game_over = True
                display_game_over(screen, score, "Time's up!")           

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)  # Yield control to browser

    pygame.quit()

def display_game_over(screen, score, reason):
    """Display game over screen with score, reason, and restart button"""
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.fill(BLACK)
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.SysFont(None, 48)
    
    # Game Over text
    game_over_text = font.render("Game Over!", True, WHITE)
    game_over_rect = game_over_text.get_rect(centerx=screen.get_width()//2, centery=screen.get_height()//2 - 90)
    screen.blit(game_over_text, game_over_rect)
    
    # Score text
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(centerx=screen.get_width()//2, centery=screen.get_height()//2 - 30)
    screen.blit(score_text, score_rect)
    
    # Reason text
    reason_text = font.render(f"{reason}", True, WHITE)
    reason_rect = reason_text.get_rect(centerx=screen.get_width()//2, centery=screen.get_height()//2 + 30)
    screen.blit(reason_text, reason_rect)
    
    # Draw restart button
    button_width = 200
    button_height = 50
    button_x = screen.get_width()//2 - button_width//2
    button_y = screen.get_height()//2 + 90
    restart_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, GREEN, restart_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, restart_rect, 2, border_radius=10)
    
    # Restart text
    restart_text = font.render("Restart", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=restart_rect.center)
    screen.blit(restart_text, restart_text_rect)
    
    pygame.display.flip()
    return restart_rect

# Run the async main function
asyncio.run(main())
