from dataclasses import dataclass


@dataclass
class Replenish:
    fullness: int
    comfort: int
    entertainment: int
    prestige: int


@dataclass
class Resource:
    name: str
    replenish: Replenish


resources = [Resource(name="Grain", replenish=Replenish(1, 0, 0, 0)),
             Resource(name="Cheese", replenish=Replenish(1, 0, 0, 0)),
             Resource(name="Wool", replenish=Replenish(0, 1, 0, 0)),
             Resource(name="Furs", replenish=Replenish(0, 1, 0, 1)),
             Resource(name="Beer", replenish=Replenish(1, 0, 1, 0)),
             Resource(name="Silk", replenish=Replenish(0, 1, 0, 1)),
             Resource(name="Salt", replenish=Replenish(0, 0, 1, 1)),
             Resource(name="Dyes", replenish=Replenish(0, 0, 1, 1)),
             ]

resourcesDict = {r.name: r for r in resources}


