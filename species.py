#ordera genesen från början så slipper du göra det flera gånger
import random
class species():
    def __init__(self,best):
        self.best = best #Den bästa individen i artens genome
        self.individer = [best]
        self.averageFit = None
        self.dropOff = 0 #
    def averageFitness(self): #Dividebyzero
        totalfitness = 0
        for individ in self.individer:
            totalfitness += individ.fitness
        self.averageFit = totalfitness/(len(self.individer))
    
    def sorteraArt(self): #Sorterar arten där högst fitness är först/ ökar också dropOff
        oldBest = self.best 
        sorted_species = sorted(self.individer, key=lambda x: x.fitness).reverse()        
        if sorted_species[0].fitness > self.best.fitness:
            self.best = sorted_species[0]
            if self.best.fitness <= oldBest.fitness:
                self.dropOff += 1
        self.individer = sorted_species
                
        
            
    def orderGenes(self, genes): #ger ordningen av generna där lägst innovationnumber går först, Gör till class variable
        sorted_genes = sorted(genes, key=lambda x: x.innovationnumber)
        return sorted_genes
    
    def createArray(self, genes, n):
        #geneDict = {}
        #for connection in genes:
        #    nr = connection.innovationnumber
        #    geneDict[str(id)] = True
        #Nu bör genes redan från början vara en dictionary?
        array = []
        for i in range(0, n+1):#Ska det vara n+1?
            if genes[i]:
                array.append[1]
            else:
                array.append[0]
        return array
    #Engligt pappret ska du få alla disjoin genes totalt. Varesig de är från genome 1 eller 2.
    #Rent tekniskt så ifall du vet antalet excess genes borde du ganska lätt kunna räkna ut antalet disjoint genes
    #Code bullet satte coeffcienten för disjoint och excess som samma.
    #Vad ifall du gör de två generna till en matris. Där raderna är genome1 och 2 och kolumner representerar en gene. Om en kolumn är 0 1 så betyder det att det är en disjoint.
    #Sen måste du lösa
    #utgå från att genes är sorterade
    def findDisjoinGenes(self, genes1, genes2): 
        #vad ifall dem inte har några gener
        tgenes1 = self.orderGenes(genes1.values())
        tgenes2 = self.orderGenes(genes1.values())
        highest = 0
        lower = 0
        if tgenes1[-1].innovationnumber >= genes2[-1].innovationnumber:
            #detta ger inte lower eftersom du kommer ha dem i array
            highest = tgenes1[-1].innovationnumber
            lower = tgenes2[-1].innovationnumber
        else:
            highest = tgenes2[-1].innovationnumber
            lower = tgenes1[-1].innovationnumber
        #Anta att du har två arrays
        genes1 = self.createArray(genes1, highest)
        genes2 = self.createArray(genes2, highest)
        disjoint = 0
        excess = 0
        excessState = False
        for i in range(0,highest+ 1): #Ska det vara +1?
            if genes1[i] != genes2[i]:
                if excessState:
                    excess += 1
                    continue
                else:
                    disjoint += 1
            if i == lower: 
                excessState = True
        return disjoint, excess

#Lär finnas något mycket bättre sätt

    def weightDifference(self, genes1, genes2):
        count = 0
        total = 0
        tgenes1 = self.orderGenes(genes1.values())
        tgenes2 = self.orderGenes(genes1.values())
        lower = 0
        if tgenes1[-1].innovationnumber >= tgenes2[-1].innovationnumber:
            #detta ger inte lower eftersom du kommer ha dem i array
            lower = tgenes2[-1].innovationnumber
        else:
            lower = tgenes1[-1].innovationnumber
        #Anta att du har två arrays
        genes1 = self.createArray(genes1, lower)
        genes2 = self.createArray(genes2, lower)
        for i in range(0, lower + 1):
            if genes1[i] == genes2[i] and genes1[i] != 0:
                count += 1
                diff = abs(genes1[i] - genes2[i])
                total += diff
        if count == 0: #Vad ska det bli om inga matchar? divide by zero
            return None
        return total/count

    #Kollar ifall genome är kompatibel till den arten
    def isCompatiable(self, testGenome):
        sGenome = self.best
        threshold = None #Sök upp
        disjoint, excess = self.findDisjoinGenes(sGenome, testGenome)
        weightDiff = self.weightDifference(sGenome, testGenome) #Spelar ordningen roll?
        disjointCoefficent = 1
        excessCoefficent = 1
        weightDiffCoefficent = 1
        factorN = None #the factor N, the number of genes in the larger genome, normalizes for genome size (N can be set to 1 if both genomes are small, i.e., consist of fewer than 20 genes). 
        Delta = ((excessCoefficent * excess)/factorN) + ((disjointCoefficent * disjoint)/factorN) + weightDiffCoefficent * weightDiff #Formel för att veta combatiblity från stanley papper
        return Delta < threshold #DET SKA VARA Self.THRESHOLD ELLER NGT HÄR
    
    def tworandomIndivids(self):
        return random.choice(self.individer, k=2)

    def createChild(self, history):
        #Genome1 ska ha högre eller lika med fitness med genome2
        #KODEN UNDER ANVÄNDS FLERA GÅNGER OCH GÅR ANTAGLIGEN ATT GÖRA OM TILL EN FUNKTION
        genome1, genome2 = self.tworandomIndivids()
        genome1 = genome1.brain
        genome2 = genome2.brain
        genes1 = self.orderGenes(genome1.connections)
        genes2 = self.orderGenes(genome2.connections)
        highest = 0
        if genes1[-1].innovationnumber >= genes2[-1].innovationnumber:
            #detta ger inte lower eftersom du kommer ha dem i array
            highest = genes1[-1].innovationnumber
        else:
            highest = genes2[-1].innovationnumber
        #Anta att du har två arrays
        genes1 = self.createArray(genes1, highest)
        genes2 = self.createArray(genes2, highest)
        babyGenes = {}
        for innonr, connection in genes1.items():
            #Ska du bara ta random vikt från föräldrer om det matchar?
            if genes2[innonr] != None: #Betyder att det matchar
                randomnr = random.choice([0, 1])
                #ta randomly någons vikt.
                if randomnr == 0:
                    #ta från genome1
                    babyGenes[innonr] = connection
                else:
                    babyGenes[innonr] = genes2[innonr]
            else:
                #Behåll alla genes från genome1
                babyGenes[innonr] = connection
            #Alla nodes från genome1 ges bara till barnet
            babyGenome = genome()
            babyGenome.connections = babyGenes
            babyGenome.nodes = genome1.nodes
            baby = player(babyGenome)
            return baby

    def sharedFitness(self): #Förstår inte riktigt men tror detta gör att inte en art tar över hela populationen
        try:
            self.individer = [element.fitness/len(self.individer) for element in self.individer]
        except Exception  as e: #divide by zero error
            print(e)
            return

    def killHalf(self): #Dödar den sämre halvan av arten. Leta efter ett mer systematiskt sätt att döda av arten
        #https://stackoverflow.com/questions/15715912/remove-the-last-n-elements-of-a-list
        #https://stackoverflow.com/questions/50451570/how-to-divide-a-list-and-delete-half-of-it-in-python
        #Arten måste vara sorterad först
        self.individer = self.individer[:len(list)//2]

    