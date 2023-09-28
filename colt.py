import random
from tkinter import * 
import tkinter.scrolledtext as tkscrolledtext
from PIL import Image, ImageTk 
import pygame
import os

# path of the sound file in the actual directory
c_path = os.path.join(os.path.dirname(__file__), 'c.mp3')
o_path = os.path.join(os.path.dirname(__file__), 'o.mp3')
pygame.mixer.init()
pygame.mixer.music.load(o_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
effect = pygame.mixer.Sound(c_path)
effect.set_volume(1.0)




class Jeu(Tk):
    def __init__(self):
        super().__init__()
        

        #définition des variables

        self.NB_JOUEURS = 3
        self.NB_WAGONS = 4
        self.NB_ACTIONS = 3
        self.NB_BALLES = 3
        self.NB_TOURS = 3
        self.JOUEUR_EN_COURS = 0
        self.MARSHALL = 0


        #définition des paramètres de la fenêtre

        self.title("Colt Express")
        self.resizable(False, False)

        #poids fenêtre

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight=1)
        
        #canvas du jeu

        self.jeu = Canvas(self, bg='Ivory', width=1600, height= 631)
        self.jeu.grid(row = 0, column= 0, sticky='nsew')
    


        #définition du menu
        
        self.maxRowMenu = 5


        self.menu = Canvas(self, bg="#0b3c5c")
        self.menu.grid(row = 1, column = 0, sticky='nsew')


        for i in [0, 6]:
            self.menu.columnconfigure(i, weight=2)
        for i in [2, 4]:
            self.menu.columnconfigure(i, weight=4)



        self.menu.rowconfigure(self.maxRowMenu -1, weight=1)
        self.menu.rowconfigure(0, weight=1)

        self.framebtns = Frame(self.menu, bg = "#0b3c5c")
        self.framebtns.grid(column = 1, row = 1)

        
        #ouverture icônes des boutons
        path = os.path.join(os.path.dirname(__file__), 'btns')
        self.icones = []
        for i in range(1, 7):
            img = self.createImg(60, 60, Image.open(f'{path}/icone{i}.png'))
            self.icones.append(img)

        #création de l'icône press start 
        
        self.img = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__), 'press.png')))

        self.btnAction = Button(self.menu, command = self.actionUne, image= self.img,bg="#0b3c5c", border = 0, highlightthickness= 0, activebackground="#006a79", state = DISABLED)
            
        
        self.btnHaut = Button(self.framebtns, command = lambda:[self.actionRetour("haut"), self.ajoutActions("haut")], image= self.icones[0], bg="#0b3c5c", border = 0, highlightthickness= 0, activebackground="#006a79")

        self.btnDroite = Button(self.framebtns,command = lambda:[self.actionRetour("droite"),self.ajoutActions("droite")], image= self.icones[1], bg="#0b3c5c", border = 0, highlightthickness = 0, activebackground="#006a79")

        self.btnBas = Button(self.framebtns, command = lambda:[self.actionRetour("bas"), self.ajoutActions("bas")], image= self.icones[2], bg="#0b3c5c", border = 0, highlightthickness= 0, activebackground="#006a79")

        self.btnGauche = Button(self.framebtns, command = lambda:[self.actionRetour("gauche"), self.ajoutActions("gauche")], image= self.icones[3], bg="#0b3c5c", border = 0, highlightthickness= 0, activebackground="#006a79")

        self.btnBraquer = Button(self.framebtns, command = lambda:[self.actionRetour("braquer"), self.ajoutActions("braquer")], image= self.icones[4], bg="#0b3c5c", border = 0, highlightthickness= 0, activebackground="#006a79")

        self.btnTirer = Button(self.framebtns, command = lambda:[self.actionRetour("tirer"),self.ajoutActions("tirer")], image= self.icones[5], bg="#0b3c5c", border = 0, highlightthickness= 0, activebackground="#006a79")




        self.bind('<Up>', lambda event:[self.actionRetour("haut"), self.ajoutActions("haut")])
        self.bind('<Down>', lambda event:[self.actionRetour("bas"), self.ajoutActions("bas")])
        self.bind('<Left>', lambda event:[self.actionRetour("gauche"), self.ajoutActions("gauche")])
        self.bind('<Right>', lambda event:[self.actionRetour("droite"), self.ajoutActions("droite")])
        self.bind('<s>', lambda event:[self.actionRetour("tirer"), self.ajoutActions("tirer")])
        self.bind('<d>', lambda event:[self.actionRetour("braquer"), self.ajoutActions("braquer")])





        self.btnHaut.grid(column = 3, columnspan = 2, row = 1)
        self.btnDroite.grid(column = 6, row = 2)
        self.btnBas.grid(column = 3, columnspan = 2, row = 3)
        self.btnGauche.grid(column = 1, row = 2)
        self.btnBraquer.grid(column = 2, columnspan = 2, row = 2)
        self.btnTirer.grid(column = 4, columnspan = 2, row = 2)

 
        self.btnAction.grid(column = 8, row = 1, rowspan = 3)



        #texte défilant

        self.textscr = tkscrolledtext.ScrolledText(self.menu,width = 50,height = 15, bg="#0b3c5c", border = 0, highlightthickness= 0, foreground = "#9db1cd", font = 200)
        self.textscr.grid(column = 10, row = 0, rowspan = self.maxRowMenu, padx = 50, pady = 50)
        

        
        

        #définition de la liste des bandits


        listenoms = ["Blue", "Red", "Black"]
        self.bandits = []
        for i in range(self.NB_JOUEURS):
            self.bandits.append(Bandit(self, self.NB_BALLES, f"{listenoms[i]}")) #  [BANDIT {i+1}]


        
        #print(self.bandits) debug

        #définition de la liste des wagons

        self.wagons = []
        for i in range(self.NB_WAGONS):
            self.wagons.append(Wagon(self, i))
        

        self.textscr.insert(END, "Bienvenue au Colt Express.\n\nÊtes-vous prêtes à les DÉPOUILLER ?\n\n\n")
        self.textscr.insert(END, "Phase Plannification :\n\n\n")
        self.textscr.insert(END, f"{self.bandits[0].nom} : c'est à toi.\n\n")
        self.textscr.see(END)

        

        #initialisation des images sur les canvas


        self.drawgame()

    @staticmethod
    def createImg(width, height, loadedImg):
        loadedImg = loadedImg.resize((width, height))
        return ImageTk.PhotoImage(loadedImg)

    @staticmethod
    def findWidth(width, height, newHeight):
       newWidth = (width / height) * newHeight
       return int(newWidth), int(newHeight)


    def actionRetour(self, action, *args): #retour instantané après chaque clic
        if action == "gauche":
            effect.play()
            self.textscr.insert(END, f"{self.bandits[self.JOUEUR_EN_COURS].nom} a décidé d'aller à gauche\n")
        elif action == "droite":
            effect.play()
            self.textscr.insert(END, f"{self.bandits[self.JOUEUR_EN_COURS].nom} a décidé d'aller à droite\n")
        elif action == "haut":
            effect.play()
            self.textscr.insert(END, f"{self.bandits[self.JOUEUR_EN_COURS].nom} a décidé d'aller en haut\n")
        elif action == "bas":
            effect.play()
            self.textscr.insert(END, f"{self.bandits[self.JOUEUR_EN_COURS].nom} a décidé d'aller en bas\n")
        elif action == "tirer":
            effect.play()
            self.textscr.insert(END, f"{self.bandits[self.JOUEUR_EN_COURS].nom} a décidé de tirer au wagon {self.bandits[self.JOUEUR_EN_COURS].wagon+1}\n")
        elif action == "braquer":
            effect.play()
            self.textscr.insert(END, f"{self.bandits[self.JOUEUR_EN_COURS].nom} a décidé de braquer au wagon {self.bandits[self.JOUEUR_EN_COURS].wagon+1}\n")
        self.textscr.see(END)


   
    def ajoutActions(self, action, *args):
        self.bandits[self.JOUEUR_EN_COURS].actions.append(action)
        if len(self.bandits[self.JOUEUR_EN_COURS].actions) == self.NB_ACTIONS:
            if self.JOUEUR_EN_COURS == self.NB_JOUEURS-1:
                self.btnAction.configure(state = NORMAL)
                self.bind('<a>', self.actionUne)

                self.textscr.insert(END, "\n\nPhase Action :\n\n\n")
                self.textscr.see(END)

                for btn in self.framebtns.grid_slaves():
                    btn.configure(state = DISABLED)

            #dissocier commandes claviers

                self.unbind('<Up>')    
                self.unbind('<Down>')    
                self.unbind('<Left>')    
                self.unbind('<Right>')    
                self.unbind('<s>')    
                self.unbind('<d>')

                self.JOUEUR_EN_COURS = 0
                return 
            self.JOUEUR_EN_COURS +=1
            self.textscr.insert(END, f"\n\n{self.bandits[self.JOUEUR_EN_COURS].nom} : c'est à toi.\n\n")
            self.textscr.see(END)




    def actionUne(self, *args):
        effect.play()

        for bandit in self.bandits:
            bandit.action()
            self.textscr.see(END)
        self.deplacementMarshall()
        self.MarshallAttaque()
        self.textscr.insert(END, "\n\n\n")
        self.textscr.see(END)

        if len(bandit.actions) == 0:
            self.NB_TOURS -= 1
            self.textscr.insert(END, "\n\n\n")
            self.textscr.see(END)
            self.btnAction.configure(state = DISABLED)
            self.unbind('<a>')

            for bandit in self.bandits:
                if bandit.balles ==0:
                    self.textscr.insert(END, f"{bandit.nom} possède {bandit.balles} balle et ")
                else:
                    self.textscr.insert(END, f"{bandit.nom} possède {bandit.balles} balles et ")
                bi = 0 #bijou
                bou = 0 #bourse
                ma = 0 #magot

                if len(bandit.butin) == 0:
                    self.textscr.insert(END, "aucun butin...")

                for butin in bandit.butin:
                    if butin.typ == "bijou":
                        bi +=1
                    if butin.typ == "bourse":
                        bou +=1
                    if butin.typ == "magot":
                        ma +=1

                if bou == 1:
                    self.textscr.insert(END, f"{bou} bourse")
                elif bou >= 2:
                    self.textscr.insert(END, f"{bou} bourses")
                if bi != 0 and bou != 0:
                    self.textscr.insert(END, " et ")
                if bi == 1:
                    self.textscr.insert(END, f"{bi} bijou")
                elif bi >= 2:
                    self.textscr.insert(END, f"{bi} bijoux")
                if bi != 0 and ma == 1:
                    self.textscr.insert(END, " et ")
                if ma == 1:
                    self.textscr.insert(END, "1 magot")
                            
                self.textscr.insert(END, ".\n")
                self.textscr.see(END)

            self.textscr.insert(END, "\n\n\n\n\n")



            if self.NB_TOURS !=0:
                self.textscr.insert(END, "Phase Plannification :\n\n\n")

            if self.NB_TOURS != 0:
                self.textscr.insert(END, f"{self.bandits[0].nom} : c'est à toi.\n\n")
            self.textscr.see(END)
            for btn in self.framebtns.grid_slaves():
                btn.configure(state = NORMAL)

            #réassocier boutons

            self.bind('<Up>', lambda event:[self.actionRetour("haut"), self.ajoutActions("haut")])
            self.bind('<Down>', lambda event:[self.actionRetour("bas"), self.ajoutActions("bas")])
            self.bind('<Left>', lambda event:[self.actionRetour("gauche"), self.ajoutActions("gauche")])
            self.bind('<Right>', lambda event:[self.actionRetour("droite"), self.ajoutActions("droite")])
            self.bind('<s>', lambda event:[self.actionRetour("tirer"), self.ajoutActions("tirer")])
            self.bind('<d>', lambda event:[self.actionRetour("braquer"), self.ajoutActions("braquer")])


        if self.NB_TOURS == 0:

            #dissocier commandes claviers

            self.unbind('<Up>')    
            self.unbind('<Down>')    
            self.unbind('<Left>')    
            self.unbind('<Right>')    
            self.unbind('<s>')
            self.unbind('<d>')

            for btn in self.framebtns.grid_slaves():
                btn.configure(state = DISABLED)
            self.textscr.insert(END, "********************************\n              FIN DE JEU\n********************************\n\n\n")
            self.Victoire()

            self.textscr.see(END)

          


    def deplacementMarshall(self):

        if self.MARSHALL == 0:
            self.jeu.move(self.MARSHALL_ID, 300, 0)
            self.MARSHALL += 1
            
        elif self.MARSHALL == 3:
            self.jeu.move(self.MARSHALL_ID, -300, 0)
            self.MARSHALL -= 1

        elif random.choice(["droite", "gauche"]) == "droite":
            self.jeu.move(self.MARSHALL_ID, 300, 0)
            self.MARSHALL += 1
        else:
            self.jeu.move(self.MARSHALL_ID, -300, 0)
            self.MARSHALL -= 1
        
    def MarshallAttaque(self):
        for bandit in self.bandits:
            if bandit.pos == "toit" or bandit.wagon != self.MARSHALL:
                continue
            
            bandit.fuir()
            bandit.lacherButin()

    def Victoire(self):
        gagnant = self.bandits[0]
        exaequo = [gagnant] 
        gagnantButin = gagnant.calculButin()
        for bandit in self.bandits:
            butinT = bandit.calculButin()
            self.textscr.insert(END,f"{bandit.nom} a obtenu {butinT}$ !\n")
            if butinT > gagnant.butinTotal:
                gagnant = bandit
                exaequo = [gagnant]
            elif butinT == gagnant.butinTotal and bandit.id != gagnant.id:
                exaequo.append(bandit)
        if gagnant.butinTotal == 0:
            self.textscr.insert(END,f"\n\nVous avez toutes... perdu...?\n")
        elif len(exaequo) == 2:
            self.textscr.insert(END,f"\n\n{exaequo[0].nom} et {exaequo[1].nom} ont eu ex-aequo.\n")
        elif len(exaequo) == 3:
            self.textscr.insert(END,f"\n\n{exaequo[0].nom}, {exaequo[1].nom} et {exaequo[2].nom} ont eu ex-aequo.\n")
        else:
            self.textscr.insert(END,f"\n\n{gagnant.nom} a gagné !\n")
        pygame.mixer.music.set_volume(0.1)


            
        



    
    def drawgame(self):

        x = 1602
        y = 633

        pos_toit = int(y * 0.286)
        pos_interieur = int(y * 0.61)
        
        #dessin du jeu

        self.ImageFond = Image.open(os.path.join(os.path.dirname(__file__), 'fond.png'))
        self.ImageFond = self.ImageFond.resize((x , y))
        self.ImageFond = ImageTk.PhotoImage(self.ImageFond)
        self.jeu.create_image(0 , 0, image=self.ImageFond, anchor="nw")

        #dessin des bandits

        for i in range(self.NB_JOUEURS):
            self.bandits[i].dessinBandit(int(x * 0.1), int((x * 0.80)+ (x* 0.06) * i ), pos_toit, i+1)

        #dessin du marshall

        self.imgM = Image.open(os.path.join(os.path.dirname(__file__), 'marshall.png'))

        xMarshall, yMarshall = self.findWidth(self.imgM.width, self.imgM.height, int(x * 0.1))
        self.imgM = self.imgM.resize((xMarshall, yMarshall))
        self.imgM = ImageTk.PhotoImage(self.imgM)
        self.MARSHALL_ID = self.jeu.create_image(int((x * 0.33)), pos_interieur, image=self.imgM, anchor="nw")

        #superposition du train

        self.ImageTrain = Image.open(os.path.join(os.path.dirname(__file__), 'train.png'))
        self.ImageTrain = self.ImageTrain.resize((x , y))
        self.ImageTrain = ImageTk.PhotoImage(self.ImageTrain)
        self.jeu.create_image(0 , 0, image=self.ImageTrain, anchor="nw")

        #nbe de butins de chaque wagon

        for i in range(4):
            self.wagons[i].label.place(x = 475 + i*300, y = int(y * 0.88))

       

        
    
    

    

class Bandit():
    def __init__(self, jeu, balles, nom):

        self.balles = balles
        self.nom = nom
        self.butin = [] #liste de Butin du bandit
        self.butinTotal = 0
        self.actions = []
        self.wagon = 3 
        self.pos = "toit" #prend en valeur soit 'interieur' soit 'toit'
        self.jeu = jeu
        self.id = None

    def action(self):
        action = self.actions.pop(0)
        if action == "gauche":
            self.bouger("gauche")
        elif action == "droite":
            self.bouger("droite")
        elif action == "haut":
            self.bouger("haut")
        elif action == "bas":
            self.bouger("bas")
        elif action == "tirer":
            self.tirer()
        elif action == "braquer":
            self.braquer()

    def actionRetour(self, action): #retour instantané après chaque clic
        action = self.actions.pop(0)
        if action == "gauche":
            self.jeu.textscr.insert(END, f"{self.nom} a décidé d'aller à gauche\n")
        elif action == "droite":
            self.jeu.textscr.insert(END, f"{self.nom} a décidé d'aller à droite\n")
        elif action == "haut":
            self.jeu.textscr.insert(END, f"{self.nom} a décidé d'aller en haut\n")
        elif action == "bas":
            self.jeu.textscr.insert(END, f"{self.nom} a décidé d'aller en bas\n")
        elif action == "tirer":
            self.jeu.textscr.insert(END, f"{self.nom} a décidé de tirer au wagon {self.wagon+1}\n")
        elif action == "braquer":
            self.jeu.textscr.insert(END, f"{self.nom} a décidé de braquer au wagon {self.wagon+1}\n")
        

    def bouger(self, action):

        if action == "gauche" and self.wagon != 0:
            self.jeu.jeu.move(self.id, -300, 0)
            self.wagon -= 1
            self.jeu.textscr.insert(END,f"{self.nom} est allée à {action}\n")
            
        elif action == "droite" and self.wagon != 3:
            self.jeu.jeu.move(self.id, 300, 0)
            self.wagon += 1
            self.jeu.textscr.insert(END,f"{self.nom} est allée à {action}\n")
        elif action == "haut" and self.pos == "interieur":
            self.jeu.jeu.move(self.id, 0, -205)
            self.pos = "toit"
            self.jeu.textscr.insert(END,f"{self.nom} est allée en {action}\n")
        elif action == "bas" and self.pos == "toit":
            self.jeu.jeu.move(self.id, 0, 205)
            self.pos = "interieur"
            self.jeu.textscr.insert(END,f"{self.nom} est allée en {action}\n")
        else:
            if action in ["gauche", "droite"]:
                self.jeu.textscr.insert(END,f"{self.nom} ne peut pas aller à {action}\n")
            elif action in ["bas", "haut"]:
                self.jeu.textscr.insert(END,f"{self.nom} ne peut pas aller en {action}\n")
        
        



    def tirer(self):
        if self.balles == 0:
            self.jeu.textscr.insert(END,f"{self.nom} n'a plus de balles.\n")
            return

        cibles = []
        for bandit in self.jeu.bandits:
            if self.wagon == bandit.wagon:
                if self.pos == bandit.pos:
                    if self.id != bandit.id:
                        cibles.append(bandit)
        if len(cibles) >= 1:
            cible = random.choice(cibles)
            self.jeu.textscr.insert(END,f"{self.nom} a tiré sur {cible.nom}\n")
            cible.lacherButin()
        else:
            self.jeu.textscr.insert(END,f"{self.nom} a tiré sur... personne.\n")
        self.balles -= 1
        




    def braquer(self):
        if self.pos == "toit":
            self.jeu.textscr.insert(END,f"{self.nom} ne peut pas récupérer de butin\n")
            return

        wagon = self.jeu.wagons[self.wagon]

        if len(wagon.listeButin) == 0:
            self.jeu.textscr.insert(END,f"{self.nom} n'a trouvé aucun butin.\n")
            return

        
        butinAcquis = wagon.listeButin.pop(random.randint(0, len(wagon.listeButin)-1))
        self.butin.append(butinAcquis)

        if butinAcquis.typ == "bourse":
            self.jeu.textscr.insert(END,f"{self.nom} a récupéré une {butinAcquis.typ} d'une valeur de {butinAcquis.valeur}$\n")
            
        else:
            self.jeu.textscr.insert(END,f"{self.nom} a récupéré un {butinAcquis.typ} d'une valeur de {butinAcquis.valeur}$\n")

        wagon.majButin()
        


    def lacherButin(self):

        if len(self.butin) == 0:
            return 

        butinPerdu = self.butin.pop(random.randint(0, len(self.butin)-1))
        wagon = self.jeu.wagons[self.wagon]
        wagon.listeButin.append(butinPerdu)
        wagon.majButin()
       
        if butinPerdu.typ == "bourse":
            self.jeu.textscr.insert(END,f"{self.nom} a lâché une {butinPerdu.typ} d'une valeur de {butinPerdu.valeur}$\n")
            
        else:
            self.jeu.textscr.insert(END,f"{self.nom} a lâché un {butinPerdu.typ} d'une valeur de {butinPerdu.valeur}$\n")


    def fuir(self):
        self.jeu.jeu.move(self.id, 0, -205)
        self.pos = "toit"
        self.jeu.textscr.insert(END,f"{self.nom} touchée par le Marshall, elle a fui !\n") 

    def dessinBandit(self, hauteur, x, y, i):

        self.img = Image.open((os.path.join(os.path.dirname(__file__), 'bandit'+ str(i) + '.png')))
        xBandit, yBandit = self.jeu.findWidth(self.img.width, self.img.height, hauteur)
        self.img = self.img.resize((xBandit , yBandit))
        self.img = ImageTk.PhotoImage(self.img)
        self.id = self.jeu.jeu.create_image(x, y, image=self.img, anchor="nw")

    def calculButin(self):
        self.butinTotal = 0
        for butin in self.butin:
                self.butinTotal += butin.valeur
        return self.butinTotal
    

class Butin():
    def __init__(self, typ):

        self.typ = typ
        self.valeur = None

        if typ == "magot":
            self.valeur = 1000
        elif typ == "bijou":
            self.valeur = 500
        elif typ == "bourse":
            self.valeur = random.choice([100, 200])

class Wagon():
    def __init__(self, jeu, x):
        self.x = x   #indice du wagon (0, 1, 2, 4)
        self.listeButin = []
        self.jeu = jeu
        if x == 0:
            self.listeButin.append(Butin("magot"))
        else:
            r = random.randint(1, 4)
            for i in range(r):
                self.listeButin.append(Butin(random.choice(["bijou", "bourse"])))
        self.label = Label(self.jeu.jeu, width=10, height= 4, font=('Consolas',10), bg="#0b3c5c", fg="#9db1cd")
        self.majButin()

    def majButin(self):
        bourse = False
        bijou = False
        self.label.config(text = f"{len(self.listeButin)}\n")
        for butin in self.listeButin:
            if butin.typ == "bijou":
                if bijou == True:
                    continue
                bijou = True
            if butin.typ == "bourse":
                if bourse == True:
                    continue
                bourse = True
            self.label['text'] += butin.typ + "\n"
            



    
mon_jeu = Jeu()

mon_jeu.mainloop()