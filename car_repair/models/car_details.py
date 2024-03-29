from odoo import models, fields, api, _
from odoo .exceptions import ValidationError
from datetime import datetime, timedelta
class DetailsModel(models.Model):
    _name = "detail.model"
    _description = "Car Repair"
    _rec_name = "client_name"
    _order = "detail_priority desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    detail_id = fields.Char(string="Id", readonly=True,
                            default=lambda self: _('New'))
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company , readonly=True)
    other_record_id = fields.Many2one('res.company', check_company=True)
    detail_subject = fields.Char(string="Subject")
    detail_assignedto = fields.Char(string="Assigned To")
    detail_priority = fields.Selection(
        [('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string='Priority')
    start_date = fields.Date(string="Date of Receipt",
                             default=lambda s: fields.Date.context_today(s))
    end_date = fields.Date(string="End Date:-")

    detail_image = fields.Binary(string="Car Pic")
    status = fields.Selection(string="Status", readonly=True, tracking=True, default="received", selection=[
        ('received', 'Received'),
        ('in_diagnosis', 'In Diagnosis'),
        ('quotation_sent', 'Quotation Sent'),
        ('quotation_approve', 'Quotation Approve'),
        ('work_in_progress', 'Work In Progress'),
        ('done', 'Done')
    ])

    client_name = fields.Many2one(
        'res.users', string="User", default=lambda self: self.env.user.id)
    client_address = fields.Char(string="Client Address")
    street = fields.Char(string="Street", related='company_id.street')
    street2 = fields.Char(string="Street2", related='company_id.street2')
    city = fields.Char(string="City", related='company_id.city')
    zip = fields.Char(string="Zip", related='company_id.zip')

    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    car_info_ids = fields.One2many('car.model', 'form_id', string='Car Info')
    check_button = fields.Boolean(string="Boolean")
    code = fields.Char(string="Code")
    main_total = fields.Float(
        string="Main Total", compute="_compute_main_total")
    edit_field = fields.Boolean(string="Edit Data")
    show_bool_field = fields.Boolean(related='company_id.show_bool_field' )

    
    def write(self, vals):
        show_bool_field = vals.get('show_bool_field', self.show_bool_field)
        edit_field = vals.get('edit_field', self.edit_field)

        if show_bool_field:  
            if 'edit_field' in vals:
                edit_field = vals['edit_field']

            if  edit_field:  
                restricted_fields = [field for field in vals if field != 'edit_field']
                if restricted_fields:
                    raise ValidationError("Changes are not allowed when Edit Field is checked")
        return super(DetailsModel, self).write(vals)
    
    def _compute_main_total(self):
        for record in self:
            total = sum(record.car_info_ids.mapped('total'))
            record.main_total = total

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('detail_id', _('New')) == _('New'):
                vals['detail_id'] = self.env['ir.sequence'].next_by_code(
                    'detail.model') or _('New')
        res = super(DetailsModel, self).create(vals)
        return res
    


    def Create_Car_Diagnosis(self):
        print("Car Diagnosis Create")

    def Print_Receipt(self):
        print("Print Receipt Create")

    def Print_report(self):
        print("Print Report Create")

    def email_send(self):
        print("Send mail")

    def o_diagnosis(self):
        for rec in self:
            rec.status = 'in_diagnosis'

    def o_quotation_sent(self):
        for rec in self:
            rec.status = 'quotation_sent'

    def o_quotation_approve(self):
        for rec in self:
            rec.status = 'quotation_approve'

    def o_work_in_progress(self):
        for rec in self:
            rec.status = 'work_in_progress'

    def o_done(self):
        for rec in self:
            rec.status = 'done'

    def unlink(self):
        record = self.filtered(lambda r: r.status == 'done')
        if record:
            raise ValidationError("not delete done data")
        return super(DetailsModel, self-record).unlink()

    def action_send_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data._xmlid_lookup(
                'car_repair.send_mail_car')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data._xmlid_lookup(
                'mail.email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
            template_id = self.env.ref('car_repair.send_mail_car')[1]
        ctx = {
            'default_model': 'detail.model',
            'default_res_ids': self.ids,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.model
    def action_send_reminder_email(self):
        end_date_three_month = datetime.now() - timedelta(days=90)
        user_company_id = self.env.user.company_id.id
        records_to_remind = self.env['detail.model'].search([
            ('company_id', '=', user_company_id),
            ('status', '=', 'done'),
            ('end_date', '=', end_date_three_month),
        ])
        for record in records_to_remind:
            template_id = self.env.ref('car_repair.send_mail_car_schedule').id
            template = self.env['mail.template'].browse(template_id)
            template.with_context(object=record).send_mail(
                record.id, force_send=True)
