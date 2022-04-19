from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json
import numpy as np

import os
from flask import Flask, redirect, url_for
from werkzeug.utils import secure_filename


def get_asset(req):
    asset = json.loads(req)  # asset dictionary from click
    asset = Asset.query.get(asset['assetId'])  # get asset
    # list of all OwnsAssets that has the same asset id
    ownsAsset = OwnsAsset.query.filter_by(asset_id=asset.id).first()
    if (ownsAsset.user_id == current_user.id):
        return asset


def putAssetinCategory(asset, category):
    new_isInCategory = IsInCategory(asset_id=asset.id,
                                    category_id=category.id)
    new_isInCategory.link_IsInCategory()


def useTechinAsset(asset, tech, quant):
    new_usesTech = UsesTech(asset_id=asset.id,
                            tech_id=tech.id,
                            num_assets=quant)
    new_usesTech.link_UsesTech()


def add_asset_to_db(name, asset_made, remaining, asset_type, asset_category, asset_tech, tech_quant):
    new_asset = Asset(name=name, made=asset_made,
                      remaining_yrs=remaining,
                      ofAssetType=[],
                      isOwnedBy=[],
                      isInCategory=[],
                      usesTech=[],
                      containsAssets=[]
                      )
    db.session.add(new_asset)
    db.session.commit()

    new_ownsAsset = OwnsAsset(user_id=current_user.id,
                              asset_id=new_asset.id)
    new_ownsAsset.link_OwnsAsset()

    new_ofAssetType = OfAssetType(asset_id=new_asset.id,
                                  asset_type_id=asset_type.id)
    new_ofAssetType.link_OfAssetType()

    if not (asset_category == None):
        putAssetinCategory(new_asset, asset_category)

    for t in range(len(asset_tech)):
        useTechinAsset(new_asset, asset_tech[t], tech_quant[t])

    db.session.commit()

    return new_asset


def add_asset_from_csv(file):
    lines = file.readlines()
    assets = []
    for line in lines:
        asset_name = line[0]
        asset_quantity = line[1]  # convert to number
        asset_mileage = line[2]  # convert to number
        asset_idle = line[3]  # convert to number
        asset_category_name = line[4]
        asset_tech_name = line[5]
        asset_category = Category.query.filter_by(
            name=asset_category_name).first()
        asset_tech = Tech.query.filter_by(name=asset_tech_name).first()
        asset = add_asset_to_db(asset_name,
                                asset_quantity,
                                asset_mileage,
                                asset_idle,
                                asset_category,
                                asset_tech)
        assets.append(asset)
    return assets
