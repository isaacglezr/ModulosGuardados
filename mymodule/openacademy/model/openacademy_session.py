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
    @api.one
    @api.depends('seats', 'attendees_ids')
    def _taken_seats(self):
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * len(self.attendees_ids) / self.seats

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

    @api.one
    @api.constrains('instructor_id', 'attendees_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendees_ids:
            raise exceptions.ValidationError("A session's instructor can't be an attendee")

    _sql_constraints = [
        ("name_description_check",
         "CHECK(name != description",
         "The title of the course should not be the description"),

        ("name_unique",
         "UNIQUE(name)",
         "The course title must be unique"),
    ]
