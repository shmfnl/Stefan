from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    brand_logo = fields.Binary(related='company_id.brand_logo', readonly=False, string='Brand logo')
    brand_logo_dark = fields.Binary(related='company_id.brand_logo_dark', readonly=False, string='Brand logo dark')
    brand_primary = fields.Char(related='company_id.brand_primary', readonly=False, string='Primaire kleur')
    brand_accent = fields.Char(related='company_id.brand_accent', readonly=False, string='Accentkleur')
    navbar_bg = fields.Char(related='company_id.navbar_bg', readonly=False, string='Navbar achtergrond')
    auto_navbar_text = fields.Boolean(related='company_id.auto_navbar_text', readonly=False, string='Navbar tekst automatisch contrast')
    navbar_text = fields.Char(related='company_id.navbar_text', readonly=False, string='Navbar tekst')
    button_bg = fields.Char(related='company_id.button_bg', readonly=False, string='Primaire knop achtergrond')
    auto_button_text = fields.Boolean(related='company_id.auto_button_text', readonly=False, string='Knoptekst automatisch contrast')
    button_text = fields.Char(related='company_id.button_text', readonly=False, string='Primaire knop tekst')
    button_hover_bg = fields.Char(related='company_id.button_hover_bg', readonly=False, string='Primaire knop hover')
    button_secondary_bg = fields.Char(string='Secondary knop achtergrond', config_parameter='web_branding_company.button_secondary_bg', default='#FFFFFF')
    button_secondary_text = fields.Char(string='Secondary knop tekst', config_parameter='web_branding_company.button_secondary_text', default='#71639E')
    button_secondary_hover_bg = fields.Char(string='Secondary knop hover', config_parameter='web_branding_company.button_secondary_hover_bg', default='#EEEAF8')
    link_color = fields.Char(related='company_id.link_color', readonly=False, string='Linkkleur')
    dark_surface = fields.Char(related='company_id.dark_surface', readonly=False, string='Dark mode achtergrond')
    dark_text = fields.Char(related='company_id.dark_text', readonly=False, string='Dark mode tekst')
