from dataclasses import dataclass, field
from typing import List, Dict
from Model.parameters import Occupation
from Model.parameters import DataBase
from Model.resources import resources, resourcesDict


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
    cash: float
    store: Dict[str, float] = field(default_factory=lambda: {})

    socialPoints: int = 0
    # буферные данные
    
    recivedCash: float = 0.0
    possiblePriorResources: List[str] = field(default_factory=lambda: [])
    priorResourceName: str = None
    

    def consume(self):
        # берет ресурс, который задан аргументом, и убирает со склада в количестве 1 и удовлетворяет свои потребности
        # в количестве определеяемом типом ресурса
        priorityResource = resourcesDict[self.priorResourceName]
        self.demands.fullness.filled += priorityResource.replenish.fullness
        self.demands.comfort.filled += priorityResource.replenish.comfort
        self.demands.entertainment.filled += priorityResource.replenish.entertainment
        self.demands.prestige.filled += priorityResource.replenish.prestige
        
        self.addRes(self.priorResourceName, -1)
    
    def produce(self):
        # из occupation берет производимый ресрс и его количество производимое за единицу времени (производительность)
        # и добавляет произведенный ресурс к себе на склад
        
        resource = self.occupation.resource
        
        self.addRes(resource.name, self.occupation.productivity)
    
    def addRes(self, resName, amount):
        
        if resName in self.store.keys():
            self.store[resName] += amount
        
        else:
            self.store[resName] = amount
            
        if self.priorResourceName and self.priorResourceName in self.store.keys() and  self.store[self.priorResourceName] <= 0:
            del self.store[self.priorResourceName]
    
    def buy(self, seller, res_price):
        
        self.cash -= res_price
        seller.recivedCash += res_price
        
        self.addRes(self.priorResourceName, 1)
        seller.addres(self.priorResourceName, -1)
    
    def update(self, db: DataBase):

        self.possiblePriorResources = resources
        self.cash += self.recivedCash
        
        self.occupation.productivity = db.baseProductivity[self.occupation.name]
        
        self.produce()
        
        self.socialPoints = db.socialPointsCoeff * (self.demands.prestige.filled / self.demands.prestige.need)
