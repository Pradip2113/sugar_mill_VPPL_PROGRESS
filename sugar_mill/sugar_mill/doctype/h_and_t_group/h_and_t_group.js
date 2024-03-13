// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('H and T Group', {
	// refresh: function(frm) {

	// }
});



frappe.ui.form.on('H and T Group', {
	branch: function(frm) {
		frm.call({
			method: 'update_value',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});


frappe.ui.form.on('H and T Group', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});




