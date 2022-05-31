from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
from .assets import *
from .fleets import *
from .optimization import *
from .retrofit3Cost import *

############################
####### Optimization #######
############################

rec_views = Blueprint('rec_views', __name__)


@rec_views.route('/recommendations', methods=['GET', 'POST'])
@login_required
def view_recommendations():
    opts = current_user.getScenarios()
    return render_template("rec_html/recommendations.html",
                           user=current_user,
                           data=opts)


def add_rec_to_db(name, shortbudget, longbudget, redux, int_polluts, polls, obj, fleet):
    new_opt = Optimization(name=name,
                           short_budget=shortbudget,
                           long_budget=longbudget,
                           em_redux_req=redux,
                           fleet=[],
                           objective=[],
                           pollutants=[],
                           retrofits=[])
    db.session.add(new_opt)
    db.session.commit()

    for p in int_polluts:
        pollut = polls[p]
        new_optpollut = OptPollut(opt_id=new_opt.id,
                                  pollut_id=pollut.id)
        new_optpollut.link_OptPollut()

    new_optobj = OptObj(opt_id=new_opt.id,
                        obj_id=obj.id)
    new_optobj.link_OptObj()

    new_optwith = OptWith(opt_id=new_opt.id,
                          fleet_id=fleet.id)
    new_optwith.link_OptWith()

    db.session.commit()
    return new_opt


@rec_views.route('/recommendations/new-rec', methods=('GET', 'POST'))
@login_required
def new_recommendation():
    # fleet = Fleet.query.get(fleet_id)
    fleets = current_user.getFleets()
    num_fleets = len(fleets)
    objs = Objective.query.all()
    num_obj = len(objs)
    rets = Tech.query.all()
    num_rets = len(rets)
    polls = Pollutant.query.all()
    num_pol = len(polls)
    if request.method == 'POST':
        name = request.form.get('name')
        fleet_num = request.form.get('fleet')
        fleet = fleets[int(fleet_num)]
        shortbudget = float(request.form.get('shortbudget'))
        longbudget = float(request.form.get('longbudget'))
        redux = request.form.get('redux')
        obj_num = request.form.get('obj')
        obj = objs[int(obj_num)]
        polluts = request.form.getlist('rec_polluts')
        int_polluts = list(map(int, polluts))
        new_opt = add_rec_to_db(name, shortbudget, longbudget, redux,
                                int_polluts, polls, obj, fleet)
        return redirect(url_for('rec_views.get_rec_retros', fleet_id=fleet.id, opt_id=new_opt.id))
    return render_template("rec_html/new-rec.html",
                           num_fleets=list(range(num_fleets)),
                           fleets=fleets,
                           num_obj=list(range(num_obj)),
                           objs=objs,
                           polls=polls,
                           num_pol=list(range(num_pol)),
                           user=current_user)


@rec_views.route('/recommendations/rec-setup/rec-retros/<fleet_id>/<opt_id>', methods=('GET', 'POST'))
@login_required
def get_rec_retros(opt_id, fleet_id):
    fleet = Fleet.query.get(fleet_id)
    rets = Tech.query.all()
    num_rets = len(rets)
    opt = Optimization.query.get(opt_id)
    used_rets = fleet.getAssetsinFleet()[1]
    used = []
    [used.append(x) for x in used_rets if x not in used]
    techs = request.form.getlist('rec_techs')
    int_techs = list(map(int, techs))
    if request.method == "POST":
        for r in used:
            int_techs.append(r.id-1)
        for t in int_techs:
            tech = rets[t]
            new_opttech = OptTech(opt_id=opt.id,
                                  tech_id=tech.id)
            new_opttech.link_OptTech()
        db.session.commit()
        return redirect(url_for('rec_views.get_upper_bounds', opt_id=opt.id, fleet_id=fleet.id))
    return render_template("rec_html/rec-retros.html",
                           used=used,
                           fleet=Fleet.query.get(fleet_id),
                           num_retros=list(range(num_rets)),
                           retros=rets,
                           user=current_user)


@rec_views.route('/recommendations/rec-setup/upper-bounds/<fleet_id>/<opt_id>', methods=('GET', 'POST'))
@login_required
def get_upper_bounds(opt_id, fleet_id):
    opt = Optimization.query.get(opt_id)
    retros = opt.get_retrofits()
    assets = opt.get_assets()
    num_retros = len(retros)
    num_assets = len(assets)
    if request.method == "POST":
        upper_bounds = np.zeros((num_assets, num_retros, num_retros))
        for i in range(num_assets):
            for j in range(num_retros):
                for k in range(num_retros):
                    input = request.form.get(str(i)+"_"+str(j)+"_"+str(k))
                    upper_bounds[i][j][k] = int(input)
        return redirect(url_for('rec_views.recommendation', rec_id=opt.id, upper_bounds=upper_bounds))

    return render_template("rec_html/rec-upper-bounds.html",
                           fleet=Fleet.query.get(fleet_id),
                           num_retros=list(range(num_retros)),
                           retros=retros,
                           num_assets=list(range(num_assets)),
                           assets=assets,
                           user=current_user)


@rec_views.route('/recommendations/<rec_id>', methods=('GET', 'POST'))
@login_required
def recommendation(rec_id):
    # get the information to be put in csv
    rec = Optimization.query.get(rec_id)
    fleet = rec.get_fleet()
    assets = rec.get_assets()
    objective = rec.get_objective()
    polluts = rec.get_pollutants()
    retros = rec.get_retrofits()
    em_redux_req = rec.get_em_redux_req()
    sb = rec.short_budget
    lb = rec.long_budget
    #budgets = rec.budgets
    #longbudgets = rec.longbudgets
    req = request.args['upper_bounds']
    str = req.replace('.', ',').replace(
        '[', '').replace(']', '').replace('\n', '').replace(' ', '')
    input = np.fromstring(str[:-1], sep=',')
    upper_bounds = input.reshape((len(assets), len(retros), len(retros)))
    rem_mil_np, rem_idle_np = get_miles_idle_remaining(fleet)
    disc_cost, init_cost = get_costs(fleet, retros)
    init_fleet = get_current_fleet(fleet, retros)
    print("Init fleet: ")
    print(init_fleet)
    run_em_rate, id_em_rate = get_er(fleet, polluts, retros)
    model_file = '/Users/catherine/Desktop/cornell/greenfleet/greenfleetmanagement/greenfleetwebsite/example/retrofit3.mod'
    nv, wout, w, obj, message = run_optimization(model_file, objective,
                                                 rem_mil_np, rem_idle_np, init_fleet, disc_cost, init_cost,
                                                 upper_bounds, run_em_rate, id_em_rate,
                                                 len(assets), len(
                                                     retros), len(polluts),
                                                 em_redux_req, sb, lb,
                                                 cost=True, budgets=None, longbudgets=None,
                                                 )
    num_veh = []
    num_veh_array = []
    for row in nv.toPandas().iterrows():
        val = int(row[1].values[0])
        a, t1, t2 = row[0]
        num_veh_array.append([int(a)-1, int(t1)-1, int(t2)-1, int(val)])
        if val != 0:
            num_veh.append((assets[int(a)-1].name,
                            retros[int(t1)-1].name,
                            retros[int(t2)-1].name,
                            val))

    without = []
    for row in wout.toPandas().iterrows():
        without.append(float(row[1].values[0]))

    withchange = []
    for row in w.toPandas().iterrows():
        withchange.append(float(row[1].values[0]))

    solved = True
    if (message == 'infeasible'):
        flash("This optimization is infeasible. Try again.", category='error')
        return new_recommendation()
    else:
        flash("Optimal solution found!", category='success')

    if request.method == "POST":
        rec.upper_bounds = array_to_bytes(upper_bounds)
        rec.objective_results = obj.toPandas().iloc[0][0]
        rec.num_veh = array_to_bytes(np.asarray(num_veh_array))
        rec.with_results = array_to_bytes(np.asarray(withchange))
        rec.without_results = array_to_bytes(np.asarray(without))
        db.session.add(rec)
        db.session.commit()
        new_saved_opt = SavedOpt(user_id=current_user.id, opt_id=rec.id)
        db.session.add(new_saved_opt)
        db.session.commit()
        new_saved_opt.link_SavedOpt()
        # save upper bounds an results
        # save both as strings? separate functions to parse the strings.
        return view_recommendations()

    return render_template("rec_html/recommendation.html",
                           opt=rec,
                           obj=obj,
                           solved=solved,
                           #    assets=assets,
                           num_vehicles=num_veh,
                           em_wout_retro=without,
                           em_w_retro=withchange,
                           user=current_user)


@rec_views.route('/recommendations/recommendation/<rec_id>', methods=('GET', 'POST'))
@login_required
def view_recommendation(rec_id):
    """
    this is only if saved, the other is for when you immediately get the rec
    """
    rec = Optimization.query.get(rec_id)
    fleet = rec.get_fleet()
    assets = rec.get_assets()
    objective = rec.get_objective()
    polluts = rec.get_pollutants()
    retros = rec.get_retrofits()
    em_redux_req = rec.get_em_redux_req()
    sb = rec.short_budget
    lb = rec.long_budget
    res, em_w_retro, em_wout_retro, nv = rec.get_results()
    num_veh = []
    for row in nv:
        a = row[0]
        t1 = row[1]
        t2 = row[2]
        val = row[3]
        if val != 0:
            num_veh.append((assets[int(a)].name,
                            retros[int(t1)].name,
                            retros[int(t2)].name,
                            val))

    return render_template("rec_html/view_recommendation.html",
                           fleet=fleet,
                           opt=rec,
                           obj=objective,
                           polluts=polluts,
                           retros=retros,
                           em_redux_req=em_redux_req,
                           sb=sb, lb=lb,
                           res=res,
                           nv=num_veh,
                           em_wout_retro=em_wout_retro,
                           em_w_retro=em_w_retro,
                           user=current_user)


def array_to_bytes(array):
    # get to string like [a,a,a,a,a]
    num_elem = array.size
    reshaped = array.reshape(num_elem)
    return reshaped.tobytes()
