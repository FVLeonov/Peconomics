from dataclasses import dataclass
from time import sleep
from typing import List, Dict

from Model.agent import Agent
from Model.parameters import DataBase


@dataclass
class World:
    agentsList: List[Agent]
    myData: DataBase
    prices: Dict[str, float]

    def nextStep(self):
        supply_and_demand = {"Grain": [1, 1],
                             "Wool": [1, 1],
                             "Beer": [1, 1],
                             "Dyes": [1, 1],
                             "Silk": [1, 1]
                             }

        # фаза обновления агентов

        for a in self.agentsList:
            a.update(self.myData)

        # подсчет предложения

        for a in self.agentsList:
            for r in a.store.keys():
                supply_and_demand[r][0] += a.store[r]

        # фаза тоговли и потребления

        trade_phase_list = list(self.agentsList)
        while True:
            trade_cycle_list = list(trade_phase_list)
            if not trade_phase_list:
                break
            while True:

                # фаза вычисления приоритетного ресурса

                for a in list(trade_cycle_list):
                    top_res = None
                    top_priority = 0

                    for r in list(a.possiblePriorResources):
                        priority = \
                            (10 * (1 - a.demands.fullness.filled / a.demands.fullness.need) * r.replenish.fullness +
                             6 * (1 - a.demands.comfort.filled / a.demands.comfort.need) * r.replenish.comfort +
                             3 * (1 - a.demands.entertainment.filled / a.demands.entertainment.need) * r.replenish.entertainment +
                             2 * (1 - a.demands.prestige.filled / a.demands.prestige.need) * r.replenish.prestige) / self.prices[r.name]

                        if a.cash < self.prices[r.name]:
                            priority = 0

                        if priority <= 0:
                            a.possiblePriorResources.remove(r)

                        elif priority > top_priority:
                            top_res = r
                            top_priority = priority

                    if top_priority > 0:
                        a.priorResourceName = top_res.name
                        supply_and_demand[top_res.name][1] += 1
                        a.possiblePriorResources.remove(top_res)

                    else:
                        trade_phase_list.remove(a)
                        trade_cycle_list.remove(a)

                # фаза поиска ресурса в хранилище и его потребление (если есть в хранилище)

                for a in list(trade_cycle_list):
                    if a.priorResourceName in a.store:
                        a.consume()
                        trade_cycle_list.remove(a)

                # фаза поиска ресурса на рынке и его потребление (если был куплен)

                trade_cycle_list.sort(key=lambda x: x.cash)

                for a in list(trade_cycle_list):
                    agents_with_resource_list = [x for x in self.agentsList if a.priorResourceName in x.store]
                    agents_with_resource_list.sort(key=lambda x: x.store[a.priorResourceName])
                    if agents_with_resource_list:
                        a.buy(agents_with_resource_list[0], self.prices)
                        a.consume()
                        trade_cycle_list.remove(a)

                if not trade_cycle_list:
                    break

        # фаза обновления цен
        for r in self.prices:
            self.prices[r] += round(self.prices[r] * (2 * supply_and_demand[r][1] / (supply_and_demand[r][0] + supply_and_demand[r][1]) - 1) * self.myData.priceGrowCoeff)
            print(r, self.prices[r])

    def run(self):
        self.nextStep()
        sleep(1.0)
