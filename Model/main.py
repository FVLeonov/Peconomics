from Model.agent import Agent
from Model.parameters import DataBase, occupations
from Model.world import World

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
