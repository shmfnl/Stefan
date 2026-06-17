{
    "name": "Backend styling",
    "version": "18.0.111.1.4",
    "summary": "Phase 11c fix: secondary button velden zichtbaar in settings",
    "category": "Tools",
    "license": "LGPL-3",
    "author": "Stefan Heinen",
    "depends": ["web", "base_setup"],
    "data": [
        "views/res_config_settings_views.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "web_branding_company/static/src/js/runtime_style.js",
            "web_branding_company/static/src/js/hex_color_picker_field.js",
            "web_branding_company/static/src/xml/hex_color_picker_field.xml",
            "web_branding_company/static/src/scss/fallback.scss",
            "web_branding_company/static/src/scss/hex_color_picker_field.scss"
        ]
    },
    "application": True,
    "installable": True
}
