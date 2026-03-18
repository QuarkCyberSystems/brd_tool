frappe.ui.form.on("BRD Module Template", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Create Session"), function () {
				frappe.new_doc("BRD Session", {
					template: frm.doc.name,
				});
			});
		}
	},
});
