import pygame
import heapq
from collections import deque
import math
import os
from config import *


from PIL import Image, ImageSequence
import pygame
import io

def load_gif(filename):
    
    try:
        gif_path = resource_path(filename, IMAGES_DIRECTORY)
        pil_image = Image.open(gif_path)
        
        frames = []
        durations = []
        
        
        for frame in ImageSequence.Iterator(pil_image):
            
            frame_rgba = frame.convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
            )
            frames.append(pygame_image)
            
            
            try:
                durations.append(frame.info['duration'])
            except KeyError:
                durations.append(100)  
        
        return frames, durations
    
    except Exception as e:
        print(f"GIF yüklenemedi: {filename}")
        print(f"Hata: {e}")
        
        return [], []

def resource_path(relative_path, directory):
    
    base_path = os.path.abspath(".")
    return os.path.join(base_path, directory, relative_path)

def load_image(filename):
    
    try:
        image_path = resource_path(filename, IMAGES_DIRECTORY)
        return pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f"Resim yüklenemedi: {filename}")
        print(f"Hata: {e}")
        # Hata durumunda temel bir yüzey döndür
        surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        surface.fill(RED)  # Hata gösterimi için kırmızı kare
        return surface

def load_sound(filename):
    
    try:
        sound_path = resource_path(filename, SOUNDS_DIRECTORY)
        return pygame.mixer.Sound(sound_path)
    except pygame.error as e:
        print(f"Ses dosyası yüklenemedi: {filename}")
        print(f"Hata: {e}")
        return None

def draw_text(surface, text, size, x, y, color=WHITE):
    
    font = pygame.font.SysFont(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect

def draw_button(surface, text, size, x, y, width, height, active=False):
    
    color = BUTTON_ACTIVE_COLOR if active else BUTTON_INACTIVE_COLOR
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    pygame.draw.rect(surface, BLACK, button_rect, 2)  
    
    font = pygame.font.SysFont(FONT_NAME, size)
    text_surf = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = button_rect.center
    surface.blit(text_surf, text_rect)
    
    
    print(f"Buton oluşturuldu: {text}, Konum: {button_rect}")
    
    return button_rect

def grid_to_pixel(grid_x, grid_y):
    
    return grid_x * CELL_SIZE, grid_y * CELL_SIZE

def pixel_to_grid(pixel_x, pixel_y):
    
    return pixel_x // CELL_SIZE, pixel_y // CELL_SIZE

def draw_grid(surface, grid):
    
    
    grid_height = len(grid)
    grid_width = len(grid[0]) if grid_height > 0 else 0
    
    
    total_width = grid_width * CELL_SIZE
    total_height = grid_height * CELL_SIZE
    
    
    offset_x = (SCREEN_WIDTH - total_width) // 2
    offset_y = (SCREEN_HEIGHT - total_height) // 2
    
    
    LIGHT_YELLOW = (255, 255, 150)  
    
    
    for y in range(grid_height):
        for x in range(grid_width):
            
            rect = pygame.Rect(
                offset_x + (x * CELL_SIZE), 
                offset_y + (y * CELL_SIZE), 
                CELL_SIZE, 
                CELL_SIZE
            )
            
            
            if grid[y][x] == WALL:
                pygame.draw.rect(surface, WALL_COLOR, rect)
            elif (x, y) == PLAYER_START_POS:  
                pygame.draw.rect(surface, LIGHT_YELLOW, rect)
            else:
                pygame.draw.rect(surface, PATH_COLOR, rect)
                
            
            pygame.draw.rect(surface, GRID_LINE_COLOR, rect, GRID_LINE_WIDTH)
    
    
    try:
        door_image = load_image("door.png")
        door_image = pygame.transform.scale(door_image, (CELL_SIZE, CELL_SIZE))
    except Exception as e:
        print(f"Kapı görseli yüklenemedi: {e}")
        door_image = None
    
    
    for door_name, (door_x, door_y) in DOORS.items():
        door_rect = pygame.Rect(
            offset_x + (door_x * CELL_SIZE), 
            offset_y + (door_y * CELL_SIZE), 
            CELL_SIZE, 
            CELL_SIZE
        )
        
        
        if door_image:
            surface.blit(door_image, door_rect)
        else:
            
            pygame.draw.rect(surface, BLUE, door_rect)
        
        
        door_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)
        door_text = door_font.render(door_name, True, YELLOW)
        door_text_rect = door_text.get_rect(center=(
            offset_x + (door_x * CELL_SIZE) + CELL_SIZE // 2,
            offset_y + (door_y * CELL_SIZE) + CELL_SIZE // 2
        ))
        surface.blit(door_text, door_text_rect)
    
    
    goal_rect = pygame.Rect(
        offset_x + (GOAL_POS[0] * CELL_SIZE), 
        offset_y + (GOAL_POS[1] * CELL_SIZE), 
        CELL_SIZE, 
        CELL_SIZE
    )
    pygame.draw.rect(surface, GOAL_COLOR, goal_rect)
    
    
    return offset_x, offset_y

def draw_path(surface, path, color=YELLOW, width=2, offset_x=0, offset_y=0):
    
    if not path:
        return
    
   
    for i in range(len(path) - 1):
        start = (
            offset_x + (path[i][0] * CELL_SIZE) + CELL_SIZE // 2, 
            offset_y + (path[i][1] * CELL_SIZE) + CELL_SIZE // 2
        )
        end = (
            offset_x + (path[i+1][0] * CELL_SIZE) + CELL_SIZE // 2, 
            offset_y + (path[i+1][1] * CELL_SIZE) + CELL_SIZE // 2
        )
        pygame.draw.line(surface, color, start, end, width)
    
    
    for point in path:
        center = (
            offset_x + (point[0] * CELL_SIZE) + CELL_SIZE // 2, 
            offset_y + (point[1] * CELL_SIZE) + CELL_SIZE // 2
        )
        pygame.draw.circle(surface, color, center, 3)



def get_neighbors(grid, current, allow_walls=False):
    
    x, y = current
    neighbors = []
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            if allow_walls or grid[ny][nx] == PATH:
                neighbors.append((nx, ny))
    
    return neighbors

def get_neighbors_kylo_ren(grid, current):
    x, y = current
    neighbors = []
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  
    
    for dx, dy in directions:
        
        nx1, ny1 = x + dx, y + dy
        
        nx2, ny2 = x + 2*dx, y + 2*dy
        
       
        if 0 <= nx1 < len(grid[0]) and 0 <= ny1 < len(grid) and grid[ny1][nx1] == PATH:
            
            if 0 <= nx2 < len(grid[0]) and 0 <= ny2 < len(grid) and grid[ny2][nx2] == PATH:
                neighbors.append((nx2, ny2))  
            else:
                neighbors.append((nx1, ny1))  
    
    return neighbors

def bfs_shortest_path(grid, start, end, allow_walls=False):
    
    if start == end:
        return [start]
    
    queue = deque([start])
    visited = {start: None}  
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            path.reverse()  
            return path
        
        for neighbor in get_neighbors(grid, current, allow_walls):
            if neighbor not in visited:
                queue.append(neighbor)
                visited[neighbor] = current
    
    return [] 

def bfs_kylo_ren(grid, start, end):
    if start == end:
        return [start]
    
    queue = deque([start])
    visited = {start: None} 
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            path.reverse() 
            return path
        
        for neighbor in get_neighbors_kylo_ren(grid, current):
            if neighbor not in visited:
                queue.append(neighbor)
                visited[neighbor] = current
    
    return []  

def darth_vader_shortest_path(grid, start, end):
    
    return bfs_shortest_path(grid, start, end, allow_walls=True)

def a_star_shortest_path(grid, start, end, allow_walls=False):
    
    def heuristic(a, b):
        
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    if start == end:
        return [start]
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}  
    f_score = {start: heuristic(start, end)}  
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == end:
            
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()  
            return path
        
        for neighbor in get_neighbors(grid, current, allow_walls):
            tentative_g_score = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []  

def is_colliding(pos1, pos2):
    return pos1 == pos2

def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])