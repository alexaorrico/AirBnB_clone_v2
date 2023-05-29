import numpy as np

param = {}
param['area_loads'] = [100, 300, 500, 700, 850]  # loads in each area, kW
param['gen_costs'] = [30, 60, 70, 62, 45]  # costs of generating power in each area, Ksh.
param['loss_coefficient'] = np.array([[0.0, 0.1, 0.2, 0.4, 0.14],
                                      [0.81, 0.0, 0.3, 0.75, 0.35],
                                      [0.65, 0.8, 0.0, 0.32, 0.05],
                                      [0.45, 0.25, 0.6, 0.0, 0.12],
                                      [0.64, 0.85, 0.05, 0.62, 0.00]])

x_range = [range(851) for _ in range(5)]  # Define the range of values for each area's generation dispatch

dataset = []
for x1 in x_range[0]:
    for x2 in x_range[1]:
        for x3 in x_range[2]:
            for x4 in x_range[3]:
                for x5 in x_range[4]:
                    x = [x1, x2, x3, x4, x5]
                    # Calculate the objective values for each combination of generation dispatch
                    total_load = sum(param['area_loads'])
                    if sum(x) >= total_load:
                        gen_costs = np.array(x) * np.array(param['gen_costs'])
                        total_generation_cost = sum(gen_costs)

                        demand = np.maximum(np.array(param['area_loads']) - np.array(x), 0)
                        supply = np.maximum(np.array(x) - np.array(param['area_loads']), 0)

                        power_flow = np.zeros((len(demand), len(supply)))
                        for i in range(len(demand)):
                            for j in range(len(supply)):
                                if supply[j] >= demand[i]:
                                    power_flow[i, j] = demand[i]
                                    supply[j] -= demand[i]
                                    demand[i] = 0
                                else:
                                    power_flow[i, j] = supply[j]
                                    demand[i] -= supply[j]
                                    supply[j] = 0

                        total_loss = np.sum(power_flow * param['loss_coefficient'])

                        dataset.append({'x': x, 'f1': total_generation_cost, 'f2': total_loss})