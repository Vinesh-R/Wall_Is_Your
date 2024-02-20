############################################################################
#PARTIE FICHIER
############################################################################
tpl_grille={
    "═":(False,True,False,True),
    "║":(True,False,True,False),
    "╔":(False,True,True,False),
    "╗":(False,False,True,True),
    "╚":(True,True,False,False),
    "╝":(True,False,False,True),
    "╠":(True,True,True,False),
    "╣":(True,False,True,True),
    "╦":(False,True,True,True),
    "╩":(True,True,False,True),
    "╨":(True,False,False,False),
    "╡":(False,False,False,True),
    "╥":(False,False,True,False),
    "╞":(False,True,False,False),
    "╬":(True,True,True,True),
}

reverse_grille = {value: key for key, value in tpl_grille.items()}

def maps(argument):
    """Fonction qui nous renvoie une maps celon l'argument et la split dans une liste via la fonction readlines"""
    try:
        with open(f"maps/{argument}", "r", encoding="utf-8") as files :
            return files.readlines()
    except:

        with open(f"sauvegarde/{argument}", "r", encoding="utf-8") as files :
            return files.readlines()
        
def niveau_coherent(aventurier_nv, dragons_nv):

    dragons_nv.sort()
    for nv in dragons_nv:
        if nv <= aventurier_nv:
            aventurier_nv += 1
        else:
            return False
        
    return True

def reverse_tuple_grille(Grille) :
    strMap = list()
    for line in Grille :
        tmp = str()

        for stat in line :
            tmp += reverse_grille[stat]
        
        strMap.append(tmp)
    
    return strMap


def verification(lst):
    """Fonction qui va prendre en parametre une liste (la maps du jeu) et va l'analyser sous plusieur condition pour vérifier que la maps est prete a etre chargée"""
    for i in lst:
        for z in i:
            if z not in tpl_grille and z and z != "A" and z!= " " and z!="D" and z!= "M" and z!= "V":
                try:
                    int(z) == z
                    z*-1!=z
                except:    
                    return False
    for i in lst:
        if i == "":
            return False
    if lst==[]:#si le fichier est vide return False
        return False
    verif_map_complete=tri(lst)[0]
    verif_map = supp(tri(lst)," ")[0]
    verif_a = supp(tri(lst)[1]," ")
    verif_d = supp(tri(lst)[2]," ")

    lst_d=[]
    tp_d=""
    #map

    taille_ligne=len(verif_map_complete[0])
    taille_collone=len(verif_map_complete)

    for l in verif_map_complete:
        if len(l) != taille_ligne:
            return False
        
    for s in verif_map:
        if s not in tpl_grille:
            return False
        
    #dragon
    niveau_dragon = []
    if len(verif_d) == 0 :
        return False
    
    for d in verif_d:

        try:
            int(d[1])
            int(d[2])
            int(d[3])
            if  d[0] != "D":
                return False
        except:
            return False
        
        if int(d[1])>=taille_collone or int(d[2])>=taille_ligne:#vérifie que la position du dragon est cohèrente a la map !
            return False
        niveau_dragon.append(int(d[3]))
        tp_d = (d[1],d[2])
        lst_d.append(tp_d)

    for k in range(len(lst_d)):
        for j in range(k+1, len(lst_d)):
            if lst_d[k] == lst_d[j]:
                return False
    
    #aventurier
    if len(verif_a) != 1:#verifie qu'il ny a qu'un aventurier
        return False
    for a in verif_a:

        try:
            int(a[1])
            int(a[2])
            if a[0] != "A":
                return False
        except:
            return False
        
        if int(a[1])>=taille_collone or int(a[2])>=taille_ligne:#vérifie que la position de l'aventurier est cohèrente a la map !
            return False
        try:
            if a[3].isnumeric() != True or a[4] == "M":
                return False  
        except:
            pass

        try:
            niveau_aventurier = int(a[3])
        except:
            niveau_aventurier=1

    if niveau_coherent(niveau_aventurier,niveau_dragon) != True:
        return False

    return True#si tous les test de la map on été reussi la fonction return True

def supp(lst,arg):
    """Fonction qui prend en parametre la liste d'un fichiers maps et supprime les arg de cette liste"""
    mot=""
    lst_2=[]
    for i in lst:
        mot=""
        for z in i :
            if z != arg :
                mot+=z
        lst_2.append(mot)
    return lst_2  
 

def tri(lst):
    """Fonction qui prend en parametre une liste avec toute les infos de la map et les transforme en liste de liste 
    séparant les différente info"""

    grille=[]
    aventurier=[]
    dragon=[]

    for i in lst:
        if i[0]  in tpl_grille :
            grille.append(i)
    
        if i[0]=="A":
            aventurier.append(i)

        if i[0]=="D":
            dragon.append(i)

    return [grille,aventurier,dragon]


def grille_tuple(lst):
    """Fonction qui prend en parametre une liste avec la disposition des caractere représantant la maps et renvoie cette map sous forme de tuple"""
    grille=lst[0]

    tpl=[]

    for i in grille:
        ti=[]
        for z in i:
            ti.append(tpl_grille[z])
            
        tpl.append(ti)

    return tpl


def aventurier_(lst):
    """Fonction qui prend en parametre la liste des infos de la maps et renvoie un dictionnaire avec les niveau et la position de l'aventure"""
    aventurier_=supp(supp(lst[1]," "),"A")

    dic_aventurier = {}
    dic_aventurier["position"]=(int(aventurier_[0][0]),int(aventurier_[0][1]))

    if len(aventurier_[0]) == 2:
        dic_aventurier["niveau"]=1

    else:
        dic_aventurier["niveau"]=int(aventurier_[0][2])

    dic_aventurier["etat"]="V"
    
    return dic_aventurier

def dragon_(lst):
    """Fonction qui prend en parametre une liste avec les infos de la maps et qui renvoie un dictionnaire possédant des dictionnaire des dragon avec leur niveau et leur position et une liste avec ces meme dragons"""
    dragon_ = supp(supp(lst[2]," "),"D")

    lesdragons = []
    count = 0
    for i in dragon_ :
        count += 1
        try:
            if i[3] == "V":
                lesdragons.append({"position" : (int(i[0]),int(i[1])),"niveau":int(i[2]),"etat":"V"})
            if i[3] == "M":
                lesdragons.append({"position" : (int(i[0]),int(i[1])),"niveau":int(i[2]),"etat":"M"})
        except:
            lesdragons.append({"position" : (int(i[0]),int(i[1])),"niveau":int(i[2]),"etat":"V"})
    return lesdragons



