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
        

class Cube:
    def __init__(self):
        self.cubies = []
        self.build_solved()
        
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
                    if x == 1:  faces['x+'] = 'R'
                    if x == -1: faces['x-'] = 'O'
                    if y == 1:  faces['y+'] = 'W'
                    if y == -1: faces['y-'] = 'Y'
                    if z == 1:  faces['z+'] = 'G'
                    if z == -1: faces['z-'] = 'B'
                    
                    self.cubies.append(Cubie(coords, faces))
                    
    def parse_sequence(self, sequence):
        #parse an algorithm from a sting (r,l',u2, etc.)
        print("parse")
           
    def r(self):
        print('r')
    
    def r_prime(self):
        print('r_prime')
    
    def u(self):
        print('u')
    
    def u_prime(self):
        print("u_prime")
    
    def d(self):
        print('d')
    
    def d_prime(self):
        print("d_prime")
    
    def l(self):
        print('l')
        
    def l_prime(self):
        print('l_prime')
        
                    
                    