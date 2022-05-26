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
                        opt=[],
                        reduxPollut=[]
                        )
    pollut2 = Pollutant(name="CO",
                        description="Description of CO",
                        public=True,
                        opt=[],
                        reduxPollut=[]
                        )
    pollut3 = Pollutant(name="NOx",
                        description="Description of NOx",
                        public=True,
                        opt=[],
                        reduxPollut=[]
                        )
    pollut4 = Pollutant(name="VOC",
                        description="Description of VOC",
                        public=True,
                        opt=[],
                        reduxPollut=[]
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
    all_types = Type.query.all()
    tech1 = Tech(name="None",
                 description="No retrofit used.",
                 public=True,
                 usesTech=[],
                 opt=[],
                 reduxPollut=[],
                 applicableType=[],
                 longCost1=[], longCost2=[],
                 shortCost1=[], shortCost2=[])
    tech2 = Tech(name="DOC",
                 description="Retrofit DOC.",
                 public=True,
                 usesTech=[],
                 opt=[],
                 reduxPollut=[],
                 applicableType=[],
                 longCost1=[], longCost2=[],
                 shortCost1=[], shortCost2=[])
    tech3 = Tech(name="FTF",
                 description="Retrofit FTF.",
                 public=True,
                 usesTech=[],
                 opt=[],
                 reduxPollut=[],
                 applicableType=[],
                 longCost1=[], longCost2=[],
                 shortCost1=[], shortCost2=[])
    tech4 = Tech(name="pass DPF",
                 description="Retrofit pass DPF.",
                 public=True,
                 usesTech=[],
                 opt=[],
                 reduxPollut=[],
                 applicableType=[],
                 longCost1=[], longCost2=[],
                 shortCost1=[], shortCost2=[])
    tech5 = Tech(name="act DPF",
                 description="Retrofit act DPF.",
                 public=True,
                 usesTech=[],
                 opt=[],
                 reduxPollut=[],
                 applicableType=[],
                 longCost1=[], longCost2=[],
                 shortCost1=[], shortCost2=[])
    tech6 = Tech(name="new 2008",
                 description="Retrofit new 2008.",
                 public=True,
                 usesTech=[],
                 opt=[],
                 reduxPollut=[],
                 applicableType=[],
                 longCost1=[], longCost2=[],
                 shortCost1=[], shortCost2=[])
    tech7 = Tech(name="CNG Converted",
                 description="Retrofit CNG Converted.",
                 public=True,
                 usesTech=[],
                 opt=[],
                 reduxPollut=[],
                 applicableType=[],
                 longCost1=[], longCost2=[],
                 shortCost1=[], shortCost2=[])
    techs = [tech1, tech2, tech3, tech4, tech5, tech6, tech7]
    for t in techs:
        db.session.add(t)
    db.session.commit()
    add_reduxpolluts(tech2, tech3, tech4, tech5, tech6, tech7)
    add_applicable_types(all_types, techs)
    add_zerocosts(tech1, tech2, tech3, tech4, tech5, tech6, tech7)
    add_costs(tech1, tech2, tech3, tech4, tech5, tech6, tech7)
    db.session.commit()


def add_reduxpolluts(tech2, tech3, tech4, tech5, tech6, tech7):
    rp1 = ReduxPollut(tech_id=tech2.id, pollut_id=1, redux=0.75)
    rp2 = ReduxPollut(tech_id=tech2.id, pollut_id=2, redux=0.6)
    rp3 = ReduxPollut(tech_id=tech2.id, pollut_id=3, redux=1)
    rp4 = ReduxPollut(tech_id=tech2.id, pollut_id=4, redux=0.5)
    rp5 = ReduxPollut(tech_id=tech3.id, pollut_id=1, redux=0.5)
    rp6 = ReduxPollut(tech_id=tech3.id, pollut_id=2, redux=0.7)
    rp7 = ReduxPollut(tech_id=tech3.id, pollut_id=3, redux=1)
    rp8 = ReduxPollut(tech_id=tech3.id, pollut_id=4, redux=0.7)
    rp9 = ReduxPollut(tech_id=tech4.id, pollut_id=1, redux=0.15)
    rp10 = ReduxPollut(tech_id=tech4.id, pollut_id=2, redux=0.2)
    rp11 = ReduxPollut(tech_id=tech4.id, pollut_id=3, redux=1)
    rp12 = ReduxPollut(tech_id=tech4.id, pollut_id=4, redux=0.05)
    rp13 = ReduxPollut(tech_id=tech5.id, pollut_id=1, redux=0.15)
    rp14 = ReduxPollut(tech_id=tech5.id, pollut_id=2, redux=0.2)
    rp15 = ReduxPollut(tech_id=tech5.id, pollut_id=3, redux=1)
    rp16 = ReduxPollut(tech_id=tech5.id, pollut_id=4, redux=0.05)
    rp17 = ReduxPollut(tech_id=tech6.id, pollut_id=1, redux=1)
    rp18 = ReduxPollut(tech_id=tech6.id, pollut_id=2, redux=1)
    rp19 = ReduxPollut(tech_id=tech6.id, pollut_id=3, redux=1)
    rp20 = ReduxPollut(tech_id=tech6.id, pollut_id=4, redux=1)
    rp21 = ReduxPollut(tech_id=tech7.id, pollut_id=1, redux=1)
    rp22 = ReduxPollut(tech_id=tech7.id, pollut_id=2, redux=1)
    rp23 = ReduxPollut(tech_id=tech7.id, pollut_id=3, redux=1)
    rp24 = ReduxPollut(tech_id=tech7.id, pollut_id=4, redux=1)
    all_r = [rp1, rp2, rp3, rp4, rp5, rp6, rp7, rp8, rp9, rp10, rp11, rp12,
             rp13, rp14, rp15, rp16, rp17, rp18, rp19, rp20, rp21, rp22, rp23, rp24]
    for r in all_r:
        r.link_ReduxPollut()
        db.session.add(r)


def add_sc_dotio(c, t1, t2):
    for t in range(1, 6):
        sc = ShortCost(tech1_id=t1.id, tech2_id=t2.id, type_id=t, cost=c)
        db.session.add(sc)
    db.session.commit()


def add_lc_dotio(c, t1, t2):
    for t in range(1, 6):
        lc = LongCost(tech1_id=t1.id, tech2_id=t2.id, type_id=t, cost=c)
        db.session.add(lc)
    db.session.commit()


def add_lc_school(c, t1, t2):
    for t in range(6, 8):
        sc = LongCost(tech1_id=t1.id, tech2_id=t2.id, type_id=t, cost=c)
        db.session.add(sc)
    db.session.commit()


def add_sc_school(c, t1, t2):
    for t in range(6, 8):
        sc = ShortCost(tech1_id=t1.id, tech2_id=t2.id, type_id=t, cost=c)
        db.session.add(sc)
    db.session.commit()


def add_costs(tech1, tech2, tech3, tech4, tech5, tech6, tech7):
    techs = [tech1, tech2, tech3, tech4, tech5, tech6, tech7]
    for t in techs:
        if t.id != tech2:
            add_sc_dotio(1660, t, tech2)
            add_lc_dotio(1660, t, tech2)
            add_sc_school(1000, t, tech2)
            add_lc_school(1000, t, tech2)
        if t.id != tech3:
            add_sc_dotio(8260, t, tech3)
            add_lc_dotio(8260, t, tech3)
            add_sc_school(8260, t, tech3)
            add_lc_school(8260, t, tech3)
        if t.id != tech4:
            add_sc_dotio(15240, t, tech4)
            add_lc_dotio(15240, t, tech4)
            add_sc_school(8000, t, tech4)
            add_lc_school(8000, t, tech4)
        if t.id != tech5:
            add_sc_dotio(16693, t, tech5)
            add_lc_dotio(16693, t, tech5)
            add_sc_school(16000, t, tech5)
            add_lc_school(16000, t, tech5)
        if t.id != tech6:
            add_sc_dotio(10000, t, tech6)
            add_lc_dotio(10000, t, tech6)
            add_sc_school(10000, t, tech6)
            add_lc_school(10000, t, tech6)
        if t.id != tech7:
            add_sc_dotio(25000, t, tech7)
            add_lc_dotio(25000, t, tech7)
            add_sc_school(70000, t, tech7)
            add_lc_school(70000, t, tech7)
    add_sc_dotio(80, tech2, tech1)
    add_sc_dotio(80, tech3, tech1)
    add_lc_dotio(80, tech2, tech1)
    add_lc_dotio(80, tech3, tech1)
    add_sc_dotio(120, tech4, tech1)
    add_lc_dotio(180, tech4, tech1)
    add_sc_dotio(180, tech5, tech1)
    add_lc_dotio(180, tech5, tech1)
    add_sc_dotio(0, tech6, tech1)
    add_sc_dotio(0, tech7, tech1)
    add_lc_dotio(0, tech6, tech1)
    add_lc_dotio(0, tech7, tech1)
    add_sc_school(40, tech2, tech1)
    add_lc_school(40, tech2, tech1)
    add_sc_school(40, tech3, tech1)
    add_lc_school(40, tech3, tech1)
    add_sc_school(60, tech4, tech1)
    add_lc_school(60, tech4, tech1)
    add_sc_school(80, tech5, tech1)
    add_lc_school(80, tech5, tech1)
    add_sc_school(0, tech6, tech1)
    add_lc_school(0, tech6, tech1)
    add_sc_school(0, tech7, tech1)
    add_lc_school(0, tech7, tech1)


def add_zerocosts(tech1, tech2, tech3, tech4, tech5, tech6, tech7):
    for t in [tech1, tech2, tech3, tech4, tech5, tech6, tech7]:
        for typ in range(1, 7):
            lc = LongCost(tech1_id=t.id, tech2_id=t.id, type_id=typ, cost=0)
            sc = ShortCost(tech1_id=t.id, tech2_id=t.id, type_id=typ, cost=0)
            db.session.add(lc)
            db.session.add(sc)
    db.session.commit()


def add_applicable_types(types, techs):
    for type in types:
        for tech in techs:
            new_at = ApplicableType(tech_id=tech.id, type_id=type.id)
            db.session.add(new_at)
            db.session.commit()
            new_at.link_ApplicableType()

# rendering the HTML page which has the button


@views.route('/json')
def json():
    return render_template('json.html')


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/information')
def information():
    return render_template("information.html", user=current_user)


@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def get_dash():
    assets = current_user.getAssets()
    fleets = current_user.getFleets()
    techs = current_user.getTechs()
    return render_template("dashboard.html",
                           user=current_user,
                           assets=assets,
                           fleets=fleets,
                           techs=techs)


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
