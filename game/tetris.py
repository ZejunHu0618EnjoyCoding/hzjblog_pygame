import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸与标题
WIDTH, HEIGHT = 300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris Game")

# 定义时钟用于控制游戏刷新率
clock = pygame.time.Clock()

# 网格配置：20行10列，每个格子尺寸（根据窗口尺寸计算）
ROWS, COLS = 20, 10
cell_size = WIDTH // COLS  # 30像素
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# 定义 Tetromino 形状（这里只定义部分形状，后续可扩展）
TETROMINOES = {
    'I': [[(0,1), (1,1), (2,1), (3,1)]],
    'O': [[(0,0), (0,1), (1,0), (1,1)]],
    'T': [[(0,1), (1,0), (1,1), (1,2)]],
    # 其他形状可以继续添加：L, J, S, Z 等
}

def check_collision(grid, shape, pos):
    """检查传入的方块（以偏移坐标定义）放置在 pos 位置是否会发生碰撞"""
    for (i, j) in shape:
        x = pos[0] + i
        y = pos[1] + j
        # 超出底部、左右边界或已填充的格子，则发生碰撞
        if x >= ROWS or y < 0 or y >= COLS or grid[x][y]:
            return True
    return False

def lock_tetromino(grid, shape, pos):
    """将当前方块固定到网格中"""
    for (i, j) in shape:
        grid[pos[0] + i][pos[1] + j] = 1

def draw_grid(screen, grid):
    """绘制固定的方块"""
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j]:
                rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, (200, 200, 200), rect)
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)  # 边框

def draw_tetromino(screen, shape, pos):
    """绘制当前下落的方块"""
    for (i, j) in shape:
        x = (pos[1] + j) * cell_size
        y = (pos[0] + i) * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 255, 0), rect)
        pygame.draw.rect(screen, (50, 50, 50), rect, 1)

# 初始选择一个方块（这里可随机选择一个）
current_shape_key = random.choice(list(TETROMINOES.keys()))
current_tetromino = TETROMINOES[current_shape_key][0]
# 初始位置：位于网格上方中间
current_pos = [0, COLS // 2 - 2]

# 下落相关变量（单位：毫秒）
fall_delay = 500  # 每 500 毫秒下落一格
last_fall_time = pygame.time.get_ticks()

running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 每隔 fall_delay 毫秒，让当前方块向下移动一格
    if current_time - last_fall_time > fall_delay:
        last_fall_time = current_time
        new_pos = [current_pos[0] + 1, current_pos[1]]
        if not check_collision(grid, current_tetromino, new_pos):
            current_pos = new_pos
        else:
            # 碰撞发生，固定当前方块到网格，并生成新方块
            lock_tetromino(grid, current_tetromino, current_pos)
            # 此处简单实现：随机选择下一个方块
            current_shape_key = random.choice(list(TETROMINOES.keys()))
            current_tetromino = TETROMINOES[current_shape_key][0]
            current_pos = [0, COLS // 2 - 2]
            # 若新方块立即碰撞，则游戏结束（此处暂未处理，可后续完善）
            if check_collision(grid, current_tetromino, current_pos):
                print("Game Over")
                running = False

    # 绘制部分
    screen.fill((0, 0, 0))  # 清屏
    draw_grid(screen, grid)
    draw_tetromino(screen, current_tetromino, current_pos)
    pygame.display.flip()   # 更新屏幕

    clock.tick(60)          # 控制 60 FPS

pygame.quit()
sys.exit()