from odoo import models, fields, api


class CarInfo(models.Model):
    _name = "car.model"
    _description = "car info"
    _rec_name = "car_name"

    car_name = fields.Char(string="Car")
    license_plate = fields.Char(string="License Plate")
    car_model = fields.Char(string="Model")
    chassis_number = fields.Char(string="chassis Number")
    fuel_type = fields.Selection(string="Fuel Type", selection=[(
        'petrol', 'Petrol'), ('diesel', 'Diesel'), ('electric', 'Electric')])
    car_manufacturing = fields.Char(string="Car Manufacturing year")
    under_guarantee = fields.Selection(string="Under Guarantee", selection=[
                                       ('y', 'yes'), ('n', 'no')])
    nature_of_service = fields.Selection(string="Nature Of Service", selection=[
                                         ('full', 'Full Service'), ('wash', 'Wash')])
    car_service_charge = fields.Float(string="Car Service Charge")
    car_oil_price = fields.Float(string="Car Oil Price")
    car_washing_charge = fields.Float(string="Car Washing Charge")
    total = fields.Float(string="Sub Total", compute="_compute_total")


    form_id = fields.Many2one(
        'detail.model', string='Form Id', ondelete='cascade', required=True)

    
    @api.depends('car_service_charge', 'car_oil_price', 'car_washing_charge')
    def _compute_total(self):
        for val in self:
            val.total = val.car_service_charge + val.car_oil_price + val.car_washing_charge

