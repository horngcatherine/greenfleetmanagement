from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from .assets import *
from .fleets import *
from .views import views

######################
####### Assets #######
######################

asset_views = Blueprint('asset_views', __name__)


@asset_views.route('/assets', methods=['GET', 'POST'])
@login_required
def view_assets():
    return render_template("assets.html",
                           user=current_user,
                           data=current_user.getAssets())


@asset_views.route('/assets/delete-asset', methods=['POST'])
def delete_asset():
    asset = get_asset(request.data)
    if asset:
        db.session.delete(asset)
        db.session.commit()
    return jsonify({})


@asset_views.route('/assets/asset/<asset_id>', methods=('GET', 'POST'))
@login_required
def view_asset(asset_id):
    # TODO: make sure only owner of asset can access it
    # view what fleet it's in
    asset = Asset.query.get(asset_id)  # get asset
    return render_template("asset.html",
                           user=current_user,
                           asset=asset)


@asset_views.route('assets/new-asset', methods=['GET', 'POST'])
@login_required
def add_asset():
    # TODO: add to a fleet or can be null
    all_asset_types = Type.query.all()
    all_cat = Category.query.all()
    all_tech = Tech.query.all()
    num_typ = len(all_asset_types)
    num_cat = len(all_cat)
    num_tech = len(all_tech)

    if request.method == 'POST':
        assettyp_num = request.form.get('asset')
        asset_name = request.form.get('asset_name')
        asset_type = all_asset_types[int(assettyp_num)]

        asset_made = request.form.get('asset_made')
        asset_remaining = request.form.get('asset_remaining')

        asset_category_num = request.form.get('asset_category')
        asset_category = all_cat[int(asset_category_num)]

        asset_techs = request.form.getlist('asset_tech')
        int_asset_techs = list(map(int, asset_techs))

        asset_tech = []
        for int_at in int_asset_techs:
            asset_tech.append(all_tech[int_at])

        asset_tech_num = request.form.get('asset_tech_quant').replace(" ", "")
        str_quants = asset_tech_num.split(",")
        asset_tech_quant = []
        for str in str_quants:
            asset_tech_quant.append(int(str))

        if not asset_type:
            flash('No selected asset type!', category='error')
        elif not asset_made:
            flash('No year asset!', category='error')
        elif asset_remaining == 0:
            flash('No years remaining!', category='error')
        elif not asset_category:
            flash('No category!', category='error')
        elif len(asset_tech) == 0:
            flash('No retrofit!', category='error')
        elif len(int_asset_techs) != len(asset_tech_quant):
            flash('Not enough quantities provided!', category='error')
        else:
            add_asset_to_db(asset_name,
                            int(asset_made),
                            int(asset_remaining),
                            asset_type,
                            asset_category,
                            asset_tech,
                            asset_tech_quant)
            flash('Asset added!', category='success')
            # redirect to asset page
            return view_assets()

    return render_template("new-asset.html",
                           user=current_user,
                           typs=all_asset_types,
                           num_typs=list(range(num_typ)),
                           cats=all_cat,
                           num_cats=list(range(num_cat)),
                           techs=all_tech,
                           num_techs=list(range(num_tech)))


@asset_views.route('/assets/edit-asset/<asset_id>', methods=('GET', 'POST'))
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
                           category=asset.getCategory(),
                           cats=all_cat,
                           tech=asset.getTech(),
                           techs=all_tech,
                           num_cats=list(range(num_cat)),
                           num_techs=list(range(num_tech)))


@asset_views.route('assets/upload-assets', methods=['GET', 'POST'])
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
            add_asset_from_csv(open_file)
            flash('Assets added!', category='success')
    return render_template("upload-assets.html",
                           user=current_user)
