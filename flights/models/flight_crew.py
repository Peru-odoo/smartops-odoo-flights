# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields


class FlightCrew(models.Model):
    _name = 'flight.crew'
    _inherit = 'flight.base'

    partner_id = fields.Many2one('res.partner')
    role_id = fields.Many2one('flight.crew.role')
    flight_id = fields.Many2one('flight.flight')


class FlightCrewRole(models.Model):
    _name = 'flight.crew.role'

    code = fields.Char()
    description = fields.Char()
