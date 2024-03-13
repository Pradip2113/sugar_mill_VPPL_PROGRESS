// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Slip Boy Assignment', {
//     refresh: function(frm) {
//             frm.set_query("village", function() { // Replace with the name of the link field
//                 return {
//                     filters: [
//                         ["Village", "circle_office", '=', frm.doc.circle_office] // Replace with your actual filter criteria
//                     ]
//                 };
//             });
//         }
//     });




//     frappe.ui.form.on('Child Slip Boy Assignment Circle Office', {
//         circle_office: function(frm) {
//             frm.set_query("circle_office", "circle_office_table_os", function(doc, cdt, cdn) {
//                 let d = locals[cdt][cdn];
//                 var alreadyavailablevillageintable = [];
//                 frm.doc.circle_office_table_os.forEach(function(row) {
//                     alreadyavailablevillageintable.push(row.circle_office);
//                 });
//                 return {
//                     filters: [['name', 'not in', alreadyavailablevillageintable],]
//                 };
//             });
    
    
//         },
//     });


//     frappe.ui.form.on('Child Slip Boy Assignment Circle Office', {
//         circle_office: function(frm) {
//             frm.set_query("circle_office", "circle_office_table_fm", function(doc, cdt, cdn) {
//                 let d = locals[cdt][cdn];
//                 var alreadyavailablevillageintable = [];
//                 frm.doc.circle_office_table_fm.forEach(function(row) {
//                     alreadyavailablevillageintable.push(row.circle_office);
//                 });
//                 return {
//                     filters: [['name', 'not in', alreadyavailablevillageintable],]
//                 };
//             });
    
    
//         },
//     });

frappe.ui.form.on('Child Slip Boy Access', {
    village: function(frm) {
        frm.set_query("village", "village_table_sb", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            var alreadyavailablevillageintable = [];
            frm.doc.village_table_sb.forEach(function(row) {
                alreadyavailablevillageintable.push(row.village);
            });
            return {
                filters: [['name', 'not in', alreadyavailablevillageintable], ['Route', 'circle_office', '=', doc.circle_office]]
            };
        });


    },
});


frappe.ui.form.on('Slip Boy Assignment', {
    circle_office: function(frm) {
        frm.set_query("village", "village_table_sb", function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {

                filters: [
                    ['Route', 'circle_office', '=', doc.circle_office]
                ]
            };
        });
    },
});

frappe.ui.form.on('Slip Boy Assignment', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});





// frappe.ui.form.on('Slip Boy Assignment', {
//     villages_remove: function(frm, cdt, cdn) {
//             frappe.msgprint("fkdfjksnjksdfjk")
//     }
//     });


// frappe.ui.form.on('Slip Boy Assignment', {
//     refresh: function(frm) {
//         var pp = [];
//         frm.doc.villages.forEach(function(row) {
//             pp.push(row.village);
//         });

//     }
// }),

// frappe.ui.form.on('Child Slip Boy Access', {



//     villages_remove: function(frm, cdt, cdn) {

//         var d = locals[cdt][cdn];

//         var alreadyavailablevillageintable = [];
// 		frm.doc.villages.forEach(function(row) {
//             alreadyavailablevillageintable.push(row.village);
//         });
//         frappe.msgprint(String(pp));
//         frappe.msgprint(String(alreadyavailablevillageintable));
//         frappe.msgprint("Row deleted successfully!");
//       }
//     })



    // frappe.ui.form.on('Child Slip Boy Access', {
    //     villages_remove: function(frm, cdt, cdn) {

    //         var d = locals[cdt][cdn];

    //         var alreadyavailablevillageintable = [];
    //         frm.doc.villages.forEach(function(row) {
    //             alreadyavailablevillageintable.push(row.village);
    //         });

    //         frappe.msgprint(alreadyavailablevillageintable);
    //         frappe.msgprint("Row deleted successfully!");
    //       }
    //     })