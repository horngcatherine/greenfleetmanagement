from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json

import os
from flask import Flask, redirect, url_for
from werkzeug.utils import secure_filename

# Users/catherine/Desktop/cornell/fa21/greenfleet/greenfleetwebsite
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'csv', 'txt'}

views = Blueprint('views', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#####################
####### Basic #######
#####################


@views.route('/')
def home():
    # cat1 = Category(name='Category 1', description='Description for Catgory 1')
    # cat2 = Category(name='Category 2', description='Description for Catgory 2')
    # tech1 = Tech(name='Technology 1',
    #              description='Description for Tech 1', public=True)
    # tech2 = Tech(name='Technology 2',
    #              description='Description for Tech 2', public=True)
    # db.session.add(cat1)
    # db.session.add(cat2)
    # db.session.add(tech1)
    # db.session.add(tech2)
    # db.session.commit()
    return render_template("home.html", user=current_user)


@views.route('/information')
def information():
    return render_template("information.html", user=current_user)


@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def get_assetsfleets():
    assets = current_user.getAssets()
    fleets = current_user.getFleets()
    return render_template("dashboard.html", user=current_user, assets=assets, fleets=fleets)


######################
####### Assets #######
######################

def get_asset(req):
    asset = json.loads(req)  # asset dictionary from click
    asset = Asset.query.get(asset['assetId'])  # get asset
    # list of all OwnsAssets that has the same asset id
    ownsAsset = OwnsAsset.query.filter_by(asset_id=asset.id).first()
    if (ownsAsset.user_id == current_user.id):
        return asset


@views.route('/assets', methods=['GET', 'POST'])
@login_required
def view_assets():
    return render_template("assets.html",
                           user=current_user,
                           data=current_user.getAssets())


@views.route('/assets/delete-asset', methods=['POST'])
def delete_asset():
    asset = get_asset(request.data)
    if asset:
        db.session.delete(asset)
        db.session.commit()
    return jsonify({})


@views.route('/assets/asset/<asset_id>', methods=('GET', 'POST'))
@login_required
def view_asset(asset_id):
    # TODO: make sure only owner of asset can access it
    # view what fleet it's in
    asset = Asset.query.get(asset_id)  # get asset
    return render_template("asset.html",
                           user=current_user,
                           asset=asset)


@views.route('assets/new-asset', methods=['GET', 'POST'])
@login_required
def add_asset():
    # TODO: add to a fleet or can be null
    all_cat = Category.query.all()
    all_tech = Tech.query.all()
    num_cat = len(all_cat)
    num_tech = len(all_tech)

    if request.method == 'POST':
        asset_name = request.form.get('asset_name')
        asset_quantity = request.form.get('asset_quantity')
        asset_mileage = request.form.get('asset_mileage')
        asset_idle = request.form.get('asset_idle')
        asset_category_num = request.form.get('asset_category')
        asset_category = all_cat[int(asset_category_num)]
        asset_tech_num = request.form.get('asset_tech')
        asset_tech = all_tech[int(asset_tech_num)]

        nameexists = Asset.query.filter_by(name=asset_name).first()

        if not asset_name:
            flash('No name!', category='error')
        elif not asset_quantity:
            flash('No assets declared!', category='error')
        elif asset_quantity == 0:
            flash('0 assets!', category='error')
        elif not asset_mileage:
            flash('No remaining mileage!', category='error')
        elif not asset_idle:
            flash('No remaining idle time!', category='error')
        elif len(asset_name) < 1:
            flash('Name is too short!', category='error')
        elif nameexists:
            flash('Asset name taken!', category='error')
        else:
            new_asset = Asset(name=asset_name,
                              number=asset_quantity,
                              rem_mileage=asset_mileage,
                              rem_idle=asset_idle)
            new_ownsAsset = OwnsAsset(user_id=current_user.id,
                                      asset_id=new_asset.id)
            new_isInCategory = IsInCategory(asset_id=new_asset.id,
                                            category_id=asset_category.id)
            new_usesTech = UsesTech(asset_id=new_asset.id,
                                    tech_id=asset_tech.id)
            new_asset.ownsAssets = [new_ownsAsset]
            new_asset.isInCategory = [new_isInCategory]
            new_asset.usesTech = [new_usesTech]
            asset_category.isInCategory = [new_isInCategory]
            asset_tech.usesTech = [new_usesTech]

            db.session.add(new_asset)
            db.session.add(new_ownsAsset)
            db.session.add(new_isInCategory)
            db.session.add(new_usesTech)
            db.session.commit()
            flash('Asset added!', category='success')
            # redirect to asset page

    return render_template("new-asset.html",
                           user=current_user,
                           cats=all_cat,
                           num_cats=list(range(num_cat)),
                           techs=all_tech,
                           num_techs=list(range(num_tech)))


@views.route('/assets/edit-asset/<asset_id>', methods=('GET', 'POST'))
@login_required
def edit_asset(asset_id):
    # TODO: make sure only owner of asset can access it
    # TODO: make sure it's not None
    # Add to a fleet
    asset = Asset.query.get(asset_id)  # get asset
    all_cat = Category.query.all()
    all_tech = Tech.query.all()
    num_cat = len(all_cat)
    num_tech = len(all_tech)

    if request.method == 'POST':
        new_asset_name = request.form.get('asset_name')
        new_asset_quantity = request.form.get('asset_quantity')
        new_asset_mileage = request.form.get('asset_mileage')
        new_asset_idle = request.form.get('asset_idle')
        asset_category_num = request.form.get('asset_category')
        asset_tech_num = request.form.get('asset_tech')

        if new_asset_name:
            nameexists = Asset.query.filter_by(name=new_asset_name).first()
            if len(new_asset_name) < 1:
                flash('Name is too short!', category='error')
            elif nameexists:
                flash('Asset name taken!', category='error')
            else:
                asset.name = new_asset_name
        asset.number = new_asset_quantity
        asset.rem_mileage = new_asset_mileage
        asset.rem_idle = new_asset_idle
        new_category = all_cat[int(asset_category_num)]
        new_tech = all_tech[int(asset_tech_num)]
        asset.setTech(new_tech)
        asset.setCategory(new_category)
        db.session.commit()
        flash('Asset updated!', category='success')
    return render_template("edit-asset.html",
                           user=current_user,
                           asset=asset,
                           category=asset.getCategory()[0],
                           cats=all_cat,
                           tech=asset.getTech()[0],
                           techs=all_tech,
                           num_cats=list(range(num_cat)),
                           num_techs=list(range(num_tech)))


@views.route('assets/upload-assets', methods=['GET', 'POST'])
@login_required
def upload_assets():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # DO STUFF WITH FILES
            print(filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            open_file = open(UPLOAD_FOLDER + filename, 'r')
            lines = open_file.readlines()
            for line in lines:
                print(line)
            # return redirect(url_for('download_file', name=filename))
            # get file, create assets and fleet
    return render_template("upload-assets.html",
                           user=current_user)

    ######################
    ####### Fleets #######
    ######################


def get_fleet(req):
    fleet = json.loads(req)  # asset dictionary from click
    fleet = Fleet.query.get(fleet['fleetId'])  # get fleet
    managesFleet = ManagesFleet.query.filter_by(fleet_id=fleet.id).first()
    if (managesFleet.user_id == current_user.id):
        return fleet


@views.route('/fleets', methods=['GET', 'POST'])
@login_required
def view_fleets():
    return render_template("fleets.html",
                           user=current_user,
                           data=current_user.getFleets())


@views.route('/fleets/delete-fleet', methods=['POST'])
def delete_fleet():
    fleet = get_fleet(request.data)
    if fleet:
        db.session.delete(fleet)
        db.session.commit()
    return jsonify({})


@views.route('/fleets/fleet/<fleet_id>', methods=('GET', 'POST'))
@login_required
def view_fleet(fleet_id):
    # TODO: make sure only owner of asset can access it
    fleet = Fleet.query.get(fleet_id)  # get asset
    return render_template("fleet.html",
                           user=current_user,
                           fleet=fleet,
                           assets=fleet.getAssetsinFleet())


@views.route('/fleets/new-fleet', methods=['GET', 'POST'])
@login_required
def add_fleet():
    all_user_assets = current_user.getAssets()
    num_user_assets = len(all_user_assets)
    # show only assets not in a fleet
    if request.method == 'POST':
        fleet_name = request.form.get('fleet_name')
        fleet_description = request.form.get('fleet_description')
        fleet_assets = request.form.getlist('fleet_assets')
        int_fleet_assets = list(map(int, fleet_assets))
        nameexists = Fleet.query.filter_by(name=fleet_name).first()

        if len(fleet_name) < 1:
            flash('Name is too short!', category='error')
        elif nameexists:
            flash('Fleet name taken!', category='error')
        else:
            new_fleet = Fleet(name=fleet_name,
                              description=fleet_description,
                              containsAssets=[])
            db.session.add(new_fleet)
            new_managesFleet = ManagesFleet(user_id=current_user.id,
                                            fleet_id=new_fleet.id)
            new_fleet.managesFleets = [new_managesFleet]
            for int_asset in int_fleet_assets:
                asset = all_user_assets[int_asset]
                new_containsAsset = ContainsAsset(fleet_id=new_fleet.id,
                                                  asset_id=asset.id)
                new_fleet.containsAssets.append(new_containsAsset)
                db.session.add(new_containsAsset)

            db.session.add(new_managesFleet)
            db.session.commit()
            flash('fleet added!', category='success')

    return render_template("new-fleet.html",
                           user=current_user,
                           data=current_user.getFleets(),
                           assets=all_user_assets,
                           num_assets=list(range(num_user_assets)))


@views.route('/fleets/edit-fleet/<fleet_id>', methods=('GET', 'POST'))
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
            fleet.containsAssets.append(new_containsAsset)
            db.session.add(new_containsAsset)

        db.session.commit()
        flash('Fleet updated!', category='success')
    return render_template("edit-fleet.html",
                           user=current_user,
                           fleet=fleet,
                           assets=all_user_assets,
                           num_assets=list(range(num_user_assets)))

############################
####### Technologies #######
############################


def get_tech(req):
    tech = json.loads(req)  # asset dictionary from click
    tech = Tech.query.get(tech['techId'])  # get tech
    ownsTech = OwnsTech.query.filter_by(tech_id=tech.id).first()
    if (ownsTech.user_id == current_user.id):
        return tech


@views.route('/techs', methods=['GET', 'POST'])
@login_required
def view_techs():
    return render_template("techs.html",
                           user=current_user,
                           data=Tech.query.all())


@views.route('/techs/delete-tech', methods=['POST'])
def delete_tech():
    tech = get_tech(request.data)
    if tech:
        db.session.delete(tech)
        db.session.commit()
    return jsonify({})


@views.route('/techs/tech/<tech_id>', methods=('GET', 'POST'))
@login_required
def view_tech(tech_id):
    # TODO: make sure only owner of tech can access it
    # view what fleet it's in
    tech = Tech.query.get(tech_id)  # get tech
    return render_template("tech.html",
                           user=current_user,
                           tech=tech)


@views.route('techs/new-tech', methods=['GET', 'POST'])
@login_required
def add_tech():
    # TODO: add to a fleet or can be null

    if request.method == 'POST':
        tech_name = request.form.get('tech_name')
        tech_description = request.form.get('tech_description')

        nameexists = Tech.query.filter_by(name=tech_name).first()

        if not tech_name:
            flash('No name!', category='error')
        elif len(tech_name) < 1:
            flash('Name is too short!', category='error')
        elif nameexists:
            flash('tech name taken!', category='error')
        else:
            new_tech = Tech(name=tech_name,
                            description=tech_description)
            new_ownstech = OwnsTech(user_id=current_user.id,
                                    tech_id=new_tech.id)
            new_tech.ownsTech = [new_ownstech]

            db.session.add(new_tech)
            db.session.add(new_ownstech)
            db.session.commit()
            flash('Retrofit added!', category='success')
            # redirect to tech page

    return render_template("new-tech.html",
                           user=current_user)


@views.route('/techs/edit-tech/<tech_id>', methods=('GET', 'POST'))
@login_required
def edit_tech(tech_id):
    # TODO: make sure only owner of tech can access it
    # TODO: make sure it's not None
    # Add to a fleet
    tech = Tech.query.get(tech_id)  # get tech

    if request.method == 'POST':
        new_tech_name = request.form.get('tech_name')
        new_tech_description = request.form.get('tech_description')

        if new_tech_name:
            nameexists = Tech.query.filter_by(name=new_tech_name).first()
            if len(new_tech_name) < 1:
                flash('Name is too short!', category='error')
            elif nameexists:
                flash('tech name taken!', category='error')
            else:
                tech.name = new_tech_name
        tech.description = new_tech_description
        db.session.commit()
        flash('tech updated!', category='success')
    return render_template("edit-tech.html",
                           user=current_user,
                           tech=tech)
