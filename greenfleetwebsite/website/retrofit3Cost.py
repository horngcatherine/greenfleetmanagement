#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from locale import PM_STR
from socket import SO_BROADCAST
from tkinter import OptionMenu
from .parse_input import *
import sys
import os


def get_input_from_csv(csv_file, numVehicleTypes, numRetrofitTypes, numPollutants,):
    input_df = pd.read_csv(csv_file)
    rem_mil_np = get_rem_mil(input_df,
                             numVehicleTypes)
    rem_idle_np = get_rem_idle(input_df,
                               numVehicleTypes)
    init_fleet = get_init_flt(input_df,
                              numVehicleTypes,
                              numRetrofitTypes)
    disc_cost = get_long_term_costs(input_df,
                                    numVehicleTypes,
                                    numRetrofitTypes)
    init_cost = get_short_term_costs(input_df,
                                     numVehicleTypes,
                                     numRetrofitTypes)
    upper_bound = get_upper_bounds(input_df,
                                   numVehicleTypes,
                                   numRetrofitTypes)
    run_em_rate = get_running_em_rt(input_df,
                                    numVehicleTypes,
                                    numRetrofitTypes,
                                    numPollutants)
    id_em_rate = get_idle_em_rt(input_df,
                                numVehicleTypes,
                                numRetrofitTypes,
                                numPollutants)
    return rem_mil_np, rem_idle_np, init_fleet, disc_cost, init_cost, upper_bound, run_em_rate, id_em_rate


def run_optimization(model_file, objective,
                     rem_mil_np, rem_idle_np, init_fleet, disc_cost, init_cost,
                     upper_bound, run_em_rate, id_em_rate,
                     numVehicleTypes, numRetrofitTypes, numPollutants,
                     em_redux_req, sb, lb,
                     cost=True, budgets=None, longbudgets=None,
                     ):
    """
    csv_file: csv file of info
    objective: long_term_cost, short_term_cost, PM_emission, CO_emission, NOx_emission, VOC_emission
    numVehicleTypes: number of vehicle types
    numRetrofitTypes: number of retrofit types
    numPollutants: number of pollutants
    em_redux_req: emission reduction requirements, length of numPollutants
    sb: short term budget
    lb: long term budget
    cost: whether or not we are minimizing cost, True by default
    budgets: short budgets if cost = False, None by default
    longbudgets: long budgets if cost = False, None by default
    """
    try:
        print("Step 1")
        from amplpy import AMPL, Environment
        os.chdir(os.path.dirname(__file__) or os.curdir)
        print("Step 2")
        # Create an AMPL instance
        ampl = AMPL(Environment(
            '/Users/catherine/Desktop/cornell/greenfleet/ampl.macos64'))
        print("Step 3")
        # Read the model and data files.
        ampl.read(os.path.join(model_file))
        print("Step 4")
        ###############################
        ######## SET OBJECTIVE ########
        ###############################
        print("Step 5")
        if not cost:
            print("Step 6")
            ampl.eval('''
                    param numB;	# number of short term budget options
                    param numLB;	# number of long term budget options
                    ''')
            numB = ampl.getParameter('numB')
            numB.setValues([len(budgets)])
            numLB = ampl.getParameter('numLB')
            numLB.setValues([len(longbudgets)])
            ampl.eval('''
                    set Bs = 1..numB;
                    set LBs = 1..numLB;
                    param budgets{Bs};
                    param longbudgets{LBs};
                    param PMfred{Bs,LBs};
                    param COfred{Bs,LBs};
                    param NOxfred{Bs,LBs};
                    param VOCfred{Bs,LBs};
                    ''')
        print("Step 7")
        obj = ampl.getObjective(objective.ampl_obj())
        print("Step 8")
        ################################
        ######## SET PARAMETERS ########
        ################################

        i = ampl.getParameter('numVehicleTypes')
        i.setValues([numVehicleTypes])

        j = ampl.getParameter('numRetrofitTypes')
        j.setValues([numRetrofitTypes])

        p = ampl.getParameter('numPollutants')
        p.setValues([numPollutants])

        m = ampl.getParameter('m')
        for i in range(numVehicleTypes):
            m[i+1] = float(rem_mil_np[i])
        print('Set remaining number of miles a vehicle of type i will travel.')

        w = ampl.getParameter('w')

        for i in range(numVehicleTypes):
            w[i+1] = float(rem_idle_np[i])
        print('Set remaining number of hours vehicle of type i will idle.')

        B = ampl.getParameter('B')
        B.setValues([sb])
        print('Set short term budget for retrofits and early retirements')

        LB = ampl.getParameter('LB')
        LB.setValues([lb])
        print('Set long term budget')

        print(em_redux_req)

        frac = ampl.getParameter('frac')
        frac.setValues(em_redux_req)
        print('Set fraction reduction required for pollutant p')

        f = ampl.getParameter('f')
        for i in range(numVehicleTypes):
            for j in range(numRetrofitTypes):
                f[i+1, j+1] = int(init_fleet[i][j])
        print('Set number of vehicles of type i with retrofit package j in intial fleet.')

        c = ampl.getParameter('c')
        for i in range(numVehicleTypes):
            for j in range(numRetrofitTypes):
                for k in range(numRetrofitTypes):
                    c[i+1, j+1, k+1] = disc_cost[i][j][k]
        print('Set discounted cost of switching from retrofit j to k on vehicle type i')

        d = ampl.getParameter('d')
        for i in range(numVehicleTypes):
            for j in range(numRetrofitTypes):
                for k in range(numRetrofitTypes):
                    d[i+1, j+1, k+1] = init_cost[i][j][k]
        print('Set initial cost of switching from retrofit j to k on vehicle type i')

        u = ampl.getParameter('u')
        for i in range(numVehicleTypes):
            for j in range(numRetrofitTypes):
                for k in range(numRetrofitTypes):
                    u[i+1, j+1, k+1] = upper_bound[i][j][k]
        print('Set upper bound on number of vehicles of type i to go from retrofit package j to k.')

        rer = ampl.getParameter('rer')
        for i in range(numVehicleTypes):
            for j in range(numRetrofitTypes):
                for k in range(numPollutants):
                    rer[i+1, j+1, k+1] = run_em_rate[i][j][k]
        print('Set g/mile running emission rate for pollutant p by vehicle of type i w/ retrofit package j')

        ier = ampl.getParameter('ier')
        for i in range(numVehicleTypes):
            for j in range(numRetrofitTypes):
                for k in range(numPollutants):
                    ier[i+1, j+1, k+1] = id_em_rate[i][j][k]
        print('Set g/hour idling emission rate for pollutant p by vehicle of type i w/ retrofit package j')

        ###############################
        ############ SOLVE ############
        ###############################
        if cost:
            ampl.solve()
            #print('Cost: ', obj.value())
        else:
            pm = ampl.getParameter('PMfred')
            co = ampl.getParameter('COfred')
            nox = ampl.getParameter('NOxfred')
            voc = ampl.getParameter('VOCfred')
            em = [pm, co, nox, voc]
            eretro = ampl.getVariable('Eretrofit')
            ebase = ampl.getVariable('Ebase')
            for a in range(len(budgets)):
                B.setValues([budgets[a]])
                print('Set short term budget for retrofits and early retirements')
                for b in range(len(longbudgets)):
                    LB.setValues([longbudgets[b]])
                    print('Set long term budget')
                    ampl.solve()
                    for i in range(numPollutants):
                        em[i][a+1, b+1] = 1 - \
                            (eretro[i+1].value()/ebase[i+1].value())

        ###############################
        ######### PRINT VALUES ########
        ###############################
        r = ampl.getVariable('r')
        num_vehicles = r.getValues()
        #print('Number of vehicles of type i to go from retrofit package j to k:')
        # print(num_vehicles)

        Ebase = ampl.getVariable('Ebase')
        em_wout_retro = Ebase.getValues()
        #print('Emissions if no retrofits changed:')
        # print(em_wout_retro)

        Eretrofit = ampl.getVariable('Eretrofit')
        em_w_retro = Eretrofit.getValues()
        #print('Emissions w/ retrofits changed:')
        # print(em_w_retro)
        return num_vehicles, em_wout_retro, em_w_retro
    except Exception as e:
        print(e)
        raise


def run_optimization_from_csv(csv_file, model_file, objective,
                              numVehicleTypes, numRetrofitTypes, numPollutants,
                              em_redux_req, sb, lb,
                              cost=True, budgets=None, longbudgets=None,
                              ):
    mil, idle, init, disc, cost, upper, rer, ier = get_input_from_csv(
        csv_file, numVehicleTypes, numRetrofitTypes, numPollutants,)
    return run_optimization(model_file, objective,
                            mil, idle, init, disc, cost,
                            upper, rer, ier,
                            numVehicleTypes, numRetrofitTypes, numPollutants,
                            em_redux_req, sb, lb,
                            cost=True, budgets=None, longbudgets=None,
                            )
