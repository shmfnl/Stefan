/** @odoo-module **/
function injectRuntimeStyle(cssText) {
    let styleTag = document.getElementById("web_branding_company_runtime_style");
    if (!styleTag) {
        styleTag = document.createElement("style");
        styleTag.id = "web_branding_company_runtime_style";
        document.head.appendChild(styleTag);
    }
    styleTag.textContent = cssText;
}
function setCssVariables(data) {
    if (!data) return;
    if (data.navbar_bg) document.documentElement.style.setProperty('--web-branding-navbar-bg', data.navbar_bg);
    if (data.navbar_text) document.documentElement.style.setProperty('--web-branding-navbar-text', data.navbar_text);
}
function setImportantStyle(el, prop, value) {
    if (!el || !value) return;
    el.style.setProperty(prop, value, 'important');
}
function applyMukInlineBranding(data) {
    const bg = data?.navbar_bg;
    const text = data?.navbar_text;
    if (!bg || !text) return;
    const selectors = [
        'body.mk_sidebar_type_large .o_navbar',
        'body.mk_sidebar_type_small .o_navbar',
        'body.mk_sidebar_type_invisible .o_navbar',
        'body.mk_sidebar_type_large .o_main_navbar',
        'body.mk_sidebar_type_small .o_main_navbar',
        'body.mk_sidebar_type_invisible .o_main_navbar',
        'body.mk_sidebar_type_large header.o_navbar',
        'body.mk_sidebar_type_small header.o_navbar',
        'body.mk_sidebar_type_invisible header.o_navbar',
    ];
    const textSelectors = [
        'body.mk_sidebar_type_large .o_navbar a',
        'body.mk_sidebar_type_small .o_navbar a',
        'body.mk_sidebar_type_invisible .o_navbar a',
        'body.mk_sidebar_type_large .o_navbar i',
        'body.mk_sidebar_type_small .o_navbar i',
        'body.mk_sidebar_type_invisible .o_navbar i',
        'body.mk_sidebar_type_large .o_navbar span',
        'body.mk_sidebar_type_small .o_navbar span',
        'body.mk_sidebar_type_invisible .o_navbar span',
        'body.mk_sidebar_type_large .mk_app_menu button',
        'body.mk_sidebar_type_small .mk_app_menu button',
        'body.mk_sidebar_type_invisible .mk_app_menu button',
    ];
    selectors.forEach((selector) => {
        document.querySelectorAll(selector).forEach((el) => {
            setImportantStyle(el, 'background-color', bg);
            setImportantStyle(el, 'background-image', 'none');
            setImportantStyle(el, 'color', text);
            setImportantStyle(el, 'border-bottom', 'none');
        });
    });
    textSelectors.forEach((selector) => {
        document.querySelectorAll(selector).forEach((el) => {
            setImportantStyle(el, 'color', text);
        });
    });
}
async function loadRuntimeStyle() {
    try {
        const response = await fetch('/web_branding_company/runtime_style.css', { credentials: 'same-origin', cache: 'no-store' });
        if (!response.ok) return;
        const cssText = await response.text();
        injectRuntimeStyle(cssText);
    } catch (err) {
        console.warn('web_branding_company runtime style kon niet worden geladen', err);
    }
}
async function loadRuntimeBrandingJson() {
    try {
        const response = await fetch('/web_branding_company/runtime_branding.json', { credentials: 'same-origin', cache: 'no-store' });
        if (!response.ok) return;
        const data = await response.json();
        setCssVariables(data);
        applyMukInlineBranding(data);
    } catch (err) {
        console.warn('web_branding_company runtime branding json kon niet worden geladen', err);
    }
}
async function refreshBranding() { await loadRuntimeStyle(); await loadRuntimeBrandingJson(); }
if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', refreshBranding); } else { refreshBranding(); }
window.addEventListener('focus', refreshBranding);
window.addEventListener('load', refreshBranding);
setInterval(loadRuntimeBrandingJson, 2500);
