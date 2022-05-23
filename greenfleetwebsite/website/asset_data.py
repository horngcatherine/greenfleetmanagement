import numpy as np
from .models import LongCost, ShortCost
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


# def school_short_to2008(asset):
#     remaining = 25 - asset.remaining_yrs
#     if remaining < 0:
#         remaining = 0
#     if remaining > 24:
#         remaining = 24
#     if asset.getType().name == "Long school bus":
#         costs = [81345.76, 67770.64, 56433.45, 46965.26, 39057.94, 32454.19, 26939.09, 22333.19, 18486.6, 15274.13,
#                  12591.26, 10350.67, 8479.456, 6916.72, 5611.608, 4521.651, 3611.379, 2851.17, 2216.285, 1686.064, 1243.253, 873.4412, 564.5949, 306.6635, 91.25341]
#     else:
#         costs = [58999.42, 49961.36, 42291.6, 35782.98, 30259.72, 25572.65, 21595.16, 18219.83, 15355.51, 12924.82,
#                  10862.12, 9111.699, 7626.279, 6365.74, 5296.039, 4388.282, 3617.953, 2964.246, 2409.506, 1938.749, 1539.262, 1200.254, 912.569, 668.4377, 461.2661]
#     return costs[remaining]


# def school_long_to2008(asset):
#     if asset.getType().name == "Long school bus":
#         return 81345.76
#     else:
#         return 58999.42


# def dotio_short_to2008(asset):
#     made = asset.made-1990
#     if made < 0:
#         made = 0
#     if made > 16:
#         made = 16
#     if (asset.getType().name == "Class 8, high mileage" or asset.getType().name == "Class 8, low mileage"):
#         class8 = [1087.499, 1230.406, 1404.953, 1618.145, 1878.539, 2196.584, 2585.046,
#                   3059.514, 6552.853, 10587.67, 15294.88, 20833.89, 27398.88, 35226.54, 44605.52, 55887.93, 69503.45]
#         return class8[made]
#     if (asset.getType().name == "Class 6, high mileage" or asset.getType().name == "Class 6, low mileage"):
#         class6 = [209.1639, 255.4734, 312.0359, 381.1215, 465.5028, 568.5665, 694.4486, 848.2015,
#                   1884.197, 3149.565, 4695.089, 6582.796, 8888.447, 11704.57, 15144.2, 19345.37, 24476.69]
#         return class6[made]


# def dotio_short_toCNG(asset):
#     if (asset.getType().name == "Class 8, low mileage"):
#         cost = [24200, 23400, 22600, 21800, 21000,
#                 20200, 19400, 18600, 17800, 17000]
#     if (asset.getType().name == "Class 8, high mileage"):
#         cost = [23400, 21800, 20200, 18600, 17000,
#                 15400, 13800, 12200, 10600, 9000]
#     if (asset.getType().name == "Class 6, low mileage"):
#         cost = [24555.56, 24111.11, 23666.67, 23222.22, 22777.78,
#                 22333.33, 21888.89, 21444.44, 21000, 20555.56]
#     if (asset.getType().name == "Class 6, high mileage"):
#         cost = [24111.11, 23222.22, 22333.33, 21444.44, 20555.56,
#                 19666.67, 18777.78, 17888.89, 17000, 16111.11]
#     remaining = asset.remaining_yrs - 1
#     if remaining > 9:
#         remaining = 9
#     return cost[remaining]


# def get_short_cost(asset, retrofit1, retrofit2):
#     if (retrofit1.name == retrofit2.name):
#         return 0
#     if (dotio(asset)):
#         if (retrofit2.name == "DOC"):
#             return 1660
#         if (retrofit2.name == "FTF"):
#             return 8260
#         remaining = asset.remaining_yrs - 1
#         if remaining > 9:
#             remaining = 9
#         if (retrofit2.name == "passDPF"):
#             short_costs = [15675.71, 15947.82, 16206.97, 16453.79,
#                            16688.84, 16912.71, 17125.91, 17328.96, 17522.35, 17706.52]
#             return short_costs[remaining]
#         if (retrofit2.name == "actDPF"):
#             short_costs = [17204.05, 17476.16, 17735.31, 17982.12,
#                            18217.18, 18441.04, 18654.25, 18857.3, 19050.68, 19234.85]
#             return short_costs[remaining]
#         if (retrofit2.name == "2008"):
#             if (retrofit1.name == "None"):
#                 if (asset.getType().name == "Class 8, low mileage" or asset.getType().name == "Class 8, high mileage"):
#                     costs = [3059.514, 6552.853, 10587.67, 15294.88, 20833.89,
#                              27398.88, 35226.54, 44605.52, 55887.93, 69503.45]
#                 if (asset.getType().name == "Class 6, low mileage" or asset.getType().name == "Class 6, high mileage"):
#                     costs = [848.2015, 1884.197, 3149.565, 4695.089, 6582.796,
#                              8888.447, 11704.57, 15144.2, 19345.37, 24476.69]
#                 return costs[remaining]
#             return dotio_short_to2008(asset)
#         if (retrofit2.name == "CNG Converted"):
#             return dotio_short_toCNG(asset)
#         if (retrofit2.name == "None"):
#             return 0
#     else:
#         if (retrofit2.name == "DOC"):
#             return 1000
#         if (retrofit2.name == "passDPF"):
#             return 8000
#         if (retrofit2.name == "actDPF"):
#             return 16000
#         if (retrofit2.name == "2008"):
#             return school_short_to2008(asset)
#         if (retrofit2.name == "None"):
#             if (retrofit1.name == "DOC" or retrofit1.name == "FTF"):
#                 return 80
#             if (retrofit1.name == "passDPF"):
#                 return 120
#             if (retrofit1.name == "actDPF"):
#                 return 180
#     return 0


# def get_long_cost(asset, retrofit1, retrofit2):
#     # get the cost of switching asset from retrofit 1 to 2
#     if (retrofit1.name == retrofit2.name):
#         return 0
#     if (dotio(asset)):
#         if (retrofit2.name == "DOC"):
#             return 1660
#         if (retrofit2.name == "FTF"):
#             return 8260
#         if (retrofit2.name == "passDPF"):
#             return 15240
#         if (retrofit2.name == "actDPF"):
#             return 16693
#         if (retrofit2.name == "new 2008"):
#             if asset.getType().name == "Class 8, high mileage" or asset.getType().name == "Class 8, low mileage":
#                 return 160000
#             else:
#                 return 63000
#         if (retrofit2.name == "CNG Converted"):
#             return 25000
#         if (retrofit2.name == "None"):
#             if (retrofit1.name == "DOC" or retrofit1.name == "FTF"):
#                 return 80
#             if (retrofit1.name == "passDPF" or retrofit1.name == "actDPF"):
#                 return 180
#     else:
#         if (retrofit2.name == "DOC"):
#             return 1000
#         if (retrofit2.name == "passDPF"):
#             return 8000
#         if (retrofit2.name == "actDPF"):
#             return 16000
#         if (retrofit2.name == "new 2008"):
#             return school_long_to2008(asset)
#         if (retrofit2.name == "None"):
#             if (retrofit1.name == "DOC"):
#                 return 40
#             if (retrofit1.name == "passDPF"):
#                 return 60
#             if (retrofit1.name == "actDPF"):
#                 return 80
#     return 0

def get_long_cost(asset, retrofit1, retrofit2):
    lc = LongCost.query.filter_by(
        tech1_id=retrofit1.id, tech2_id=retrofit2.id, type_id=asset.id).first()
    return lc.cost


def get_short_cost(asset, retrofit1, retrofit2):
    sc = ShortCost.query.filter_by(
        tech1_id=retrofit1.id, tech2_id=retrofit2.id, type_id=asset.id).first()
    return sc.cost


def get_dotio_rer_base(asset, pollut):
    if pollut.name == "PM2.5":
        # class 8
        if asset.getType().name == "Class 8, high mileage" or asset.getType().name == "Class 8, low mileage":
            if asset.made >= 1996:
                return 0.1872
            else:
                rer = [1.0602, 0.5656, 0.5607, 0.5559, 0.1901, 0.1887]
                return rer[asset.made - 1990]
        else:  # class 6
            if asset.made >= 1998:
                return 0.1472
            else:
                rer = [0.759, 0.5007, 0.4997, 0.4985,
                       0.2495, 0.2477, 0.2457, 0.2431]
                return rer[asset.made - 1990]
    if pollut.name == "CO":
        return 1
    if pollut.name == "NOx":
        return 14
    if pollut.name == "VOC":
        return 0.6


def get_school_rer_base(asset, pollut):
    if pollut.name == "PM2.5":
        rer = [0.0221, 0.0221, 0.1403, 0.1403, 0.1403, 0.1403, 0.1403, 0.1403, 0.1403, 0.1403, 0.1403, 0.1403,
               0.1402, 0.2258, 0.2252, 0.9513, 1.9384, 1.9259, 1.5827, 2.0375, 2.0387, 2.899, 2.899, 2.899, 2.899]
    if pollut.name == "CO":
        rer = [0.355, 0.227, 1.898, 1.917, 1.937, 1.956, 1.976, 1.995, 2.015, 2.035, 2.054, 2.074,
               1.993, 2.068, 2.052, 2.921, 2.893, 2.843, 3.838, 4.022, 4.041, 6.355, 6.632, 6.664, 6.713]
    if pollut.name == "NOx":
        rer = [3.632, 3.635, 6.702, 6.706, 6.709, 9.275, 11.119, 11.736, 11.739, 11.743, 11.746, 14.655, 13.87,
               14.384, 14.117, 13.968, 13.722, 13.436, 14.267, 18.912, 18.855, 13.668, 13.668, 13.668, 13.668]
    if pollut.name == "VOC":
        rer = [0.285, 0.285, 0.369, 0.371, 0.373, 0.658, 0.661, 0.663, 0.665, 0.667, 0.669, 0.671,
               0.655, 0.663, 0.653, 0.823, 0.81, 0.795, 1.021, 1.309, 1.307, 1.136, 1.136, 1.302, 1.302]
    return rer[2008-asset.made]


def get_dotio_CNG2008_rer(asset, pollut):
    if pollut.name == "PM2.5":
        if asset.getType().name == "Class 8, high mileage" or asset.getType().name == "Class 8, low mileage":
            return 0.0142
        else:
            return 0.0107
    if pollut.name == "CO":
        return 0.355
    if pollut.name == "NOx":
        return 3.632
    if pollut.name == "VOC":
        return 0.285


def get_school_CNG2008_rer(pollut):
    if pollut.name == "PM2.5":
        return 0.0221
    if pollut.name == "CO":
        return 0.355
    if pollut.name == "NOx":
        return 3.632
    if pollut.name == "VOC":
        return 0.285


def get_rer(asset, retrofit, pollut):
    if dotio(asset):
        if (retrofit.name == "CNG Converted" or retrofit.name == "new 2008"):
            return get_dotio_CNG2008_rer(asset, pollut)
        return retrofit.getRedux(pollut) * get_dotio_rer_base(asset, pollut)
    else:
        if (retrofit.name == "CNG Converted" or retrofit.name == "new 2008"):
            return get_school_CNG2008_rer(pollut)
        return retrofit.getRedux(pollut) * get_school_rer_base(asset, pollut)


def get_dotio_ier_base(asset, pollut):
    if pollut.name == "PM2.5":
        if asset.made >= 1994:
            return 0.9237
        elif asset.made == 1990:
            return 2.9201
        else:
            return 1.7112
    if pollut.name == "CO":
        return 22
    if pollut.name == "NOx":
        return 55
    if pollut.name == "VOC":
        return 5


def get_school_ier_base(asset, pollut):
    if pollut.name == "PM2.5":
        ier = [0.9237, 0.9237, 0.9237, 0.9237, 0.9237, 0.9237, 0.9237, 0.9237, 0.9237, 0.9237, 0.9237, 0.9237,
               0.9237, 0.9237, 0.9237, 1.7112, 1.7112, 1.7112, 2.9201, 2.9201, 2.9201, 4.9404, 4.9404, 4.9404, 4.9404]
    if pollut.name == "CO":
        ier = [2.5175, 2.5175, 21.04, 21.2575, 21.4725, 21.69, 21.9075, 22.125, 22.3425, 22.5575, 22.775, 22.9925,
               22.1, 22.925, 22.7525, 32.39, 32.08, 31.525, 42.5575, 44.59, 44.8075, 72.9925, 73.535, 73.89, 74.425]
    if pollut.name == "NOx":
        ier = [14.9, 14.91, 27.495, 27.5075, 27.52, 41.79, 46.5475, 48.1425, 48.155, 48.17, 48.1825, 60.1175, 56.895,
               59.0025, 57.91, 57.3, 56.2875, 55.1175, 58.525, 77.5775, 77.345, 56.0675, 56.0675, 56.0675, 56.0675]
    if pollut.name == "VOC":
        ier = [2.2075, 2.2075, 2.855, 2.8725, 2.89, 5.095, 5.11, 5.1275, 5.1425, 5.16, 5.175, 5.1925,
               5.07, 5.1275, 5.05, 6.3675, 6.25, 6.15, 7.8975, 10.1275, 10.11, 8.7875, 8.7875, 10.0775, 10.0775]
    return ier[2008-asset.made]


def get_dotio_CNG2008_ier(pollut):
    if pollut.name == "PM2.5":
        return 0.9237
    if pollut.name == "CO":
        return 2.5175
    if pollut.name == "NOx":
        return 14.9
    if pollut.name == "VOC":
        return 2.2075


def get_school_CNG2008_ier(pollut):
    if pollut.name == "PM2.5":
        return 0.9237
    if pollut.name == "CO":
        return 2.5175
    if pollut.name == "NOx":
        return 14.9
    if pollut.name == "VOC":
        return 2.2075


def get_ier(asset, retrofit, pollut):
    if dotio(asset):
        if (retrofit.name == "CNG Converted" or retrofit.name == "new 2008"):
            return get_dotio_CNG2008_ier(pollut)
        return retrofit.getRedux(pollut) * get_dotio_ier_base(asset, pollut)
    else:
        if (retrofit.name == "CNG Converted" or retrofit.name == "new 2008"):
            return get_school_CNG2008_ier(pollut)
        return retrofit.getRedux(pollut) * get_school_ier_base(asset, pollut)
