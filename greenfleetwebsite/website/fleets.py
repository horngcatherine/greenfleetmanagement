from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json
import numpy as np

import os
from flask import Flask, redirect, url_for
from werkzeug.utils import secure_filename


def get_fleet(req):
    fleet = json.loads(req)  # asset dictionary from click
    fleet = Fleet.query.get(fleet['fleetId'])  # get fleet
    managesFleet = ManagesFleet.query.filter_by(fleet_id=fleet.id).first()
    if (managesFleet.user_id == current_user.id):
        return fleet


def add_fleet_to_db(fleet_name, fleet_description, int_fleet_assets, all_user_assets, asset_num_quant):
    new_fleet = Fleet(name=fleet_name,
                      description=fleet_description,
                      containsAssets=[])
    db.session.add(new_fleet)
    new_managesFleet = ManagesFleet(user_id=current_user.id,
                                    fleet_id=new_fleet.id)
    new_fleet.managesFleets.append(new_managesFleet)
    for i in range(len(int_fleet_assets)):
        asset = all_user_assets[int_fleet_assets[i][0]]
        tech = asset.getTech()[0][int_fleet_assets[i][1]]
        new_containsAsset = ContainsAsset(fleet_id=new_fleet.id,
                                          asset_id=asset.id,
                                          asset_tech_id=tech.id,
                                          num_assets=asset_num_quant[i])
        asset.containsAssets.append(new_containsAsset)
        new_fleet.containsAssets.append(new_containsAsset)
        db.session.add(new_containsAsset)

    db.session.add(new_managesFleet)
    db.session.commit()


def upload_fleet():
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
            fleet_assets = add_asset_from_csv(open_file)
            fleet_name = request.form.get('fleet_name')
            fleet_description = request.form.get('fleet_description')
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
                for asset in fleet_assets:
                    new_containsAsset = ContainsAsset(fleet_id=new_fleet.id,
                                                      asset_id=asset.id)
                    new_fleet.containsAssets.append(new_containsAsset)
                    db.session.add(new_containsAsset)

            db.session.add(new_managesFleet)
            db.session.commit()
            flash('Fleet added!', category='success')

    return render_template("upload-fleet.html",
                           user=current_user)
