from dataclasses import dataclass


@dataclass
class Replenish:
    fullness: float
    comfort: float
    entertainment: float
    prestige: float


@dataclass
class Resource:
    name: str
    replenish: Replenish


resources = [Resource(name="Grain", replenish=Replenish(1, 0, 0, 0)),
             Resource(name="Wool", replenish=Replenish(0, 1, 0, 0)),
             Resource(name="Beer", replenish=Replenish(1, 0, 1, 0)),
             Resource(name="Dyes", replenish=Replenish(0, 0, 1, 1)),
             Resource(name="Silk", replenish=Replenish(0, 1, 0, 1))
             ]

resourcesDict = {r.name: r for r in resources}
