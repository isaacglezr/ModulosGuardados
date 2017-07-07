
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'desc_marca.wizard'

#    def _default_sessions(self):
#        return self.env['product.pricelist.item'].browse(self._context.get('active_ids$

    Marca_wiz = fields.Many2one('x_marcas', string="Marca", required=True)
    Descuento_wiz = fields.Integer(string="Descuento")

    @api.multi
    def subscribe(self):
        self.Marca_wiz.Descuentos_wiz |= self.Descuento_wiz
        return {}

# -*- coding: utf-8 -*-

#from odoo import models, fields, api

#class Wizard(models.TransientModel):
 #   _name = 'openacademy.wizard'

  #  def _default_sessions(self):
   #     return self.env['openacademy.session'].browse(self._context.get('active_ids'))

#    session_wiz_ids = fields.Many2many('openacademy.session', string="Session", requir$
#    attendee_wiz_ids = fields.Many2many('res.partner', string="Attendees")

#    @api.multi
#    def subscribe(self):
#        for session in self.session_wiz_ids:
#            session.attendees_ids |= self.attendee_wiz_ids
#        return {}


