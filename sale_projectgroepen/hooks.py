def post_init_hook(env):
    ProjectGroup = env['sale.project.group']
    ProductTemplate = env['product.template']
    Pricelist = env['product.pricelist']

    if 'x_studio_spuk_project_maastricht' not in ProductTemplate._fields and \
       'x_studio_beperk_tot_maastricht_producten' not in Pricelist._fields:
        return

    maastricht_group = ProjectGroup.search([('name', '=', 'Maastricht')], limit=1)
    if not maastricht_group:
        maastricht_group = ProjectGroup.create({
            'name': 'Maastricht',
            'code': 'MAASTRICHT',
            'active': True,
            'description': 'Automatisch aangemaakt vanuit bestaande Maastricht Studio-velden.',
        })

    if 'x_studio_spuk_project_maastricht' in ProductTemplate._fields:
        products = ProductTemplate.search([('x_studio_spuk_project_maastricht', '=', True)])
        for product in products:
            if maastricht_group not in product.project_group_ids:
                product.with_context(skip_projectgroep_propagation=True).write({
                    'project_group_ids': [(4, maastricht_group.id)]
                })

    existing = ProductTemplate.search([('project_group_ids', '!=', False), ('optional_product_ids', '!=', False)])
    existing._propagate_projectgroepen_to_optional_products()

    if 'x_studio_beperk_tot_maastricht_producten' in Pricelist._fields:
        pricelists = Pricelist.search([('x_studio_beperk_tot_maastricht_producten', '=', True)])
        for pricelist in pricelists:
            vals = {'allowed_project_group_ids': [(4, maastricht_group.id)]}
            if pricelist.project_group_policy == 'none':
                vals['project_group_policy'] = 'remove_invalid'
            pricelist.write(vals)
