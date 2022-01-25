import numpy as np
import cvxpy as cp
import pandas as pd

##################
### USER INPUT ###
##################

# n, number of VehicleTypes
numVehicleTypes = 50
# m, number of RetrofitTypes
numRetrofitTypes = 5
# p, number Pollutants
numPollutants = 4
# CSV file of inputs
csv_file = 'input_template.csv'
input_df = pd.read_csv(csv_file)

###################
### EXCEL INPUT ###
###################

### Fleet Inputs ###

# id; col 0 is asset number

# remaining mileage; col 1 is mileage
rem_mil = input_df.iloc[:, 1].values
rem_mil_np = np.asarray(rem_mil)
assert (rem_mil_np.all() >= 0)
assert (rem_mil_np.shape == (numVehicleTypes,))

# remaining idle time; col 2 is idle time
rem_idle = input_df.iloc[:, 2].values
rem_idle_np = np.asarray(rem_idle)
assert (rem_idle_np.all() >= 0)
assert (rem_idle_np.shape == (numVehicleTypes,))

# initial fleet
init_flt = input_df.iloc[:, 3:3+numRetrofitTypes].values
init_flt_np = np.asarray(init_flt)
assert (init_flt_np.all() >= 0)
assert (init_flt_np.shape == (numVehicleTypes, numRetrofitTypes))


### Retrofit Inputs ###
# long_term_costs[i, j, k]: cost of switching vehicle type [j] of retrofit[i] to retrofit [k]
long_term_costs_np = np.zeros(
    (numRetrofitTypes, numVehicleTypes, numRetrofitTypes))
for i in range(numRetrofitTypes):
    start = 3 + numRetrofitTypes + i * numRetrofitTypes
    end = 3 + numRetrofitTypes + (i+1) * numRetrofitTypes
    long_term_costs_ri = input_df.iloc[:, start:end].values
    long_term_costs_ri_np = np.asarray(long_term_costs_ri)
    assert (long_term_costs_ri_np.shape == (
        numVehicleTypes, numRetrofitTypes))
    long_term_costs_np[i, :, :] = long_term_costs_ri_np
assert (init_flt_np.all() >= 0)


# short_term_costs[i, j, k]: cost of switching vehicle type [j] of retrofit[i] to retrofit [k]
short_term_costs_np = np.zeros(
    (numRetrofitTypes, numVehicleTypes, numRetrofitTypes))
for i in range(numRetrofitTypes):
    start = 3 + numRetrofitTypes + numRetrofitTypes**2 + i * numRetrofitTypes
    end = 3 + numRetrofitTypes + numRetrofitTypes**2 + (i+1) * numRetrofitTypes
    short_term_costs_ri = input_df.iloc[:, start:end].values
    short_term_costs_ri_np = np.asarray(short_term_costs_ri)
    assert (short_term_costs_ri_np.shape == (
        numVehicleTypes, numRetrofitTypes))
    short_term_costs_np[i, :, :] = short_term_costs_ri_np

# upper_bounds[i, j, k]: bound of switching vehicle type [j] of retrofit[i] to retrofit [k]
upper_bounds_np = np.zeros(
    (numRetrofitTypes, numVehicleTypes, numRetrofitTypes))
for i in range(numRetrofitTypes):
    start = 3 + numRetrofitTypes + 2 * \
        (numRetrofitTypes**2) + i * numRetrofitTypes
    end = 3 + numRetrofitTypes + 2 * \
        (numRetrofitTypes**2) + (i+1) * numRetrofitTypes
    upper_bounds_ri = input_df.iloc[:, start:end].values
    upper_bounds_ri_np = np.asarray(upper_bounds_ri)
    assert (upper_bounds_ri_np.shape == (
        numVehicleTypes, numRetrofitTypes))
    upper_bounds_np[i, :, :] = upper_bounds_ri_np

### Emission Inputs ###
# running_em_rt[i, j, k]: running emission rate of pollutant [k] of vehicle type [j] of retrofit [j]
running_em_rt_np = np.zeros((numRetrofitTypes, numVehicleTypes, numPollutants))
for i in range(numRetrofitTypes):
    start = 3 + numRetrofitTypes + 3 * \
        (numRetrofitTypes**2) + i * numPollutants
    end = 3 + numRetrofitTypes + 3 * \
        (numRetrofitTypes**2) + (i+1) * numPollutants
    running_em_rt_ri = input_df.iloc[:, start:end].values
    running_em_rt_ri_np = np.asarray(running_em_rt_ri)
    assert (running_em_rt_ri_np.shape == (
        numVehicleTypes, numPollutants))
    running_em_rt_np[i, :, :] = running_em_rt_ri_np

# idle_em_rt[i, j, k]: idle emission rate of pollutant [k] of vehicle type [j] of retrofit [j]
idle_em_rt_np = np.zeros((numRetrofitTypes, numVehicleTypes, numPollutants))
for i in range(numRetrofitTypes):
    start = 3 + numRetrofitTypes + 3 * \
        (numRetrofitTypes**2) + (numRetrofitTypes*numPollutants) + i * numPollutants
    end = 3 + numRetrofitTypes + 3 * \
        (numRetrofitTypes**2) + (numRetrofitTypes *
                                 numPollutants) + (i+1) * numPollutants
    idle_em_rt_ri = input_df.iloc[:, start:end].values
    idle_em_rt_ri_np = np.asarray(idle_em_rt_ri)
    assert (idle_em_rt_ri_np.shape == (
        numVehicleTypes, numPollutants))
    idle_em_rt_np[i, :, :] = idle_em_rt_ri_np

# print("Remaining mileage: \n", rem_mil_np, "\n")
# print("Remaining idle hours: \n", rem_idle_np, "\n")
# print("Initial fleet: \n", init_flt_np, "\n")
# print("Long term costs: \n", long_term_costs_np, "\n")
# print("Short term costs: \n", short_term_costs_np, "\n")
# print("Upper bounds: \n", upper_bounds_np, "\n")
# print("Running emission rate: \n", running_em_rt_np, "\n")
# print("Idle emission rate: \n", idle_em_rt_np, "\n")

# Emission reduction requirements
em_redux_req = np.asarray([0.25, -0.1, -0.1, -0.1])

# Short term budget
sb = 10000000
# Long term budget
lb = 1500000

retrofits = cp.Variable((numRetrofitTypes, numVehicleTypes, numRetrofitTypes))
long_term_cost_obj = cp.Minimize(cp.sum(retrofits @ long_term_costs_np))
short_term_cost_obj = cp.Minimize(cp.sum(retrofits @ short_term_costs_np))
non_neg = retrofits >= 0
upper_bound = retrofits <= upper_bounds_np
percent_redux = retrofits * rem_mil_np * running_em_rt_np + \
    retrofits * rem_idle_np * idle_em_rt_np <= (1 - em_redux_req) + sum()
constraints = []
