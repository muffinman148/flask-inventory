"""
Defines all sqlalchemy models and tables.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from app import db, login
from flask import url_for
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol, ButtonCol

ACCESS = {
    'guest' : 'guest',
    'user' : 'user',
    'admin' : 'admin'
}

class User(UserMixin, db.Model):
    """Defines a "User" table.

    Args:
        UserMixin: A standard flask-login classification for typical user
        parameters.
        db.Model: Baseclass for all SQLAlchemy instances.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    access = db.Column(db.String(128))

    def __repr__(self):
        """Displays user username."""

        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        """Sets password for provided user."""

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Validates provided password."""

        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        """Checks if provided id is valid."""

        return User.query.get(int(id))

    def is_admin(self):
        """Set's user access to admin."""

        return self.access == ACCESS['admin']

    def allowed(self, access_level):
        """Evaluates user access level."""

        return self.access >= access_level

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        """Creates sort url for table headers.
        
        Args:
            cls: Corresponding class
            sort: Column to be sorted
            reverse: Current direction of data
        """

        return sorted( 
            cls.query.all(), 
            key=lambda x: getattr(x, sort), 
            reverse=reverse)

class UserTable(Table):
    """Creates framework for User table.
    
    Args:
        Table: Baseclass from flask-table.
    """

    id = Col('Id', show=False)
    username = Col('Username', column_html_attrs={'class': 'username'})
    email = Col('Email')
    access = Col('Access Level')
    editUser = ButtonCol('Edit', 'editUser',\
                 url_kwargs=dict(username='username'),\
                 allow_sort = False)
    deleteUser = ButtonCol('Delete', 'deleteUser',\
                 url_kwargs=dict(username='username'),\
                 button_attrs={
                     'class': 'myclass', 
                     'data-href': 'dataLink', 
                     'data-toggle': 'modal', 
                     'data-target': '#confirm-delete'},\
                 form_attrs={
                     'class': 'myform'},\
                 allow_sort = False)
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        """Creates sort url for table headers.
        
        Args:
            col_key: Column to be sorted
            reverse: Current direction of data
        """

        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('users', sort=col_key, direction=direction)

class Measurements(db.Model):
    """Defines a "Measurements" table

    Args:
        db.Model: Baseclass for all SQLAlchemy instances.
    """

    id = db.Column(db.Integer, primary_key=True)
    warehouseCode = db.Column(db.String(3))
    partNumber = db.Column(db.String(15))
    partCount = db.Column(db.Integer)
    pieceWeight = db.Column(db.DECIMAL(16,6))
    tareWeight = db.Column(db.DECIMAL(16,6))
    totalWeight = db.Column(db.DECIMAL(16,6))
    countMethod = db.Column(db.String(1))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Displays item part number."""

        return '<Measurements {}>'.format(self.partNumber)

class MeasurementsTable(Table):
    """Creates framework for Measurements table.
    
    Args:
        Table: Baseclass from flask-table.
    """

    partNumber = Col('Part Number')
    tareWeight = Col('Tare Weight',
                td_html_attrs={'class': 'oldTareWeight'},\
                )
    partCount = Col('Part Count',\
                td_html_attrs={'class': 'oldPartCount'},\
                )

class Items(db.Model): # rpi_inv_ci_item
    """Defines an "Items" table.

    Args:
        db.Model: Baseclass for all SQLAlchemy instances.
    """

    ItemCode = db.Column(db.String(30), primary_key=True)
    ItemType = db.Column(db.String(1))
    ItemCodeDesc = db.Column(db.String(30))
    ExtendedDescriptionKey = db.Column(db.String(10))
    UseInAR = db.Column(db.String(1))
    UseInSO = db.Column(db.String(1))
    UseInPO = db.Column(db.String(1))
    UseInBM = db.Column(db.String(1))
    CalculateCommission = db.Column(db.String(1))
    DropShip = db.Column(db.String(1))
    EBMEnabled = db.Column(db.String(1))
    PriceCode = db.Column(db.String(4))
    PrintReceiptLabels = db.Column(db.String(1))
    AllocateLandedCost = db.Column(db.String(1))
    WarrantyCode = db.Column(db.String(10))
    SalesUnitOfMeasure = db.Column(db.String(4))
    PurchaseUnitOfMeasure = db.Column(db.String(4))
    StandardUnitOfMeasure = db.Column(db.String(4))
    PostToGLByDivision = db.Column(db.String(1))
    SalesAcctKey = db.Column(db.String(9))
    CostOfGoodsSoldAcctKey = db.Column(db.String(9))
    InventoryAcctKey = db.Column(db.String(9))
    PurchaseAcctKey = db.Column(db.String(9))
    ManufacturingCostAcctKey = db.Column(db.String(9))
    TaxClass = db.Column(db.String(2))
    PurchasesTaxClass = db.Column(db.String(2))
    ProductLine = db.Column(db.String(4))
    ProductType = db.Column(db.String(1))
    Valuation = db.Column(db.String(1))
    DefaultWarehouseCode = db.Column(db.String(3))
    PrimaryAPDivisionNo = db.Column(db.String(2))
    PrimaryVendorNo = db.Column(db.String(7))
    ImageFile = db.Column(db.String(30))
    Category1 = db.Column(db.String(10))
    Category2 = db.Column(db.String(10))
    Category3 = db.Column(db.String(10))
    Category4 = db.Column(db.String(10))
    ExplodeKitItems = db.Column(db.String(1))
    ShipWeight = db.Column(db.String(10))
    CommentText = db.Column(db.String(2048))
    RestockingMethod = db.Column(db.String(1))
    StandardUnitCost = db.Column(db.DECIMAL(15,6))
    StandardUnitPrice = db.Column(db.DECIMAL(15,6))
    CommissionRate = db.Column(db.DECIMAL(8,3))
    BaseCommAmt = db.Column(db.DECIMAL(11,2))
    PurchaseUMConvFctr = db.Column(db.DECIMAL(11,4))
    SalesUMConvFctr = db.Column(db.DECIMAL(11,4))
    Volume = db.Column(db.DECIMAL(10,4))
    RestockingCharge = db.Column(db.DECIMAL(10,3))
    ProcurementType = db.Column(db.String(1))
    DateCreated = db.Column(db.Date)
    TimeCreated = db.Column(db.String(8))
    UserCreatedKey = db.Column(db.String(10))
    DateUpdated = db.Column(db.Date)
    TimeUpdated = db.Column(db.String(8))
    UserUpdatedKey = db.Column(db.String(10))
    UDF_PRINT_2_LABELS = db.Column(db.String(1))
    AllowBackOrders = db.Column(db.String(1))
    AllowReturns = db.Column(db.String(1))
    AllowTradeDiscount = db.Column(db.String(1))
    ConfirmCostIncrInRcptOfGoods = db.Column(db.String(1))
    LastSoldDate = db.Column(db.Date)
    LastReceiptDate = db.Column(db.Date)
    SalesPromotionCode = db.Column(db.String(10))
    SaleStartingDate = db.Column(db.Date)
    SaleEndingDate = db.Column(db.Date)
    SaleMethod = db.Column(db.String(1))
    NextLotSerialNo = db.Column(db.String(15))
    InventoryCycle = db.Column(db.String(1))
    RoutingNo = db.Column(db.String(20))
    PlannerCode = db.Column(db.String(3))
    BuyerCode = db.Column(db.String(3))
    LowLevelCode = db.Column(db.String(2))
    PlannedByMRP = db.Column(db.String(1))
    VendorItemCode = db.Column(db.String(30))
    SetupCharge = db.Column(db.String(1))
    AttachmentFileName = db.Column(db.String(30))
    ItemImageWidthInPixels = db.Column(db.DECIMAL(4,0))
    ItemImageHeightInPixels = db.Column(db.DECIMAL(4,0))
    LastTotalUnitCost = db.Column(db.DECIMAL(15,6))
    AverageUnitCost = db.Column(db.DECIMAL(15,6))
    SalesPromotionPrice = db.Column(db.DECIMAL(15,6))
    SuggestedRetailPrice = db.Column(db.DECIMAL(15,6))
    SalesPromotionDiscountPercent = db.Column(db.DECIMAL(11,3))
    TotalQuantityOnHand = db.Column(db.DECIMAL(15,6))
    AverageBackOrderFillDays = db.Column(db.DECIMAL(5,0))
    LastAllocatedUnitCost = db.Column(db.DECIMAL(15,6))
    TotalInventoryValue = db.Column(db.DECIMAL(14,2))
    InactiveItem = db.Column(db.String(1))
    LastPhysicalCountDate = db.Column(db.Date)
