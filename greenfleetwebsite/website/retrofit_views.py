from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from .assets import *
#from .retrofits import *

#########################
####### Retrofits #######
#########################

retrofit_views = Blueprint('retrofit_views', __name__)


@retrofit_views.route('/retrofits', methods=['GET', 'POST'])
@login_required
def view_techs():
    techs = []
    for t in Tech.query.all():
        if (t.public == True or t.getUser().id == current_user.id):  # or is owned by the owner
            techs.append(t)
    return render_template("retrofit_html/techs.html",
                           user=current_user,
                           data=techs)


def get_tech(req):
    tech = json.loads(req)  # asset dictionary from click
    tech = Tech.query.get(tech['techId'])  # get asset
    # list of all OwnsAssets that has the same asset id
    ownstech = OwnsTech.query.filter_by(tech_id=tech.id).first()
    if (ownstech.user_id == current_user.id):
        return tech


@retrofit_views.route('/retrofits/delete-retrofit', methods=['POST'])
def delete_retrofit():
    req = request.data
    tech = get_tech(req)
    if tech:
        ts = [tech.usesTech, tech.ownsTech, tech.opt,
              tech.reduxPollut, tech.applicableType, tech.longCost1,
              tech.longCost2, tech.shortCost1, tech.shortCost2]
        for t in ts:
            for a in t:
                db.session.delete(a)
        db.session.delete(tech)
        db.session.commit()
    return jsonify({})


@retrofit_views.route('/retrofits/retrofit/<retrofit_id>', methods=('GET', 'POST'))
@login_required
def view_retrofit(retrofit_id):
    tech = Tech.query.get(retrofit_id)  # get tech
    polluts = Pollutant.query.all()
    return render_template("retrofit_html/tech.html",
                           user=current_user,
                           tech=tech,
                           polluts=polluts)


@retrofit_views.route('/retrofits/new-retrofit', methods=['GET', 'POST'])
@login_required
def add_retrofit():
    all_asset_types = Type.query.all()
    all_polluts = Pollutant.query.all()
    all_techs = Tech.query.all()

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
                            public=False,
                            usesTech=[],
                            ownsTech=[],
                            opt=[],
                            applicableType=[],
                            longCost1=[],
                            longCost2=[],
                            shortCost1=[],
                            shortCost2=[])
            db.session.add(new_tech)
            db.session.commit()
            newOwnsTech = OwnsTech(user_id=current_user.id,
                                   tech_id=new_tech.id)
            db.session.add(newOwnsTech)
            db.session.commit()
            for pollut in all_polluts:
                redux = request.form.get(
                    'redux_'+str(pollut.id-1))
                newReduxPollut = ReduxPollut(pollut_id=pollut.id,
                                             tech_id=new_tech.id,
                                             redux=redux)
                newReduxPollut.link_ReduxPollut()
                db.session.add(newReduxPollut)
                db.session.commit()
            for type in all_asset_types:
                for tech in all_techs:
                    lc1 = request.form.get(
                        'lc_'+str(type.id-1)+'_'+str(tech.id-1)+'_this')
                    newLongCost1 = LongCost(tech1_id=tech.id,
                                            tech2_id=new_tech.id,
                                            type_id=type.id,
                                            cost=lc1)
                    lc2 = request.form.get(
                        'lc_'+str(type.id-1)+'_this_'+str(tech.id-1))
                    newLongCost2 = LongCost(tech1_id=new_tech.id,
                                            tech2_id=tech.id,
                                            type_id=type.id,
                                            cost=lc2)
                    newLongCost1.link_LongCost()
                    db.session.add(newLongCost1)
                    newLongCost2.link_LongCost()
                    db.session.add(newLongCost2)
                    sc1 = request.form.get(
                        'sc_'+str(type.id-1)+'_'+str(tech.id-1)+'_this')
                    sc2 = request.form.get(
                        'sc_'+str(type.id-1)+'_this_'+str(tech.id-1))
                    newShortCost1 = ShortCost(tech1_id=tech.id,
                                              tech2_id=new_tech.id,
                                              type_id=type.id,
                                              cost=sc1)
                    newShortCost2 = ShortCost(tech1_id=new_tech.id,
                                              tech2_id=tech.id,
                                              type_id=type.id,
                                              cost=sc2)
                    newShortCost1.link_ShortCost()
                    db.session.add(newShortCost1)
                    newShortCost2.link_ShortCost()
                    db.session.add(newShortCost2)
                    db.session.commit()

                newShortCost = ShortCost(tech1_id=new_tech.id,
                                         tech2_id=new_tech.id,
                                         type_id=type.id,
                                         cost=0)
                newLongCost = LongCost(tech1_id=new_tech.id,
                                       tech2_id=new_tech.id,
                                       type_id=type.id,
                                       cost=0)
                db.session.add(newShortCost)
                db.session.add(newLongCost)
                db.session.commit()
                newShortCost.link_ShortCost()
                newLongCost.link_LongCost()

                applicable = request.form.getlist('applicable')
                for ap in applicable:
                    type = all_asset_types[int(ap)]
                    newApplicableType = ApplicableType(
                        tech_id=new_tech.id, type_id=type.id)
                    newApplicableType.link_ApplicableType()
                    db.session.add(newApplicableType)
                    db.session.commit()

            flash('Retrofit added!', category='success')
            # redirect to tech page
            return view_techs()

    return render_template("retrofit_html/new-tech.html",
                           user=current_user,
                           types=all_asset_types,
                           polluts=all_polluts,
                           techs=all_techs,
                           num_types=range(len(all_asset_types)),
                           num_polluts=range(len(all_polluts)),
                           num_techs=range(len(all_techs)))


@retrofit_views.route('/retrofits/edit-retrofit/<retrofit_id>', methods=('GET', 'POST'))
@login_required
def edit_retrofit(retrofit_id):
    tech = Tech.query.get(retrofit_id)  # get tech

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
    return render_template("retrofit_html/edit-tech.html",
                           user=current_user,
                           tech=tech)
