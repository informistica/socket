class Pagella:
  
  def __init__(self, nome):
    self.nome = nome
    self.pagella = []
    #Adattamento
    self.materie = []

  
  def populate(self):
    self.pagella.append(("ITALIANO",8,5))
    self.pagella.append(("STORIA",8,4))
    self.pagella.append(("MATEMATICA",10,3))
    self.pagella.append(("LINGUA INGLESE",9,0))
    self.pagella.append(("TELECOMUNICAZIONI",10,7))
    self.pagella.append(("INFORMATICA",5,0))
    self.pagella.append(("SISTEMI E RETI",5,0))
    self.pagella.append(("TECN. PROG. SIST. I.",4,0))
    self.pagella.append(("SCIENZE MOTORIE E SP",6,0))

  def show(self):
    print(f"{self.nome}")
    for i in range(len(self.pagella)):
      print(self.pagella[i])
    print("---")

  def totAssenze(self):
    totAssenze = 0
    for i in range(len(self.pagella)):
      if self.pagella[i][2] != 0:
        totAssenze += self.pagella[i][2]
    return totAssenze

  def insufficienze(self):
    tot = 0
    for i in range(len(self.pagella)):
      if self.pagella[i][1] <= 5:
        tot += 1
    return tot

  def media(self):
    tot = 0
    for i in range(len(self.pagella)):
        tot += self.pagella[i][1]
    return tot/len(self.pagella)
    

  def maxAndMin(self):
    max = 0
    min = 11
    for i in range(len(self.pagella)):
      if(self.pagella[i][1] > max):
        max = self.pagella[i][1]
      if(self.pagella[i][1] < min):
        min = self.pagella[i][1]
    return {"minimo": min, "massimo" : max}
  
  def aggiungiMateria(self, dati):
    self.materie.append(dati[1])
    self.pagella.append(dati)


class Tabellone:
  def __init__(self):
    self.pagelle = []

  def push(self,pagella):
    self.pagelle.append(pagella)

  def pop(self, nome):
    index = self.cercaPagella(nome)
    if index != -1:
      self.pagelle.pop(index)
    else:
      print("Nome non presente")

  def cercaPagella(self,nome):
    for i in range(len(self.pagelle)):
      if(self.pagelle[i].nome == nome):
        return i
    return -1

  def __repr__(self):
    stringTabellone = ""
    for i in range(len(self.pagelle)):
      stringTabellone += self.pagelle[i].nome + "\n"
      for j in range(len(self.pagelle[i].pagella)):
        stringTabellone += str(self.pagelle[i].pagella[j]) + ""
        stringTabellone += "\n"
    return stringTabellone
  

