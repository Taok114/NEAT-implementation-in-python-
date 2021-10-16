#Hur många barn varje art ska ha fit (average fittness)/(average fitnessum (när det gäller alla arter)) * population size
import math
from species import species
from history import connectionhistory
from genome import genome
from player import player

class population():
    def __init__(self):
        self.species = []
        self.innoHistory = connectionhistory()
        self.players = []
        self.size = 50
    #Du behövder egentligen bara göra all evolution och sånt efter population i den nurvarande generationen har dött
    #Dela upp spelarna i art
    
    def putInSpecies(self):
        #ta bort alla individer i arten
        #Best kommer inte försvinna för den är en enskild variabel
        for art in self.species:
            self.individer = []
        #Gå igenom varje player och kolla om de är kompatibel med någon av arterna annars blir det en ny art
        for player in self.players:
            for art in self.species:
                if art.isCompatiable(player.brain):
                    art.individer.append(player)
                    break #Går till nästa player?
            #Ifall den kommer hit är den inte kompatibel med någon art så en ny måste skapas
            nyArt = species(player)
            self.species.append(nyArt)
            
    
    def sortSpecies(self): #Sorts species by fitness
        self.species = sorted(self.species, key=lambda x: (x.averageFit), reverse=True)

    def killHalfSpecies(self):
        for art in self.species:#T
            art.killHalf()
            art.sharedFitness() #Ska man göra detta förre eller efter man dödat av hälften?
            art.averageFitness()

    def averageFitnessSumma(self):
        sum = 0
        for art in self.species:
            sum += art.averageFit
        return sum
    
    def tommaSpecies(self):
        self.species = [x for x in self.species if not (len(x.individer) == 0)]

    def killDroppedOffSpecies(self):
        self.species = [x for x in self.species if not (x.dropOff == 15)]

    def killBadSpecies(self):
        sum = self.averageFitnessSumma()
        self.species = [x for x in self.species if not (x.averageFit/sum * self.size < 1)]

    def fitnessCalculation(self): #Göra fitnessharing här istället? Nej för då blir det anorlunda för antalet indivder här är större än vad det är senare
        #Räknar ut fitness från varje player
        #Nu ligger playersarna i arter så ugå inte från self.players
        for art in self.species:
            for individ in art.individer:
                individ.fitness = 1 + len(individ.brain.connections) * 100
            art.sorteraArt

    def nextGeneration(self):
        self.putInSpecies()
        self.fitnessCalculation()
        self.killHalfSpecies()
        self.tommaSpecies()
        self.killDroppedOffSpecies()
        self.killBadSpecies()
        self.sortSpecies()
        barn = []
        averageSum = self.averageFitnessSumma()
        for art in self.species: #Du behöver ge innovationhistory
            barn.append(art.best)
            amountOfChildren = math.floor(art.averageFit/averageSum * self.size - 1) #mängden barn den arten får -1 för den bästa redan är i arten
            print(amountOfChildren)
            j = 0
            for i in range(0, amountOfChildren): #Inte plus 1 för 0 är 0 lmao
                barn.append(art.createChild(self.innoHistory))
        if len(barn) != self.size: #ifall det finns mer platser så ge mer barn till den bästa arten
            bestArt = self.species[0]
            antal = self.size - len(barn)
            for i in range(0,antal):
                barn.append(bestArt.createChild(self.innoHistory))
        self.individer = barn

    def startPopulation(self):
        startBrain = genome()
        startPlayer = player(startBrain)
        startPlayer.brain.initalizeNetwork()
        self.players.append(startPlayer)
        self.nextGeneration()