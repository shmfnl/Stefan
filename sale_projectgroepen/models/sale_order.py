from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _projectgroepen_restriction_active(self):
        self.ensure_one()
        pricelist = self.pricelist_id
        return bool(pricelist and pricelist.project_group_policy != 'none' and pricelist.allowed_project_group_ids)

    def _get_invalid_projectgroep_lines(self):
        self.ensure_one()
        if not self.pricelist_id:
            return self.env['sale.order.line']
        return self.order_line.filtered(
            lambda l: not l.display_type and l.product_id and not l._product_matches_projectgroep_rule(l.product_id)
        )

    def _get_orphan_display_lines(self, remaining_lines):
        ordered = remaining_lines.sorted(key=lambda l: (l.sequence or 0, l._origin.id or 0, str(l.id)))
        orphan = self.env['sale.order.line']
        count = len(ordered)
        for idx, line in enumerate(ordered):
            if not line.display_type:
                continue
            has_real_line = False
            for nxt in ordered[idx + 1:count]:
                if nxt.display_type == 'line_section':
                    break
                if not nxt.display_type:
                    has_real_line = True
                    break
            if not has_real_line:
                orphan |= line
        return orphan

    def _get_lines_to_remove(self):
        self.ensure_one()
        invalid_lines = self._get_invalid_projectgroep_lines()
        if not invalid_lines:
            return invalid_lines
        remaining_lines = self.order_line - invalid_lines
        return invalid_lines | self._get_orphan_display_lines(remaining_lines)

    def _format_removed_products_message(self, removed_lines):
        product_names = removed_lines.filtered(lambda l: not l.display_type and l.product_id).mapped('product_id.display_name')
        section_names = removed_lines.filtered(lambda l: l.display_type == 'line_section').mapped('name')
        note_names = removed_lines.filtered(lambda l: l.display_type == 'line_note').mapped('name')
        parts = []
        if product_names:
            if len(product_names) == 1:
                parts.append(_('Verwijderd product:\n- %(items)s') % {'items': product_names[0]})
            else:
                parts.append(_('Verwijderde producten:\n- %(items)s') % {'items': '\n- '.join(product_names)})
        if section_names:
            parts.append(_('Verwijderde secties:\n- %(items)s') % {'items': '\n- '.join(section_names)})
        if note_names:
            parts.append(_('Verwijderde notities:\n- %(items)s') % {'items': '\n- '.join(note_names)})
        header = _('%(count)s productregel(s) en gekoppelde structuurregels zijn automatisch verwijderd omdat de gekozen prijslijst het product niet toestaat of alleen producten toestaat binnen de toegestane projectgroepen.') % {'count': len(product_names)}
        return header if not parts else header + '\n\n' + '\n\n'.join(parts)

    def _apply_projectgroep_policy(self, post_chatter_message=False):
        for order in self:
            if not order.pricelist_id:
                continue
            invalid_lines = order._get_invalid_projectgroep_lines()
            if not invalid_lines:
                continue
            lines_to_remove = order._get_lines_to_remove()
            policy = order.pricelist_id.project_group_policy
            info_message = order._format_removed_products_message(lines_to_remove)
            blocked_only = invalid_lines.filtered(lambda l: l._is_blocked_on_current_pricelist(l.product_id))
            if policy == 'block_invalid':
                names = ', '.join(invalid_lines.mapped('product_id.display_name'))
                raise ValidationError(_('Deze prijslijst staat één of meer producten niet toe. Niet-toegestane producten: %s') % names)
            if policy == 'remove_invalid' or blocked_only or policy == 'none':
                lines_to_remove.unlink()
                if post_chatter_message and info_message and hasattr(order, 'message_post'):
                    order.message_post(body=info_message.replace('\n', '<br/>'), subtype_xmlid='mail.mt_note')

    @api.onchange('pricelist_id')
    def _onchange_pricelist_id_projectgroepen_cleanup(self):
        if not self.pricelist_id:
            return {}
        invalid_lines = self._get_invalid_projectgroep_lines()
        if not invalid_lines:
            return {}
        lines_to_remove = self._get_lines_to_remove()
        policy = self.pricelist_id.project_group_policy
        blocked_only = invalid_lines.filtered(lambda l: l._is_blocked_on_current_pricelist(l.product_id))
        if policy in ('remove_invalid', 'none') or blocked_only:
            info_message = self._format_removed_products_message(lines_to_remove)
            self.order_line = self.order_line - lines_to_remove
            return {'warning': {'title': _('Productregels automatisch verwijderd'), 'message': info_message}}
        if policy == 'block_invalid':
            names = ', '.join(invalid_lines.mapped('product_id.display_name'))
            return {'warning': {'title': _('Niet-toegestane producten aanwezig'), 'message': _('Deze prijslijst staat één of meer producten niet toe. Controleer deze regels: %s') % names}}
        return {}

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        orders._apply_projectgroep_policy(post_chatter_message=True)
        return orders

    def write(self, vals):
        result = super().write(vals)
        if 'pricelist_id' in vals or 'order_line' in vals:
            self._apply_projectgroep_policy(post_chatter_message=True)
        return result


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_toegestane_product_template_ids = fields.Many2many(
        'product.template', compute='_compute_toegestane_producten_hulpvelden', store=False,
        readonly=True, string='Toegestane productsjablonen (hulp)'
    )
    x_toegestane_product_ids = fields.Many2many(
        'product.product', compute='_compute_toegestane_producten_hulpvelden', store=False,
        readonly=True, string='Toegestane productvarianten (hulp)'
    )

    @api.depends(
        'order_id.pricelist_id',
        'order_id.pricelist_id.allowed_project_group_ids',
        'order_id.pricelist_id.project_group_policy',
        'order_id.pricelist_id.forbidden_product_tmpl_ids',
    )
    def _compute_toegestane_producten_hulpvelden(self):
        Template = self.env['product.template']
        Product = self.env['product.product']
        for line in self:
            pricelist = line.order_id.pricelist_id
            tmpl_domain = [('sale_ok', '=', True)]
            product_domain = [('sale_ok', '=', True)]
            if pricelist:
                forbidden_ids = pricelist.forbidden_product_tmpl_ids.ids
                if forbidden_ids:
                    tmpl_domain.append(('id', 'not in', forbidden_ids))
                    product_domain.append(('product_tmpl_id', 'not in', forbidden_ids))
                tmpl_domain.append(('excluded_pricelist_ids', 'not in', [pricelist.id]))
                product_domain.append(('product_tmpl_id.excluded_pricelist_ids', 'not in', [pricelist.id]))
                if pricelist.project_group_policy != 'none' and pricelist.allowed_project_group_ids:
                    group_ids = pricelist.allowed_project_group_ids.ids
                    tmpl_domain.append(('project_group_ids', 'in', group_ids))
                    product_domain.append(('product_tmpl_id.project_group_ids', 'in', group_ids))
            line.x_toegestane_product_template_ids = Template.search(tmpl_domain)
            line.x_toegestane_product_ids = Product.search(product_domain)

    def _current_pricelist(self):
        self.ensure_one()
        return self.order_id.pricelist_id if self.order_id else self.env['product.pricelist']

    def _is_blocked_on_current_pricelist(self, product):
        self.ensure_one()
        pricelist = self._current_pricelist()
        if not pricelist or not product:
            return False
        tmpl = product.product_tmpl_id
        return bool(tmpl in pricelist.forbidden_product_tmpl_ids or pricelist in tmpl.excluded_pricelist_ids)

    def _allowed_project_groups(self):
        self.ensure_one()
        return self.order_id.pricelist_id.allowed_project_group_ids if self.order_id and self.order_id.pricelist_id else self.env['sale.project.group']

    def _product_matches_direct_projectgroep_rule(self, product):
        self.ensure_one()
        if self._is_blocked_on_current_pricelist(product):
            return False
        if not self.order_id or not self.order_id._projectgroepen_restriction_active():
            return True
        allowed_groups = self._allowed_project_groups()
        template_groups = product.product_tmpl_id.project_group_ids
        return bool(template_groups and (template_groups & allowed_groups))

    def _is_allowed_as_optional_product(self, product):
        self.ensure_one()
        if self._is_blocked_on_current_pricelist(product):
            return False
        if not self.order_id or not product:
            return False
        product_tmpl = product.product_tmpl_id
        valid_parent_lines = self.order_id.order_line.filtered(
            lambda l: not l.display_type and l.product_id and l.id != self.id and l._product_matches_direct_projectgroep_rule(l.product_id)
        )
        for parent_line in valid_parent_lines:
            if product_tmpl in parent_line.product_id.product_tmpl_id.optional_product_ids:
                return True
        return False

    def _product_matches_projectgroep_rule(self, product):
        self.ensure_one()
        if self._is_blocked_on_current_pricelist(product):
            return False
        if self._product_matches_direct_projectgroep_rule(product):
            return True
        return self._is_allowed_as_optional_product(product)

    @api.onchange('order_id', 'product_id', 'product_template_id')
    def _onchange_projectgroepen_cleanup(self):
        result = {}
        for line in self:
            if line.display_type or not line.order_id:
                continue
            result['domain'] = {
                'product_template_id': [('id', 'in', line.x_toegestane_product_template_ids.ids)],
                'product_id': [('id', 'in', line.x_toegestane_product_ids.ids)],
            }
            invalid = False
            if line.product_id and not line._product_matches_projectgroep_rule(line.product_id):
                invalid = True
            elif 'product_template_id' in line._fields and line.product_template_id:
                variant = line.product_template_id.product_variant_id
                if variant and not line._product_matches_projectgroep_rule(variant):
                    invalid = True
            if invalid:
                removed_product = line.product_id.display_name or line.product_template_id.display_name
                line.product_id = False
                if 'product_template_id' in line._fields:
                    line.product_template_id = False
                result['warning'] = {
                    'title': _('Product verwijderd'),
                    'message': _('Het product "%s" is verwijderd omdat de gekozen prijslijst dit product niet toestaat.') % removed_product,
                }
        return result

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines.mapped('order_id')._apply_projectgroep_policy(post_chatter_message=True)
        return lines.exists()

    def write(self, vals):
        result = super().write(vals)
        self.mapped('order_id')._apply_projectgroep_policy(post_chatter_message=True)
        return result
