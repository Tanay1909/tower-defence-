import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock for FPS control
clock = pygame.time.Clock()
FPS = 60

# Game variables
player_health = 10
currency = 100
enemy_speed = 2
tower_cost = 50

# Path for enemies (list of points)
path = [(50, 50), (750, 50), (750, 550), (50, 550)]

# Enemy class
class Enemy:
    def __init__(self):
        self.x, self.y = path[0]
        self.path_index = 0
        self.health = 5

    def move(self):
        if self.path_index < len(path) - 1:
            target_x, target_y = path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            dist = math.hypot(dx, dy)
            if dist < enemy_speed:
                self.path_index += 1
            else:
                self.x += enemy_speed * dx / dist
                self.y += enemy_speed * dy / dist

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 10)

    def reached_end(self):
        return self.path_index == len(path) - 1

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.cooldown = 30
        self.timer = 0

    def shoot(self, enemies):
        if self.timer == 0:
            for enemy in enemies:
                dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if dist <= self.range:
                    enemy.health -= 1
                    self.timer = self.cooldown
                    break
        else:
            self.timer -= 1

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), 15)
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.range, 1)

# Initialize enemies and towers
enemies = [Enemy()]
towers = []

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if currency >= tower_cost:
                towers.append(Tower(mx, my))
                currency -= tower_cost

    # Draw path
    for i in range(len(path) - 1):
        pygame.draw.line(screen, BLACK, path[i], path[i + 1], 5)

    # Update and draw enemies
    for enemy in enemies[:]:
        enemy.move()
        enemy.draw()
        if enemy.reached_end():
            player_health -= 1
            enemies.remove(enemy)
        elif enemy.health <= 0:
            enemies.remove(enemy)
            currency += 10

    # Update and draw towers
    for tower in towers:
        tower.shoot(enemies)
        tower.draw()

    # Spawn new enemies
    if pygame.time.get_ticks() % 2000 < FPS:
        enemies.append(Enemy())

    # Draw HUD
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {player_health}", True, BLACK)
    currency_text = font.render(f"Currency: {currency}", True, BLACK)
    screen.blit(health_text, (10, 10))
    screen.blit(currency_text, (10, 50))

    # End game if health is 0
    if player_health <= 0:
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    pygame.display.flip()

pygame.quit()
