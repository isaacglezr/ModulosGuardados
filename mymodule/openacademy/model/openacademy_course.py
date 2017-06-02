from odoo import models, fields, api

class Course(models.Model):

	_name = 'openacademy.course' #model odoo name

	name = fields.Char(string='title', required=True) # field reserved to identified name rec
	description = fields.Text(string='Description')
        responsible_id = fields.Many2one("res.users", ondelete="set null", index=True)
        session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
        region = fields.Char(string='Region', readonly=True, related='responsible_id.name')

        _sql_constraints = [
            ("name_description_check",
             "CHECK(name != description",
             "The title of the course should not be the description"),

            ("name_unique",
             "UNIQUE(name)",
             "The course title must be unique"),
        ]

        @api.multi
        def copy(self, default=None):
#           default['name'] = self.name + ' (copy) '

            copied_count = self.search_count(
                [('name', '=like', u"Copy of {}%".format(self.name))])
            if not copied_count:
                new_name = u"Copy of {}".format(self.name)
            else:
                new_name = u"Copy of {} ({})".format(self.name, copied_count)
            default['name'] = new_name
            return super(Course, self).copy(default)

   #     @api.multi
   #     @api.onchange('responsible_id', 'region')
   #     def x_region(self):
   #         res = {}
   #         if self.responsible_id:
   #             res['region'] = {'region': [('region', '=', self.responsible_id.id)]}
   #         return res
