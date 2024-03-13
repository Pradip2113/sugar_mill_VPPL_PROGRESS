// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Advance Request item', {
	refresh: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];
			frm.set_query("code_no", function() { // Replace with the name of the link field
				return {
					filters: [
						// ["H and T Contract", "season", '=', frm.doc.season]
						["H and T Contract", "old_no", '=', d.code_no] // Replace with your actual filter criteria
					]
				};
			});
		}
	});
	
	frappe.ui.form.on('Advance Request item', {
		code_no: function(frm) {
			frm.call({
				method:'fetch_amount',//function name defined in python
				doc: frm.doc, //current document
			});
			
		}
	});
	
	// frappe.ui.form.on("Advance Request item", {
	//     sanction_amount: function(frm, cdt, cdn) {
	//         var d = locals[cdt][cdn];
	//         var total = 0;
	//          total = d.sacn_limit - d.sanction_amount;
	// 		frappe.msgprint(str(total))
	//         frm.set_value(d.bal_amt, total);
	//     }
	// })
	
	frappe.ui.form.on('Advance Request item', {
		per_cart_amount: function(frm) {
			frm.call({
				method:'paid_amount',//function name defined in python
				doc: frm.doc, //current document
			});
			
		}
	});

// frappe.ui.form.on('Advance Request', {
// 	gang_type: function(frm) {
// 		frm.call({
// 			method:'fetch_amount',//function name defined in python
// 			doc: frm.doc, //current document
// 		});
		
// 	}
// });

// frappe.ui.form.on('Advance Request item', {
// 	code_no: function(frm) {
// 		frm.call({
// 			method:'old_record_set',//function name defined in python
// 			doc: frm.doc, //current document
// 		});
		
// 	}
// });

// frappe.ui.form.on("Advance Request item", {
// 	advance:function(frm, cdt, cdn){
// 	var d = locals[cdt][cdn];
// 	var total1 = 0;
// 	var total2 = 0.0;
// 	frm.doc.items.forEach(function(d) { total1 += d.advance; });
// 	frm.set_value("paid_amount_till_today", total1);
// 	total2 = frm.doc.amount_limit - total1;
// 	frm.set_value("remaining_amount", total2);
// 	refresh_field("paid_amount_till_today");
// 	refresh_field("remaining_amount");

//   },
//    items_remove:function(frm, cdt, cdn){
// 	var d = locals[cdt][cdn];
// 	var total1 = 0;
// 	var total2 = 0.0;
// 	frm.doc.items.forEach(function(d) { total1 += d.advance; });
// 	frm.set_value("paid_amount_till_today", total1);
// 	total2 = frm.doc.amount_limit - total1;
// 	frm.set_value("remaining_amount", total2);
// 	refresh_field("paid_amount_till_today");
// 	refresh_field("remaining_amount");
//    }
//  });