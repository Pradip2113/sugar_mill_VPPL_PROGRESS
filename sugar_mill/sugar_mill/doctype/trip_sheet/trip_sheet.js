// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Trip Sheet', {
// 	transporter_code: function(frm) {frm.call({
// 			method:'hdata',//function name defined in python
// 			doc: frm.doc, //current document
// 		});
		
// 	}
// });

frappe.ui.form.on('Trip Sheet', {
	cartno: function(frm) {frm.call({
			method:'carthdata',//function name defined in python
			doc: frm.doc, //current document
		});
		
	}
});

frappe.ui.form.on('Trip Sheet', {
	setup: function(frm) {
		frm.set_query("plot_no", function(doc) {
			return {
				filters: [
				    ['Crop Harvesting', 'season', '=', frm.doc.season],
				]
			};
		});
	},
})

frappe.ui.form.on('Trip Sheet', {
	setup: function(frm) {
		frm.set_query("transporter_code", function(doc) {
			return {
				filters: [
				    ['H and T Contract', 'bas_pali', '=', 0],
				]
			};
		});
	},
})

frappe.ui.form.on('Trip Sheet', {
    onload: function(frm) {
		var tmt = frm.doc.old_transporter_code
        frm.set_value('transporter_code', tmt);
        }
});


frappe.ui.form.on('Trip Sheet', {
	transporter_code: function(frm) {frm.call({
			method:'get_transporter_info',//function name defined in python
			doc: frm.doc, //current document
		});
		
	}
});