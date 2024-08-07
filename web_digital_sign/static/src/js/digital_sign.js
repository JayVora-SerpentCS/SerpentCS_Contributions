/** @odoo-module */

import { BinaryField } from "@web/views/fields/binary/binary_field";
import { registry } from "@web/core/registry";
import { onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { isBinarySize, toBase64Length } from "@web/core/utils/binary";
import { useService } from "@web/core/utils/hooks";

export class FieldSignature extends BinaryField {

    setup() {
        super.setup();
        this.empty_sign = [];
        this.sign_options = {
            'decor-color': '#D1D0CE',
            'color': '#000',
            'background-color': '#fff',
            'height': '150',
            'width': '550',
        };
        this.orm = useService("orm");
        this.drawsign = useRef("drawsign")

        onWillStart(async () => {
            await loadJS("/web_digital_sign/static/lib/jSignature/jSignatureCustom.js");
        });

        onMounted(async () => {
            let $signature = $(this.drawsign.el).find('.signature')
            this.renderSignature();
            $signature.jSignature("init", this.sign_options);
            $signature.change(() => {
                this.save_sign()
            });
            this.empty_sign = $signature.jSignature("getData",
                'image');
        })
    }

    async renderSignature() {
        var url = this.props.placeholder;
        if (this.props.record.data.signature && !isBinarySize(this.props.record.data[this.props.name])) {
            url = 'data:image/png;base64,' + this.props.record.data[this.props.name]
        } else if (this.props.record?.data?.signature) {
            this.field = {
                model: this.props.record.resModel,
                id: this.props.record.resId,
                field: this.props.name,
                filename_field: this.fileName,
                filename: this.fileName || "",
                data: isBinarySize(this.props.record.data[this.props.name])
                    ? null
                    : this.props.record.data[this.props.name],
            };
        } else {
            url = this.placeholder;
        }
        if (!this.props.readonly) {
            $('> img').remove();
            if (this.props.record.data.signature) {
                const binary_image = await this.orm.call(this.field.model, 'read', [this.field.id, [this.field.field]],)
                if (binary_image) {
                    self.$(".signature").jSignature("clear");
                    self.$(".signature").jSignature("setData",
                        'data:image/png;base64,' + binary_image[0].signature);
                }
            } else {
                $('> img').remove();
                $('.signature > canvas').remove();
                var sign_options = {
                    'decor-color': '#D1D0CE',
                    'color': '#000',
                    'background-color': '#fff',
                    'height': '150',
                    'width': '550',
                };
            }
        } else if (this.mode === 'create') {
            $('> img').remove();
            $('> canvas').remove();
            if (!this.value) {
                $(".signature").empty().jSignature("init", {
                    'decor-color': '#D1D0CE',
                    'color': '#000',
                    'background-color': '#fff',
                    'height': '150',
                    'width': '550',
                });
            }
        }
    }

    save_sign() {
        var self = this;
        $('> img').remove();
        var signature = $(".signature").jSignature("getData", 'image');
        var is_empty = signature ?
            self.empty_sign[1] === signature[1] :
            false;
        if (!is_empty && typeof signature !== "undefined" && signature[1]) {
            const changes = { [this.props.name]: signature[1] || false };
            this.props.record.update(changes);
        }
    }

    sign_clean() {
        $(".signature > canvas").remove();
        $('> img').remove();
        $(".signature").attr("tabindex", "0");
        var sign_options = {
            'decor-color': '#D1D0CE',
            'color': '#000',
            'background-color': '#fff',
            'height': '150',
            'width': '550',
            'clear': true,
        };
        $(".signature").jSignature(sign_options);
        $(".signature").focus();
    }

}
FieldSignature.template = "web_digital_sign.FieldSignature";

registry.category("fields").add("digital_signature", FieldSignature);