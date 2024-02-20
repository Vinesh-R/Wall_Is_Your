############################################################################
#PARTIE AFFICHAGE
############################################################################

import datetime
import sys
from time import sleep
from os import listdir, path
from random import choices

from fltk import *
from fichier  import *
from fltk import PIL_AVAILABLE

import audio
import guiMoteur as gui
import moteurV2 as moteur


if not PIL_AVAILABLE : 
    print("Veuillez installer la bibliotheque PILLOW derniere version")
    sys.exit()

color=None
Map=None 
skin=None
Donjon= None

try :
    resolution = sys.argv[1].split("x")
    WEIGHT = int(resolution[0])
    HEIGHT = int(resolution[1])

except :
    WEIGHT = 1400 #taille ecran largeur (suceptible a des modifs)
    HEIGHT = 800 #taille ecran hauteur (suceptible a des modifs)

audio.init()
WEIGHT_fixe = WEIGHT #taille ecran largeur (NON suceptible a des modifs)
HEIGHT_fixe = HEIGHT #taille ecran hauteur (NON suceptible a des modifs)

back=((WEIGHT*0.06142,HEIGHT*0.9025),(WEIGHT*0.1371,HEIGHT*0.93375))#coordonnées du bouton retour
exit=((WEIGHT*0.966428,HEIGHT*0.01375),(WEIGHT*0.992857,HEIGHT*0.031481))#coordonnées du bouton quitter

Couleurs = ["red", "blue","yellow", "cyan", "magenta", "white"]#liste de couleur (pour colorée la fleche de l'intention)

cree_fenetre(WEIGHT, HEIGHT)


def begin_screen():
    """Fonction qui lance l'ecran de menu principal et redirige ensuite l'utilisateur sur l'option choisie"""
    global HEIGHT
    global WEIGHT

    WEIGHT = WEIGHT_fixe
    HEIGHT = HEIGHT_fixe

    redimensionne_fenetre(WEIGHT,HEIGHT)
    efface_tout()
    image(WEIGHT/2, HEIGHT/2,"media/wallpaper.png" , largeur=WEIGHT,hauteur=HEIGHT)
    image(WEIGHT/2,HEIGHT/2 + HEIGHT*0.10 ,"media/menu_choice.png", largeur = int(WEIGHT*0.2),hauteur=int(HEIGHT*0.55))
    image(int(WEIGHT/2),int(HEIGHT*0.1),"media/logo.png", largeur = int(WEIGHT*0.30),hauteur=int(HEIGHT*0.36))
    image(WEIGHT*0.98,HEIGHT*0.03,"media/exit_button.png",largeur= int(WEIGHT*0.03),hauteur=int(HEIGHT*0.034)) 
    mise_a_jour()
    
    boucle = True

    while boucle:
        a=attend_clic_gauche()
        if a[0]>WEIGHT*0.426 and a[0]<WEIGHT*0.568 and a[1]> HEIGHT*0.447 and a[1]<HEIGHT*0.538:
            boucle = False
            maps_skin()

        if a[0]>WEIGHT*0.426 and a[0]<WEIGHT*0.568 and a[1]> HEIGHT*0.575 and a[1]<HEIGHT*0.668:
            boucle = False
            start()

        if a[0]>WEIGHT*0.426 and a[0]<WEIGHT*0.568 and a[1]> HEIGHT*0.672 and a[1]<HEIGHT*0.8:
            boucle = False
            sauvegarde()

        if gui.est_dans_rectangle(a,exit):
            ferme_fenetre()

def maps_skin():
    """Fonction (menu) qui nous demande de choisir entre le menu des skins et celui des maps"""

    efface_tout()

    image(WEIGHT/2, HEIGHT/2,"media/space.png" , largeur=WEIGHT,hauteur=HEIGHT)
    image(WEIGHT/2, HEIGHT/2.4,"media/menu_maps_skin.png" ,largeur=int(WEIGHT*0.3),hauteur=int(HEIGHT*0.7))
    image(WEIGHT*0.1,HEIGHT*0.92,"media/back_button.png",largeur= int(WEIGHT*0.08),hauteur=int(HEIGHT*0.034))
    image(WEIGHT*0.98,HEIGHT*0.03,"media/exit_button.png",largeur= int(WEIGHT*0.03),hauteur=int(HEIGHT*0.034)) 

    mise_a_jour()

    boucle=True

    while boucle:
        a = attend_clic_gauche()

        if a[0] > WEIGHT*0.324 and a[0] < WEIGHT*0.655 and a[1] > HEIGHT*0.217 and a[1] < HEIGHT*0.44:
            boucle = False
            chose_maps()

        if a[0]>WEIGHT*0.324 and a[0]<WEIGHT*0.655 and a[1]> HEIGHT*0.525 and a[1]<HEIGHT*0.751:
            boucle = False
            skin_menu()

        if gui.est_dans_rectangle(a,back):
            begin_screen()

        if gui.est_dans_rectangle(a,exit):
            ferme_fenetre()
                    

def chose_maps():
    """Fonction du choix de la maps dans le dossier maps"""
    global Map

    efface_tout()

    image(WEIGHT/2, HEIGHT/2,"media/space.png" , largeur=WEIGHT,hauteur=HEIGHT)
    image(WEIGHT/1.8,HEIGHT*0.02,"media/maps_t.png")
    image(WEIGHT*0.1,HEIGHT*0.92,"media/back_button.png",largeur= int(WEIGHT*0.08),hauteur=int(HEIGHT*0.034))
    image(WEIGHT*0.98,HEIGHT*0.03,"media/exit_button.png",largeur= int(WEIGHT*0.03),hauteur=int(HEIGHT*0.034))

    dic_coo={}
    lst_fichier = listdir("maps")

    w=0.1
    h=0.35
    w_t=0.06
    h_t=0.38

    coo=((WEIGHT*0.0369,HEIGHT*0.1453),(WEIGHT*0.159,HEIGHT * 0.418))

    if len(lst_fichier)>10:
        texte(WEIGHT*0.1,HEIGHT/2,"L'AFFICHAGE NE PEUT AFFICHER QUE  10 MAPS",taille=int(WEIGHT*0.028),couleur="red",tag="warning")
        mise_a_jour()
        sleep(3)
        efface("warning")

    if lst_fichier == [] :
        texte(WEIGHT*0.1,HEIGHT/2,"PAS DE MAPS DANS LE DOSSIER MAPS",taille=int(WEIGHT*0.028),couleur="red")

    for i in lst_fichier:
        
        if w >= 0.9 :
            w=0.1
            h+=0.47
            h_t+=0.33
            w_t=0.06
            coo=((WEIGHT*0.0369,HEIGHT*0.47592),(WEIGHT*0.159,HEIGHT * 0.77407)) 

        dic_coo[i]=coo

        fileName = path.splitext(i)[0]

        image(WEIGHT*w, HEIGHT*h/1.4,"media/porte_maps.png",largeur=int(WEIGHT*0.1),hauteur=int(HEIGHT*0.17))
        texte(WEIGHT*w_t, HEIGHT*h_t, fileName, taille=int(WEIGHT*0.03), couleur = "red")

        w+=0.2
        w_t+=0.2

        coo=((coo[0][0]+WEIGHT*0.161 ,coo[0][1]), (coo[1][0]+WEIGHT*0.23229,coo[1][1]))

    boucle=True

    while boucle:
        a=attend_clic_gauche()

        for i in dic_coo:

            if gui.est_dans_rectangle(a,dic_coo[i]) == True:
                boucle = False
                Map = i
                begin_screen()

            if gui.est_dans_rectangle(a,back):
                boucle = False
                maps_skin()

            if gui.est_dans_rectangle(a,exit):
                boucle = False
                ferme_fenetre()
                    
            

def sauvegarde() :
    """Fonction du choix de la map dans le dossier suavegarde"""
    global Map

    efface_tout()

    image(WEIGHT/2, HEIGHT/2,"media/space.png" , largeur=WEIGHT,hauteur=HEIGHT)
    image(WEIGHT/1.8,HEIGHT*0.02,"media/maps_t.png")
    image(WEIGHT*0.1,HEIGHT*0.92,"media/back_button.png",largeur= int(WEIGHT*0.08),hauteur=int(HEIGHT*0.034))
    image(WEIGHT*0.98,HEIGHT*0.03,"media/exit_button.png",largeur= int(WEIGHT*0.03),hauteur=int(HEIGHT*0.034))

    lst_fichier= listdir("sauvegarde")

    dic_coo={}

    w=0.1
    h=0.35
    w_t=0.04
    h_t=0.38

    coo=((WEIGHT*0.0369,HEIGHT*0.1453),(WEIGHT*0.159,HEIGHT * 0.418))

    if lst_fichier == [] :#affiche un message pour avertir la non présence de fichier dans le dossier sauvegarde
        texte(WEIGHT*0.1,HEIGHT/2,"PAS DE MAPS DANS LE DOSSIER SAUVEGARDE",taille=int(WEIGHT*0.028),couleur="red")

    for i in lst_fichier: 

        if w >= 0.9 :
            w=0.1
            h+=0.47
            h_t+=0.33
            w_t=0.06
            coo=((WEIGHT*0.0369,HEIGHT*0.47592),(WEIGHT*0.159,HEIGHT * 0.77407))

        dic_coo[i]=coo

        fileName = path.splitext(i)[0]

        image(WEIGHT*w, HEIGHT*h/1.4,"media/porte_maps.png",largeur=int(WEIGHT*0.1),hauteur=int(HEIGHT*0.17))
        texte(WEIGHT*w_t, HEIGHT*h_t, fileName, taille=int(WEIGHT*0.03), couleur = "red")

        w+=0.2
        w_t+=0.2
        
        coo=((coo[0][0]+WEIGHT*0.161 ,coo[0][1]),(coo[1][0]+WEIGHT*0.23229,coo[1][1]))

    boucle=True

    while boucle:
        a=attend_clic_gauche()

        if gui.est_dans_rectangle(a,back):
            boucle = False
            begin_screen()

        if gui.est_dans_rectangle(a,exit):
            boucle = False
            ferme_fenetre()

        for i in dic_coo:
            if gui.est_dans_rectangle(a,dic_coo[i]) == True:
                Map = i
                boucle = False
                begin_screen()


def skin_menu() :
    """Fonction du choix du skin entre le mario et le originale ainsi que la ligne de couleur"""
    global skin,color

    efface_tout()

    image(WEIGHT/2, HEIGHT/2,"media/space.png" , largeur=WEIGHT,hauteur=HEIGHT)
    image(WEIGHT/1.8,HEIGHT*0.02,"media/maps_t.png")
    image(WEIGHT*0.1,HEIGHT*0.92,"media/back_button.png",largeur= int(WEIGHT*0.08),hauteur=int(HEIGHT*0.034))
    image(WEIGHT*0.98,HEIGHT*0.03,"media/exit_button.png",largeur= int(WEIGHT*0.03),hauteur=int(HEIGHT*0.034))

    texte(WEIGHT*0.2,HEIGHT*0.1,"Choisissez votre skin de jeu !" ,taille=int(WEIGHT*0.035),couleur="yellow")
    image(WEIGHT/3,HEIGHT/2,"media/mario.png",largeur=int(WEIGHT*0.1),hauteur=int(HEIGHT*0.3))
    texte( WEIGHT*0.28,HEIGHT - HEIGHT/3,"MARIO",taille=int(WEIGHT*0.025),couleur="red")
    image(WEIGHT - WEIGHT/3,HEIGHT/2,"media/Knight_s.png",largeur=int(WEIGHT*0.15),hauteur=int(HEIGHT*0.3))
    texte( WEIGHT*0.63,HEIGHT - HEIGHT/3,"KNIGHT",taille=int(WEIGHT*0.025),couleur="grey")

    image(WEIGHT*0.49,HEIGHT*0.87,"media/ligne_color_button.png",largeur=int(WEIGHT*0.173),hauteur=int(HEIGHT*0.078))
    
    dic_skin={
        "mario":((WEIGHT*(479/1920),HEIGHT*(349/1080)),(WEIGHT*(774/1920),HEIGHT*(766/1080))),
        "originale":((WEIGHT*(1142/1920),HEIGHT*(376/1080)),(WEIGHT*(1456/1920),HEIGHT*(772/1080)))
        }
    
    if color ==  "RNG" :
        image(WEIGHT*0.64,HEIGHT*0.87,"media/on.png",largeur=int(WEIGHT*0.151/2.4),hauteur=int(HEIGHT*0.166/2.4))
    else:
        image(WEIGHT*0.64,HEIGHT*0.87,"media/off.png",largeur=int(WEIGHT*0.151/2.4),hauteur=int(HEIGHT*0.166/2.4))

    boucle=True

    while boucle:
        a=attend_clic_gauche()
        if gui.est_dans_rectangle(a,dic_skin["mario"]) == True:
            skin = "mario"
            boucle = False
            begin_screen()

        if gui.est_dans_rectangle(a,dic_skin["originale"]) == True:
            skin = "originale"
            boucle = False
            begin_screen()

        if gui.est_dans_rectangle(a,back):
            boucle = False
            maps_skin()

        if gui.est_dans_rectangle(a,exit):
            boucle = False
            ferme_fenetre()
        if gui.est_dans_rectangle(a,((569, 671),(805, 724))):
            if color == None :
                color = "RNG"
            else:
                color = None
            skin_menu()
    mise_a_jour()
    

def donjonGUI(grille):
    """Fonction qui va crée le donjon(salle)"""
    global HEIGHT, WEIGHT

    efface_tout()
    conteneur = dict()


    if skin == "originale":
        gui.fixeTexture(f"{skin}")

    else :
        #skin mario
        gui.fixeTexture(f"{skin}")
        
    x, y = gui.DimensionTotale

    redimX = WEIGHT / (gui.DimensionTotale[0] * len(grille[0]))
    redimY = HEIGHT / (gui.DimensionTotale[1] * len(grille))

    redim = min(redimX,redimY)

    if redim < 1 :
        gui.redimentionne(redim)
    
    HEIGHT = gui.DimensionTotale[1] * len(grille)
    WEIGHT = gui.DimensionTotale[0] * len(grille[0])

    redimensionne_fenetre(WEIGHT,HEIGHT)
    rectangle(0,0,WEIGHT,HEIGHT, remplissage="black", tag="bg")
    
    
    x, y = gui.DimensionTotale

    for i in range(len(grille)) :

        x = gui.DimensionTotale[0]

        for j in range(len(grille[i])) :

            gui.creer_salle(conteneur, x//2, y//2, grille[i][j],(i,j))
            x += gui.DimensionTotale[0]*2

        y += gui.DimensionTotale[1]*2
        
    mise_a_jour()
    
    return conteneur

def deplacement(aventurier,chemin,conteneur):
    """Fonction qui effectue le deplacemement de l'aventurier celon le chemin donnée et retrace la ligne de l'intention a chaque mouvemment"""

    while len(chemin) > 1: 
        if color == None:
            trace_ligne(chemin,conteneur,"red")
        else:
            trace_ligne(chemin,conteneur,choices(Couleurs))

        aventurier["position"]= chemin.pop()
        pose_aventurier(aventurier,conteneur)
        mise_a_jour()
        sleep(0.3)

    while len(chemin) !=0 :
        aventurier["position"]= chemin.pop()
        pose_aventurier(aventurier,conteneur)
        sleep(0.3)
        efface("chemin")
        mise_a_jour()

    pose_aventurier(aventurier,conteneur)



def pose_aventurier(aventurier,conteneur):
    """Fonction qui va poser l'aventurier celon ça place dans le dictionnaire"""
    global skin

    taille_w= gui.DimensionTotale[0]
    taille_h=gui.DimensionTotale[1]

    tailletexte = int(taille_w * 0.13)

    efface("A")
    efface("niveauTA")

    pos = gui.donne_centre(conteneur,aventurier["position"] )


    if skin == "originale":

        couleur = "yellow"

        if aventurier["etat"] == "V":
            if aventurier["niveau"] >1:
                image(pos[0],pos[1],"media/Knight_lvl2.png",largeur=int(0.5*taille_w),hauteur=int(taille_h*0.5), tag="A")
            else:    
                image(pos[0],pos[1],"media/Knight_s.png",largeur=int(0.5*taille_w),hauteur=int(taille_h*0.5), tag="A")

            L, l = int(taille_w * 0.5), int(taille_h * 0.5)

        else:
            image(pos[0],pos[1],"media/tombstone.png",largeur=int(0.5*taille_w),hauteur=int(taille_h*0.5), tag="A")   
    else:
        couleur = "yellow"

        if aventurier["etat"] == "V":
            if aventurier["niveau"] > 1:
                image(pos[0],pos[1],"media/mario_lvl2.png",largeur=int(0.5*taille_w),hauteur=int(taille_h*0.5), tag="A")
                L, l = int(taille_w * 0.5), int(taille_h * 0.5)
            else:
                image(pos[0],pos[1],"media/mario.png",largeur=int(0.3*taille_w),hauteur=int(taille_h*0.3), tag="A")
                L, l = int(taille_w * 0.3) + 17, int(taille_h * 0.3)
        else:
            image(pos[0],pos[1],"media/mario_dead.png",largeur=int(0.5*taille_w),hauteur=int(taille_h*0.5), tag="A")

    if aventurier["etat"] == "V" :
        posTextX = pos[0] - (L // 2)
        posTextY = pos[1] - (l // 2) - 5
        texte(posTextX, posTextY, aventurier["niveau"], couleur=couleur, taille = tailletexte, tag="niveauTA")

def pose_dragon(dragon,conteneur):
    """Fonction qui pose les dragons celon ça place dans leurs dictionnaires"""
    global skin
    taille_w= gui.DimensionTotale[0]
    taille_h=gui.DimensionTotale[1]

    tailleTexte = int(taille_w * 0.12)

    efface("D")
    efface("niveauTD")
    
    if skin == "originale":

        for i in dragon:

            pos = gui.donne_centre(conteneur,i["position"])

            if i["etat"] == "V":

                if i["niveau"] > 1:
                    image(pos[0],pos[1],"media/Dragon_lvl2.png",largeur=int(0.45*taille_w),hauteur=int(taille_h*0.45), tag="D")
                    L, l = int(taille_w * 0.45), int(taille_h * 0.45)
                else:
                    image(pos[0],pos[1],"media/Dragon_s.png",largeur=int(0.5*taille_w),hauteur=int(taille_h*0.5), tag="D")
                    L, l = int(taille_w * 0.5), int(taille_h * 0.5)

                posTextX = pos[0] - (L // 2) - 2
                posTextY = pos[1] - (l // 2) - 10
                texte(posTextX, posTextY, i["niveau"], couleur="yellow", taille = tailleTexte, tag="niveauTD")

            else:
                if i["niveau"] > 1:
                    image(pos[0],pos[1],"media/Dragon_lvl2_dead.png",largeur=int(0.5*taille_w),hauteur=int(taille_h*0.5), tag="D")
                else:
                    image(pos[0],pos[1],"media/Dragon_dead.png",largeur=int(0.35*taille_w),hauteur=int(taille_h*0.35), tag="D")

    else:

        for i in dragon:

            pos = gui.donne_centre(conteneur,i["position"])

            if i["etat"] == "V":

                if i["niveau"] > 1:
                    image(pos[0],pos[1],"media/bowser.png",largeur=int(0.4*taille_w),hauteur=int(taille_h*0.4), tag="D")
                    L, l = int(taille_w * 0.4), int(taille_h * 0.4)

                else:
                    image(pos[0],pos[1],"media/goomba.png",largeur=int(0.3*taille_w),hauteur=int(taille_h*0.3), tag="D")
                    L, l = int(taille_w * 0.3), int(taille_h * 0.3)
            
                posTextX = pos[0] - (L // 2) - 2
                posTextY = pos[1] - (l // 2) - 5
                texte(posTextX, posTextY, i["niveau"], couleur="yellow", taille = tailleTexte, tag="niveauTD")

            else:
                if i["niveau"] > 1:
                    image(pos[0],pos[1],"media/bowser_dead.png",largeur=int(0.4*taille_w),hauteur=int(taille_h*0.4), tag="D")
                else:
                    image(pos[0],pos[1],"media/goomba_dead.png",largeur=int(0.3*taille_w),hauteur=int(taille_h*0.3), tag="D")


def dicDragon2str(dragons):
    """Fonction qui transforme les values du dictionnaire en chaine de caractere"""
    strDragon = list()

    for d in dragons :
        dragon = "D " + " ".join(map(str, d["position"]))
        dragon = dragon + " " + str(d["niveau"]) + " " + d["etat"]
        strDragon.append(dragon)
    
    return strDragon

def to_save(grille,aventurier,dragons):
    """Fonction qui sauvegarde la partie dans le dossier sauvegarde avec comme nom de fichier le temps actuelle"""

    date = datetime.datetime.now()
    time = date.strftime("%H%M%S")

    Aventurier = "A " + " ".join(map(str, aventurier["position"]))
    Aventurier = Aventurier + " " + str(aventurier["niveau"]) + " " + aventurier["etat"]

    Dragons = dicDragon2str(dragons)

    Grille = reverse_tuple_grille(grille)
    Grille.append(Aventurier)
    Grille = Grille + Dragons


    with open(f"sauvegarde/{time}.txt", "a+", encoding="utf-8") as f:
        for elem in Grille :
            f.write(elem)
            f.write("\n")
        
    
def combat(aventurier,dragon_lst):
    """Fonction qui detecte si deux entité (aventurier et dragon) sont sur une meme case si c'est le cas retourne l'entité en question"""
    for i in dragon_lst:
        if i["position"] == aventurier["position"]:
            return i

def trouve_cle(aventurier,dragon,pos):
    for i in dragon :
        if i["position"] == pos :
            return "D"
    else:
        return "A"

def perdant(aventurier,dragon):
    if aventurier["niveau"] >= dragon["niveau"]:
        return dragon
    else:
        return aventurier    

def nbr_dragon_in_life(dragon):
    """Donne le nombre de dragon en vie dans la partie via la liste_dictionnaire des dragons"""
    count=0
    for i in dragon:
        if i["etat"] == "V":
            count+=1
    return count

def tue(entite,aventurier,dragon):
    """Tue l'entité qui se trouve dans le dictionnaire aventurier ou la list_dico dragon et si c'est un dragon rajoute +1 au niveau de l'aventurier ainsi que supprimer ça position dans le gui moteur"""
    type=trouve_cle(aventurier,dragon,entite["position"])
    if type == "D" :
        pos = entite['position']
        Donjon.remove_dragon_pos(pos)
        Donjon.niveauDragonEleve = dragon_niveau_eleve(dragon)
        aventurier["niveau"]+=1

    entite["etat"] = "M"


    
def victoire(dragon):
    if nbr_dragon_in_life(dragon) == 0 :
        if skin == "originale" :
            audio.play("aventurier")
        else :
            audio.play("mario")
        return True
    
def defaite(aventurier):
    if aventurier["etat"] == "M":
        if skin == "originale" :
            audio.play("gameOverA")
        else :
            audio.play("gameOverM")

        return True
    
    else :
        if skin == "originale" :
            audio.play("aventurier")
        else :
            audio.play("mario")

        return False
        
def positionDragons(dragons) -> list :
    """Récupere toute les positions des dragons dans une liste et les renvoies"""
    positions = list()

    for dragon in dragons :
        if dragon["etat"] == "V" :
            positions.append(dragon["position"])
    
    return positions


def dragon_niveau_eleve(dragons) -> int:
    """Trouver dragons au plus haut niveau"""

    maxNiveau = 1

    for dragon in dragons :
        if dragon["niveau"] > maxNiveau and dragon["etat"] ==  "V":
            maxNiveau = dragon["niveau"]

    return maxNiveau


def verifie_postion_entité(salle, aventurier, Posdragons) -> bool :
    """
    Verifie si une entitée est présente dans la salle
    """

    if salle == aventurier["position"] or salle in Posdragons :
        return True

    return False

def pivoter(dojon: moteur.Donjon, contenuer, salle:tuple) :
    """Fonction permet de rotate la salle"""

    i,j = salle
    dojon.rotate(salle)

    nv_structure = dojon.donjon[i][j]
    gui.modifier_salle(contenuer, salle, nv_structure)

def fin_de_jeu(aventurier,dragon):
    """Vérifie si le jeu est dans la poistion (victoire) ou (défaite) si ce n'est pas le cas elle ne fait rien"""
    global WEIGHT,HEIGHT

    if victoire(dragon) == True:
        if WEIGHT < 300 or HEIGHT < 300:
            redimensionne_fenetre(1440,1080)
            WEIGHT,HEIGHT= 1440,1080
            rectangle(0,0,WEIGHT,HEIGHT, remplissage="black", tag="bg")
        image(WEIGHT/2.1,HEIGHT/2.2,"media/finish-menu.png",largeur =int(WEIGHT*(0.1375*2)),hauteur = int(HEIGHT*(0.2211*2)))
        image(WEIGHT/1.85,HEIGHT/2.4,"media/replay_button.png",largeur =int(WEIGHT*0.02857),hauteur = int(HEIGHT*(0.04444)))
        image(WEIGHT/2.18,HEIGHT/2.4,"media/bouton_finish.png",largeur =int(WEIGHT*0.121428),hauteur = int(HEIGHT*(0.064444)))
        image(WEIGHT/2.07,HEIGHT/3.5,"media/logo.png",largeur =int(WEIGHT*0.155),hauteur = int(HEIGHT*(0.19444)))
        image(WEIGHT/2.07,HEIGHT/1.945,"media/home.png",largeur =int(WEIGHT*0.1),hauteur = int(HEIGHT*(0.2)))
        image(WEIGHT*0.48,HEIGHT*0.2,"media/victory.png",largeur=int(WEIGHT*0.509/2),hauteur=int(HEIGHT*0.144/2))
        image(WEIGHT*0.47,HEIGHT*0.57,"media/victo.png",largeur=int(WEIGHT*0.509/2),hauteur=int(HEIGHT*0.144/2))
        mise_a_jour()
        audio.play("victory")
        
        
        boucle=True

        while boucle == True:
            a=attend_clic_gauche()
            if gui.est_dans_rectangle(a,((WEIGHT*0.5235,HEIGHT*0.3875),(WEIGHT*0.55428,HEIGHT*0.44))):
                start()
            if gui.est_dans_rectangle(a,((WEIGHT*0.46,HEIGHT*0.455),(WEIGHT*0.4928,HEIGHT*0.53))):
                begin_screen()
            if gui.est_dans_rectangle(a,((WEIGHT*0.3971,HEIGHT*0.34111),(WEIGHT*0.515,HEIGHT*0.44125))):
                ferme_fenetre()

    if defaite(aventurier) == True:
        if WEIGHT < 300 or HEIGHT < 300:
            redimensionne_fenetre(1440,1080)
            WEIGHT,HEIGHT= 1440,1080
            rectangle(0,0,WEIGHT,HEIGHT, remplissage="black", tag="bg")

        image(WEIGHT/2.1,HEIGHT/2.2,"media/finish-menu.png",largeur =int(WEIGHT*(0.1375*2)),hauteur = int(HEIGHT*(0.2211*2)))
        image(WEIGHT/1.85,HEIGHT/2.4,"media/replay_button.png",largeur =int(WEIGHT*0.02857),hauteur = int(HEIGHT*(0.04444)))
        image(WEIGHT/2.18,HEIGHT/2.4,"media/bouton_finish.png",largeur =int(WEIGHT*0.121428),hauteur = int(HEIGHT*(0.064444)))
        image(WEIGHT/2.07,HEIGHT/3.5,"media/logo.png",largeur =int(WEIGHT*0.155),hauteur = int(HEIGHT*(0.19444)))
        image(WEIGHT/2.07,HEIGHT/1.945,"media/home.png",largeur =int(WEIGHT*0.1),hauteur = int(HEIGHT*(0.2)))
        image(WEIGHT*0.47,HEIGHT*0.57,"media/you_lose.png",largeur=int(WEIGHT*0.544/3),hauteur=int(HEIGHT*0.274/3))
        mise_a_jour()
        audio.play("Game Over")

        boucle=True

        while boucle == True:
            a=attend_clic_gauche()
            if gui.est_dans_rectangle(a,((WEIGHT*0.5235,HEIGHT*0.3875),(WEIGHT*0.55428,HEIGHT*0.44))):
                start()
            if gui.est_dans_rectangle(a,((WEIGHT*0.46,HEIGHT*0.455),(WEIGHT*0.4928,HEIGHT*0.53))):
                begin_screen()
            if gui.est_dans_rectangle(a,((WEIGHT*0.3971,HEIGHT*0.34111),(WEIGHT*0.515,HEIGHT*0.44125))):
                ferme_fenetre()
   

def trace_ligne(chemin:list, conteneur:dict, couleur:str) :
    """Trace la ligne de l'intention"""
    efface("chemin")
    for i in range(len(chemin) - 1, 0, -1) :
        centre1X, centre1Y = gui.donne_centre(conteneur, chemin[i])
        centre2X, centre2Y = gui.donne_centre(conteneur, chemin[i-1])

        ligne(centre1X, centre1Y, centre2X, centre2Y, couleur=couleur, tag="chemin", epaisseur=2)


def start():
    """Fonction (Moteur du jeu) qui suite au choix start dans le menu va lancer le jeu avec les parametre globaux map,skin,donjon"""
    global Map,skin,Donjon,color

    if Map == None :
        grille=['╗╝╩╞╦╔', '╩╦╡╩╝╠', '╦╬╡╝╔╥', '╬═╥╩╚╗', '╨╦╬╔╣╗', "╬╨╩╨╞╔", 'A25', 'D421', 'D202', 'D403']
    else:
        grille = supp( maps(f"{Map}"),"\n")
    if skin == None:
        skin = "originale"

    if verification(grille) == False:#vérifie que la grille est jouable sinon refut de la traiter
        texte(WEIGHT*0.2,HEIGHT*0.3,"Le fichier ne respecte pas le format veuillez voir la notice ",taille=int(WEIGHT*0.02),couleur="red")
        mise_a_jour()
        sleep(1)
        begin_screen()
    else:
        grille_2 = tri(grille) #grille triée
        grille_3 = grille_tuple(grille_2) #représentation de la grille sous frome de tuple

        dragons = dragon_(grille_2)
        aventurier = aventurier_(grille_2)
        conteneur = donjonGUI(grille_3)

        PosDragons = positionDragons(dragons)

        Donjon = moteur.Donjon(grille_3, PosDragons, dragon_niveau_eleve(dragons))
        pose_dragon(dragons,conteneur)
        pose_aventurier(aventurier,conteneur)
        loop = True
        chemin = []
        
        while loop :
                
            chemin = Donjon.give_path(aventurier["position"], dragons)
            efface("chemin")
            if color == None :
                trace_ligne(chemin, conteneur, "red")
            else:
                trace_ligne(chemin, conteneur, choices(Couleurs))
            Ev = attend_ev()
            typeEv = type_ev(Ev)

            if typeEv == "Quitte"  or (typeEv == "Touche" and touche(Ev) == "Escape"):
                break

            elif typeEv == "Touche" and touche(Ev) == "h"  :
                begin_screen()

            elif typeEv == "Touche" and touche(Ev) == "r" :#recommence la partie
                start()

            elif typeEv == "Touche" and touche(Ev) == "s" :#sauvegarde la partie
                sleep(1)
                to_save(grille_3,aventurier,dragons)
                
            elif typeEv == "Touche" and (touche(Ev) == "Return" or touche(Ev) == "space") :
                deplacement(aventurier,chemin,conteneur)
                l=combat(aventurier,dragons)

                if l != None:
                    perd=perdant(aventurier,l)
                    tue(perdant(aventurier,l),aventurier,dragons)
                    pose_dragon(dragons,conteneur)
                    pose_aventurier(aventurier,conteneur)
                    fin_de_jeu(aventurier,dragons)
            
            elif typeEv == "ClicGauche" :
                clic = (abscisse(Ev), ordonnee(Ev))

                for salle in conteneur :

                    if gui.est_dans_rectangle(clic, conteneur[salle][2]) :
                        pivoter(Donjon, conteneur, salle)

                        if verifie_postion_entité(salle, aventurier, PosDragons) :
                            pose_dragon(dragons,conteneur)
                            pose_aventurier(aventurier,conteneur)
            
            else :
                pass


try :
    begin_screen()#on lance le jeu via l'ecran de menu
except :
    pass

    