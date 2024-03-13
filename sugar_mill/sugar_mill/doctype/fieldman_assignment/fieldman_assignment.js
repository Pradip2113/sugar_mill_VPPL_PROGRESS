// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fieldman Assignment', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Child Slip Boy Assignment Circle Office', {
	circle_office: function(frm) {
		frm.set_query("circle_office", "circle_office_table_fm", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			var alreadyavailablevillageintable = [];
			frm.doc.circle_office_table_fm.forEach(function(row) {
				alreadyavailablevillageintable.push(row.circle_office);
			});
			return {
				filters: [['name', 'not in', alreadyavailablevillageintable],]
			};
		});


	},
});