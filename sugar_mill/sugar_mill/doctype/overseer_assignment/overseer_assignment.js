// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overseer Assignment', {
	// refresh: function(frm) {

	// }
});


// frappe.ui.form.on('Child Slip Boy Assignment Circle Office', {
// 	circle_office: function(frm) {
// 		frm.set_query("circle_office", "circle_office_table_os", function(doc, cdt, cdn) {
// 			let d = locals[cdt][cdn];
// 			var alreadyavailablevillageintable = [];
// 			frm.doc.circle_office_table_os.forEach(function(row) {
// 				alreadyavailablevillageintable.push(row.circle_office);
// 			});
// 			return {
// 				filters: [['name', 'not in', alreadyavailablevillageintable],]
// 			};
// 		});
// 	},
// });




frappe.ui.form.on('Overseer Assignment', {
	button: function(frm) {

		frm.call({
			method: 'amount',//function name defined in python
			doc: frm.doc, //current document
		});
		
	}
});
