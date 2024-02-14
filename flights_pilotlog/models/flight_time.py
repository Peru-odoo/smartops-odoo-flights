# Copyright 2024 Apexive <https://apexive.com/>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import fields, models


class FlightPilotTime(models.Model):
    """This model records Flight statistics.

    In aviation, pilots use logbooks to record flight statistics and flight
    time. These logbooks are essential for tracking their flying experience,
    meeting regulatory requirements, and for career progression.

    There are two main types of records logged:

    * Function Time: This refers to the time spent performing specific
      functions during the flight, such as Pilot in Command (PIC), Second in
      Command (SIC), Pilot Under Supervision (PICUS), etc.

    * Condition Time: This refers to the time spent flying under specific
      conditions, such as night time, instrument meteorological conditions
      (IMC), actual instrument conditions, etc.

    Each type of records are individual to every pilot. For example, if Night
    time for the flight was 120 minutes total, with 60 minutes PIC for one pilot
    and 60 minutes PIC for another pilot, then every pilot records PIC 60, but
    Night time might be different. For example, first pilot flew 60 minutes,
    then they passed control to the second pilot and 10 minutes later had nap
    for 50 minutes, then the first pilot record Night 70 minutes, while for the
    second pilot the Night time is 120.

    """

    _name = 'flight.time'
    _inherit = 'flight.base'
    _description = 'Pilot Flight Time'

    flight_id = fields.Many2one('flight.flight', 'Flight')
    partner_id = fields.Many2one('res.partner', 'Pilot')
    time_type_id = fields.Many2one('flight.time.kind')
    minutes = fields.Integer("Number of minutes")


class FlightTimeKind(models.Model):
    _name = 'flight.time.kind'
    _description = 'Flight Statistics Type'

    name = fields.Char("Code")
    description = fields.Char("Description")
# group = fields.Selection([
#     ("condition", "Condition time"),
#     ("function", "Function time"),
# ])
