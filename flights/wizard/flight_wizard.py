# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).

import json
import base64
import logging
# TODO: json can be optimized by using https://pypi.org/project/json-stream/

from odoo import fields, models


_logger = logging.getLogger(__name__)


class MagicWizard(models.TransientModel):

    _name = 'flight.wizard'

    action = fields.Selection([
        ("pilot_log_mcc", "mccPILOTLOG")
    ], "Supported formats", required=True, default="pilot_log_mcc")

    payload = fields.Binary("File", required=True, attachment=False)
    filename = fields.Char(string="Filename")
    override = fields.Boolean("Override existing records", default=True)

    def do_action(self):
        if self.action == "pilot_log_mcc":
            return self.do_pilot_log_mcc()
        else:
            raise NotImplementedError()

    def _update_flight_data(self, vals):
        existing = self.env['flight.data'].search([
            ('source_type', '=', vals['source_type']),
            ('source_model', '=', vals['source_model']),
            ('source_ref', '=', vals['source_ref']),
        ])
        if existing:
            if self.override:
                existing.write({
                    "raw_text": vals["raw_text"],
                    "is_parsed": False,
                })
            return existing
        else:
            return self.env['flight.data'].create(vals)

    def do_pilot_log_mcc(self):
        SOURCE_TYPE = 'pilot_log_mcc'
        TABLE_MAP = {
            "aircraft": "flight.aircraft",
            "airfield": "flight.airfield",
            "flight": "flight.flight",
            "pilot": "res.partner",
        }

        # Load data into `flight.data` table first
        for data in json.loads(base64.decodebytes(self.payload)):
            table = data.get("table").lower()
            if table not in TABLE_MAP:
                continue
            model = TABLE_MAP[table]
            self._update_flight_data({
                'source_type': SOURCE_TYPE,
                'source_model': model,
                'source_ref': data.get("guid"),
                'raw_text': json.dumps(data)
            })

        # Parse data
        # TODO: use queue_job for async work?
        # TODO: In case if we don't use queue_job, but have performance issue,
        # we may add a counter and make cr.commit() every 1000 records
        for flight_data in self.env['flight.data'].search([
                ("source_type", "=", SOURCE_TYPE),
                ("source_model", "in", ["flight.airfield", "flight.aircraft", "res.partner"]),
                ("is_parsed", "=", False)
        ]):
            flight_data._data_parse()

        # parse flights last because they have references to other models
        for flight_data in self.env['flight.data'].search([
                ("source_type", "=", SOURCE_TYPE),
                ("source_model", "in", ["flight.flight"]),
                ("is_parsed", "=", False)
        ]):
            flight_data._data_parse()

        return {'type': 'ir.actions.act_window_close'}
