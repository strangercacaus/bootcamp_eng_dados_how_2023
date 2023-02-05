# Este script gera um feed de eventos aleatórios conforme os parâmetros da função:

from fake_web_events import Simulation
import json

simulation = Simulation(user_pool_size=100, sessions_per_day=10000)
events = simulation.run(duration_seconds=5)

for event in events:
    print(json.dumps(event, indent=4))