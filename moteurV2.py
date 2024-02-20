from collections import deque

class Donjon :
    def __init__(self, donjon:list, positionsDragons:list, highLevelDragon:int) -> None:
        self.donjon = donjon
        self.positionsDragons = positionsDragons
        self.highLevelDragon = highLevelDragon

        
        self.__paths = dict()

        self.ignore = list()

        self.Isize = len(self.donjon)
        self.Jsize= len(self.donjon[0])


    def rotate(self, position:tuple) -> None:
        """Permet de pivoter la salle"""
        i,j = position
        room = self.donjon[i][j]
        self.donjon[i][j] = (room[3], room[0], room[1], room[2])


    def is_connected(self, position1:tuple, position2:tuple) -> bool:
        """verifie si 2 salle sont connecté"""
        i, j = position1
        x, y = position2

        room1 = self.donjon[i][j]
        room2 = self.donjon[x][y]

        if x == i-1 :
            return room1[0] and room2[2]
        elif x == i+1 :
            return room1[2] and room2[0]
        elif y == j+1 :
            return room1[1] and room2[3]
        elif y == j-1 :
            return room1[3] and room2[1]
        else :
            return False

    def check_limit(self, position:tuple) -> True:
        i, j = position

        if i < 0 or i >= self.Isize :
            return False
        if j < 0 or j >= self.Jsize :
            return False

        return True


    def give_neighbors(self, position:tuple) -> list:
        """Donnes tous les voisins d'une salle"""
        i,j = position

        neighbors = list()
        tmpneighbors = [(i,j-1), (i-1,j), (i,j+1), (i+1,j)]

        for pos in tmpneighbors :
            if self.check_limit(pos) and self.is_connected(position, pos):
                neighbors.append(pos)
        
        return neighbors
    

    def search(self, positionA:tuple, Dragons:list) -> list:
        """Fonction pour parcourir pour trouver les monstres"""
        self.__paths.clear()
        
        queue = deque()
        parents = dict()
        isVisited = list()

        queue.append(positionA)
        isVisited.append(positionA)
        parents[positionA] = tuple()

        while len(queue) != 0 :
            node  = queue.popleft()

            if node in self.positionsDragons :
                path = self.track_parent(parents, positionA, node)

                indexDragon = give_dragon(Dragons, path)
                level = Dragons[indexDragon]["niveau"]

                if level == self.highLevelDragon :
                    return path
                else :
                    self.__paths[level] = path
            
            neighbors = self.give_neighbors(node)

            for pos in neighbors :
                if pos not in isVisited and pos not in self.ignore:
                    parents[pos] = node
                    isVisited.append(pos)
                    queue.append(pos)

        return self.maxLevel()
    

    def give_path(self, positionA:tuple, Dragons:list) -> list:
        """Fonction permet de donner la chemin sous la forme d'une liste."""

        while True :
            path = self.search(positionA, Dragons)

            if path != [] and self.is_dragon_in_the_way(path) :
                self.ignore.append(path[0])
            else :
                self.ignore.clear()
                return path
    
    def is_dragon_in_the_way(self, path:list) -> bool :
        dragon = path[0]

        for i in range(1, len(path)) :
            if path[i] in self.positionsDragons :
                return True

        return False

    def maxLevel(self) -> list :
        if len(self.__paths) != 0 :
            level = max(self.__paths)
            return self.__paths[level]
        
        return list()
    

    def track_parent(self, parents:dict, postionA:tuple, positionD:tuple) -> list:
        path = [positionD]

        while path[-1] != postionA :
            path.append(parents[path[-1]])
        
        return path
    

    def remove_dragon_pos(self, position) -> None :
        try : 
            self.positionsDragons.remove(position)
        except ValueError : 
            pass
        

def give_dragon(dragons:list, path:list) -> int :
    for i in range(len(dragons)) :
        if dragons[i]["position"] == path[0] and dragons[i]["etat"] == "V":
            return i
    
    return -1