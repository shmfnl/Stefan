import json
from odoo import http
from odoo.http import request

class WebBrandingCompanyController(http.Controller):

    @http.route('/web_branding_company/runtime_branding.json', type='http', auth='user', website=False, sitemap=False)
    def runtime_branding_json(self, **kwargs):
        company = request.env.company.sudo()
        icp = request.env['ir.config_parameter'].sudo()
        payload = {
            'navbar_bg': (company.navbar_bg or '#71639E').strip() or '#71639E',
            'navbar_text': (company.navbar_text or '#FFFFFF').strip() or '#FFFFFF',
            'button_secondary_bg': (icp.get_param('web_branding_company.button_secondary_bg', '#FFFFFF') or '#FFFFFF').strip(),
            'button_secondary_text': (icp.get_param('web_branding_company.button_secondary_text', '#71639E') or '#71639E').strip(),
            'button_secondary_hover_bg': (icp.get_param('web_branding_company.button_secondary_hover_bg', '#EEEAF8') or '#EEEAF8').strip(),
        }
        return request.make_response(json.dumps(payload), headers=[
            ('Content-Type', 'application/json; charset=utf-8'),
            ('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0'),
        ])

    @http.route('/web_branding_company/runtime_style.css', type='http', auth='user', website=False, sitemap=False)
    def runtime_style_css(self, **kwargs):
        company = request.env.company.sudo()
        icp = request.env['ir.config_parameter'].sudo()
        navbar_bg = (company.navbar_bg or '#71639E').strip() or '#71639E'
        navbar_text = (company.navbar_text or '#FFFFFF').strip() or '#FFFFFF'
        button_bg = (company.button_bg or '#71639E').strip() or '#71639E'
        button_text = (company.button_text or '#FFFFFF').strip() or '#FFFFFF'
        button_hover_bg = (company.button_hover_bg or '#5E5485').strip() or '#5E5485'
        button_secondary_bg = (icp.get_param('web_branding_company.button_secondary_bg', '#FFFFFF') or '#FFFFFF').strip()
        button_secondary_text = (icp.get_param('web_branding_company.button_secondary_text', '#71639E') or '#71639E').strip()
        button_secondary_hover_bg = (icp.get_param('web_branding_company.button_secondary_hover_bg', '#EEEAF8') or '#EEEAF8').strip()
        link_color = (company.link_color or '#0EA5E9').strip() or '#0EA5E9'
        brand_primary = (company.brand_primary or '#71639E').strip() or '#71639E'
        brand_accent = (company.brand_accent or '#0EA5E9').strip() or '#0EA5E9'

        logo_rules = ''
        if company.brand_logo:
            logo_rules += f"""
.o_main_navbar .o_menu_brand,
.o_main_navbar .o_menu_brand:hover,
.o_main_navbar .o_menu_brand:focus {{
    background-image: url('/web/image/res.company/{company.id}/brand_logo');
    background-repeat: no-repeat;
    background-position: center left;
    background-size: contain;
    min-width: 160px;
    width: 160px;
    text-indent: -9999px;
    overflow: hidden;
    white-space: nowrap;
    display: inline-block;
}}
"""
        if company.brand_logo_dark:
            logo_rules += f"""
html.o_dark_mode .o_main_navbar .o_menu_brand,
html[data-theme="dark"] .o_main_navbar .o_menu_brand {{
    background-image: url('/web/image/res.company/{company.id}/brand_logo_dark');
}}
"""

        content_link_selectors = ".o_form_view .o_field_widget a[href]:not(.btn):not(.dropdown-item):not(.nav-link):not(.o_menu_brand), .o_form_view .oe_title a[href]:not(.btn):not(.dropdown-item):not(.nav-link):not(.o_menu_brand), .o_list_view tbody a[href]:not(.btn):not(.dropdown-item):not(.nav-link):not(.o_menu_brand), .o_kanban_view .o_kanban_record a[href]:not(.btn):not(.dropdown-item):not(.nav-link):not(.o_menu_brand), .o_control_panel .breadcrumb a, .btn-link"

        css = f"""
:root {{ --web-branding-navbar-bg: {navbar_bg}; --web-branding-navbar-text: {navbar_text}; }}
.o_main_navbar, .o_navbar, header.o_navbar {{ background-color: {navbar_bg} !important; color: {navbar_text} !important; background-image: none !important; border-bottom: none !important; }}
/* MuK selectors */
body.mk_sidebar_type_large .o_navbar,
body.mk_sidebar_type_small .o_navbar,
body.mk_sidebar_type_invisible .o_navbar,
body.mk_sidebar_type_large .o_main_navbar,
body.mk_sidebar_type_small .o_main_navbar,
body.mk_sidebar_type_invisible .o_main_navbar,
body.mk_sidebar_type_large header.o_navbar,
body.mk_sidebar_type_small header.o_navbar,
body.mk_sidebar_type_invisible header.o_navbar {{ background-color: {navbar_bg} !important; color: {navbar_text} !important; background-image: none !important; border-bottom: none !important; }}
.o_main_navbar a, .o_main_navbar .dropdown-toggle, .o_main_navbar .o_menu_brand, .o_main_navbar .oe_topbar_name, .o_main_navbar .o-dropdown--menu .dropdown-item, .o_main_navbar .o_nav_entry, .o_main_navbar i, .o_main_navbar span,
body.mk_sidebar_type_large .o_navbar a, body.mk_sidebar_type_large .o_navbar i, body.mk_sidebar_type_large .o_navbar span,
body.mk_sidebar_type_small .o_navbar a, body.mk_sidebar_type_small .o_navbar i, body.mk_sidebar_type_small .o_navbar span,
body.mk_sidebar_type_invisible .o_navbar a, body.mk_sidebar_type_invisible .o_navbar i, body.mk_sidebar_type_invisible .o_navbar span,
body.mk_sidebar_type_large .mk_app_menu button, body.mk_sidebar_type_small .mk_app_menu button, body.mk_sidebar_type_invisible .mk_app_menu button {{ color: {navbar_text} !important; }}
.btn-primary, .o_cp_buttons .btn-primary, .o_form_button_save, .o_btn_primary {{ background-color: {button_bg} !important; border-color: {button_bg} !important; color: {button_text} !important; }}
.btn-primary:hover, .btn-primary:focus, .btn-primary:active, .o_cp_buttons .btn-primary:hover, .o_cp_buttons .btn-primary:focus, .o_form_button_save:hover, .o_form_button_save:focus, .o_btn_primary:hover, .o_btn_primary:focus {{ background-color: {button_hover_bg} !important; border-color: {button_hover_bg} !important; color: {button_text} !important; }}
.btn-secondary, .o_cp_buttons .btn-secondary, .o_form_button_cancel, .o_form_button_edit {{ background-color: {button_secondary_bg} !important; border-color: {button_secondary_bg} !important; color: {button_secondary_text} !important; }}
.btn-secondary:hover, .btn-secondary:focus, .btn-secondary:active, .o_cp_buttons .btn-secondary:hover, .o_cp_buttons .btn-secondary:focus, .o_form_button_cancel:hover, .o_form_button_cancel:focus, .o_form_button_edit:hover, .o_form_button_edit:focus {{ background-color: {button_secondary_hover_bg} !important; border-color: {button_secondary_hover_bg} !important; color: {button_secondary_text} !important; }}
{content_link_selectors} {{ color: {link_color} !important; }}
.dropdown-item.active, .dropdown-item:active, .nav-pills .nav-link.active, .page-item.active .page-link, .form-check-input:checked, .progress-bar, .badge.text-bg-primary, .bg-primary {{ background-color: {brand_primary} !important; border-color: {brand_primary} !important; }}
.nav-pills .nav-link.active, .page-item.active .page-link, .badge.text-bg-primary, .text-bg-primary {{ color: #FFFFFF !important; }}
.o_field_widget .form-control:focus, .o_input:focus, .form-control:focus, .form-select:focus, textarea:focus {{ border-color: {brand_accent} !important; box-shadow: 0 0 0 0.2rem {brand_accent}33 !important; }}
{logo_rules}
""".strip()
        return request.make_response(css, headers=[
            ('Content-Type', 'text/css; charset=utf-8'),
            ('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0'),
        ])
