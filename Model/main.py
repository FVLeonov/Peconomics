from Model.agent import Agent, Demands, Demand
from Model.parameters import DataBase, occupations
from Model.world import World

if __name__ == '__main__':

    demands = Demands(Demand(2, 0), Demand(2, 0), Demand(2, 0), Demand(2, 0))

    agents = [
        Agent(name="Bazil", occupation=occupations['CropFarmer'], cash=100.0,demands=Demands(Demand(2, 0), Demand(2, 0), Demand(2, 0), Demand(2, 0))),
        Agent(name="Vladimir", occupation=occupations['Sericulturist'], cash=100.0, demands=Demands(Demand(2, 0), Demand(2, 0), Demand(2, 0), Demand(2, 0))),
        Agent(name="Oleg", occupation=occupations['SheepFarmer'], cash=100.0, demands=Demands(Demand(2, 0), Demand(2, 0), Demand(2, 0), Demand(2, 0))),
        Agent(name="Kuz'ma", occupation=occupations['Brewer'], cash=100.0, demands=Demands(Demand(2, 0), Demand(2, 0), Demand(2, 0), Demand(2, 0))),
        Agent(name="Igor", occupation=occupations['Dyer'], cash=100.0, demands=Demands(Demand(2, 0), Demand(2, 0), Demand(2, 0), Demand(2, 0)))
    ]
    
    initial_prices = {"Grain": 50,
                      "Wool": 50,
                      "Beer": 50,
                      "Dyes": 50,
                      "Silk": 50

        
                      }
    
    database = DataBase(
        baseProductivity=
        {
            "CropFarmer": 5,
            "SheepFarmer": 2,
            "Brewer": 2,
            "Dyer": 2,
            "Sericulturist": 2
        },
        socialPointsCoeff=1,
        priceGrowCoeff=0.1
    )
    world = World(agentsList=agents, myData=database, prices=initial_prices)
    x = 0
    while x < 100:
        x += 1
        world.run()
