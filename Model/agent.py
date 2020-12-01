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
    demands: Demands
    occupation: Occupation
    cash: float
    store: Dict[str, float] = field(default_factory=lambda: {})

    socialPoints: float = 0
    # буферные данные

    recivedCash: float = 0.0
    possiblePriorResources: List[str] = field(default_factory=lambda: [])
    priorResourceName: str = None

    def consume(self):
        # берет ресурс и убирает со склада в количестве 1 и удовлетворяет свои потребности в количестве
        # определеяемом типом ресурса
        resource = resourcesDict[self.priorResourceName]
        if self.demands.fullness.filled < self.demands.fullness.need:
            self.demands.fullness.filled += resource.replenish.fullness
        if self.demands.comfort.filled < self.demands.comfort.need:
            self.demands.comfort.filled += resource.replenish.comfort
        if self.demands.entertainment.filled < self.demands.entertainment.need:
            self.demands.entertainment.filled += resource.replenish.entertainment
        if self.demands.prestige.filled < self.demands.prestige.need:
            self.demands.prestige.filled += resource.replenish.prestige

        self.add_res(self.priorResourceName, -1)

    def produce(self):
        # из occupation берет производимый ресрс и его количество производимое за единицу времени (производительность)
        # и добавляет произведенный ресурс к себе на склад

        resource = self.occupation.resource

        self.add_res(resource.name, self.occupation.productivity)

    def add_res(self, res_name, amount):

        if res_name in self.store.keys():
            self.store[res_name] += amount

        else:
            self.store[res_name] = amount

        if self.priorResourceName and self.priorResourceName in self.store.keys() and self.store[self.priorResourceName] <= 0:
            del self.store[self.priorResourceName]

    def buy(self, seller, res_prices):

        self.cash -= res_prices[self.priorResourceName]
        seller.recivedCash += res_prices[self.priorResourceName]

        self.add_res(self.priorResourceName, 1)
        seller.add_res(self.priorResourceName, -1)

    def calc_demands(self):

        for d in [self.demands.fullness, self.demands.comfort, self.demands.entertainment, self.demands.prestige]:
            d.filled = 0
            d.need = 1

    def update(self, db: DataBase):

        self.possiblePriorResources = list(resources)
        self.cash += self.recivedCash
        self.recivedCash = 0

        self.occupation.productivity = db.baseProductivity[self.occupation.name]

        self.socialPoints = db.socialPointsCoeff * (self.demands.prestige.filled / self.demands.prestige.need)

        self.calc_demands()
        self.produce()


