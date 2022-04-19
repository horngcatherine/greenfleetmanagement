import numpy as np
# Asset names:
# Class 8, low mileage; Class 8, high mileage; Class 6, low mileage; Class 6, high mileage
# Long school bus, Short school bus


def dotio(asset):

    if asset.getType().name == "Long school bus" or asset.getType().name == "Short school bus":
        return False
    else:
        return True


def get_asset_mileage_idle(asset):
    bus_miles = [181466.3, 171527.3, 161588.3, 151649.3, 146518.8, 136761.5, 133276.2, 127309.7, 121580.3, 116074.4,
                 110931.9, 105937.8, 101082.3, 96382.23, 91859.5, 87411.79, 83039.36, 78624.22, 74281.81, 69772.19,
                 66912.04, 60464.94, 55655.92, 50437.23, 44939.45]
    bus_idle = [867.255, 819.755, 772.255, 724.755, 700.2359, 653.6039, 636.9472, 608.4326, 581.0509, 554.7372,
                530.1605, 506.2927, 483.0879, 460.6254, 439.0106, 417.7543, 396.8578, 375.7572, 355.0041, 333.4519,
                319.7829, 288.9712, 265.9881, 241.0472, 214.7725]
    rem = asset.remaining_yrs
    if (asset.getType().name == "Class 8, low mileage"):
        return rem * 8000, rem * 180
    if (asset.getType().name == "Class 8, high mileage"):
        return rem * 16000, rem * 180
    if (asset.getType().name == "Class 6, low mileage"):
        return rem * 8000, rem * 20
    if (asset.getType().name == "Class 6, high mileage"):
        return rem * 16000, rem * 20
    if (asset.getType().name == "Long school bus" or asset.getType().name == "Short school bus"):
        return bus_miles[25 - rem], bus_idle[25 - rem]

# Retrofit names:
# DOTIO- None, DOC, FTF, pass DPF, act DPF, new 2008, CNG Converted
# School- None,	DOC, pass DPF, act DPF, new 2008
# Shared (None, DOC, pass DPF, act DPT, new 2008)
# Unshared (FTF, CNG Converted)


def school_short_to2008(asset):
    if asset.getType().name == "Long school bus":
        costs = [81345.76, 67770.64, 56433.45, 46965.26, 39057.94, 32454.19, 26939.09, 22333.19, 18486.6, 15274.13,
                 12591.26, 10350.67, 8479.456, 6916.72, 5611.608, 4521.651, 3611.379, 2851.17, 2216.285, 1686.064, 1243.253, 873.4412, 564.5949, 306.6635, 91.25341]
    else:
        costs = [58999.42, 49961.36, 42291.6, 35782.98, 30259.72, 25572.65, 21595.16, 18219.83, 15355.51, 12924.82,
                 10862.12, 9111.699, 7626.279, 6365.74, 5296.039, 4388.282, 3617.953, 2964.246, 2409.506, 1938.749, 1539.262, 1200.254, 912.569, 668.4377, 461.2661]
    return costs[25 - asset.rem]


def school_long_to2008(asset):
    if asset.getType().name == "Long school bus":
        return 81345.76
    else:
        return 58999.42


def dotio_short_to2008(asset):
    if (asset.getType().name == "Class 8, high mileage" or asset.getType().name == "Class 8, low mileage"):
        class8 = [1087.499, 1230.406, 1404.953, 1618.145, 1878.539, 2196.584, 2585.046,
                  3059.514, 6552.853, 10587.67, 15294.88, 20833.89, 27398.88, 35226.54, 44605.52, 55887.93, 69503.45]
        return class8[asset.made-1990]
    if (asset.getType().name == "Class 6, high mileage" or asset.getType().name == "Class 6, low mileage"):
        class6 = [209.1639, 255.4734, 312.0359, 381.1215, 465.5028, 568.5665, 694.4486, 848.2015,
                  1884.197, 3149.565, 4695.089, 6582.796, 8888.447, 11704.57, 15144.2, 19345.37, 24476.69]
        return class6[asset.made-1990]


def dotio_short_toCNG(asset):
    if (asset.getType().name == "Class 8, low mileage"):
        cost = [24200, 23400, 22600, 21800, 21000,
                20200, 19400, 18600, 17800, 17000]
    if (asset.getType().name == "Class 8, high mileage"):
        cost = [23400, 21800, 20200, 18600, 17000,
                15400, 13800, 12200, 10600, 9000]
    if (asset.getType().name == "Class 6, low mileage"):
        cost = [24555.56, 24111.11, 23666.67, 23222.22, 22777.78,
                22333.33, 21888.89, 21444.44, 21000, 20555.56]
    if (asset.getType().name == "Class 6, high mileage"):
        cost = [24111.11, 23222.22, 22333.33, 21444.44, 20555.56,
                19666.67, 18777.78, 17888.89, 17000, 16111.11]
    return cost[asset.made-1]


def get_short_cost(asset, retrofit1, retrofit2):
    if (retrofit1.name == retrofit2.name):
        return 0
    if (dotio(asset)):
        if (retrofit2.name == "DOC"):
            return 1660
        if (retrofit2.name == "FTF"):
            return 8260
        if (retrofit2.name == "passDPF"):
            short_costs = [15675.71, 15947.82, 16206.97, 16453.79,
                           16688.84, 16912.71, 17125.91, 17328.96, 17522.35, 17706.52]
            return short_costs[asset.rem - 1]
        if (retrofit2.name == "actDPF"):
            short_costs = [17204.05, 17476.16, 17735.31, 17982.12,
                           18217.18, 18441.04, 18654.25, 18857.3, 19050.68, 19234.85]
            return short_costs[asset.rem - 1]
        if (retrofit2.name == "2008"):
            if (retrofit1.name == "None"):
                if (asset.getType().name == "Class 8, low mileage" or asset.getType().name == "Class 8, high mileage"):
                    costs = [3059.514, 6552.853, 10587.67, 15294.88, 20833.89,
                             27398.88, 35226.54, 44605.52, 55887.93, 69503.45]
                if (asset.getType().name == "Class 6, low mileage" or asset.getType().name == "Class 6, high mileage"):
                    costs = [848.2015, 1884.197, 3149.565, 4695.089, 6582.796,
                             8888.447, 11704.57, 15144.2, 19345.37, 24476.69]
                return costs[asset.rem + 1]
            return dotio_short_to2008(asset)
        if (retrofit2.name == "CNG"):
            return dotio_short_toCNG(asset)
        if (retrofit2.name == "None"):
            return 0
    else:
        if (retrofit2.name == "DOC"):
            return 1000
        if (retrofit2.name == "passDPF"):
            return 8000
        if (retrofit2.name == "actDPF"):
            return 16000
        if (retrofit2.name == "2008"):
            return school_short_to2008(asset)
        if (retrofit2.name == "None"):
            if (retrofit1.name == "DOC" or retrofit1.name == "FTF"):
                return 80
            if (retrofit1.name == "passDPF"):
                return 120
            if (retrofit1.name == "actDPF"):
                return 180
    return 0


def get_long_cost(asset, retrofit1, retrofit2):
    # get the cost of switching asset from retrofit 1 to 2
    if (retrofit1.name == retrofit2.name):
        return 0
    if (dotio(asset)):
        if (retrofit2.name == "DOC"):
            return 1660
        if (retrofit2.name == "FTF"):
            return 8260
        if (retrofit2.name == "passDPF"):
            return 15240
        if (retrofit2.name == "actDPF"):
            return 16693
        if (retrofit2.name == "2008"):
            if asset.getType().name == "Class 8, high mileage" or asset.getType().name == "Class 8, low mileage":
                return 160000
            else:
                return 63000
        if (retrofit2.name == "CNG"):
            return 25000
        if (retrofit2.name == "None"):
            if (retrofit1.name == "DOC" or retrofit1.name == "FTF"):
                return 80
            if (retrofit1.name == "passDPF" or retrofit1.name == "actDPF"):
                return 180
    else:
        if (retrofit2.name == "DOC"):
            return 1000
        if (retrofit2.name == "passDPF"):
            return 8000
        if (retrofit2.name == "actDPF"):
            return 16000
        if (retrofit2.name == "2008"):
            return school_long_to2008(asset)
        if (retrofit2.name == "None"):
            if (retrofit1.name == "DOC"):
                return 40
            if (retrofit1.name == "passDPF"):
                return 60
            if (retrofit1.name == "actDPF"):
                return 80
    return 0


def get_rer_class8(asset, retrofit):
    if retrofit.name == "None":
        if asset.made >= 1996:
            return 0.1872
        else:
            rer = [1.0602, 0.5656, 0.5607, 0.5559, 0.1901, 0.1887]
            return rer[asset.made - 1990]
    if retrofit.name == "DOC":
        if asset.made >= 1996:
            return 0.1404
        else:
            rer = [0.79515, 0.4242, 0.420525, 0.416925, 0.142575, 0.141525]
            return rer[asset.made - 1990]
    if retrofit.name == "FTF":
        if asset.made >= 1996:
            return 0.0936
        else:
            rer = [0.5301, 0.2828, 0.28035, 0.27795, 0.09505, 0.09435]
            return rer[asset.made - 1990]
    if retrofit.name == "pass DPF" or retrofit.name == "act DPF":
        if asset.made >= 1996:
            return 0.02808
        else:
            rer = [0.15903, 0.08484, 0.084105,
                   0.083385, 0.028515, 0.028305]
            return rer[asset.made - 1990]
    if retrofit.name == "2008" or retrofit.name == "CNG":
        return 0.0142


def get_rer_class6(asset, retrofit):
    if retrofit.name == "None":
        if asset.made >= 1998:
            return 0.1472
        else:
            ier = [0.759, 0.5007, 0.4997, 0.4985,
                   0.2495, 0.2477, 0.2457, 0.2431]
            return ier[asset.made - 1990]
    if retrofit.name == "DOC":
        if asset.made >= 1998:
            return 0.107125
        else:
            ier = [0.56925, 0.375525, 0.374775, 0.373875,
                   0.187125, 0.185775, 0.184275, 0.182325]
            return ier[asset.made - 1990]
    if retrofit.name == "FTF":
        if asset.made >= 1998:
            return 0.07135
        else:
            ier = [0.3795, 0.25035, 0.24985, 0.24925,
                   0.12475, 0.12385, 0.12285, 0.12155]
            return ier[asset.made - 1990]
    if retrofit.name == "pass DPF" or retrofit.name == "act DPF":
        if asset.made >= 1998:
            return 0.021405
        else:
            ier = [0.11385, 0.075105, 0.074955, 0.074775,
                   0.037425, 0.037155, 0.036855, 0.036465]
            return ier[asset.made - 1990]
    if retrofit.name == "2008" or retrofit.name == "CNG":
        return 0.0107


def get_rer(asset, retrofit, pollut):
    if dotio(asset):
        if asset.getType().name == "Class 8, high mileage" or asset.getType().name == "Class 8, low mileage":
            return get_rer_class8(asset, retrofit)
        else:
            return get_rer_class6(asset, retrofit)
    else:
        return 0.5


def get_ier(asset, retrofit, pollut):
    return 0.5
