from odoo import models, fields, api


class hrExperience(models.Model):
    _name = 'hr.experience'
    _description = "Hiring the Heros!"
    name = fields.Char("Name")
    date_to = fields.Date("Date To", required='1')
    date_from = fields.Date("Date From", required='1')
    education = fields.Boolean("Is Educated")
    college = fields.Char("The College/Company", help="from where you gained this experience")
    state = fields.Selection(string='State', selection=[('active', 'Active'), ('expired', 'Expired')])  # default=active
    document = fields.Binary("Documents")
    description = fields.Text("Description")
    employee_id = fields.Many2one('hr.employee', string='Employee ID')
    contract_id = fields.Char(compute="_compute_contract_id", string='Contract', store=True)
    expiration_date = fields.Date(string='Expiration Date', compute="_compute_expiration_date", store=True)

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

    @api.constrains('date_from')
    def _check_date_from(self):
        for record in self:
            if record.date_from > record.date_to:
                raise models.ValidationError('Date from must not be after Date to!')
            if record.date_from > fields.Date.today():
                raise models.ValidationError('Date from must be in the past!')
            if record.date_from == fields.Date.today():
                raise models.ValidationError('Date from must be in the past!')

    @api.constrains('date_to')
    def _check_date_to(self):
        for record in self:
            if record.date_to > fields.Date.today():
                raise models.ValidationError('Date to must be in the past!')
            if record.date_to == fields.Date.today():
                raise models.ValidationError('Date to must be in the past!')

    @api.depends('state')
    def _compute_expiration_date(self):
        for record in self:
            if record.state == 'expired':
                record.expiration_date = fields.Date.today()

    @api.depends('employee_id')
    def _compute_contract_id(self):
        for record in self:
            if record.employee_id.contract_id != False:
                record.contract_id = record.employee_id.contract_id.name


class Experiences(models.Model):
    _inherit = 'hr.employee'
    experiences = fields.One2many('hr.experience', 'employee_id')
