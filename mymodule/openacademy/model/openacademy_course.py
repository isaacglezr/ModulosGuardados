from odoo import models, fields

class Course(models.Model):

	_name = 'openacademy.course' #model odoo name

	name = fields.Char(string='title', required=True) # field reserved to identified name rec
	description = fields.Text(string='Description')
