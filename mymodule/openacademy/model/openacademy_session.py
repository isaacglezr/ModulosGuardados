from datetime import timedelta
from odoo import models, fields, exceptions, api

class Session(models.Model):

    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Datetime(default=fields.Datetime.now)
    duration = fields.Float(digits=(6,2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one("res.partner", string="Instructor", domain=['|',("instructor","=",True),('category_id.name', "ilike", "Teacher")])
    course_id = fields.Many2one("openacademy.course", ondelete="cascade", string="Course", required=True)
    attendees_ids = fields.Many2many("res.partner", string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute="_taken_seats")
    active = fields.Boolean(default=True)
    end_date = fields.Datetime(string="End Date", store=True, compute="_get_end_date", inverse="_set_end_date")
    hours = fields.Float(string="Duration in hours", compute='_get_hours', inverse='_set_hours')
    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)
    color = fields.Integer()
    state = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done"),], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'


    @api.one
    @api.depends('seats', 'attendees_ids')
    def _taken_seats(self):
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * len(self.attendees_ids) / self.seats

    @api.one
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    @api.onchange('seats', 'attendees_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning':{
                    'title':"Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendees_ids):
            return {
                'warning':{
                    'title':"Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

    @api.depends('attendees_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendees_ids)

    @api.one
    @api.constrains('instructor_id', 'attendees_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendees_ids:
            raise exceptions.ValidationError("A session's instructor can't be an attendee")

