from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from .assets import *
from .fleets import *

######################
####### Fleets #######
######################

fleet_views = Blueprint('fleet_views', __name__)


@fleet_views.route('/fleets', methods=['GET', 'POST'])
@login_required
def view_fleets():
    return render_template("fleets.html",
                           user=current_user,
                           data=current_user.getFleets())


@fleet_views.route('/fleets/delete-fleet', methods=['POST'])
def delete_fleet():
    fleet = get_fleet(request.data)
    if fleet:
        db.session.delete(fleet)
        db.session.commit()
    return jsonify({})


@fleet_views.route('/fleets/fleet/<fleet_id>', methods=('GET', 'POST'))
@login_required
def view_fleet(fleet_id):
    # TODO: make sure only owner of asset can access it
    fleet = Fleet.query.get(fleet_id)  # get asset
    return render_template("fleet.html",
                           user=current_user,
                           fleet=fleet,
                           assets=fleet.getAssetsinFleet())


@fleet_views.route('/fleets/new-fleet', methods=['GET', 'POST'])
@login_required
def add_fleet():
    all_user_assets = current_user.getAssets()
    num_user_assets = len(all_user_assets)
    num_techs = []
    for asset in all_user_assets:
        num_techs.append(list(range(len(asset.getTech()[0]))))

    # show only assets not in a fleet
    if request.method == 'POST':
        fleet_name = request.form.get('fleet_name')
        fleet_description = request.form.get('fleet_description')

        fleet_assets = request.form.getlist('fleet_assets')
        int_fleet_assets = []
        for str in fleet_assets:
            str_nums = str.split(";")
            int_fleet_assets.append((int(str_nums[0]), int(str_nums[1])))

        asset_tech_num = request.form.get('asset_num').replace(" ", "")
        str_num = asset_tech_num.split(",")
        asset_num_quant = []
        for str in str_num:
            asset_num_quant.append(int(str))

        nameexists = Fleet.query.filter_by(name=fleet_name).first()

        if len(fleet_name) < 1:
            flash('Name is too short!', category='error')
        elif nameexists:
            flash('Fleet name taken!', category='error')
        elif len(fleet_assets) == (asset_num_quant):
            flash('Unequal number of assets and quantities!', category='error')
        else:
            add_fleet_to_db(fleet_name, fleet_description,
                            int_fleet_assets, all_user_assets, asset_num_quant)
            flash('fleet added!', category='success')
            return view_fleets()

    return render_template("new-fleet.html",
                           user=current_user,
                           data=current_user.getFleets(),
                           assets=all_user_assets,
                           num_assets=list(range(num_user_assets)),
                           num_techs=num_techs
                           )


@fleet_views.route('/fleets/edit-fleet/<fleet_id>', methods=('GET', 'POST'))
@login_required
def edit_fleet(fleet_id):
    all_user_assets = current_user.getAssets()
    num_user_assets = len(all_user_assets)
    # TODO: make sure only owner of asset can access it
    # TODO: make sure it's not None
    # TODO: if empty, just don't change it
    # edit fleet assets
    fleet = Fleet.query.get(fleet_id)  # get fleet
    if request.method == 'POST':
        new_fleet_name = request.form.get('fleet_name')
        fleet.name = new_fleet_name

        new_fleet_description = request.form.get('fleet_description')
        fleet.description = new_fleet_description

        fleet_assets = request.form.getlist('fleet_assets')
        int_fleet_assets = list(map(int, fleet_assets))
        for int_asset in int_fleet_assets:
            asset = all_user_assets[int_asset]
            new_containsAsset = ContainsAsset(fleet_id=fleet.id,
                                              asset_id=asset.id)
            new_containsAsset.link_ContainsAsset()

        db.session.commit()
        flash('Fleet updated!', category='success')
    return render_template("edit-fleet.html",
                           user=current_user,
                           fleet=fleet,
                           assets=all_user_assets,
                           num_assets=list(range(num_user_assets)))
