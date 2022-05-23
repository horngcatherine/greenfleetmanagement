from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    managesFleets = db.relationship('ManagesFleet', cascade="all, delete")
    ownsTech = db.relationship('OwnsTech', cascade="all, delete")
    ownsAssets = db.relationship('OwnsAsset', cascade="all, delete")

    def getAssets(self):
        """
        Returns the assets the user owns.
        """
        assets = []
        # query to get all ownsAssets with
        ownsAssets = OwnsAsset.query.filter_by(user_id=self.id).all()
        for ownsasset in ownsAssets:  # ownsAsset is of type OwnsAsset
            assets_owned = Asset.query.filter_by(id=ownsasset.asset_id).all()
            for asset in assets_owned:
                assets.append(asset)
        return assets

    def getFleets(self):
        """
        Returns the fleets the user manages
        """
        fleets = []
        # query to get all ownsAssets with
        managesFleets = ManagesFleet.query.filter_by(user_id=self.id).all()
        for managesFleet in managesFleets:  # ownsAsset is of type OwnsAsset
            fleets_managed = Fleet.query.filter_by(
                id=managesFleet.fleet_id).all()
            for fleet in fleets_managed:
                fleets.append(fleet)
        return fleets

    def getTechs(self):
        techs = []
        ownsTech = OwnsTech.query.filter_by(user_id=self.id).all()
        for ot in ownsTech:
            techs_owned = Tech.query.filter_by(id=ot.tech_id).all()
            for to in techs_owned:
                techs.append(to)
        return techs


class Fleet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    containsAssets = db.relationship('ContainsAsset')
    managesFleets = db.relationship('ManagesFleet')
    opt = db.relationship('OptWith')

    def getAssetsinFleet(self):
        """
        Returns the assets in the fleet.
        """
        # ContainsAssets where the fleet id matches the fleet id
        containsAssets = ContainsAsset.query.filter_by(fleet_id=self.id).all()
        assets = []
        techs = []
        nums = []
        for containsAsset in containsAssets:
            # get assets with the same id as the asset id in containsAsset
            assets.append(containsAsset.get_assets())
            techs.append(containsAsset.get_tech())
            nums.append(containsAsset.get_num_assets())
        return assets, techs, nums

    def getAssetTechNames(self):
        tech_names = []
        for t in self.getAssetsinFleet()[1]:
            tech_names.append(t.name)
        return tech_names

    def getManager(self):
        """
        Returns the user that manages the fleet.
        """
        m = []
        managesFleets = ManagesFleet.query.filter_by(fleet_id=self.id).all()
        for managesFleet in managesFleets:
            managers = User.query.filter_by(id=managesFleet.user_id).all()
            for manager in managers:
                m.append(manager)
        return m

    def getRetrofitsUsed(self):
        techs = []
        assets = self.getAssetsinFleet()
        for asset in assets:
            techs.append(asset.getTech())
        return techs


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    ofAssetType = db.relationship('OfAssetType', cascade="all, delete")
    longCost = db.relationship('LongCost', cascade="all, delete")
    shortCost = db.relationship('ShortCost', cascade="all, delete")
    applicableType = db.relationship('ApplicableType', cascade="all, delete")


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    made = db.Column(db.Integer)
    remaining_yrs = db.Column(db.Integer)
    ofAssetType = db.relationship('OfAssetType', cascade="all, delete")
    isOwnedBy = db.relationship('OwnsAsset', cascade="all, delete")
    isInCategory = db.relationship('IsInCategory', cascade="all, delete")
    usesTech = db.relationship('UsesTech', cascade="all, delete")
    containsAssets = db.relationship('ContainsAsset', cascade="all, delete")

    def getType(self):
        ofAssetType = OfAssetType.query.filter_by(asset_id=self.id).first()
        typ = Type.query.filter_by(id=ofAssetType.asset_type_id).first()
        return typ

    def getOwner(self):
        """
        Returns the owner of asset.
        """
        o = []
        ownsAssets = OwnsAsset.query.filter_by(asset_id=self.id).all()
        for ownsAsset in ownsAssets:
            owners = User.query.filter_by(id=ownsAsset.user_id).all()
            for owner in owners:
                o.append(owner)
        return o

    def getFleetContainer(self):
        """
        Returns the fleet asset is in.
        """
        f = []
        containsAssets = ContainsAsset.query.filter_by(asset_id=self.id).all()
        for containsAsset in containsAssets:
            fleets = Fleet.query.filter_by(id=containsAsset.fleet_id).all()
            for fleet in fleets:
                f.append(fleet)
        return f

    def getCategory(self):
        """
        Returns the category asset is in.
        """
        inCats = IsInCategory.query.filter_by(asset_id=self.id).first()
        cat = Category.query.filter_by(id=inCats.category_id).all()
        return cat[0]

    def setCategory(self, category):
        """
        Returns the category asset is in.
        """
        inCats = IsInCategory.query.filter_by(asset_id=self.id).all()
        for inCat in inCats:
            inCat.category_id = category.id
        db.session.commit()
        return

    def getTech(self):
        """
        Returns the technology asset uses.
        """
        useTechs = UsesTech.query.filter_by(asset_id=self.id).all()
        techs = []
        num_techs = []
        for useTech in useTechs:
            num = useTech.num_assets
            tech = Tech.query.filter_by(id=useTech.tech_id).first()
            techs.append(tech)
            num_techs.append(num)
        return techs, num_techs

    def getTechNames(self):
        techs, _ = self.getTech()
        names = []
        for t in techs:
            names.append(t.name)
        return names

    def setTech(self, tech):
        """
        Returns the category asset is in.
        """
        useTechs = UsesTech.query.filter_by(asset_id=self.id).all()
        for useTech in useTechs:
            useTech.tech_id = tech.id
        db.session.commit()
        return


class OfAssetType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    asset_type_id = db.Column(db.Integer, db.ForeignKey('type.id'))

    def link_OfAssetType(self):
        a = Asset.query.get(self.asset_id)
        a.ofAssetType.append(self)
        db.session.add(a)
        b = Type.query.get(self.asset_type_id)
        b.ofAssetType.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    isInCategory = db.relationship('IsInCategory', cascade="all, delete")

    def getAssetsInCat(self):
        """
        Returns the assets in category.
        """
        a = []
        inCats = IsInCategory.query.filter_by(category_id=self.id).all()
        for inCat in inCats:
            assets = Asset.query.filter_by(id=inCat.asset_id).all()
            for asset in assets:
                a.append(asset)
        return a


class Tech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    public = db.Column(db.Boolean)
    usesTech = db.relationship('UsesTech', cascade="all, delete")
    ownsTech = db.relationship('OwnsTech', cascade="all, delete")
    opt = db.relationship('OptTech', cascade="all, delete")
    reduxPollut = db.relationship('ReduxPollut', cascade="all, delete")
    applicableType = db.relationship('ApplicableType', cascade="all, delete")
    longCost1 = db.relationship(
        'LongCost', foreign_keys='LongCost.tech1_id', cascade="all, delete")
    longCost2 = db.relationship(
        'LongCost', foreign_keys='LongCost.tech2_id', cascade="all, delete")
    shortCost1 = db.relationship(
        'ShortCost', foreign_keys='ShortCost.tech1_id', cascade="all, delete")
    shortCost2 = db.relationship(
        'ShortCost', foreign_keys='ShortCost.tech2_id', cascade="all, delete")

    def getApplicableTypes(self):
        app = []
        for t in self.applicableType:
            type = Type.query.get(t.type_id)
            app.append(type)
        return app

    def getUser(self):
        ownsTech = OwnsTech.query.filter_by(tech_id=self.id).first()
        return User.query.filter_by(id=ownsTech.user_id).first()

    def getRedux(self, pollutant):
        reduxPolluts = ReduxPollut.query.filter_by(tech_id=self.id).all()
        if len(reduxPolluts) == 0:
            return 1
        for rp in reduxPolluts:
            if pollutant.id == rp.pollut_id:
                return rp.redux
        return 1


class Pollutant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    public = db.Column(db.Boolean)
    opt = db.relationship('OptPollut', cascade="all, delete")
    reduxPollut = db.relationship('ReduxPollut', cascade="all, delete")


class Objective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    opt = db.relationship('OptObj', cascade="all, delete")

    def ampl_obj(self):
        if self.id == 1:
            return "long_term_cost"
        if self.id == 2:
            return "short_term_cost"


class Optimization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_budget = db.Column(db.Integer)
    long_budget = db.Column(db.Integer)
    em_redux_req = db.Column(db.String(150))
    fleet = db.relationship('OptWith', cascade="all, delete")
    objective = db.relationship('OptObj', cascade="all, delete")
    pollutants = db.relationship('OptPollut', cascade="all, delete")
    retrofits = db.relationship('OptTech', cascade="all, delete")

    def get_em_redux_req(self):
        split = self.em_redux_req.split(',')
        if len(split) == 1:
            return []
        return list(map(float, split))

    def get_fleet(self):
        optwith = self.fleet[0]
        fleet_id = optwith.fleet_id
        fleet = Fleet.query.get(fleet_id)
        return fleet

    def get_objective(self):
        optobj = self.objective[0]
        obj_id = optobj.obj_id
        obj = Objective.query.get(obj_id)
        return obj

    def get_pollutants(self):
        polls = []
        optpols = self.pollutants
        for optpol in optpols:
            poll_id = optpol.pollut_id
            poll = Pollutant.query.get(poll_id)
            polls.append(poll)
        return polls

    def get_retrofits(self):
        retros = []
        opttechs = self.retrofits
        for opttech in opttechs:
            re_id = opttech.tech_id
            r = Tech.query.get(re_id)
            retros.append(r)
        return retros


class ManagesFleet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'))

    def link_ManagesFleet(self):
        a = User.query.get(self.user_id)
        a.managesFleets.append(self)
        db.session.add(a)
        b = Pollutant.query.get(self.pollut_id)
        b.managesFleets.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class OwnsAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))

    def link_OwnsAsset(self):
        a = User.query.get(self.user_id)
        a.ownsAssets.append(self)
        db.session.add(a)
        b = Asset.query.get(self.asset_id)
        b.isOwnedBy.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class ContainsAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    asset_tech_id = db.Column(db.Integer, db.ForeignKey('tech.id'))
    num_assets = db.Column(db.Integer)

    def link_ContainsAsset(self):
        a = Asset.query.get(self.asset_id)
        a.containsAssets.append(self)
        db.session.add(a)
        b = Fleet.query.get(self.fleet_id)
        b.containsAssets.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()

    def get_assets(self):
        return Asset.query.get(self.asset_id)

    def get_tech(self):
        return Tech.query.get(self.asset_tech_id)

    def get_num_assets(self):
        return self.num_assets


class IsInCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))

    def link_IsInCategory(self):
        a = Asset.query.get(self.asset_id)
        a.isInCategory.append(self)
        db.session.add(a)
        b = Category.query.get(self.category_id)
        b.isInCategory.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class UsesTech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    num_assets = db.Column(db.Integer)

    def link_UsesTech(self):
        a = Asset.query.get(self.asset_id)
        a.usesTech.append(self)
        db.session.add(a)
        b = Tech.query.get(self.tech_id)
        b.usesTech.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class OptPollut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opt_id = db.Column(db.Integer, db.ForeignKey('optimization.id'))
    pollut_id = db.Column(db.Integer, db.ForeignKey('pollutant.id'))

    def link_OptPollut(self):
        a = Optimization.query.get(self.opt_id)
        a.pollutants.append(self)
        db.session.add(a)
        b = Pollutant.query.get(self.pollut_id)
        b.opt.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class OptTech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opt_id = db.Column(db.Integer, db.ForeignKey('optimization.id'))
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id'))

    def link_OptTech(self):
        a = Optimization.query.get(self.opt_id)
        a.retrofits.append(self)
        db.session.add(a)
        b = Tech.query.get(self.tech_id)
        b.opt.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class OptObj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opt_id = db.Column(db.Integer, db.ForeignKey('optimization.id'))
    obj_id = db.Column(db.Integer, db.ForeignKey('objective.id'))

    def link_OptObj(self):
        a = Optimization.query.get(self.opt_id)
        a.objective.append(self)
        db.session.add(a)
        b = Objective.query.get(self.obj_id)
        b.opt.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class OptWith(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opt_id = db.Column(db.Integer, db.ForeignKey('optimization.id'))
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'))

    def link_OptWith(self):
        a = Optimization.query.get(self.opt_id)
        a.fleet.append(self)
        db.session.add(a)
        b = Fleet.query.get(self.fleet_id)
        b.opt.append(self)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class ReduxPollut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pollut_id = db.Column(db.Integer, db.ForeignKey('pollutant.id'))
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id'))
    redux = db.Column(db.Float)

    def link_ReduxPollut(self):
        a = Pollutant.query.get(self.pollut_id)
        a.reduxPollut.append(self)
        db.session.add(a)
        c = Tech.query.get(self.tech_id)
        c.reduxPollut.append(self)
        db.session.add(c)
        db.session.add(self)
        db.session.commit()


class OwnsTech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id'))

    def link_OwnsTech(self):
        a = User.query.get(self.user_id)
        b = Tech.query.get(self.tech_id)
        a.ownsTech.append(self)
        b.ownsTech.append(self)
        db.session.add(a)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()


class ShortCost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech1_id = db.Column(db.Integer, db.ForeignKey('tech.id'))
    tech2_id = db.Column(db.Integer, db.ForeignKey('tech.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    cost = db.Column(db.Float)

    def link_ShortCost(self):
        a = Tech.query.get(self.tech1_id)
        b = Tech.query.get(self.tech2_id)
        c = Type.query.get(self.type_id)
        a.shortCost1.append(self)
        b.shortCost2.append(self)
        c.shortCost.append(self)
        db.session.add(a)
        db.session.add(b)
        db.session.add(c)
        db.session.add(self)
        db.session.commit()


class LongCost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech1_id = db.Column(db.Integer, db.ForeignKey('tech.id'))
    tech2_id = db.Column(db.Integer, db.ForeignKey('tech.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    cost = db.Column(db.Float)

    def link_LongCost(self):
        a = Tech.query.get(self.tech1_id)
        b = Tech.query.get(self.tech2_id)
        c = Type.query.get(self.type_id)
        a.longCost1.append(self)
        b.longCost2.append(self)
        c.longCost.append(self)
        db.session.add(a)
        db.session.add(b)
        db.session.add(c)
        db.session.add(self)
        db.session.commit()


class ApplicableType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))

    def link_ApplicableType(self):
        a = Tech.query.get(self.tech_id)
        b = Type.query.get(self.type_id)
        a.applicableType.append(self)
        b.applicableType.append(self)
        db.session.add(a)
        db.session.add(b)
        db.session.add(self)
        db.session.commit()
