#fake_3d_main.py
import pygame
import math
from cube import Cube

'''
creates a 'fake' 3d representation of the cube. no actual 3d models or rendering are used,
rather we store the state of the cube in 3d, then perform mathematical rotations and project the
result onto a 2d screen, drawing flat polygons with the illusion of 3d. this is how games like
doom worked before true 3d rendering
'''

class CubeRenderer:
    def __init__(self, cube):
        self.cube = cube
        self.angle_x = -150 * math.pi / 180  
        self.angle_y = 90 * math.pi / 180  
        self.scale = 50
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        self.label_font = pygame.font.SysFont("Arial", 22, bold=True)
        
        #face direction label mapping
        self.face_labels = {
            'x+': 'R',
            'x-': 'L',
            'y+': 'U',
            'y-': 'D',
            'z+': 'F',
            'z-': 'B'
        }
    
    def project_3d_to_2d(self, point_3d):
        """Simple 3D to 2D projection with rotation"""
        x, y, z = point_3d
        
        #apply rotations
        #rotate around Y axis
        x1 = x * math.cos(self.angle_y) - z * math.sin(self.angle_y)
        z1 = x * math.sin(self.angle_y) + z * math.cos(self.angle_y)
        
        #rotate around X axis
        y1 = y * math.cos(self.angle_x) - z1 * math.sin(self.angle_x)
        z2 = y * math.sin(self.angle_x) + z1 * math.cos(self.angle_x)
        
        #isometric projection, where should it appear on screen
        screen_x = 400 + (x1 - z2) * self.scale
        screen_y = 300 + y1 * self.scale
        
        #return both 2D position and depth (z2)
        return (int(screen_x), int(screen_y)), z2

    def rotated_z(self, point_3d):
        x, y, z = point_3d
        
        x1 = x * math.cos(self.angle_y) - z * math.sin(self.angle_y)
        z1 = x * math.sin(self.angle_y) + z * math.cos(self.angle_y)
        
        y1 = y * math.cos(self.angle_x) - z1 * math.sin(self.angle_x)
        z2 = y * math.sin(self.angle_x) + z1 * math.cos(self.angle_x)
        
        return z2

    def get_face_points(self, position_3d, face_dir):
        x, y, z = position_3d
        face_size = 0.5
        
        if face_dir == 'x+':
            return [(x+face_size,y-face_size,z-face_size),
                    (x+face_size,y+face_size,z-face_size),
                    (x+face_size,y+face_size,z+face_size),
                    (x+face_size,y-face_size,z+face_size)]
        elif face_dir == 'x-':
            return [(x-face_size,y-face_size,z-face_size),
                    (x-face_size,y+face_size,z-face_size),
                    (x-face_size,y+face_size,z+face_size),
                    (x-face_size,y-face_size,z+face_size)]
        elif face_dir == 'y+':
            return [(x-face_size,y+face_size,z-face_size),
                    (x+face_size,y+face_size,z-face_size),
                    (x+face_size,y+face_size,z+face_size),
                    (x-face_size,y+face_size,z+face_size)]
        elif face_dir == 'y-':
            return [(x-face_size,y-face_size,z-face_size),
                    (x+face_size,y-face_size,z-face_size),
                    (x+face_size,y-face_size,z+face_size),
                    (x-face_size,y-face_size,z+face_size)]
        elif face_dir == 'z+':
            return [(x-face_size,y-face_size,z+face_size),
                    (x+face_size,y-face_size,z+face_size),
                    (x+face_size,y+face_size,z+face_size),
                    (x-face_size,y+face_size,z+face_size)]
        elif face_dir == 'z-':
            return [(x-face_size,y-face_size,z-face_size),
                    (x+face_size,y-face_size,z-face_size),
                    (x+face_size,y+face_size,z-face_size),
                    (x-face_size,y+face_size,z-face_size)]
        return []

    def draw_cube(self, screen):
        """Draw the cube with depth sorting"""
        #collect all faces with their depth for sorting
        faces_to_draw = []
        
        for cubie in self.cube.cubies:
            x, y, z = cubie.position
            for face_dir, color in cubie.faces.items():
                points_3d = self.get_face_points((x, y, z), face_dir)
                depth = sum(self.rotated_z(p) for p in points_3d) / 4
                
                faces_to_draw.append({
                    'cubie_pos': (x, y, z),
                    'face_dir': face_dir,
                    'color': color,
                    'depth': depth
                })
        
        #sort faces by depth (back to front)
        faces_to_draw.sort(key=lambda f: f['depth'], reverse=True)
        
        #draw faces from back to front
        for face_info in faces_to_draw:
            self.draw_face(screen, 
                          face_info['cubie_pos'], 
                          face_info['face_dir'], 
                          face_info['color'])
    
    def draw_face(self, screen, position_3d, face_dir, color):
        """Draw a single face of a cubie with borders and shading"""
        #map colors to pygame colors with slight variations for shading
        base_color_map = {
            'R': (255, 50, 50),
            'O': (255, 165, 0),
            'B': (50, 50, 255),
            'G': (50, 255, 50),
            'W': (255, 255, 255),
            'Y': (255, 255, 100)
        }
        
        border_color_map = {
            'R': (200, 30, 30),
            'O': (220, 140, 0),
            'B': (30, 30, 200),
            'G': (30, 200, 30),
            'W': (220, 220, 220),
            'Y': (220, 220, 80)
        }
        
        base_color = base_color_map.get(color, (128, 128, 128))
        border_color = border_color_map.get(color, (100, 100, 100))
        
        points_3d = self.get_face_points(position_3d, face_dir)
        
        if points_3d:
            projected_points = []
            for point in points_3d:
                (screen_x, screen_y), _ = self.project_3d_to_2d(point)
                projected_points.append((screen_x, screen_y))
            
            pygame.draw.polygon(screen, base_color, projected_points)
            pygame.draw.polygon(screen, (0, 0, 0), projected_points, 10)
            
            if len(projected_points) == 4:
                inset_points = []
                for i in range(4):
                    x1, y1 = projected_points[i]
                    x2, y2 = projected_points[(i + 1) % 4]
                    x3, y3 = projected_points[(i + 2) % 4]
                    
                    dx1 = x2 - x1
                    dy1 = y2 - y1
                    dx2 = x3 - x2
                    dy2 = y3 - y2
                    
                    length1 = math.sqrt(dx1*dx1 + dy1*dy1)
                    length2 = math.sqrt(dx2*dx2 + dy2*dy2)
                    
                    if length1 > 0 and length2 > 0:
                        perp1 = (-dy1/length1, dx1/length1)
                        perp2 = (-dy2/length2, dx2/length2)
                        
                        avg_perp = ((perp1[0] + perp2[0])/2, (perp1[1] + perp2[1])/2)
                        avg_len = math.sqrt(avg_perp[0]*avg_perp[0] + avg_perp[1]*avg_perp[1])
                        
                        if avg_len > 0:
                            inset_x = x2 + avg_perp[0]/avg_len * 2
                            inset_y = y2 + avg_perp[1]/avg_len * 2
                            inset_points.append((inset_x, inset_y))
                
                if len(inset_points) == 4:
                    pygame.draw.polygon(screen, border_color, inset_points, 2)
                
                x, y, z = position_3d
                is_center = sum(abs(v) for v in (x, y, z)) == 1

                if is_center and face_dir in self.face_labels:
                    cx = sum(p[0] for p in projected_points) / 4
                    cy = sum(p[1] for p in projected_points) / 4
                    label = self.face_labels[face_dir]
                    text = self.label_font.render(label, True, (0, 0, 0))
                    rect = text.get_rect(center=(cx, cy))
                    screen.blit(text, rect)

def build_move(event):
    key_map = {
        pygame.K_r: "R",
        pygame.K_l: "L",
        pygame.K_u: "U",
        pygame.K_d: "D",
        pygame.K_f: "F",
        pygame.K_b: "B",
        pygame.K_m: "M",
        pygame.K_e: "E",
        pygame.K_s: "S",
        pygame.K_x: "X",
        pygame.K_y: "Y",
        pygame.K_z: "Z",
    }
    
    if event.key not in key_map:
        return None
    
    move = key_map[event.key]
    mods = pygame.key.get_mods()
    
    if mods & pygame.KMOD_SHIFT:
        move += "'"
    elif mods & pygame.KMOD_CTRL:
        move += "2"
        
    return move

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("3D Rubik's Cube - Drag to Rotate View")
    clock = pygame.time.Clock()
    
    cube = Cube()
    renderer = CubeRenderer(cube)
    
    font = pygame.font.SysFont('Arial', 17)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    renderer.dragging = True
                    renderer.last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:
                    renderer.scale = min(renderer.scale + 5, 100)
                elif event.button == 5:
                    renderer.scale = max(renderer.scale - 5, 20)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    renderer.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if renderer.dragging:
                    current_pos = pygame.mouse.get_pos()
                    dx = current_pos[0] - renderer.last_mouse_pos[0]
                    dy = current_pos[1] - renderer.last_mouse_pos[1]
                    
                    renderer.angle_y += dx * 0.01
                    renderer.angle_x += dy * 0.01
                    
                    renderer.last_mouse_pos = current_pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cube = Cube()
                    renderer.cube = cube
                elif event.key == pygame.K_q:
                    cube.random_scramble(20)
                else:
                    move = build_move(event)
                    if move:
                        cube.rotate(move)
        
        screen.fill((30, 30, 40))
        renderer.draw_cube(screen)
        
        instructions = [
            "Mouse: Drag to rotate view | Scroll to zoom",
            "Keys: R/U/L/D/F/B - Move faces | M/E/S - Slice moves",
            "Hold Shift+Key for prime moves",
            "Hold Ctrl+Key for double moves",
            "Space: Reset cube | Q: Random scramble"
        ]
        
        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (10, 10 + i * 25))
        
        angle_text = f"Rotation: X={renderer.angle_x*180/math.pi:.1f}°, Y={renderer.angle_y*180/math.pi:.1f}°"
        angle_surface = font.render(angle_text, True, (200, 200, 200))
        screen.blit(angle_surface, (10, 570))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
