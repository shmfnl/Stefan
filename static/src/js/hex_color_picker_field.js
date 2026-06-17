/** @odoo-module **/
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useState, onWillUpdateProps } from "@odoo/owl";
const HEX_RE = /^#[0-9A-Fa-f]{6}$/;
export class HexColorPickerField extends Component {
    static template = "web_branding_company.HexColorPickerField";
    static props = { ...standardFieldProps };
    static supportedTypes = ["char"];
    setup() { this.state = useState({ text: this._currentRecordValue() }); onWillUpdateProps((nextProps) => { this.state.text = this._currentRecordValue(nextProps); }); }
    _normalizeDisplay(value) { return String(value || "").trim().toUpperCase(); }
    _isValidHex(value) { return HEX_RE.test(String(value || "").trim()); }
    _currentRecordValue(props = this.props) { const fromRecord = props?.record?.data && props?.name ? props.record.data[props.name] : undefined; const raw = fromRecord !== undefined && fromRecord !== null && fromRecord !== '' ? fromRecord : props?.value; return this._normalizeDisplay(raw || ''); }
    _commit(value) { const clean = this._normalizeDisplay(value); if (this.props.record && typeof this.props.record.update === "function" && this.props.name) { this.props.record.update({ [this.props.name]: clean }); return; } if (typeof this.props.update === "function") this.props.update(clean); }
    get colorValue() { const current = this.state.text || this._currentRecordValue(); return this._isValidHex(current) ? current : "#000000"; }
    get invalidClass() { const current = this.state.text || this._currentRecordValue(); return this._isValidHex(current) ? "" : " o_hex_color_picker_invalid"; }
    get displayText() { return this.state.text || this._currentRecordValue(); }
    onColorInput(ev) { const value = this._normalizeDisplay(ev.target.value); this.state.text = value; this._commit(value); }
    onTextInput(ev) { this.state.text = this._normalizeDisplay(ev.target.value); }
    onTextBlur() { if (this._isValidHex(this.state.text)) { this._commit(this.state.text); } else { this.state.text = this._currentRecordValue(); } }
}
registry.category("fields").add("hex_color_picker", { component: HexColorPickerField, supportedTypes: ["char"] });
