from odoo import models, fields, api
# from odoo.osv import expression


class Product(models.Model):
    _inherit = 'product.template'

    product_code_ok = fields.Boolean(string="Can You Show code?")
    code = fields.Char(string='Code')

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None, order=None):
        args = list(args or [])
        if not (name == '' and operator == 'ilike'):
            args += ['|', (self._rec_name, operator, name),
                     ('code', operator, name)]
            return self._search(args, limit=limit, access_rights_uid=name_get_uid, order=order)

