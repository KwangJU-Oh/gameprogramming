import pygame
import math
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("탄성 충돌 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# 물리 엔진 설정
class Ball:
    def __init__(self, x, y, radius, color, mass=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # 화면 경계 충돌
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy *= -1

def detect_collision(ball1, ball2):
    dx = ball1.x - ball2.x
    dy = ball1.y - ball2.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance < ball1.radius + ball2.radius:
        return True
    return False

def resolve_collision(ball1, ball2):
    dx = ball1.x - ball2.x
    dy = ball1.y - ball2.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance == 0:
        return

    # 충돌 방향 단위 벡터
    nx = dx / distance
    ny = dy / distance

    # 상대 속도
    dvx = ball1.vx - ball2.vx
    dvy = ball1.vy - ball2.vy

    # 속도 차원의 투영
    velocity_along_normal = dvx * nx + dvy * ny

    # 물체가 서로 멀어지고 있으면 무시
    if velocity_along_normal > 0:
        return

    # 충돌 반발 계수 (탄성 충돌)
    e = 1.0

    # 충돌량 계산
    j = -(1 + e) * velocity_along_normal
    j /= (1 / ball1.mass + 1 / ball2.mass)

    # 충격량을 각 물체에 적용
    impulse_x = j * nx
    impulse_y = j * ny

    ball1.vx += impulse_x / ball1.mass
    ball1.vy += impulse_y / ball1.mass
    ball2.vx -= impulse_x / ball2.mass
    ball2.vy -= impulse_y / ball2.mass

# 게임 초기화
player = Ball(100, 100, 20, BLUE, mass=2)
goal = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 50, 100, 100)

balls = [Ball(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 20, RED) for _ in range(5)]

running = True
while running:
    screen.fill(WHITE)

    # 종료 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 플레이어 조작
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.vx -= 0.2
    if keys[pygame.K_RIGHT]:
        player.vx += 0.2
    if keys[pygame.K_UP]:
        player.vy -= 0.2
    if keys[pygame.K_DOWN]:
        player.vy += 0.2

    # 공 움직임
    player.move()
    for ball in balls:
        ball.move()

    # 충돌 처리
    for ball in balls:
        if detect_collision(player, ball):
            resolve_collision(player, ball)
        for other_ball in balls:
            if ball != other_ball and detect_collision(ball, other_ball):
                resolve_collision(ball, other_ball)

    # 목표 지점
    pygame.draw.rect(screen, GREEN, goal)
    if goal.collidepoint(player.x, player.y):
        print("목표 도달!")
        running = False

    # 공 그리기
    player.draw()
    for ball in balls:
        ball.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
