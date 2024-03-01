from odoo import fields, models


class EmailSendMessageWizard(models.TransientModel):
    _name = 'email.send.wizard'
    _description = "Eamil Wizard"

    recipient = fields.Char(string="Recipient")
    subject =  fields.Char(string="subject")
    message = fields.Char()