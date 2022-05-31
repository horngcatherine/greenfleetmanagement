import numpy as np
import pandas as pd
from .asset_data import *
from .models import *
from . import db


def get_miles_idle_remaining(fleet):
    assets = fleet.get_non_dup_assets()
    l = len(assets)
    m = np.zeros((l,))
    i = np.zeros((l,))
    for j in range(l):
        asset = assets[j]
        mil, idle = get_asset_mileage_idle(asset)
        m[j] = mil
        i[j] = idle
    return m, i


def get_current_fleet(fleet, retros):
    assets, techs, nums = fleet.getAssetsinFleet()
    non_dup_assets = fleet.get_non_dup_assets()
    current = np.zeros((len(non_dup_assets), len(retros)))
    for i in range(len(assets)):
        for j in range(len(non_dup_assets)):
            if (assets[i] == non_dup_assets[j]):
                for k in range(len(retros)):
                    if (retros[k] == techs[i]):
                        current[j, k] = nums[i]
    return current


def get_costs(fleet, retros):
    assets, _, _ = fleet.getAssetsinFleet()
    r = len(retros)
    c = np.zeros((len(assets), r, r))
    d = np.zeros((len(assets), r, r))
    for i in range(len(assets)):
        for j in range(r):
            for k in range(r):
                c[i][j][k] = get_short_cost(assets[i], retros[j], retros[k])
                d[i][j][k] = get_long_cost(assets[i], retros[j], retros[k])
    return c, d


def get_er(fleet, polluts, retros):
    assets, _, _ = fleet.getAssetsinFleet()
    rer = np.zeros((len(assets), len(retros), len(polluts)))
    ier = np.zeros((len(assets), len(retros), len(polluts)))
    for i in range(len(assets)):
        for j in range(len(retros)):
            for k in range(len(polluts)):
                rer[i][j][k] = get_rer(assets[i], retros[j], polluts[k])
                ier[i][j][k] = get_ier(assets[i], retros[j], polluts[k])
    return rer, ier


def get_input_from_db(fleet, retros, polluts):
    miles_rem, idle_rem = get_miles_idle_remaining(fleet)
    current_fleet = get_current_fleet(fleet)
    short_term_costs, long_term_costs = get_costs(fleet, retros)
    rer, ier = get_er(fleet, polluts, retros)
    upper_bounds = get_upper_bounds(fleet, retros)
    return miles_rem, idle_rem, current_fleet, short_term_costs, long_term_costs, upper_bounds, rer, ier
