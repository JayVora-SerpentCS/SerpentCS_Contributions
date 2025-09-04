/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";

ListController.prototype.expandlist = async function () {
    try {
        this.env.services.ui.block();

        var group = this.model.root.groups;
        for (let i = 0; i < group.length; i++) {
            if (group[i].isFolded) {
                await group[i].toggle();
            }
            var groupOfList = await group[i].list.model.root.groups[i].list.model.root.groups[i].list.groups;
            await this._onClickChild(groupOfList);
        }
        document.getElementsByClassName("exp-btn")[0].classList.add('o_hidden');
        document.getElementsByClassName("cmp-btn")[0].classList.remove('o_hidden');
    } catch (err) {
        console.error("Failed to expand groups:", err);
    } finally {
        this.env.services.ui.unblock();
    }
},

ListController.prototype.compresslist = async function () {
    this.model.root.groups.forEach((el) => {
        if (!el.isFolded) {
          el.toggle();
        }
    });
    document.getElementsByClassName("cmp-btn")[0].classList.add('o_hidden');
    document.getElementsByClassName("exp-btn")[0].classList.remove('o_hidden');
};

ListController.prototype.recursivelist = async function (groups) {
    groups.forEach((el) => {
        if (el.isFolded) {
          el.toggle();
        }

        if (el.list.groups) {
            if (el.list.groups.length > 0) {
                this.recursivelist(el.list.groups);
            }
        }
    });
};

ListController.prototype._onClickChild = async function (groupOfList) {
    if (groupOfList) {
        for (let j = 0; j < groupOfList.length; j++) {
            if (groupOfList[j].isFolded) {
                await groupOfList[j].toggle();
            }
            await this._onClickChild(groupOfList[j].list.groups);
        }
    }
};
