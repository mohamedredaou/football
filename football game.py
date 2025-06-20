import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("football")

BLUE = (0, 120, 255)
RED = (255, 50, 50)
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

PLAYER_SIZE = 40
BALL_RADIUS = 15
GOAL_WIDTH = 120
GOAL_HEIGHT = 80
GOAL_DEPTH = 20

PLAYER_SPEED = 5
BALL_SPEED = 7
FRICTION = 0.98

player1 = pygame.Rect(100, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
player2 = pygame.Rect(WIDTH - 100 - PLAYER_SIZE, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
ball = [WIDTH // 2, HEIGHT // 2]
ball_velocity = [0, 0]

score_blue = 0
score_red = 0
font = pygame.font.SysFont(None, 36)

# إنشاء المرميين
goal_blue = pygame.Rect(0, HEIGHT // 2 - GOAL_HEIGHT // 2, GOAL_DEPTH, GOAL_HEIGHT)
goal_red = pygame.Rect(WIDTH - GOAL_DEPTH, HEIGHT // 2 - GOAL_HEIGHT // 2, GOAL_DEPTH, GOAL_HEIGHT)

# دالة لرسم عناصر 3D بسيطة
def draw_3d_rect(surface, rect, color, depth):
    # الوجه الأمامي
    pygame.draw.rect(surface, color, rect)
    
    # الجوانب الجانبية (تأثير 3D)
    pygame.draw.polygon(surface, pygame.Color(color).lerp(BLACK, 0.3), [
        (rect.right, rect.top),
        (rect.right + depth, rect.top - depth // 2),
        (rect.right + depth, rect.bottom - depth // 2),
        (rect.right, rect.bottom)
    ])
    pygame.draw.polygon(surface, pygame.Color(color).lerp(BLACK, 0.5), [
        (rect.left, rect.bottom),
        (rect.left, rect.top),
        (rect.left + depth, rect.top - depth // 2),
        (rect.left + depth, rect.bottom - depth // 2)
    ])

# دالة لرسم الكرة
def draw_ball(x, y):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), BALL_RADIUS)
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), BALL_RADIUS, 2)
    
    # تفاصيل الكرة
    pygame.draw.line(screen, BLACK, (x - BALL_RADIUS + 5, y), (x + BALL_RADIUS - 5, y), 2)
    pygame.draw.arc(screen, BLACK, (x - 10, y - 10, 20, 20), 0, math.pi, 2)
    pygame.draw.arc(screen, BLACK, (x - 10, y - 10, 20, 20), math.pi, 2 * math.pi, 2)

# حلقة اللعبة الرئيسية
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a] and player1.left > 0:
        player1.x -= PLAYER_SPEED
    if keys[pygame.K_d] and player1.right < WIDTH:
        player1.x += PLAYER_SPEED
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PLAYER_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PLAYER_SPEED
    
    if keys[pygame.K_LEFT] and player2.left > 0:
        player2.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player2.right < WIDTH:
        player2.x += PLAYER_SPEED
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PLAYER_SPEED
    
    ball[0] += ball_velocity[0]
    ball[1] += ball_velocity[1]
    ball_velocity[0] *= FRICTION
    ball_velocity[1] *= FRICTION
    
    if ball[0] - BALL_RADIUS < 0:
        ball[0] = BALL_RADIUS
        ball_velocity[0] = -ball_velocity[0] * 0.8
    if ball[0] + BALL_RADIUS > WIDTH:
        ball[0] = WIDTH - BALL_RADIUS
        ball_velocity[0] = -ball_velocity[0] * 0.8
    if ball[1] - BALL_RADIUS < 0:
        ball[1] = BALL_RADIUS
        ball_velocity[1] = -ball_velocity[1] * 0.8
    if ball[1] + BALL_RADIUS > HEIGHT:
        ball[1] = HEIGHT - BALL_RADIUS
        ball_velocity[1] = -ball_velocity[1] * 0.8

    for player, color in [(player1, BLUE), (player2, RED)]:
        dx = ball[0] - player.centerx
        dy = ball[1] - player.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < PLAYER_SIZE // 2 + BALL_RADIUS:
            angle = math.atan2(dy, dx)

            target_x = player.centerx + (PLAYER_SIZE // 2 + BALL_RADIUS) * math.cos(angle)
            target_y = player.centery + (PLAYER_SIZE // 2 + BALL_RADIUS) * math.sin(angle)
            ball[0] = target_x
            ball[1] = target_y

            speed_factor = 1.5
            ball_velocity[0] = math.cos(angle) * BALL_SPEED * speed_factor
            ball_velocity[1] = math.sin(angle) * BALL_SPEED * speed_factor

    if goal_blue.collidepoint(ball[0], ball[1]):
        score_red += 1
        ball = [WIDTH // 2, HEIGHT // 2]
        ball_velocity = [0, 0]
        pygame.time.delay(1000)
    
    if goal_red.collidepoint(ball[0], ball[1]):
        score_blue += 1
        ball = [WIDTH // 2, HEIGHT // 2]
        ball_velocity = [0, 0]
        pygame.time.delay(1000)

    screen.fill(GREEN)

    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 80, 2)

    draw_3d_rect(screen, goal_blue, BLUE, 10)
    draw_3d_rect(screen, goal_red, RED, -10)

    pygame.draw.rect(screen, BLUE, player1)
    pygame.draw.rect(screen, RED, player2)

    pygame.draw.circle(screen, WHITE, player1.center, PLAYER_SIZE // 3)
    pygame.draw.circle(screen, WHITE, player2.center, PLAYER_SIZE // 3)

    draw_ball(ball[0], ball[1])
    
    score_text = font.render(f"blue: {score_blue}  -  red : {score_red}", True, YELLOW)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    
    controls = font.render("player blue : WASD  |  player red : stocks", True, YELLOW)
    screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)
