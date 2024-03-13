// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fertilizer Material Request Item", "qty", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
     if(d.rate >= 0 && d.qty >= 0){
        var result = ((d.rate * d.qty)).toFixed(2);
        frappe.model.set_value(cdt, cdn, 'amount', result);
    }
});

frappe.ui.form.on("Fertilizer Material Request Item", "rate", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
     if(d.rate >= 0 && d.qty >= 0){
        var result = ((d.rate * d.qty)).toFixed(2);
        frappe.model.set_value(cdt, cdn, 'amount', result);
    }
});

frappe.ui.form.on('Fertilizer Material Request', {
	vehicle_type: function(frm) {
		frm.clear_table("items")
		frm.refresh_field('items')
		frm.call({
				method:'opcost',//function name defined in python
				doc: frm.doc, //current document
			});
	}
});

frappe.ui.form.on('Fertilizer Material Request', {
	labor_count: function(frm) {
		frm.refresh_field('items')
		frm.call({
				method:'labor',//function name defined in python
				doc: frm.doc, //current document
			});
	}
});

frappe.ui.form.on("Fertilizer Material Request", {
    season: function(frm) {
        // if (frm.doc.isfarmer == 1) { // Replace with the name of the checkbox field
            frm.set_query("h_and_t_contract", function() { // Replace with the name of the link field
                return {
                    filters: [
                        ["H and T Contract", "season", '=', frm.doc.season],
                    ]
                };
            });
        // }
    }
});
