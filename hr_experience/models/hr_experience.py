from odoo import models, fields, api
from datetime import datetime

class hrExperience(models.Model):
    _name = 'hr.experience'
    _description = "Hiring the Heroes!"
    name = fields.Char("Name")
    date_to = fields.Date("Date To", required='1')
    date_from = fields.Date("Date From", required='1')
    education = fields.Boolean("Is Educated")
    college = fields.Char("The College/Company", help="from where you gained this experience")
    state = fields.Selection(string='State', selection=[('active', 'Active'), ('expired', 'Expired')],
                             readonly='1', default='active')
    document = fields.Binary("Documents")
    description = fields.Text("Description")
    employee_id = fields.Many2one('hr.employee', string='Employee ID')
    contract_id = fields.Char('Contract', readonly=True)
    expiration_date = fields.Date(string='Expiration Date')

    def name_get(self):
        rec = []
        for field in self:
            rec.append((field.id, '%s, %s' % (field.name, field.employee_id.name)))
        return rec

    @api.model
    def default_get(self, fields):
        rec = super(hrExperience, self).default_get(fields)
        rec['employee_id'] = self._context.get('active_id')
        return rec

    @api.onchange('employee_id')
    def onchange_contract_id(self):
        self.contract_id = self.employee_id.contract_id.name

    @api.constrains('date_from', 'date_to', 'expiration_date', 'state')
    def _check_date_from(self):
        for record in self:
            if record.date_from > record.date_to or record.date_from > fields.Date.today():
                raise models.ValidationError('Date from must be in the past and must not be after Date to!')
            elif record.date_from == fields.Date.today() or record.date_from == record.date_to:
                raise models.ValidationError('Date from must be in the past!')
            elif record.date_to > fields.Date.today() or record.date_to == fields.Date.today():
                raise models.ValidationError('Date to must be in the past!')

    def action_activate(self):
        for rec in self:
            rec.expiration_date = False
            rec.state = 'active'

    def action_expired(self):
        today=datetime.today().date()
        expired_rec= self.search([('expiration_date','<=',today),('state','=','active')])
        expired_rec.write({'state':'expired'})




class Experiences(models.Model):
    _inherit = 'hr.employee'
    experiences = fields.One2many('hr.experience', 'employee_id')
