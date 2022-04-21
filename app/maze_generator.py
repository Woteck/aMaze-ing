# maze_generator.py

import random

class MAZE_GENERATOR:
    MUR = 'm'
    CHEMIN = 'c'
    TEMP = 'n'
    GAUCHE, DROITE, HAUT, BAS = 'g', 'd', 'h', 'b'

    def __init__(self, height: int = 3, width: int = 3) -> None:
        self.HEIGHT = height
        self.WIDTH = width
        self.lab = []

    def cheminsautour(self, mur):
        autour = 0
        if (self.lab[mur[0]-1][mur[1]] == 'c'):
            autour += 1
        if (self.lab[mur[0]+1][mur[1]] == 'c'):
            autour += 1
        if (self.lab[mur[0]][mur[1]-1] == 'c'):
            autour +=1
        if (self.lab[mur[0]][mur[1]+1] == 'c'):
            autour += 1
        return autour

    def create_murs(self, case, murs, pos):
        """ fonction qui génère le labyrinthe """   
        c_autour = self.cheminsautour(case)
        if c_autour<2:
            self.lab[case[0]][case[1]]='c'
            if pos != 'b':
                if (case[0] != 0):
                    if (self.lab[case[0]-1][case[1]] != 'c'):
                        self.lab[case[0]-1][case[1]] = 'm'
                    if ([case[0]-1, case[1]] not in murs):
                        murs.append([case[0]-1, case[1]])
            if pos != 'h':
                if (case[0] != self.HEIGHT-1):
                    if (self.lab[case[0]+1][case[1]] != 'c'):
                        self.lab[case[0]+1][case[1]] = 'm'
                    if ([case[0]+1, case[1]] not in murs):
                        murs.append([case[0]+1, case[1]])
            if pos != 'd':
                if (case[1] != 0):
                    if (self.lab[case[0]][case[1]-1] != 'c'):
                        self.lab[case[0]][case[1]-1] = 'm'
                    if ([case[0], case[1]-1] not in murs):
                        murs.append([case[0], case[1]-1])
            if pos != 'g':
                if (case[1] != self.WIDTH-1):
                    if (self.lab[case[0]][case[1]+1] != 'c'):
                        self.lab[case[0]][case[1]+1] = 'm'
                    if ([case[0], case[1]+1] not in murs):
                        murs.append([case[0], case[1]+1])
        for i in murs:
            if i[0]==case[0] and i[1]==case[1]:
                murs.remove(i)

    def create_maze(self):
        #création du labyrinthe, pour l'instant les cases sont vides
        for i in range(0, self.HEIGHT):
            ligne = []
            for j in range(0, self.WIDTH):
                ligne.append(MAZE_GENERATOR.TEMP)
            self.lab.append(ligne)

        #on choisit une case au hasard pour commencer le labyrinthe 
        dep_height = random.randint(1, self.HEIGHT-2)
        dep_width  = random.randint(1, self.WIDTH -2)

        #on la transforme en chemin
        self.lab[dep_height][dep_width] = MAZE_GENERATOR.CHEMIN
        
        #on rajoute des murs autour
        murs = []
        murs.append([dep_height - 1, dep_width])
        murs.append([dep_height, dep_width - 1])
        murs.append([dep_height, dep_width + 1])
        murs.append([dep_height + 1, dep_width])

        mur = MAZE_GENERATOR.MUR
        self.lab[dep_height-1][dep_width]   = mur
        self.lab[dep_height][dep_width - 1] = mur
        self.lab[dep_height][dep_width + 1] = mur
        self.lab[dep_height + 1][dep_width] = mur

        #print(self.lab)

        while murs:
            #on prend un mur au hasard
            rand_mur = murs[random.randint(0,len(murs))-1]
            #mur de gauche
            if rand_mur[1]!=0:
                if (self.lab[rand_mur[0]][rand_mur[1]-1]=='n' and self.lab[rand_mur[0]][rand_mur[1]+1]=='c'):
                    self.create_murs(rand_mur, murs, MAZE_GENERATOR.GAUCHE)				
                    continue
            if rand_mur[0] != 0:
                if (self.lab[rand_mur[0]-1][rand_mur[1]] == 'n' and self.lab[rand_mur[0]+1][rand_mur[1]] == 'c'):
                    self.create_murs(rand_mur, murs, MAZE_GENERATOR.HAUT)
                    continue
            if (rand_mur[0] != self.HEIGHT-1):
                if (self.lab[rand_mur[0]+1][rand_mur[1]] == 'n' and self.lab[rand_mur[0]-1][rand_mur[1]] == 'c'):
                    self.create_murs(rand_mur, murs, MAZE_GENERATOR.BAS)
                    continue
            if (rand_mur[1] != self.WIDTH-1):
                if (self.lab[rand_mur[0]][rand_mur[1]+1] == 'n' and self.lab[rand_mur[0]][rand_mur[1]-1] == 'c'):
                    self.create_murs(rand_mur, murs, MAZE_GENERATOR.DROITE)
                    continue
            for i in murs:
                if i[0]==rand_mur[0] and i[1]==rand_mur[1]:
                    murs.remove(i)
        
        # on transforme les cases restantes en murs
        for i in range(0, self.HEIGHT):
            for j in range(0, self.WIDTH):
                if (self.lab[i][j] == 'n'):
                    self.lab[i][j] = 'm'

        # on  définit une entrée et une sortie
        for i in range(0, self.WIDTH):
            if (self.lab[1][i] == 'c'):
                self.lab[0][i] = 'c'
                break

        for i in range(self.WIDTH-1, 0, -1):
            if (self.lab[self.HEIGHT-2][i] == 'c'):
                self.lab[self.HEIGHT-1][i] = 'c'
                break
        
        return self.lab

if __name__ == '__main__':
    from colorama import init, Fore
    init()

    mg = MAZE_GENERATOR(10, 10)
    mg.create_maze()

    for row in mg.lab:
        print(' '.join([Fore.RED+thing if thing=='c' else Fore.GREEN+thing for thing in row]))