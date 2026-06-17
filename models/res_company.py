import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

HEX_RE = re.compile(r'^#[0-9A-Fa-f]{6}$')

class ResCompany(models.Model):
    _inherit = 'res.company'

    brand_logo = fields.Binary(string='Brand logo', attachment=True)
    brand_logo_dark = fields.Binary(string='Brand logo dark', attachment=True)
    brand_primary = fields.Char(string='Primaire kleur', default='#71639E')
    brand_accent = fields.Char(string='Accentkleur', default='#0EA5E9')
    navbar_bg = fields.Char(string='Navbar achtergrond', default='#71639E')
    auto_navbar_text = fields.Boolean(string='Navbar tekst automatisch contrast', default=True)
    navbar_text = fields.Char(string='Navbar tekst', default='#FFFFFF')
    button_bg = fields.Char(string='Primaire knop achtergrond', default='#71639E')
    auto_button_text = fields.Boolean(string='Knoptekst automatisch contrast', default=True)
    button_text = fields.Char(string='Primaire knop tekst', default='#FFFFFF')
    button_hover_bg = fields.Char(string='Primaire knop hover', default='#5E5485')
    link_color = fields.Char(string='Linkkleur', default='#0EA5E9')
    dark_surface = fields.Char(string='Dark mode achtergrond', default='#111827')
    dark_text = fields.Char(string='Dark mode tekst', default='#F9FAFB')

    @api.constrains(
        'brand_primary', 'brand_accent', 'navbar_bg', 'navbar_text',
        'button_bg', 'button_text', 'button_hover_bg', 'link_color',
        'dark_surface', 'dark_text'
    )
    def _check_hex_colors(self):
        labels = {
            'brand_primary': _('Primaire kleur'),
            'brand_accent': _('Accentkleur'),
            'navbar_bg': _('Navbar achtergrond'),
            'navbar_text': _('Navbar tekst'),
            'button_bg': _('Primaire knop achtergrond'),
            'button_text': _('Primaire knop tekst'),
            'button_hover_bg': _('Primaire knop hover'),
            'link_color': _('Linkkleur'),
            'dark_surface': _('Dark mode achtergrond'),
            'dark_text': _('Dark mode tekst'),
        }
        for company in self:
            for field_name, label in labels.items():
                value = (company[field_name] or '').strip()
                if value and not HEX_RE.match(value):
                    raise ValidationError(_('%s moet een geldige HEX-kleur zijn, bijvoorbeeld #0E5E6F.') % label)
