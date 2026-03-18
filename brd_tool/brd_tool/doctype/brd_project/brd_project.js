frappe.ui.form.on("BRD Project", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(
				__("New BRD Session"),
				function () {
					let d = new frappe.ui.Dialog({
						title: __("Create BRD Session"),
						fields: [
							{
								fieldname: "template",
								fieldtype: "Link",
								label: __("BRD Template"),
								options: "BRD Module Template",
								reqd: 1,
								filters: { is_active: 1 },
							},
						],
						primary_action_label: __("Create"),
						primary_action(values) {
							d.hide();
							frappe.call({
								method: "brd_tool.api.create_session",
								args: {
									project: frm.doc.name,
									template: values.template,
								},
								callback(r) {
									if (r.message) {
										frappe.set_route(
											"Form",
											"BRD Session",
											r.message.name
										);
									}
								},
							});
						},
					});
					d.show();
				},
				__("Actions")
			);
		}
	},
});
