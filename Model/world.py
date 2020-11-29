from dataclasses import dataclass
from time import sleep
from typing import List
from typing import Dict

from Model.agent import Agent
from Model.parameters import DataBase, occupations


@dataclass
class World:
    agentsList: List[Agent]
    myData: DataBase
    prices: Dict

    def nextStep(self):
        supply_and_demand = {"Grain": [1, 1],
                             "Cheese": [1, 1],
                             "Wool": [1, 1],
                             "Furs": [1, 1],
                             "Beer": [1, 1],
                             "Silk": [1, 1],
                             "Salt": [1, 1],
                             "Dyes": [1, 1]
                             }

        for a in self.agentsList:
            for r in a.store:
                supply_and_demand += a.store[r]

        # фаза обновления агентов

        for a in self.agentsList:
            a.update(self.myData)

        # фаза тоговли и потребления
        trade_phase_list = self.agentsList
        while True:
            trade_cycle_list = trade_phase_list
            if not trade_phase_list:
                break
            while True:

                # фаза вычисления приоритетного ресурса

                for a in trade_cycle_list:
                    top_res = None
                    top_priority = 0

                    for r in a.possiblePriorResources:
                        priority = \
                            (10 * (1 - a.demands.fullness.filled / a.demands.fullness.need) * r.replenish.fullness +
                             6 * (1 - a.demands.comfort.filled / a.demands.comfort.need) * r.replenish.comfort +
                             3 * (1 - a.demands.entertainment.filled / a.demands.entertainment.need) * r.replenish.entertainment +
                             2 * (1 - a.demands.prestige.filled / a.demands.prestige.need) * r.replenish.prestige) / \
                            self.prices[r.name]

                        if priority > top_priority:
                            top_res = r
                            top_priority = priority

                        if priority <= 0:
                            a.possiblePriorResources.remove(r)

                    if top_priority > 0:
                        a.priorResource = top_res
                        supply_and_demand[top_res.name][1] += 1
                        a.possiblePriorResources.remove(top_res)

                    else:
                        trade_phase_list.remove(a)

                # фаза поиска ресурса в хранилище и его потребление (если есть в хранилище)

                for a in trade_cycle_list:
                    if a.priorResource in a.store:
                        a.consume()
                        trade_cycle_list.remove(a)

                # фаза поиска ресурса на рынке и его потребление (если был куплен)

                trade_cycle_list.sort(key=lambda x: x.cash)

                for a in trade_cycle_list:
                    if a.cash < self.prices[a.priorResource.name]:
                        a.possiblePriorResources.remove(a.priorResource)
                        break
                    else:
                        agents_with_resource_list = [x for x in trade_cycle_list if a.priorResource in x.store]
                        agents_with_resource_list.sort(key=lambda x: x.store[a.priorResource])
                        a.buy(agents_with_resource_list[0], self.prices)
                        a.consume()
                        trade_cycle_list.remove(a)

                if not trade_cycle_list:
                    break

        # фаза обновления цен
        for r in self.prices:
            self.prices[r] += self.myData.priceGrowCoeff * (2 * (supply_and_demand[r][0] / supply_and_demand[r][1]) - 1)

    def run(self):
        self.nextStep()
        sleep(1.0)


if __name__ == '__main__':
    agents = [
        Agent(name="Ivan", occupation=occupations['CropFarmer'], cash=10.0)
    ]

    initial_prices = {"Grain": 1,
                      "Cheese": 1,
                      "Wool": 1,
                      "Furs": 1,
                      "Beer": 1,
                      "Silk": 1,
                      "Salt": 1,
                      "Dyes": 1

                      }

    database = DataBase(
        baseProductivity=
        {
            "CropFarmer": 4,
            "CattleFarmer": 3,
            "SheepFarmer": 5,
            "Hunter": 3,
            "Brewer": 5,
            "Sericulturist": 3,
            "Salter": 4,
            "Dyer": 3
        },
        socialPointsCoeff=1,
        priceGrowCoeff=1
    )
    world = World(agentsList=agents, myData=database, prices=initial_prices)
    world.run()
