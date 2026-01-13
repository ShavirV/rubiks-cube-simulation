# graphics_main.py
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
        self.angle_x = 30 * math.pi / 180  #start at 30 degrees for better view
        self.angle_y = -45 * math.pi / 180  #start at -45 degrees
        self.scale = 50
        self.dragging = False
        self.last_mouse_pos = (0, 0)
    
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
    
    def get_face_center_depth(self, position_3d, face_dir):
        """Calculate the depth of a face center for sorting"""
        x, y, z = position_3d
        
        if face_dir == 'x+':
            return (x + 0.5, y, z)  #right
        elif face_dir == 'x-':
            return (x - 0.5, y, z)  #left
        elif face_dir == 'y+':
            return (x, y + 0.5, z)  #up
        elif face_dir == 'y-':
            return (x, y - 0.5, z)  #down
        elif face_dir == 'z+':
            return (x, y, z + 0.5)  #front
        elif face_dir == 'z-':
            return (x, y, z - 0.5)  #Back
        return (x, y, z)
    
    def draw_cube(self, screen):
        """Draw the cube with depth sorting"""
        #collect all faces with their depth for sorting
        faces_to_draw = []
        
        for cubie in self.cube.cubies:
            x, y, z = cubie.position
            for face_dir, color in cubie.faces.items():
                #calculate face center in 3D for depth sorting
                face_center = self.get_face_center_depth((x, y, z), face_dir)
                
                #project to get depth
                _, depth = self.project_3d_to_2d(face_center)
                
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
            'R': (255, 50, 50),     # Bright Red
            'O': (255, 165, 0),     # Orange
            'B': (50, 50, 255),     # Bright Blue
            'G': (50, 255, 50),     # Bright Green
            'W': (255, 255, 255),   # White
            'Y': (255, 255, 100)    # Bright Yellow
        }
        
        #darker shade for borders
        border_color_map = {
            'R': (200, 30, 30),     # Darker Red
            'O': (220, 140, 0),     # Darker Orange
            'B': (30, 30, 200),     # Darker Blue
            'G': (30, 200, 30),     # Darker Green
            'W': (220, 220, 220),   # Light Gray
            'Y': (220, 220, 80)     # Darker Yellow
        }
        
        base_color = base_color_map.get(color, (128, 128, 128))
        border_color = border_color_map.get(color, (100, 100, 100))
        
        x, y, z = position_3d
        
        #calculate face corners for a 'solid' object
        face_size = 0.5  
        points_3d = []
        
        if face_dir == 'x+':
            #right face
            x_offset = 0.5
            points_3d = [
                (x + x_offset, y - face_size, z - face_size),
                (x + x_offset, y + face_size, z - face_size),
                (x + x_offset, y + face_size, z + face_size),
                (x + x_offset, y - face_size, z + face_size)
            ]
        elif face_dir == 'x-':
            #left face
            x_offset = -0.5
            points_3d = [
                (x + x_offset, y - face_size, z - face_size),
                (x + x_offset, y + face_size, z - face_size),
                (x + x_offset, y + face_size, z + face_size),
                (x + x_offset, y - face_size, z + face_size)
            ]
        elif face_dir == 'y+':
            #up face
            y_offset = 0.5
            points_3d = [
                (x - face_size, y + y_offset, z - face_size),
                (x + face_size, y + y_offset, z - face_size),
                (x + face_size, y + y_offset, z + face_size),
                (x - face_size, y + y_offset, z + face_size)
            ]
        elif face_dir == 'y-':
            #down face
            y_offset = -0.5
            points_3d = [
                (x - face_size, y + y_offset, z - face_size),
                (x + face_size, y + y_offset, z - face_size),
                (x + face_size, y + y_offset, z + face_size),
                (x - face_size, y + y_offset, z + face_size)
            ]
        elif face_dir == 'z+':
            #front face
            z_offset = 0.5
            points_3d = [
                (x - face_size, y - face_size, z + z_offset),
                (x + face_size, y - face_size, z + z_offset),
                (x + face_size, y + face_size, z + z_offset),
                (x - face_size, y + face_size, z + z_offset)
            ]
        elif face_dir == 'z-':
            #back face
            z_offset = -0.5
            points_3d = [
                (x - face_size, y - face_size, z + z_offset),
                (x + face_size, y - face_size, z + z_offset),
                (x + face_size, y + face_size, z + z_offset),
                (x - face_size, y + face_size, z + z_offset)
            ]
        
        if points_3d:
            #project all points to 2D
            projected_points = []
            for point in points_3d:
                (screen_x, screen_y), _ = self.project_3d_to_2d(point)
                projected_points.append((screen_x, screen_y))
            
            #draw the face fill
            pygame.draw.polygon(screen, base_color, projected_points)
            
            #draw a thicker border to separate pieces
            pygame.draw.polygon(screen, (0, 0, 0), projected_points, 10)
            
            #draw inner border for 3D effect
            if len(projected_points) == 4:
                #calculate inset points for inner border
                inset_points = []
                for i in range(4):
                    x1, y1 = projected_points[i]
                    x2, y2 = projected_points[(i + 1) % 4]
                    x3, y3 = projected_points[(i + 2) % 4]
                    
                    #calculate direction vectors
                    dx1 = x2 - x1
                    dy1 = y2 - y1
                    dx2 = x3 - x2
                    dy2 = y3 - y2
                    
                    #normalize and perpendicular vectors
                    length1 = math.sqrt(dx1*dx1 + dy1*dy1)
                    length2 = math.sqrt(dx2*dx2 + dy2*dy2)
                    
                    if length1 > 0 and length2 > 0:
                        #perpendicular vectors pointing inward
                        perp1 = (-dy1/length1, dx1/length1)
                        perp2 = (-dy2/length2, dx2/length2)
                        
                        #average for corner direction
                        avg_perp = ((perp1[0] + perp2[0])/2, (perp1[1] + perp2[1])/2)
                        avg_len = math.sqrt(avg_perp[0]*avg_perp[0] + avg_perp[1]*avg_perp[1])
                        
                        if avg_len > 0:
                            #move point inward
                            inset_x = x2 + avg_perp[0]/avg_len * 2
                            inset_y = y2 + avg_perp[1]/avg_len * 2
                            inset_points.append((inset_x, inset_y))
                
                if len(inset_points) == 4:
                    #draw inner border with border color
                    pygame.draw.polygon(screen, border_color, inset_points, 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("3D Rubik's Cube - Drag to Rotate View")
    clock = pygame.time.Clock()
    
    cube = Cube()
    renderer = CubeRenderer(cube)
    
    #font for instructions
    font = pygame.font.SysFont('Arial', 17)
    
    #main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  #left mouse button
                    renderer.dragging = True
                    renderer.last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:  #mouse wheel up
                    renderer.scale = min(renderer.scale + 5, 100)
                elif event.button == 5:  #mouse wheel down
                    renderer.scale = max(renderer.scale - 5, 20)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    renderer.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if renderer.dragging:
                    current_pos = pygame.mouse.get_pos()
                    dx = current_pos[0] - renderer.last_mouse_pos[0]
                    dy = current_pos[1] - renderer.last_mouse_pos[1]
                    
                    #update rotation angles based on mouse movement
                    renderer.angle_y += dx * 0.01
                    renderer.angle_x += dy * 0.01
                    
                    renderer.last_mouse_pos = current_pos
            elif event.type == pygame.KEYDOWN:
                #keyboard controls for cube moves
                if event.key == pygame.K_r:
                    cube.rotate("R")
                elif event.key == pygame.K_u:
                    cube.rotate("U")
                elif event.key == pygame.K_l:
                    cube.rotate("L")
                elif event.key == pygame.K_d:
                    cube.rotate("D")
                elif event.key == pygame.K_f:
                    cube.rotate("F")
                elif event.key == pygame.K_b:
                    cube.rotate("B")
                elif event.key == pygame.K_m:
                    cube.rotate("M")
                elif event.key == pygame.K_e:
                    cube.rotate("E")
                elif event.key == pygame.K_s:
                    cube.rotate("S")
                elif event.key == pygame.K_SPACE:
                    #reset cube
                    cube = Cube()
                    renderer.cube = cube
                elif event.key == pygame.K_q:
                    #random scramble
                    cube.random_scramble(20)
        
        #clear screen with dark gray background
        screen.fill((30, 30, 40))
        
        #draw cube
        renderer.draw_cube(screen)
        
        #draw instructions
        instructions = [
            "Mouse: Drag to rotate view | Scroll to zoom",
            "Keys: R/U/L/D/F/B - Move faces | M/E/S - Slice moves",
            "Space: Reset cube | Q: Random scramble"
        ]
        
        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (10, 10 + i * 25))
        
        #draw current rotation info
        angle_text = f"Rotation: X={renderer.angle_x*180/math.pi:.1f}°, Y={renderer.angle_y*180/math.pi:.1f}°"
        angle_surface = font.render(angle_text, True, (200, 200, 200))
        screen.blit(angle_surface, (10, 570))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()