from odoo import models, fields

class Course(models.Model):

	_name = 'openacademy.course' #model odoo name

	name = fields.Char(string='title', required=True) # field reserved to identified name rec
	description = fields.Text(string='Description')
        responsible_id = fields.Many2one("res.users", ondelete="set null", index=True)
        session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
