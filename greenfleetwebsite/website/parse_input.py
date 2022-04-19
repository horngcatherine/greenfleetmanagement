
import numpy as np
import pandas as pd

# ##################
# ### USER INPUT ###
# ##################


def get_rem_mil(input_df, numVehicleTypes):
    # remaining mileage; col 1 is mileage
    rem_mil = input_df.iloc[:, 1].values
    rem_mil_np = np.asarray(rem_mil)
    assert (rem_mil_np.all() >= 0)
    assert (rem_mil_np.shape == (numVehicleTypes,))
    return rem_mil_np


def get_rem_idle(input_df, numVehicleTypes):
    # remaining idle time; col 2 is idle time
    rem_idle = input_df.iloc[:, 2].values
    rem_idle_np = np.asarray(rem_idle)
    assert (rem_idle_np.all() >= 0)
    assert (rem_idle_np.shape == (numVehicleTypes,))
    return rem_idle_np


def get_init_flt(input_df, numVehicleTypes, numRetrofitTypes):
    # initial fleet
    init_flt = input_df.iloc[:, 3:3+numRetrofitTypes].values
    init_flt_np = np.asarray(init_flt)
    assert (init_flt_np.all() >= 0)
    assert (init_flt_np.shape == (numVehicleTypes, numRetrofitTypes))
    return init_flt_np


### Retrofit Inputs ###
def get_long_term_costs(input_df, numVehicleTypes, numRetrofitTypes):
    # long_term_costs[i, j, k]: cost of switching vehicle type [j] of retrofit[i] to retrofit [k]
    long_term_costs_np = np.zeros(
        (numVehicleTypes, numRetrofitTypes,  numRetrofitTypes))
    for i in range(numRetrofitTypes):
        start = 3 + numRetrofitTypes + i * numRetrofitTypes
        end = 3 + numRetrofitTypes + (i+1) * numRetrofitTypes
        long_term_costs_ri = input_df.iloc[:, start:end].values
        long_term_costs_ri_np = np.asarray(long_term_costs_ri)
        assert (long_term_costs_ri_np.shape == (
            numVehicleTypes, numRetrofitTypes))
        long_term_costs_np[:, i, :] = long_term_costs_ri_np
    assert (get_init_flt(input_df, numVehicleTypes,
            numRetrofitTypes).all() >= 0)
    return long_term_costs_np


def get_short_term_costs(input_df, numVehicleTypes, numRetrofitTypes):
    # short_term_costs[i, j, k]: cost of switching vehicle type [j] of retrofit[i] to retrofit [k]
    short_term_costs_np = np.zeros(
        (numVehicleTypes, numRetrofitTypes, numRetrofitTypes))
    for i in range(numRetrofitTypes):
        start = 3 + numRetrofitTypes + numRetrofitTypes**2 + i * numRetrofitTypes
        end = 3 + numRetrofitTypes + \
            numRetrofitTypes**2 + (i+1) * numRetrofitTypes
        short_term_costs_ri = input_df.iloc[:, start:end].values
        short_term_costs_ri_np = np.asarray(short_term_costs_ri)
        assert (short_term_costs_ri_np.shape == (
            numVehicleTypes, numRetrofitTypes))
        short_term_costs_np[:, i, :] = short_term_costs_ri_np
    return short_term_costs_np


def get_upper_bounds(input_df, numVehicleTypes, numRetrofitTypes):
    # upper_bounds[i, j, k]: bound of switching vehicle type [j] of retrofit[i] to retrofit [k]
    upper_bounds_np = np.zeros(
        (numVehicleTypes, numRetrofitTypes, numRetrofitTypes))
    for i in range(numRetrofitTypes):
        start = 3 + numRetrofitTypes + 2 * \
            (numRetrofitTypes**2) + i * numRetrofitTypes
        end = 3 + numRetrofitTypes + 2 * \
            (numRetrofitTypes**2) + (i+1) * numRetrofitTypes
        upper_bounds_ri = input_df.iloc[:, start:end].values
        upper_bounds_ri_np = np.asarray(upper_bounds_ri)
        assert (upper_bounds_ri_np.shape == (
            numVehicleTypes, numRetrofitTypes))
        upper_bounds_np[:, i, :] = upper_bounds_ri_np
    return upper_bounds_np

### Emission Inputs ###


def get_running_em_rt(input_df, numVehicleTypes, numRetrofitTypes, numPollutants):
    # running_em_rt[i, j, k]: running emission rate of pollutant [k] of vehicle type [j] of retrofit [j]
    running_em_rt_np = np.zeros(
        (numVehicleTypes, numRetrofitTypes, numPollutants))
    for i in range(numRetrofitTypes):
        start = 3 + numRetrofitTypes + 3 * \
            (numRetrofitTypes**2) + i * numPollutants
        end = 3 + numRetrofitTypes + 3 * \
            (numRetrofitTypes**2) + (i+1) * numPollutants
        running_em_rt_ri = input_df.iloc[:, start:end].values
        running_em_rt_ri_np = np.asarray(running_em_rt_ri)
        assert (running_em_rt_ri_np.shape == (
            numVehicleTypes, numPollutants))
        running_em_rt_np[:, i, :] = running_em_rt_ri_np
    return running_em_rt_np


def get_idle_em_rt(input_df, numVehicleTypes, numRetrofitTypes, numPollutants):
    # idle_em_rt[i, j, k]: idle emission rate of pollutant [k] of vehicle type [j] of retrofit [j]
    idle_em_rt_np = np.zeros(
        (numVehicleTypes, numRetrofitTypes, numPollutants))
    for i in range(numRetrofitTypes):
        start = 3 + numRetrofitTypes + 3 * \
            (numRetrofitTypes**2) + \
            (numRetrofitTypes*numPollutants) + i * numPollutants
        end = 3 + numRetrofitTypes + 3 * \
            (numRetrofitTypes**2) + (numRetrofitTypes *
                                     numPollutants) + (i+1) * numPollutants
        idle_em_rt_ri = input_df.iloc[:, start:end].values
        idle_em_rt_ri_np = np.asarray(idle_em_rt_ri)
        assert (idle_em_rt_ri_np.shape == (
            numVehicleTypes, numPollutants))
        idle_em_rt_np[:, i, :] = idle_em_rt_ri_np
    return idle_em_rt_np
