from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    allowed_project_group_ids = fields.Many2many(
        'sale.project.group',
        'product_pricelist_project_group_rel',
        'pricelist_id',
        'project_group_id',
        string='Toegestane projectgroepen',
        help='Alleen producten binnen deze projectgroepen mogen gekozen worden op deze prijslijst.',
    )
    forbidden_product_tmpl_ids = fields.Many2many(
        'product.template',
        'product_pricelist_forbidden_product_rel',
        'pricelist_id',
        'product_tmpl_id',
        string='Verboden producten',
        domain=[('sale_ok', '=', True)],
        help='Deze producten mogen op deze prijslijst niet gekozen worden.',
    )
    project_group_policy = fields.Selection(
        [
            ('none', 'Geen beperking'),
            ('remove_invalid', 'Niet-toegestane regels verwijderen'),
            ('block_invalid', 'Niet-toegestane regels blokkeren'),
        ],
        string='Projectgroepenbeleid',
        default='none',
        required=True,
    )
