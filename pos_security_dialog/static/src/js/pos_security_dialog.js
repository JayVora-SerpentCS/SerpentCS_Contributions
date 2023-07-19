odoo.define("pos_security_dialog.SecurityDialog", function (require) {
    "use strict";

    const NumpadWidget = require('point_of_sale.NumpadWidget');
    const Registries = require('point_of_sale.Registries');

    const PosExtendNumpadWidget = (NumpadWidget) =>
    class extends NumpadWidget {
        changeMode(mode) {
            if (!this.hasPriceControlRights && mode === 'price') {
                return;
            }
            if (!this.hasManualDiscount && mode === 'discount') {
                return;
            }
            if(mode === 'price' || mode === 'discount') {
                this.openSecurityDialog(mode);
            }else {
                this.trigger('set-numpad-mode', { mode });
            }
        }
        async openSecurityDialog(mode){
            const { confirmed, payload: inputPin } = await this.showPopup('NumberPopup', {
                isPassword: true,
                title: this.env._t('Password ?'),
                startingValue: null,
            });
            if (!confirmed) return false;
            if (this.env.pos.company.security_key === inputPin) {
                this.trigger('set-numpad-mode', { mode });
            } else {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Incorrect Password'),
                });
                this.trigger('set-numpad-mode', { mode: 'quantity' });
            }
        }
    };

    Registries.Component.extend(NumpadWidget, PosExtendNumpadWidget);

    return NumpadWidget;

});
