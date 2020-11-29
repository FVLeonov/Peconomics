from dataclasses import dataclass

from Model.resources import Resource, resources
from typing import Dict


@dataclass
class Occupation:
    name: str
    resource: Resource
    productivity: float
    socialLevel: int


resources = {o.name: o for o in resources}

occupations = [
    Occupation(name="CropFarmer", resource=resources["Grain"], productivity=0.0, socialLevel=1),
    Occupation(name="CattleFarmer", resource=resources["Cheese"], productivity=0.0, socialLevel=1),
    Occupation(name="SheepFarmer", resource=resources["Wool"], productivity=0.0, socialLevel=1),
    Occupation(name="Salter", resource=resources["Salt"], productivity=0.0, socialLevel=2),
    Occupation(name="Hunter", resource=resources["Furs"], productivity=0.0, socialLevel=2),
    Occupation(name="Brewer", resource=resources["Beer"], productivity=0.0, socialLevel=2),
    Occupation(name="Sericulturist", resource=resources["Silk"], productivity=0.0, socialLevel=3),
    Occupation(name="Dyer", resource=resources["Dyes"], productivity=0.0, socialLevel=3)
]

occupations = {o.name: o for o in occupations}


@dataclass
class DataBase:
    # базовая продуктивность разных родов деятельности
    baseProductivity: Dict
    socialPointsCoeff: float
    priceGrowCoeff: float
#    cropFarmerBaseProductivity: float
#    cattleFarmerBaseProductivity: float
#    sheepFarmerBaseProductivity: float
#    hunterBaseProductivity: float
#    brewerBaseProductivity: float
#    sericulturistBaseProductivity: float
#    salterBaseProductivity: float
#    dyerBaseProductivity: float
