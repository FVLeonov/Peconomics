from dataclasses import dataclass
from Model.parameters import Occupation
from Model.parameters import DataBase
from Model.resources import resources


@dataclass
class Demand:
    need: int
    filled: int


@dataclass
class Demands:  # потребность
    fullness: Demand
    comfort: Demand
    entertainment: Demand
    prestige: Demand


@dataclass
class Agent:
    name: str
    demands = Demands(Demand(1, 0), Demand(1, 0), Demand(1, 0), Demand(1, 0))
    occupation: Occupation
    socialPoints = 0
    cash: float
    store = {}
    
    # буферные данные
    
    recivedCash = 0
    possiblePriorResources = []
    priorResource = None
    
    def consume(self):
        # берет ресурс, который задан аргументом, и убирает со склада в количестве 1 и удовлетворяет свои потребности
        # в количестве определеяемом типом ресурса
        self.demands.fullness.filled += self.priorResource.replenish.fullness
        self.demands.comfort.filled += self.priorResource.replenish.comfort
        self.demands.entertainment.filled += self.priorResource.replenish.entertainment
        self.demands.prestige.filled += self.priorResource.replenish.prestige
        
        self.addRes(self.priorResource, -1)
    
    def produce(self):
        # из occupation берет производимый ресрс и его количество производимое за единицу времени (производительность)
        # и добавляет произведенный ресурс к себе на склад
        
        resource = self.occupation.resource
        
        self.addRes(resource, self.occupation.productivity)
    
    def addRes(self, res, amount):
        
        if res in self.store.keys():
            self.store[res] += amount
        
        else:
            self.store[res] = amount
            
        if self.store[self.priorResource] <= 0:
            del self.store[self.priorResource]
    
    def buy(self, seller, res_price):
        
        self.cash -= res_price
        seller.recivedCash += res_price
        
        self.addRes(self.priorResource, 1)
        seller.addres(self.priorResource, -1)
    
    def update(self, db: DataBase):

        self.possiblePriorResources = resources
        self.cash += self.recivedCash
        
        self.occupation.productivity = db.baseProductivity[self.occupation.name]
        
        self.produce()
        
        self.socialPoints = db.socialPointsCoeff * (self.demands.prestige.filled / self.demands.prestige.need)
