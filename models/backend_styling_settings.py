from odoo import fields, models

class BackendStylingSettings(models.TransientModel):
    _name = 'backend.styling.settings'
    _description = 'Backend Styling Settings (compat shim)'

    company_id = fields.Many2one('res.company', string='Bedrijf', required=True, default=lambda self: self.env.company)

    brand_logo = fields.Binary(related='company_id.brand_logo', readonly=False, string='Brand logo')
    brand_logo_dark = fields.Binary(related='company_id.brand_logo_dark', readonly=False, string='Brand logo dark')
    brand_primary = fields.Char(related='company_id.brand_primary', readonly=False, string='Primaire kleur')
    brand_accent = fields.Char(related='company_id.brand_accent', readonly=False, string='Accentkleur')
    navbar_bg = fields.Char(related='company_id.navbar_bg', readonly=False, string='Navbar achtergrond')
    navbar_text = fields.Char(related='company_id.navbar_text', readonly=False, string='Navbar tekst')
    button_bg = fields.Char(related='company_id.button_bg', readonly=False, string='Primaire knop achtergrond')
    button_text = fields.Char(related='company_id.button_text', readonly=False, string='Primaire knop tekst')
    button_hover_bg = fields.Char(related='company_id.button_hover_bg', readonly=False, string='Primaire knop hover')
    link_color = fields.Char(related='company_id.link_color', readonly=False, string='Linkkleur')
