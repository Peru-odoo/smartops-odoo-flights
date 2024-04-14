# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import models, fields, api, _


class FlightFlight(models.Model):
    _name = 'flight.flight'
    _description = 'Flight'

    _rec_name = 'flight_number_id'

    aircraft_id = fields.Many2one('flight.aircraft')
    date = fields.Date("Flight Date")
    display_date = fields.Date("Date", compute="_compute_flight_time")

    flight_number_id = fields.Many2one('flight.number')
    operator_id = fields.Many2one("res.partner", "Operator Company")

    crew_ids = fields.One2many('flight.crew', 'flight_id', "Crew")
    pax_ids = fields.Many2many("res.partner", string="Passengers")

    departure_id = fields.Many2one('flight.aerodrome')
    arrival_id = fields.Many2one('flight.aerodrome')
    event_time_ids = fields.One2many('flight.event.time', 'flight_id', string="Flight Timing Events")
    event_duration_ids = fields.One2many('flight.event.duration', 'flight_id', string="Flight Timing Durations")
    flight_duration = fields.Integer("Flight Time", compute='_compute_flight_time')
    total_duration = fields.Integer("Total Flight Time", compute='_compute_flight_time')
    departure_time_id = fields.Many2one('flight.event.time', compute='_compute_flight_time')
    arrival_time_id = fields.Many2one('flight.event.time', compute='_compute_flight_time')

    param_ids = fields.One2many('flight.flight.param', 'flight_id')

    errors = fields.Text(compute='_compute_errors')
    has_errors = fields.Boolean(compute='_compute_has_errors', store=True, string="⚠️")

    @api.depends('event_duration_ids')
    def _compute_flight_time(self):
        for flight in self:
            flight.flight_duration = 0
            flight.total_duration = 0
            flight.departure_time_id = None
            flight.arrival_time_id = None
            flight.display_date = flight.date
            for event_duration in flight.event_duration_ids:
                start_code = event_duration.start_id.kind_id.code
                # TODO: check computation
                if start_code == "OB":
                    flight.total_duration = event_duration.duration
                    flight.display_date = event_duration.start_id.time
                elif start_code == "TO":
                    flight.flight_duration = event_duration.duration
                    flight.departure_time_id = event_duration.start_id
                    flight.arrival_time_id = event_duration.end_id

    @api.depends("aircraft_id", "date")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.aircraft_id.registration}: {record.date}"

    def _compute_has_errors(self):
        for record in self:
            record.has_errors = bool(record.errors)

    def _compute_errors(self):
        for record in self:
            record.errors = "\n".join(record._check_errors())

    def _check_errors(self):
        """Can be extended by other modules"""
        self.ensure_one()
        result = []
        if not self.departure_id:
            result.append(_("Departure aerodrome is not set"))
        if not self.arrival_id:
            result.append(_("Arrival aerodrome is not set"))

        if self.flight_duration > self.total_duration:
            result.append("Flight time > Total time")

        return result

    def action_check_errors(self):
        self._compute_has_errors()

    def get_time_by_code(self, code, time_kind="A", time_format="%H:%M"):
        self.ensure_one()
        time = self.event_time_ids.filtered(lambda r: r.time_kind == time_kind and r.kind_id.code == code).time
        if time:
            return time.strftime(time_format)
        else:
            return

    def get_param_by_code(self, code):
        self.ensure_one()
        self.param_ids.filtered(lambda r: r.param_type_id.code == code).value


class FlightFlightParam(models.Model):
    _name = 'flight.flight.param'
    _description = 'Flight Parameter'

    flight_id = fields.Many2one('flight.flight')
    param_type_id = fields.Many2one('flight.flight.param.type')
    value = fields.Float()


class FlightFlightParamType(models.Model):
    _name = 'flight.flight.param.type'
    _description = 'Flight Parameter Type'

    # Rename "name" to "description"
    name = fields.Char()
    code = fields.Char()


class FlightNumber(models.Model):
    _name = 'flight.number'
    _description = 'Flight Number'

    prefix_id = fields.Many2one('flight.prefix')
    numbers = fields.Char()

    @api.depends("prefix_id.name", "numbers")
    def _compute_display_name(self):
        for r in self:
            r.display_name = f"{r.prefix_id.name} {r.numbers}"


class FlightPrefix(models.Model):
    _name = 'flight.prefix'
    _description = 'Flight Number Prefix'

    name = fields.Char("Prefix")
    description = fields.Char()
