// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bas Pali', {
	// refresh: function(frm) {

	// }
});


// frappe.ui.form.on('Child Village List', {
// 	village_name: function(frm) {
// 		frm.set_query("village_name", "village_list", function(doc, cdt, cdn) {
// 			let d = locals[cdt][cdn];
// 			var alreadyavailablevillageintable = [];
// 			frm.doc.village_list.forEach(function(row) {
//                 alreadyavailablevillageintable.push(row.village_name);
//             });

// 			return {
// 				filters: [['Village', 'not in', alreadyavailablevillageintable],['Village', 'circle_office', '=', frm.doc.circle]]
// 			};
// 		});

// 		frm.set_query("h_and_t_contract_code", "transporter_table", function(doc, cdt, cdn) {
// 			let d = locals[cdt][cdn];
// 			var alreadyavailablevillageintable = [];
// 			frm.doc.village_list.forEach(function(row) {
//                 alreadyavailablevillageintable.push(row.village_name);
//             });

// 			return {
// 				filters: [['H and T Contract', 'village_tra', 'in', alreadyavailablevillageintable]]
// 			};
// 		});
// 	},
// }); 


