import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Configurações iniciais do modelo
def simulate_seir(num_individuals=200, infection_radius=0.35, initial_infected=1, initial_exposed=0,
                  infection_rate=0.2, exposure_rate=0.2, recovery_rate=0.04, incubation_period=21, social_distancing=False,
                  distancing_percentage=0.5, distancing_threshold=15, frames=200):
    def create_individuals(n, infected, exposed, distancing=False, distancing_percentage=0.0, incubation_period=10):
        individuals = []
        for i in range(n):
            state = "S"
            if infected > 0:
                state = "I"
                infected -= 1
            elif exposed > 0:
                state = "E"
                exposed -= 1
            individual = {"x": random.uniform(0, 5),
                          "y": random.uniform(0, 5),
                          "incubation_timer": incubation_period if state == "E" else 0,
                          "social_distancing_active": False,
                          "state": state,
                          "next_state": state}
            individuals.append(individual)
        return individuals

    individuals = create_individuals(num_individuals, initial_infected, initial_exposed, social_distancing, distancing_percentage, incubation_period)

    # Configurações para a animação
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    colors = {"S": "blue", "E": "yellow", "I": "red", "R": "green"}

    states_history = {"S": [num_individuals - initial_infected - initial_exposed], "E": [initial_exposed], "I": [initial_infected], "R": [0]}

    # Atualização da simulação
    # Seleciona os indivíduos que seguirão o distanciamento social quando o limite de infecções for atingido
    num_distancing = int(distancing_percentage * len(individuals))
    distancing_individuals = random.sample(individuals, num_distancing)
    for individual in distancing_individuals:
        individual['social_distancing_active'] = False

    def update(frame):
        # Atualiza a posição dos indivíduos
        for individual in individuals:
            if social_distancing and individual['social_distancing_active']:
                # Movimento aleatório reduzido para indivíduos em distanciamento social
                movement_factor = 0.03
                individual["x"] = max(0, min(5, individual["x"] + random.uniform(-movement_factor, movement_factor)))
                individual["y"] = max(0, min(5, individual["y"] + random.uniform(-movement_factor, movement_factor)))
            else:
                # Movimento aleatório reduzido para indivíduos em distanciamento social
                movement_factor = 0.05 if individual['social_distancing_active'] else 0.25
                individual["x"] = max(0, min(5, individual["x"] + random.uniform(-movement_factor, movement_factor)))
                individual["y"] = max(0, min(5, individual["y"] + random.uniform(-movement_factor, movement_factor)))

        # Avalia interações de infecção
        for i, individual in enumerate(individuals):
            if individual["state"] == "I":
                for other in individuals:
                    if other["state"] == "S":
                        distance = np.sqrt((individual["x"] - other["x"])**2 + (individual["y"] - other["y"])**2)
                        if distance < infection_radius and random.uniform(0, 1) < infection_rate:
                            other["next_state"] = "E"
                            other["incubation_timer"]=incubation_period

        # Avalia transição de estados
        for individual in individuals:
            if individual["state"] == "E":
                if individual["incubation_timer"] > 0:
                    individual["incubation_timer"] -= 1
                elif individual["incubation_timer"] == 0:
                    individual["next_state"] = "I"
                    individual["next_state"] = "I"
            elif individual["state"] == "I":
                if random.uniform(0, 1) < recovery_rate:
                    individual["next_state"] = "R"

        # Atualiza estados
        for individual in individuals:
            individual["state"] = individual["next_state"]

        # Atualiza o histórico dos estados
        counts = {"S": 0, "E": 0, "I": 0, "R": 0}
        for individual in individuals:
            counts[individual["state"]] += 1

        # Ativa distanciamento social após n infecções
        if counts["I"] >= distancing_threshold:
            for individual in distancing_individuals:
                individual['social_distancing_active'] = True

        for state in states_history:
            states_history[state].append(counts[state])

        # Limpa e redesenha o gráfico
        ax1.clear()
        for individual in individuals:
            ax1.plot(individual["x"], individual["y"], "o", color=colors[individual["state"]])
        ax1.set_xlim(0, 5)
        ax1.set_ylim(0, 5)
        ax1.set_title("Simulação do Modelo SEIR")

        # Atualiza o gráfico de área
        ax2.clear()
        ax2.stackplot(range(len(states_history["S"])),
                      states_history["I"],
                      states_history["E"],
                      states_history["S"],
                      states_history["R"],
                      labels=["Infectados", "Expostos", "Suscetíveis", "Recuperados"],
                      colors=["red", "yellow", "blue", "green"],
                      baseline='zero')
        ax2.legend(loc="upper right")
        ax2.set_title("Evolução dos Estados SEIR")
        ax2.set_ylim(0, num_individuals)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=100, repeat=False)
    plt.show()

N=100
# Exemplo de chamada da função
simulate_seir(social_distancing=True ,num_individuals=N,distancing_threshold=100*0.15, distancing_percentage=1.0,frames=700)
