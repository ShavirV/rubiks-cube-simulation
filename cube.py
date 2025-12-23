#cube.py

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
        
        #for use with Cube.rotate(), easy way to define all possible moves
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
            
            "S":  [('z', 0,  1)],  
            "S":  [('z', 0, -1)],  
            "S":  [('z', 0,  2)],  
            
            #full rotations are implemented as a composite of other rotations (X == R + M' + L' )
            
            "X":  [('x', 1,  1), ('x', 0,  1), ('x', -1, -1)],
            "X'": [('x', 1, -1), ('x', 0, -1), ('x', -1, -1)],
            "X'": [('x', 1,  2), ('x', 0,  2), ('x', -1,  2)],
            
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
                    if x == 1:  faces['x+'] = 'G'
                    if x == -1: faces['x-'] = 'B'
                    if y == 1:  faces['y+'] = 'W'
                    if y == -1: faces['y-'] = 'Y'
                    if z == 1:  faces['z+'] = 'R'
                    if z == -1: faces['z-'] = 'O'
                    
                    self.cubies.append(Cubie(coords, faces))
                    
    #parse an algorithm from a sting (R L' U2 etc.)
    def parse_sequence(self, sequence):
        moves = sequence.split()
        for move in moves:
            if not self.MOVE_MAP[move]:
                print(f"Unknown move {move}.")
                continue 
            self.rotate(self.MOVE_MAP[move])
        print(f"sequence {sequence} parsed and applied!")
           
    def rotate(axis, layer, direction):
        """ works with the move_map to apply transformations to the cube
        Args:
            axis a char {x, y, z}: axis to rotate around
            layer an int {-1, 0, 1}: layer to rotate
            direction an int {1, -1, 2}: regular, prime, double move
        """
        
                    
                    