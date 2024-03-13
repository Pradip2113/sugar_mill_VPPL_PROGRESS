// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Cane Inward Slip', {
//     transporter_code: function(frm, cdt, cdn) {
//         var d = frm.doc.transporter_code
//         frm.set_value('harvester_code', d);
//     }
// });

// frappe.ui.form.on('Cane Inward Slip', {
// 	transporter_code: function(frm) {frm.call({
// 			method:'cn',//function name defined in python
// 			doc: frm.doc, //current document
// 		});
		
// 	}
// });
frappe.ui.form.on('Cane Inward Slip', {
	plot_no: function(frm) 
	{frm.call({
			method:'hdata',//function name defined in python
			doc: frm.doc, //current document
		});
		
	}
});
frappe.ui.form.on('Cane Inward Slip', {
	transporter_code: function(frm) 
	{frm.call({
			method:'vivo',//function name defined in python
			doc: frm.doc, //current document
		});
		
	}
});
// Filter for Harvester on H and T Contract
frappe.ui.form.on("Cane Inward Slip", {
    refresh: function(frm) {
        // if (frm.doc.isfarmer == 1) { // Replace with the name of the checkbox field
            frm.set_query("harvester_code", function() { // Replace with the name of the link field
                return {
                    filters: [
                        //["Farmer List", "is_harvester", '=', 1], // Replace with your actual filter criteria
                        ["Farmer List", "workflow_state", '=', 'Approved']
                    ]
                };
            });
        // }
    }
});
frappe.ui.form.on("Cane Inward Slip", {
    refresh: function(frm) {
        // if (frm.doc.isfarmer == 1) { // Replace with the name of the checkbox field
            frm.set_query("transporter_code", function() { // Replace with the name of the link field
                return {
                    filters: [
                       // ["H and T Contract", "docstatus", '=', 1], // Replace with your actual filter criteria
                    ]
                };
            });
        // }
    },
});

frappe.ui.form.on("Cane Inward Slip", {
	onload: function(frm) {
		
        frm.call({
        			method:'get_infodata',//function name defined in python
        			doc: frm.doc, //current document
        		});
        	}
});



// frappe.ui.form.on('Cane Inward Slip', {
// 	show: function(frm) {
// 		frm.call({
// 			method:'show_data',//function name defined in python
// 			doc: frm.doc, //current document
// 		});

// 	}
// });



frappe.ui.form.on('Cane Inward Slip', {
	manually_entry_for_rfid: function (frm) {
	  var manuallyWeight = frm.doc.manually_entry_for_rfid;
	  var loadedWeightField = frm.get_field('rfid_tag');
	  if (manuallyWeight) {
		loadedWeightField.df.read_only = 0;
	  } else {
		loadedWeightField.df.read_only = 1;
		frm.set_value("rfid_tag", 0.0);
	  }
	  loadedWeightField.refresh();
	}
  });

frappe.ui.form.on('Cane Inward Slip', {
	after_save: function(frm) {
		frm.call({
		method:'call_indicator',//function name defined in python
		doc: frm.doc, //current document
		});
		
	}
});
// frappe.ui.form.on("Cane Inward Slip", {
//     onload: function(frm) {
//         if (!frm.doc.slip_no) {
//             frappe.call({
//                 method: 'slip_number',
//                 callback: function(response) {
//                     if (response.message) {
//                         let lastTokenNumber = response.message;
//                         let newTokenNumber = parseInt(lastTokenNumber) + 1;
//                         frm.doc.slip_no = newTokenNumber;
//                         frm.refresh_field('slip_no');
//                     }
//                 }
//             });
//         }
//     }
// });

frappe.ui.form.on('Cane Inward Slip', {
	

	show_pending_slip: function(frm) {
		
		frm.clear_table("pending_slip")
		frm.refresh_field('pending_slip')
		
		frm.call({

		
			method:'get_tripsheet_info',//function name defined in python

			doc: frm.doc, //current document
		});
	}
});


