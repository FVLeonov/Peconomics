from Model.agent import Agent, Demands, Demand
from Model.parameters import database, occupations, initial_prices
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
    
    world = World(agentsList=agents, myData=database, prices=initial_prices)
    x = 0
    while x < 100:
        x += 1
        world.run()
