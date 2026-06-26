from odoo import fields, models


class SaleProjectGroup(models.Model):
    _name = 'sale.project.group'
    _description = 'Projectgroep'
    _order = 'sequence, name'

    name = fields.Char(string='Naam', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(string='Actief', default=True)
    description = fields.Text(string='Omschrijving')
    company_id = fields.Many2one('res.company', string='Bedrijf')
    color = fields.Integer(string='Kleurindex')
    sequence = fields.Integer(string='Volgorde', default=10)
