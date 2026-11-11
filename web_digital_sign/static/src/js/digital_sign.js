/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { ImageField } from "@web/views/fields/image/image_field";

import { onMounted, onPatched, useRef } from "@odoo/owl";

/**
 * FieldSignature: legacy v14 FieldBinaryImage-based widget rewritten as an OWL
 * field component. The signature is drawn on a <canvas> (mouse/touch/pen via
 * pointer events; this replaces the legacy jSignature jQuery plugin) and stored
 * as a base64 PNG data URL in the Binary field, exactly as the v14 widget did.
 */
export class FieldSignature extends ImageField {
    static template = "FieldSignature";
    static props = { ...ImageField.props };

    setup() {
        super.setup();
        this.canvasRef = useRef("canvas");
        this.sign_options = {
            "decor-color": "#D1D0CE",
            "color": "#000",
            "background-color": "#fff",
            "height": "150",
            "width": "550",
        };
        this.has_strokes = false;
        this.drawing = false;
        this._initializedEl = undefined;
        this._initializedRecord = undefined;
        this._loadToken = 0;
        onMounted(() => this._init_canvas());
        onPatched(() => this._init_canvas());
    }

    /**
     * Initializes the drawing canvas (empty, or filled with the stored
     * signature). Only runs when a canvas element is (re)created or when the
     * record changes, so a drawing in progress is never wiped out.
     */
    _init_canvas() {
        const canvas = this.canvasRef.el;
        if (!canvas || this.props.readonly) {
            return;
        }
        if (canvas === this._initializedEl && this.props.record === this._initializedRecord) {
            return;
        }
        this._initializedEl = canvas;
        this._initializedRecord = this.props.record;
        this.has_strokes = false;
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const value = this.props.record.data[this.props.name];
        if (value) {
            const token = ++this._loadToken;
            const img = new Image();
            img.onload = () => {
                if (token !== this._loadToken || canvas !== this.canvasRef.el) {
                    return;
                }
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                this.has_strokes = true;
            };
            img.src = this.getUrl(this.props.name);
        }
    }

    _get_pointer_position(ev) {
        const canvas = this.canvasRef.el;
        const rect = canvas.getBoundingClientRect();
        return {
            x: (ev.clientX - rect.left) * (canvas.width / rect.width),
            y: (ev.clientY - rect.top) * (canvas.height / rect.height),
        };
    }

    _on_pointer_down(ev) {
        ev.preventDefault();
        const canvas = this.canvasRef.el;
        canvas.setPointerCapture(ev.pointerId);
        this.drawing = true;
        this.has_strokes = true;
        const ctx = canvas.getContext("2d");
        ctx.strokeStyle = this.sign_options.color;
        ctx.lineWidth = 2;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
        ctx.beginPath();
        const { x, y } = this._get_pointer_position(ev);
        ctx.moveTo(x, y);
        // draw a small segment so a simple click leaves a mark
        ctx.lineTo(x + 0.1, y);
        ctx.stroke();
    }

    _on_pointer_move(ev) {
        if (!this.drawing) {
            return;
        }
        ev.preventDefault();
        const { x, y } = this._get_pointer_position(ev);
        const ctx = this.canvasRef.el.getContext("2d");
        ctx.lineTo(x, y);
        ctx.stroke();
    }

    _on_pointer_up(ev) {
        if (!this.drawing) {
            return;
        }
        this.drawing = false;
        // v14 committed the drawing when the record was saved (the form
        // controller clicked '.save_sign'); here the value is kept in sync on
        // every stroke so it is always written with the record.
        this._on_save_sign();
    }

    _on_clear_sign(ev) {
        ev.preventDefault();
        const canvas = this.canvasRef.el;
        if (canvas) {
            const ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
        this.has_strokes = false;
        this.props.record.update({ [this.props.name]: false });
    }

    _on_save_sign(ev) {
        if (ev) {
            ev.preventDefault();
        }
        const canvas = this.canvasRef.el;
        if (!canvas || !this.has_strokes) {
            return;
        }
        const signature = canvas.toDataURL("image/png").split(",")[1];
        if (signature) {
            this.props.record.update({ [this.props.name]: signature });
        }
    }
}

export const signatureField = {
    component: FieldSignature,
    displayName: _t("Signature"),
    supportedTypes: ["binary"],
};

registry.category("fields").add("klo_signature", signatureField);
