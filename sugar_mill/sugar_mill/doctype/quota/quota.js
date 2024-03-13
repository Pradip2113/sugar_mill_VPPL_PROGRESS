// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Quota', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Quota Item', {
	item_code: function(frm) {
		// frm.refresh_field('conversion_factor');
		frm.call({
			method:'conversion_factors',
			doc:frm.doc
		})
	}
});


frappe.ui.form.on('Quota Item', {
	uom: function(frm) {
		// frm.refresh_field('conversion_factor');
		frm.call({
			method:'conversion_factors',
			doc:frm.doc
		})
	}
});


frappe.ui.form.on('Quota Item', {
    quantity: function(frm) {
        // Log the current value of item_code for the selected line
        frm.call({
            method: 'conversion_factors',
            doc: frm.doc
        });
    }
});

frappe.ui.form.on('Quota Item', {
	item_code: function(frm) {
		// frm.refresh_field('conversion_factor');
		frm.call({
			method:'get_uom_item',
			doc:frm.doc
		})
	}
});


frappe.ui.form.on("Quota Item", {
	quantity:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var total1 = 0;
	frm.doc.items.forEach(function(d) { total1 += d.quantity; });
	frm.set_value("total_quantity", total1);
	refresh_field("total_quantity");
  },
   items_remove:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var total1 = 0;
	frm.doc.items.forEach(function(d) { total1 += d.quantity; });
	frm.set_value("total_quantity", total1);
	refresh_field("total_quantity");
   }
 });