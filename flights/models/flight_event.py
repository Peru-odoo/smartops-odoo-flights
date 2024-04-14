# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from datetime import datetime
import pytz

from odoo import fields, models, api
from odoo.addons.base.models.res_partner import _tz_get

TIME_KIND2VALUE = {
    "S": 0,
    "T": 100,
    "E": 200,
    "A": 300,
    "R": 400,
}


class FlightEventTime(models.Model):
    """
    All events times are in UTC
    """
    _name = 'flight.event.time'
    _description = 'Flight Event Time'

    flight_id = fields.Many2one('flight.flight')
    kind_id = fields.Many2one('flight.event.kind', 'Flight Event Kind')

    time_kind = fields.Selection([
        ("S", "Scheduled"),
        ("T", "Target"),
        ("E", "Estimated"),
        ("A", "Actual"),
        ("R", "Requested"),
    ], "Time Kind", required=True, default="A")

    time = fields.Datetime()
    display_time = fields.Char(compute="_compute_display_time", store=True)

    @api.depends("time", "flight_id.date")
    def _compute_display_time(self):
        # display time portion only HH:MM but append +/- days difference with the flight
        # e.g. 01:15+1 - landing time next day
        # self.time.date - self.flight_id.date => append after time or skip if same / 0
        for record in self:
            time_str = record.time.strftime('%H:%M')
            flight_date = datetime.combine(record.flight_id.date, datetime.min.time())
            days = (record.time - flight_date).days
            if days:
                time_str += f' (+{days})'
            record.display_time = time_str

    @api.depends("time_kind", "kind_id.code", "display_time")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.time_kind}{record.kind_id.code}T {record.display_time}".upper()


class FlightEventDuration(models.Model):
    _name = 'flight.event.duration'
    _description = 'Flight Event Pairs'

    duration_kind_id = fields.Many2one('flight.event.duration.kind')
    start_id = fields.Many2one("flight.event.time")
    end_id = fields.Many2one("flight.event.time")
    # TODO: add constrain: the times must belong to the same flight
    flight_id = fields.Many2one("flight.flight", related="start_id.flight_id", store=True)
    name = fields.Char(related="duration_kind_id.name")
    duration = fields.Integer(compute="_compute_duration")
    sequence = fields.Integer(related="duration_kind_id.sequence")

    @api.depends("start_id.time", "end_id.time")
    def _compute_duration(self):
        for record in self:
            record.duration = (record.end_id.time - record.start_id.time).total_seconds() / 60 if record.end_id.time and record.start_id.time else 0


class FlightEventKind(models.Model):
    _name = 'flight.event.kind'
    _description = 'Flight Event Kind'
    _rec_name = 'code'

    code = fields.Char()
    description = fields.Char()


class FlightEventDurationKind(models.Model):
    _name = 'flight.event.duration.kind'
    _description = 'Flight Event Pairs Kind'

    name = fields.Char()
    sequence = fields.Integer()
    start_kind_id = fields.Many2one("flight.event.kind")
    end_kind_id = fields.Many2one("flight.event.kind")
