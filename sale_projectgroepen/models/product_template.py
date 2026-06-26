from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    project_group_ids = fields.Many2many(
        'sale.project.group',
        'product_template_project_group_rel',
        'product_tmpl_id',
        'project_group_id',
        string='Projectgroepen',
        help='Projectgroepen waarmee productselectie per prijslijst gestuurd wordt.',
    )
    excluded_pricelist_ids = fields.Many2many(
        'product.pricelist',
        'product_template_pricelist_exclude_rel',
        'product_tmpl_id',
        'pricelist_id',
        string='Niet toestaan op prijslijsten',
        help='Op deze prijslijsten mag dit product niet gekozen worden.',
    )

    def _propagate_projectgroepen_to_optional_products(self):
        if self.env.context.get('skip_projectgroep_propagation'):
            return
        for template in self:
            if not template.project_group_ids or not template.optional_product_ids:
                continue
            for optional in template.optional_product_ids:
                missing = template.project_group_ids - optional.project_group_ids
                if missing:
                    optional.with_context(skip_projectgroep_propagation=True).write({
                        'project_group_ids': [(4, gid) for gid in missing.ids]
                    })

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        templates._propagate_projectgroepen_to_optional_products()
        return templates

    def write(self, vals):
        result = super().write(vals)
        if {'project_group_ids', 'optional_product_ids'}.intersection(vals.keys()):
            self._propagate_projectgroepen_to_optional_products()
        return result
