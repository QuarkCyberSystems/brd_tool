frappe.ui.form.on("BRD Session", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.access_key) {
			// Copy Share Link button
			frm.add_custom_button(__("Copy Share Link"), function () {
				let url =
					window.location.origin +
					"/brd/session?key=" +
					frm.doc.access_key;
				frappe.utils.copy_to_clipboard(url);
				frappe.show_alert({
					message: __("Share link copied to clipboard"),
					indicator: "green",
				});
			});

			// Open portal link
			frm.add_custom_button(__("Open Portal Page"), function () {
				let url = "/brd/session?key=" + frm.doc.access_key;
				window.open(url, "_blank");
			});
		}

		// Mark as Reviewed button
		if (frm.doc.status === "Submitted") {
			frm.add_custom_button(
				__("Mark as Reviewed"),
				function () {
					frm.set_value("status", "Reviewed");
					frm.save();
				},
				__("Actions")
			);
		}

		// Progress indicator
		if (!frm.is_new() && frm.doc.progress !== undefined) {
			frm.dashboard.add_indicator(
				__("Progress: {0}%", [Math.round(frm.doc.progress)]),
				frm.doc.progress >= 100
					? "green"
					: frm.doc.progress > 0
						? "orange"
						: "red"
			);
		}
	},
});
