#cube.py

import random

#implementing the basic representation of each cubie (piece) and the cube as a whole

class Cubie:
    def __init__(self, position, faces):
        """
        Args:
            position, vector (x, y, z) each in {-1, 0, 1}
            this allows each cubie to know its absolute position in the cube's vector space
            faces, dictionary: stores a mapping of (face: colour) for rotation info
        """
        
        self.position = position
        self.faces = faces
        self.center_label = None
        
        #add annotations for center pieces (for solving and gui clarity)
        if len(self.faces) == 1:
            face_dir = next(iter(self.faces.keys()))
            label_map = {
                'z+': 'F',
                'z-': 'B',
                'y+': 'U',
                'y-': 'D',
                'x-': 'L',
                'x+': 'R'
            }
            self.center_label = label_map.get(face_dir)
        
        self.FACE_ROTATIONS = {
            'x': {
                'y+': 'z-',
                'z-': 'y-',
                'y-': 'z+',
                'z+': 'y+'
            },
            'y': {
                'x+': 'z+',
                'z+': 'x-',
                'x-': 'z-',
                'z-': 'x+'
            },
            'z': {
                'x+': 'y-',
                'y-': 'x-',
                'x-': 'y+',
                'y+': 'x+'
            }
        }
        
        #to reassign face annotations when rotating the entire cube
        self.LABEL_ROTATIONS = {
            'x': {
                'U': 'B', 'B': 'D', 'D': 'F', 'F': 'U'
            },
            'y': {
                'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'
            },
            'z': {
                'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'
            }
        }

    
         
    def transform(self, transformation):
        axis, layer, direction = transformation
        x, y, z = self.position
        #select relevant coord to this transformation
        coord = {'x' : x, 'y' : y, 'z': z}[axis]
        
        #only transform if in layer affected
        if coord != layer:
            return
        
        #-1 becomes 3 turns 
        turns = direction % 4
        
        for _ in range(turns):
            self.position = self.rotate_pos(self.position, axis)
            
            #remap colours
            face_map = self.FACE_ROTATIONS[axis]
            new_faces = {}
            for face, color in self.faces.items():
                new_faces[face_map.get(face, face)] = color
            self.faces = new_faces
            
            #rotate center label if it has one
            if self.center_label:
                rot = self.LABEL_ROTATIONS.get(axis, {})
                if direction > 0:
                    self.center_label = rot.get(self.center_label, self.center_label)
                else: #prime rotation
                    inv = {v: k for k, v in rot.items()}
                    self.center_label = inv.get(self.center_label, self.center_label)
        
    #apply a vector transformation according to the axis we rotate around
    def rotate_pos(self, pos, axis):
         x, y, z = pos
         
         if axis == 'x':
             return (x, z, -y) 
         if axis == 'y':
             return (-z, y, x)
         if axis == 'z':
             return (y, -x, z)
    
    #basic print all attributes of the cubie
    def __repr__(self):
        faces_str = ", ".join(f"{k}:{v}" for k, v in sorted(self.faces.items()))
        return f"Cubie(pos={self.position}, faces={{ {faces_str} }})"
    
"""
      | y+
      |
      |
     / \           
z+ /     \ x+
 /         \
     
"""   

class Cube:
    def __init__(self):
        self.cubies = []
        self.build_solved()
        
        """
        for use with Cube.rotate(), easy way to define all possible moves
            axis a char {x, y, z}: axis to rotate around
            layer an int {-1, 0, 1}: layer to rotate
            direction an int {1, -1, 2}: regular, prime, double move
        """
        self.MOVE_MAP = {
            "R":  [('x', 1,  1)],
            "R'": [('x', 1, -1)],
            "R2": [('x', 1,  2)],
            
            "L":  [('x', -1, -1)],
            "L'": [('x', -1,  1)],
            "L2": [('x', -1,  2)],
            
            "U":  [('y', 1,  1)],
            "U'": [('y', 1, -1)],
            "U2": [('y', 1,  2)],
            
            "D":  [('y', -1, -1)],
            "D'": [('y', -1,  1)],
            "D2": [('y', -1,  2)],
            
            "F":  [('z', 1,  1)],
            "F'": [('z', 1, -1)],
            "F2": [('z', 1,  2)],
            
            "B":  [('z', -1, -1)],
            "B'": [('z', -1, 1)],
            "B2": [('z', -1, 2)],    
            
            #slice moves
            
            "M":  [('x', 0, -1)],
            "M'": [('x', 0,  1)],
            "M2": [('x', 0,  2)],
            
            "E":  [('y', 0, -1)],
            "E'": [('y', 0,  1)],
            "E2": [('y', 0,  2)],
            
            "S":   [('z', 0,  1)],  
            "S'":  [('z', 0, -1)],  
            "S2":  [('z', 0,  2)],  
            
            #full rotations are implemented as a composite of other rotations (X == R + M' + L' )
            
            "X":  [('x', 1,  1), ('x', 0,  1), ('x', -1,  1)],
            "X'": [('x', 1, -1), ('x', 0, -1), ('x', -1, -1)],
            "X2": [('x', 1,  2), ('x', 0,  2), ('x', -1,  2)],
            
            "Y": [('y', 1,  1), ('y', 0,  1), ('y', -1,  1)],
            "Y'": [('y', 1, -1), ('y', 0, -1), ('y', -1, -1)],
            "Y2": [('y', 1,  2), ('y', 0,  2), ('y', -1,  2)],
            
            "Z":  [('z', 1,  1), ('z', 0,  1), ('z', -1,  1)],
            "Z'": [('z', 1, -1), ('z', 0, -1), ('z', -1, -1)],
            "Z2": [('z', 1,  2), ('z', 0,  2), ('z', -1,  2)],      
        }
        
    def build_solved(self):
        
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    coords = (x, y, z)
                    if coords == (0, 0, 0):
                        continue #no internal core
                    
                    #construct faces from coords
                    #white on top, green left, red right
                    faces = {}
                    if x == -1: faces['x-'] = 'O'  #left
                    if x ==  1: faces['x+'] = 'R'  #right

                    if y == -1: faces['y-'] = 'Y'  #down
                    if y ==  1: faces['y+'] = 'W'  #up

                    if z == -1: faces['z-'] = 'B'  #back
                    if z ==  1: faces['z+'] = 'G'  #front
                    
                    self.cubies.append(Cubie(coords, faces))
                    
    #parse an algorithm from a sting (R L' U2 etc.)
    def parse_sequence(self, sequence):
        moves = sequence.split()
        for move in moves:
            if not self.MOVE_MAP[move]:
                print(f"Unknown move {move}.")
                continue 
            self.rotate(move)
        print(f"sequence {sequence} parsed and applied!")
           
    def rotate(self, move_str):
        #move is passed in as a string R, L', M2, etc.
        #works with the move_map to apply transformations to the cube
        operations = self.MOVE_MAP[move_str]
        if not operations:
            print(f"move {move_str} invalid or not in move map")
            return

        for operation in operations:
            for cubie in self.cubies:
                cubie.transform(operation)
    
    def dump_cubies(self):
        print("=== CUBIE DUMP ===")
        for cubie in sorted(self.cubies, key=lambda c: c.position):
            print(cubie)
        print("==================")
    
    def get_face_grid(self, face):
        """
        face: one of 'x+', 'x-', 'y+', 'y-', 'z+', 'z-'
        returns: 3x3 list of colours
        """

        grid = [[None for _ in range(3)] for _ in range(3)]

        for cubie in self.cubies:
            if face not in cubie.faces:
                continue

            x, y, z = cubie.position
            color = cubie.faces[face]

            #map cubie position -> row/col depending on face
            if face == 'y+':      #up: x (L->R), z (B->F)
                row = 1 - z
                col = x + 1
            elif face == 'y-':    #down
                row = z + 1
                col = x + 1
            elif face == 'z+':    #front
                row = 1 - y
                col = x + 1
            elif face == 'z-':    #back (mirrored)
                row = 1 - y
                col = 1 - x
            elif face == 'x+':    #right
                row = 1 - y
                col = 1 - z
            elif face == 'x-':    #left
                row = 1 - y
                col = z + 1

            grid[row][col] = color

        return grid

    def print_face(self, grid):
        for row in grid:
            print(" ".join(cell or "?" for cell in row))
            
    def print_net(self):
        U = self.get_face_grid('y+')
        D = self.get_face_grid('y-')
        F = self.get_face_grid('z+')
        B = self.get_face_grid('z-')
        L = self.get_face_grid('x-')
        R = self.get_face_grid('x+')

        print("=== CUBE NET ===")

        #up (indent it a little)
        for r in range(3):
            print("       " + " ".join(U[r]))

        #Left, Front, Right, Back
        for r in range(3):
            print(
                " ".join(L[r]) + "   " +
                " ".join(F[r]) + "   " +
                " ".join(R[r]) + "   " +
                " ".join(B[r])
            )

        #down
        for r in range(3):
            print("       " + " ".join(D[r]))

        print("================")
        
    def random_scramble(self, length=30):
        SCRAMBLE_MOVES = [
            "R", "R'", "R2",
            "L", "L'", "L2",
            "U", "U'", "U2",
            "D", "D'", "D2",
            "F", "F'", "F2",
            "B", "B'", "B2"
        ]
        scramble = ""
        for _ in range(length):
            move = random.choice(SCRAMBLE_MOVES)
            self.rotate(move)
            scramble += (move + " ")
        print("Scramble: " + scramble)
            
        
        
        
            
        
        
        


                    
                    