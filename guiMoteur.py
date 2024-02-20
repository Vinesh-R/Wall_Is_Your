import fltk
from typing import Hashable

Image = None

DimensionSalle = 110,110
DimensionCoté = None
DimensionHautBas = None

DimensionTotale = None

def donne_positionEtDimenstion(coordSalle:tuple, coté:int) -> tuple:
    if coté == 0 :
        dimS = DimensionSalle[1] // 2
        x, y = coordSalle[0], coordSalle[1] - dimS
        dimension = DimensionHautBas

    elif coté == 1 :
        dimS = DimensionSalle[0] // 2
        x,y = coordSalle[0] + dimS, coordSalle[1]
        dimension = DimensionCoté

    elif coté == 2 :
        dimS = DimensionSalle[1] // 2
        x, y = coordSalle[0], coordSalle[1] + dimS
        dimension = DimensionHautBas
    
    elif coté == 3 :
        dimS = DimensionSalle[0] // 2
        x,y = coordSalle[0] - dimS, coordSalle[1]
        dimension = DimensionCoté

    else :
        raise "coté Non trouver"
    
    return (x,y), dimension


def fixeTexture(nom:str) :
    """
    Fixe la texture de la salle.

    Args :
        nom (str) : nom de la texture.
    """
    global Image, DimensionCoté, DimensionHautBas, DimensionTotale, DimensionSalle

    if nom == "originale" :
        Image = {
            "salleVer" : "media/verticalRoom_O.png",
            "salleHor" : "media/horizontalRoom_O.png",
            0 : "media/wallUp_O.png",      #haut
            1 : "media/wallRight_O.png",   #droite
            2 : "media/wallDown_O.png",    #bas
            3 : "media/wallLeft_O.png"     #gauche
        }
        DimensionCoté = 44,72
        DimensionHautBas = 72,44

    else :
        Image = {
            "salleVer" : "media/verticalRoom_M.png",
            "salleHor" : "media/horizontalRoom_M.png",
            0 : "media/pipeUp_M.png",      #haut
            1 : "media/pipeRight_M.png",   #droite
            2 : "media/pipeDown_M.png",    #bas
            3 : "media/pipeLeft_M.png"     #gauche
        }
        DimensionCoté = 50,55
        DimensionHautBas = 55,50
    
    DimensionSalle = 110,110
    DimensionTotale = DimensionSalle[0]+(DimensionCoté[0]//2)*2, DimensionSalle[1]+(DimensionHautBas[1]//2)*2


def redimentionne(scale:int) -> None:
    """
    En cas du redimensionemnt de la salle, cette fonction mise à jour les valeurs dimenstions des images.

    Args
        scale (int) : sclaire pour redimensionner
    """
    global DimensionSalle, DimensionHautBas, DimensionCoté, DimensionTotale

    DimensionSalle = round(DimensionSalle[0] * scale), round(DimensionSalle[1] * scale)
    DimensionHautBas = round(DimensionHautBas[0] * scale), round(DimensionHautBas[1] * scale)
    DimensionCoté = round(DimensionCoté[0] * scale), round(DimensionCoté[1] * scale)
    DimensionTotale = DimensionSalle[0] + (DimensionCoté[0]//2)*2, DimensionSalle[1]+(DimensionHautBas[1]//2)*2


def donne_gammeRectangle(coordSalle:tuple, structure:tuple) -> tuple:
    """
    renvoie les coords de la salle comme une rectangle.
    """
    x, y = coordSalle
    con = list()

    for i in range(4) :
        if structure[i] :
            if i%2 == 0 :
                con.append(DimensionHautBas)
            else :
                con.append(DimensionCoté)
        else :
            con.append((0,0))
    
    debutX = x - (DimensionSalle[0] // 2) - con[3][0] // 2
    debutY = y - (DimensionSalle[1] // 2) - con[0][1] // 2

    finX = x + (DimensionSalle[0] // 2) + con[1][0] // 2
    finY = y + (DimensionSalle[1] // 2) + con[2][1] // 2
    
    return (debutX, debutY), (finX, finY)

"""
Structure de contenuer

dict
{
    cle (indice) : [
        fltk_ID (int) image caree,

        [fltk_ID (int) tous les images de coté],

        (coord de la salle comme un rectangle debut - fin),

        (longeur et largeur de la salle),
        
        "oriantation de salle" (str)
    ]
}

Exemmple :
 {
    (0, 0): [2, [3, 4, 0, 0], ( (145, 120), (280, 255) ), (200, 200), 'horizontale'],

    (0, 1): [5, [6, 0, 7, 0], ((373, 161), (427, 239)), (400, 200), 'horizontale']
}
"""

def creer_salle(conteneur:dict, x:int, y:int, structure:tuple, cle:Hashable) -> None:
    """
    Fonction permet de créer la salle en combinant plusieurs images.

    Args :
        contenur (dict) : une dictionaire qui s'associe une clé avec une liste (salle).
        x (int) : coord X pour poser la salle.
        y (int) : coord Y pour poser la salle.
        structure (tuple) : la structure de la salle, comme (True, true, False, False).
        cle (Hashable) : cle pou s'associer avec la salle.
    """

    directionSalle = "horizontale"

    salle = fltk.image(x, y, Image["salleHor"], largeur = DimensionSalle[0], hauteur = DimensionSalle[1])
    con = [0,0,0,0]

    for i in range(4) :
        if structure[i] :
            pos, Dim = donne_positionEtDimenstion((x,y), i)
            con[i] = fltk.image(pos[0], pos[1], Image[i], largeur=Dim[0], hauteur=Dim[1])

    gammeRectangle = donne_gammeRectangle((x,y), structure)

    conteneur[cle] = [salle, con, gammeRectangle, (x,y), directionSalle]


def modifier_salle(conteneur:dict, cle:Hashable, structure:tuple) -> None:
    """
    Fonction permet de modifier l'affichage de la salle.

    Args :
        contenur (dict) : une dictionaire qui s'associe une clé avec une liste (salle).
        cle : (Hashable) : cle s'associer avec la salla qu'on veut modifier.
        structure (tuple) : nouvelle structure de la salle.
    """

    salle:list = conteneur[cle]
    coordSalle:tuple = salle[3]
 
    fltk.efface(salle[0])

    if salle[4] == "horizontale" :
        salle[0] = fltk.image(coordSalle[0], coordSalle[1], Image["salleVer"], largeur = DimensionSalle[0], hauteur = DimensionSalle[1])
        salle[4] = "verticale"
    else :
        salle[0] = fltk.image(coordSalle[0], coordSalle[1], Image["salleHor"], largeur = DimensionSalle[0], hauteur = DimensionSalle[1])
        salle[4] = "horizontale"

    for i in range(4) :
        fltk.efface(salle[1][i])
        if structure[i] :
            pos, Dim = donne_positionEtDimenstion(coordSalle, i)
            salle[1][i] = fltk.image(pos[0], pos[1], Image[i], largeur=Dim[0], hauteur=Dim[1])
        else :
            salle[1][i] = 0
    
    salle[2] = donne_gammeRectangle(salle[3], structure)


def donne_centre(contenur:dict, cle:tuple) -> tuple:
    """
    Donne la coord centre de la salle.

    Args :
        contenur (dict) : une dictionaire qui s'associe une clé avec une liste (salle).
        cle : (Hashable) : cle s'associer avec la salla qu'on veut modifier.
    """
    return contenur[cle][3]

def est_dans_rectangle(coord:tuple, coordRectangle:tuple) -> bool :
    """
    Verifie si une coord donné est à l'interieur d'une rectangle.
    """
    (dx, dy), (fx, fy) = coordRectangle
    cx, cy = coord
    return dx <= cx <= fx and dy <= cy < fy

    
