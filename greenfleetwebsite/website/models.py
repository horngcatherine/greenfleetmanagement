from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    managesFleets = db.relationship('ManagesFleet',
                                    cascade="all, delete-orphan")
    ownsAssets = db.relationship('OwnsAsset',
                                 cascade="all, delete-orphan")
    ownsTech = db.relationship('OwnsTech',
                               cascade="all, delete-orphan")
    ownsPollut = db.relationship('OwnsPollut',
                                 cascade="all, delete-orphan")

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

    def getTech(self):
        """
        Returns the fleets the user manages
        """
        techs = []
        # query to get all ownsAssets with
        ownsTechs = OwnsTech.query.filter_by(user_id=self.id).all()
        for ownsTech in ownsTechs:  # ownsAsset is of type OwnsAsset
            techOwned = Tech.query.filter_by(
                id=ownsTech.tech_id).all()
            for tech in techOwned:
                techs.append(tech)
        return techs


class Fleet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    containsAssets = db.relationship('ContainsAsset',
                                     cascade="all, delete-orphan")
    managesFleets = db.relationship('ManagesFleet',
                                    cascade="all, delete-orphan")

    def getAssetsinFleet(self):
        """
        Returns the assets in the fleet.
        """
        assets = []
        # ContainsAssets where the fleet id matches the fleet id
        containsAssets = ContainsAsset.query.filter_by(fleet_id=self.id).all()
        for containsAsset in containsAssets:
            # get assets with the same id as the asset id in containsAsset
            assetsinfleet = Asset.query.filter_by(
                id=containsAsset.asset_id).all()
            for asset in assetsinfleet:
                assets.append(asset)
        return assets

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


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    number = db.Column(db.Integer)
    rem_mileage = db.Column(db.Float)
    rem_idle = db.Column(db.Float)
    ownsAssets = db.relationship('OwnsAsset',
                                 cascade="all, delete-orphan")
    containsAssets = db.relationship('ContainsAsset',
                                     cascade="all, delete-orphan")
    isInCategory = db.relationship('IsInCategory',
                                   cascade="all, delete-orphan")
    usesTech = db.relationship('UsesTech',
                               cascade="all, delete-orphan")

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
        c = []
        inCats = IsInCategory.query.filter_by(asset_id=self.id).all()
        for inCat in inCats:
            cats = Category.query.filter_by(id=inCat.category_id).all()
            for cat in cats:
                c.append(cat)
        return c

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
        t = []
        useTechs = UsesTech.query.filter_by(asset_id=self.id).all()
        for useTech in useTechs:
            techs = Tech.query.filter_by(id=useTech.tech_id).all()
            for tech in techs:
                t.append(tech)
        return t

    def setTech(self, tech):
        """
        Returns the category asset is in.
        """
        useTechs = UsesTech.query.filter_by(asset_id=self.id).all()
        for useTech in useTechs:
            useTech.tech_id = tech.id
        db.session.commit()
        return


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    isInCategory = db.relationship('IsInCategory',
                                   cascade="all, delete-orphan")

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
    usesTech = db.relationship('UsesTech',
                               cascade="all, delete-orphan")
    isOwnedBy = db.relationship('OwnsTech',
                                cascade="all, delete-orphan")
    opt = db.relationship('OptTech',
                          cascade="all, delete-orphan")


class Pollutant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    public = db.Column(db.Boolean)
    isOwnedBy = db.relationship('OwnsPollut',
                                cascade="all, delete-orphan")
    opt = db.relationship('OptPollut',
                          cascade="all, delete-orphan")


class Objective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(150))
    opt = db.relationship('OptObj',
                          cascade="all, delete-orphan")


class Optimization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Integer)
    objective = db.relationship('OptObj',
                                cascade="all, delete-orphan")
    pollutants = db.relationship('OptPollut',
                                 cascade="all, delete-orphan")
    retrofits = db.relationship('OptTech',
                                cascade="all, delete-orphan")


class OwnsTech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id'))


class OwnsPollut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pollut_id = db.Column(db.Integer, db.ForeignKey('pollutant.id'))


class ManagesFleet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'))


class OwnsAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))


class ContainsAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))


class IsInCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class UsesTech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id'))


class OptPollut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opt_id = db.Column(db.Integer, db.ForeignKey('optimization.id'))
    pollut_id = db.Column(db.Integer, db.ForeignKey('pollutant.id'))


class OptTech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opt_id = db.Column(db.Integer, db.ForeignKey('optimization.id'))
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id'))


class OptObj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opt_id = db.Column(db.Integer, db.ForeignKey('optimization.id'))
    obj_id = db.Column(db.Integer, db.ForeignKey('objective.id'))
