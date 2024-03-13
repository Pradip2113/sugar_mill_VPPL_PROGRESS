// Copyright (c) 2024, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sugar Allotment Order', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Allotment Order Items', {
	uom: function(frm) {
		// frm.refresh_field('conversion_factor');
		frm.call({
			method:'update_conversion_factors',
			doc:frm.doc
		})
	}
});


frappe.ui.form.on('Allotment Order Items', {
	item_code: function(frm) {
		// frm.refresh_field('conversion_factor');
		frm.call({
			method:'update_conversion_factors',
			doc:frm.doc
		})
	}
});

frappe.ui.form.on('Allotment Order Items', {
    qty: function(frm) {
        // Log the current value of item_code for the selected line
        frm.call({
            method: 'update_conversion_factors',
            doc: frm.doc
        });
    }
});



frappe.ui.form.on('Allotment Order Items', {
	item_code: function(frm) {
		// frm.refresh_field('conversion_factor');
		frm.call({
			method:'get_item_uom',
			doc:frm.doc
		})
	}
});



frappe.ui.form.on('Sugar Allotment Order', {
	release_order: function(frm) {
		frm.clear_table("items");
		frm.refresh_field('items');
		refresh_field("reference_number");
		refresh_field("reference_date");
		frm.call({
			method:'get_raw_materials',
			doc:frm.doc
		})
	}
});



frappe.ui.form.on("Allotment Order Items", {
	qty:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var total1 = 0;
	frm.doc.items.forEach(function(d) { total1 += d.qty; });
	frm.set_value("total_quantity", total1);
	refresh_field("total_quantity");
  },
   items_remove:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	var total1 = 0;
	frm.doc.items.forEach(function(d) { total1 += d.qty; });
	frm.set_value("total_quantity", total1);
	refresh_field("total_quantity");
   }
 });


frappe.ui.form.on('Sugar Allotment Order', {
    season(frm) {
        if (frm.doc.season){
            frm.doc.items.forEach(function(i){
                i.season = frm.doc.season;
            });
           
        } frm.refresh_field('items');
    }
});

frappe.ui.form.on('Allotment Order Items', {
    item_code: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        if (frm.doc.season) {
            frappe.model.set_value(child.doctype, child.name, 'season', frm.doc.season);
        }
        frm.refresh_field('items');
    }
});



	