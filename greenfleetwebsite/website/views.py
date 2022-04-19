from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from .assets import *
from .fleets import *
from .optimization import *
from .retrofit3Cost import *

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


def add_asset_types():
    assettype1 = Type(name="Class 8, low mileage",
                           description="Description of low mileage class 8 vehicle.",
                           ofAssetType=[])
    assettype2 = Type(name="Class 8, high mileage",
                           description="Description of high mileage class 8 vehicle.",
                           ofAssetType=[])
    assettype3 = Type(name="Class 6, low mileage",
                           description="Description of low mileage class 6 vehicle.",
                           ofAssetType=[])
    assettype4 = Type(name="Class 6, high mileage",
                           description="Description of high mileage class 6 vehicle.",
                           ofAssetType=[])
    assettype5 = Type(name="Long school bus",
                           description="Description of long school bus vehicle.",
                           ofAssetType=[])
    assettype6 = Type(name="Short school bus",
                           description="Description of short school bus vehicle.",
                           ofAssetType=[])
    db.session.add(assettype1)
    db.session.add(assettype2)
    db.session.add(assettype3)
    db.session.add(assettype4)
    db.session.add(assettype5)
    db.session.add(assettype6)
    db.session.commit()


def add_polluts():
    pollut1 = Pollutant(name="PM2.5",
                        description="Description of PM2.5",
                        public=True,
                        opt=[]
                        )
    pollut2 = Pollutant(name="CO",
                        description="Description of CO",
                        public=True,
                        opt=[]
                        )
    pollut3 = Pollutant(name="NOx",
                        description="Description of NOx",
                        public=True,
                        opt=[]
                        )
    pollut4 = Pollutant(name="VOC",
                        description="Description of VOC",
                        public=True,
                        opt=[]
                        )
    db.session.add(pollut1)
    db.session.add(pollut2)
    db.session.add(pollut3)
    db.session.add(pollut4)
    db.session.commit()


def add_objectives():
    opt1 = Objective(name="Long Term Cost",
                     description="Objective to minimize long term cost.",
                     opt=[])
    opt2 = Objective(name="Short Term Cost",
                     description="Objective to minimize short term cost.",
                     opt=[])
    opt3 = Objective(name="PM2.5 Emission",
                     description="Objective to minimize PM2.5 emission.",
                     opt=[])
    opt4 = Objective(name="CO Emission",
                     description="Objective to minimize CO emission.",
                     opt=[])
    opt5 = Objective(name="NOx Emission",
                     description="Objective to minimize NOx emission.",
                     opt=[])
    opt6 = Objective(name="HC Emission",
                     description="Objective to minimize HC emission.",
                     opt=[])
    db.session.add(opt1)
    db.session.add(opt2)
    db.session.add(opt3)
    db.session.add(opt4)
    db.session.add(opt5)
    db.session.add(opt6)
    db.session.commit()


def add_categories():
    cat1 = Category(name="Category 1",
                    description="Category 1 description.",
                    isInCategory=[])
    cat2 = Category(name="Category 2",
                    description="Category 2 description.",
                    isInCategory=[])
    db.session.add(cat1)
    db.session.add(cat2)
    db.session.commit()


def add_techs():
    tech1 = Tech(name="None",
                 description="No retrofit used.",
                 public=True,
                 usesTech=[],
                 opt=[])
    tech2 = Tech(name="DOC",
                 description="Retrofit DOC.",
                 public=True,
                 usesTech=[],
                 opt=[])
    tech3 = Tech(name="FTF",
                 description="Retrofit FTF.",
                 public=True,
                 usesTech=[],
                 opt=[])
    tech4 = Tech(name="pass DPF",
                 description="Retrofit pass DPF.",
                 public=True,
                 usesTech=[],
                 opt=[])
    tech5 = Tech(name="act DPF",
                 description="Retrofit act DPF.",
                 public=True,
                 usesTech=[],
                 opt=[])
    tech6 = Tech(name="new 2008",
                 description="Retrofit new 2008.",
                 public=True,
                 usesTech=[],
                 opt=[])
    tech7 = Tech(name="CNG Converted",
                 description="Retrofit CNG Converted.",
                 public=True,
                 usesTech=[],
                 opt=[])
    db.session.add(tech1)
    db.session.add(tech2)
    db.session.add(tech3)
    db.session.add(tech4)
    db.session.add(tech5)
    db.session.add(tech6)
    db.session.add(tech7)
    db.session.commit()


@views.route('/')
def home():
    # add_asset_types()
    # add_polluts()
    # add_objectives()
    # add_categories()
    # add_techs()
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


############################
####### Technologies #######
############################


@views.route('/techs', methods=['GET', 'POST'])
@login_required
def view_techs():
    techs = []
    for t in Tech.query.all():
        if (t.public == True):  # or is owned by the owner
            techs.append(t)
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
                            description=tech_description,
                            public=False)
            db.session.add(new_tech)
            db.session.commit()
            flash('Retrofit added!', category='success')
            # redirect to tech page
            return view_techs()

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

############################
####### Categories #######
############################


@views.route('/categories', methods=['GET', 'POST'])
@login_required
def view_categories():
    return render_template("categories.html",
                           user=current_user,
                           data=Category.query.all())


@views.route('/categories/delete-category', methods=['POST'])
def delete_category():
    category = get_category(request.data)
    if category:
        db.session.delete(category)
        db.session.commit()
    return jsonify({})


@views.route('/categories/category/<category_id>', methods=('GET', 'POST'))
@login_required
def view_category(category_id):
    # TODO: make sure only owner of category can access it
    # view what fleet it's in
    category = Category.query.get(category_id)  # get category
    return render_template("category.html",
                           user=current_user,
                           category=category)


@views.route('categories/new-category', methods=['GET', 'POST'])
@login_required
def add_category():
    # TODO: add to a fleet or can be null

    if request.method == 'POST':
        category_name = request.form.get('category_name')
        category_description = request.form.get('category_description')

        nameexists = Category.query.filter_by(name=category_name).first()

        if not category_name:
            flash('No name!', category='error')
        elif len(category_name) < 1:
            flash('Name is too short!', category='error')
        elif nameexists:
            flash('category name taken!', category='error')
        else:
            new_category = Category(name=category_name,
                                    description=category_description)

            db.session.add(new_category)
            db.session.commit()
            flash('Category added!', category='success')
            # redirect to category page
            return render_template("categories.html",
                                   user=current_user,
                                   data=Category.query.all())

    return render_template("new-category.html",
                           user=current_user)


@views.route('/categories/edit-category/<category_id>', methods=('GET', 'POST'))
@login_required
def edit_category(category_id):
    # TODO: make sure only owner of category can access it
    # TODO: make sure it's not None
    # Add to a fleet
    category = Tech.query.get(category_id)  # get category

    if request.method == 'POST':
        new_category_name = request.form.get('category_name')
        new_category_description = request.form.get('category_description')

        if new_category_name:
            nameexists = Category.query.filter_by(
                name=new_category_name).first()
            if len(new_category_name) < 1:
                flash('Name is too short!', category='error')
            elif nameexists:
                flash('category name taken!', category='error')
            else:
                category.name = new_category_name
        category.description = new_category_description
        db.session.commit()
        flash('category updated!', category='success')
    return render_template("edit-category.html",
                           user=current_user,
                           category=category)
