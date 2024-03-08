from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    show_bool_field = fields.Boolean(string="Show Bool Field", related='company_id.show_bool_field' , readonly=False)
    
class ResCompsny(models.Model):
    _inherit=['res.company']
    
    show_bool_field = fields.Boolean(store=True)

