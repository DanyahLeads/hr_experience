from odoo import models, fields, api


class experienceWizard(models.TransientModel):
    _name = 'add.experience'
    _description = 'Add an Experience'

    name = fields.Char("Name")
    date_to = fields.Date("Date To")
    date_from = fields.Date("Date From")
    expiration_date = fields.Date(string='Expiration Date')

    # to the button action
    def auto_configuration(self):
        values = {
            'name': self.name,
            'date_to': self.date_to,
            'date_from': self.date_from,
            'expiration_date': self.expiration_date
        }
        self.env['hr.experience'].create(values)

        return {
            'effect': {
                'fadeout': 'fast',
                'message': 'Added Successfully',
                'type': 'man',
            }
        }