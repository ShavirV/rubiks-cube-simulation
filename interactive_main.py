from cube import Cube, Cubie

def main():
    print("=== Shav's terminal based Rubik's cube simulator ===")
    print("1) Solved cube")
    print("2) Random scramble")
    
    choice = input("select option 1/2:").strip()
    
    cube = Cube()
    
    if choice == '2':
        cube.random_scramble()
    
    print("\n initial cube state: ")
    cube.print_net()
    
    print("\nEnter moves or a sequence of moves, e.g. \"R'\" or \"R U R' U'\"")
    print("type 'RESET' or 'QUIT'")
    
    #main loop
    while True:
        cmd = input("\n> ").strip().upper()
        
        if cmd == "RESET":
            cube = Cube()
            print("Reset cube to solved state.")
            cube.print_net()
            continue
        
        if cmd == "QUIT":
            print("Quitter 🫵")
            break
        
        cube.parse_sequence(cmd)
        cube.print_net()
        
    
    
    

if __name__ == "__main__":
    main()