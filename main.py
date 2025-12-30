from cube import Cube, Cubie


def main():
    cube = Cube()
    cube.print_net()
    cube.dump_cubies()
    cube.parse_sequence("R U R' U'")
    cube.dump_cubies()
    cube.print_net()
    cube.parse_sequence("U R U' R'")
    cube.print_net()
    cube.dump_cubies()
    
    for _ in range(6):
        cube.parse_sequence("R U R' U'")
        cube.print_net()
        
    print ("😓😓😓😓😓😓Jperm test")
        
    #jperm A
    cube.parse_sequence("R U R' F' R U R' U' R' F R2 U' R' U'")
    cube.print_net()
    cube.dump_cubies()
    cube.parse_sequence("R U R' F' R U R' U' R' F R2 U' R' U'")
    cube.print_net()
    cube.dump_cubies()
    
    #full cube rotations
    cube.parse_sequence("X")
    cube.print_net()
    cube.parse_sequence('Y2')
    cube.print_net()

if __name__ == "__main__":
    main()