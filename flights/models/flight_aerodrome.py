# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
import json
from odoo import models, fields, api


class FlightAerodrome(models.Model):
    _name = 'flight.aerodrome'
    _description = 'Aerodrome'
    _rec_name = 'icao'

    partner_id = fields.Many2one("res.partner", string="Address")
    country_id = fields.Many2one("res.country", related="partner_id.country_id", store=True)

    icao = fields.Char("ICAO identifier", index=True)
    iata = fields.Char("IATA identifier", index=True)
    elevation = fields.Integer("Aerodrome elevation in feet", null=True)
    aerodrome_type = fields.Selection([
        ("small_airport", "Small Airport"),
        ("medium_airport", "Medium Airport"),
        ("large_airport", "Large Airport"),
        ("heliport", "Heliport"),
        ("seaplane_base", "Seabase"),
        ("balloonport", "Balloonport"),
        ("closed", "Closed"),
    ], "Type", required=True, default="small_airport")

    _sql_constraints = [
        ("icao_unique", "unique(icao)", "Aerodrome with this ICAO already exists!"),
    ]

    def search_by_code(self, code):
        return self.search([
            "|",
            ("icao", "=", code),
            ("iata", "=", code),
        ], limit=1)

    @api.depends('icao', 'iata')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f'{record.icao} ({record.iata})' if record.iata else record.icao
