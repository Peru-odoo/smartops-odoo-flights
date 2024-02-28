# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightAircraftMake(models.Model):
    _name = 'flight.aircraft.make'
    _description = 'Aircraft Make'

    name = fields.Char()


class FlightAircraftModelTag(models.Model):
    _name = 'flight.aircraft.model.tag'
    _description = 'Aircraft Model Tag'

    name = fields.Char()

    # Examples:
    # retractable, high performance, pressurized, taa, propeller, turbine, jet, efis, aerobatic, tailwheel
    # turboprop will have turbine and propeller = turboprop
    # turbojet will have turbine and jet = turbofan


class FlightAircraftModel(models.Model):
    _name = 'flight.aircraft.model'
    _description = 'Aircraft Model'

    name = fields.Char()
    make_id = fields.Many2one("flight.aircraft.make")
    code = fields.Char("ICAO type code")  # TODO: can we just use name field for that ? - No that can be different
    tag_ids = fields.Many2many("flight.aircraft.model.tag")

    #  if   "Kg5700": is true - record 142000 lbs by defaukt as mtow (medium), otherwise record 12000 lbs by default (light)

    mtow = fields.Integer("Maximum take-off weight in pounds")

    def get_weight_category(self):
        if self.mtow >= 299200:
            return "H"
        elif self.mtow >= 12500:
            return "M"
        return "L"


    # TODO(ivank): add class and category models as per below
    # class_id = fields.Many2many()  # TODO: why not Selection / Integer ?
    # category_id = fields.Many2many() # TODO: why not Selection ?


class FlightAircraft(models.Model):
    _name = 'flight.aircraft'
    _inherit = 'flight.base'
    _description = 'Aircraft'

    _rec_name = 'registration'

    registration = fields.Char("Aircraft registration")
    sn = fields.Char("Aircraft serial number")
    year = fields.Date("Year of manufacture")

    model_id = fields.Many2one("flight.aircraft.model")
    _sql_constraints = [
        ("registration_unique", "unique(registration)", "Aircraft with this registration number already exists!")
    ]
