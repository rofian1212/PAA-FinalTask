import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
import time

def create_random_map(size=15, obstacle_density=0.3):
    """Membuat peta acak dengan obstacle"""
    map_grid = np.zeros((size, size))
    
    
    for i in range(size):
        for j in range(size):
            if random.random() < obstacle_density:
                map_grid[i, j] = 1
    
    return map_grid

def find_empty_positions(map_grid, count=3):
    """Mencari posisi kosong untuk titik awal, paket, dan tujuan"""
    size = len(map_grid)
    empty_positions = []
    
    while len(empty_positions) < count:
        x, y = random.randint(0, size-1), random.randint(0, size-1)
        if map_grid[x, y] == 0 and (x, y) not in empty_positions:
            empty_positions.append((x, y))
    
    return empty_positions

def find_path(map_grid, start, end):
    """Mencari jalur dari start ke end menggunakan A* algorithm"""
    size = len(map_grid)
    
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    
    open_set = {start}
    came_from = {}
    
    g_score = {pos: float('inf') for i in range(size) for j in range(size) for pos in [(i, j)]}
    g_score[start] = 0
    
    f_score = {pos: float('inf') for i in range(size) for j in range(size) for pos in [(i, j)]}
    f_score[start] = heuristic(start, end)
    
    while open_set:
        
        current = min(open_set, key=lambda pos: f_score[pos])
        
        if current == end:
            
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1] 
        
        open_set.remove(current)
        
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            
            if (0 <= neighbor[0] < size and 0 <= neighbor[1] < size and 
                map_grid[neighbor[0], neighbor[1]] == 0):
                
                tentative_g_score = g_score[current] + 1
                
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                    if neighbor not in open_set:
                        open_set.add(neighbor)
    
    return None
def main():
    
    map_size = 15
    map_grid = create_random_map(map_size)
    
    
    start_pos, package_pos, end_pos = find_empty_positions(map_grid, 3)
    
    
    path1 = find_path(map_grid, start_pos, package_pos)
    
    
    path2 = find_path(map_grid, package_pos, end_pos)
    
    if path1 and path2:
        
        visual_grid = map_grid.copy()
        
        
        visual_grid[package_pos[0], package_pos[1]] = 5  # Paket
        visual_grid[end_pos[0], end_pos[1]] = 6  # Tujuan
        
        
        full_path = path1 + path2[1:]  
        
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        
        colors = ['white', 'black', 'lightblue', 'lightgreen', 'blue', 'red', 'green']
        cmap = ListedColormap(colors)
        
        
        def update(frame):
            
            current_grid = visual_grid.copy()
            
            
            for i in range(min(frame, len(full_path))):
                x, y = full_path[i]
                
                if (x, y) != package_pos and (x, y) != end_pos:
                    current_grid[x, y] = 2
            
           
            if frame < len(full_path):
                x, y = full_path[frame]
                
                if (x, y) == package_pos:
                    current_grid[x, y] = 5
                
                elif (x, y) == end_pos:
                    current_grid[x, y] = 6
                else:
                    current_grid[x, y] = 4 
            
            
            ax.clear()
            ax.imshow(current_grid, cmap=cmap)
            ax.grid(True, which='both', color='gray', linewidth=0.5)
            ax.set_xticks(range(map_size))
            ax.set_yticks(range(map_size))
            
            
            labels = ['Jalan', 'Obstacle', 'Jalur Dilalui', '', 'Kurir', 'Paket', 'Tujuan']
            patches = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(len(colors))]
            ax.legend(patches, labels, loc='upper right', bbox_to_anchor=(1.3, 1))
            
            
            if frame < len(path1):
                status = "Kurir menuju paket"
            elif frame < len(full_path):
                status = "Kurir mengantar paket ke tujuan"
            else:
                status = "Pengiriman selesai"
            
            ax.set_title(f'Simulasi Pengiriman Paket - {status}')
            
            return [ax]
        
        
        ani = animation.FuncAnimation(
            fig, update, frames=len(full_path)+10, interval=300, blit=False, repeat=False
        )
        
        plt.tight_layout()
        plt.show()
        
        print(f"Titik awal: {start_pos}")
        print(f"Lokasi paket: {package_pos}")
        print(f"Titik tujuan: {end_pos}")
        print(f"Panjang jalur ke paket: {len(path1)}")
        print(f"Panjang jalur ke tujuan: {len(path2)}")
    else:
        print("Tidak dapat menemukan jalur. Coba lagi dengan peta baru.")

if __name__ == "__main__":
    main()
