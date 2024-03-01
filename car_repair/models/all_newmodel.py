from odoo import models, fields, api, _ 


class Client(models.Model):
    _name="client.model"
    _description="Client model"
    
    name = fields.Char(string="Client Name")
    

class worker(models.Model):
    _name="worker.model"
    _description="worker model"
    
    name = fields.Char(string="Worker Name")

   

