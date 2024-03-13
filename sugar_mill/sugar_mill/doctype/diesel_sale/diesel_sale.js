frappe.ui.form.on('Diesel Sale', {
    transporter: function(frm) {
        if(frm.doc.transporter)
        {
            frm.doc.harvester=false
            frm.refresh_field("harvester")
            frm.doc.party_name=null
            frm.refresh_field("party_name")
            frm.doc.contract_id=null
            frm.refresh_field("contract_id")
            frm.doc.customer_name=null
            frm.refresh_field("customer_name")
            frm.doc.total_distance_in_km=null
            frm.refresh_field("total_distance_in_km")
            frm.doc.total__weight_in_ton=null
            frm.refresh_field("total__weight_in_ton")
            frm.doc.total_diesel_allocated=null
            frm.refresh_field("total_diesel_allocated")
            frm.doc.total_diesel_allocation_remaining=null
            frm.refresh_field("total_diesel_allocation_remaining")
            frm.clear_table("diseal_sale_item")
            frm.refresh_field("diseal_sale_item")
        }
    },
    harvester: function(frm) {
        if(frm.doc.harvester)
        {
            frm.doc.transporter=false
            frm.refresh_field("transporter")
            frm.doc.party_name=null
            frm.refresh_field("party_name")
            frm.doc.contract_id=null
            frm.refresh_field("contract_id")
            frm.doc.customer_name=null
            frm.refresh_field("customer_name")
            frm.doc.total_distance_in_km=null
            frm.refresh_field("total_distance_in_km")
            frm.doc.total__weight_in_ton=null
            frm.refresh_field("total__weight_in_ton")
            frm.doc.total_diesel_allocated=null
            frm.refresh_field("total_diesel_allocated")
            frm.doc.total_diesel_allocation_remaining=null
            frm.refresh_field("total_diesel_allocation_remaining")
            frm.clear_table("diseal_sale_item")
            frm.refresh_field("diseal_sale_item")
        }
    },
    contract_id: function(frm) {
        frm.clear_table("diseal_sale_item")
        frm.refresh_field("diseal_sale_item")
        if(!frm.doc.plant)
        {
            frm.doc.contract_id=null
            frm.refresh_field("contract_id")
            frappe.throw("Please Select Branch")
        }
        if(!frm.doc.season)
        {
            frm.doc.contract_id=null
            frm.refresh_field("contract_id")
            frappe.throw("Please Select Season")
        }
        frm.call({
            method:'get_customer_name',//function name defined in python
            doc: frm.doc, //current document
        });
    }
});

frappe.ui.form.on('Diseal Sale Item', {
	qty: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var qty = parseFloat(child.qty);
		var rate = parseFloat(child.rate);
		var amount = qty * rate;
		frappe.model.set_value(cdt, cdn, 'amount', amount);
		refresh_field('amount');
	},
    rate: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var qty = parseFloat(child.qty);
		var rate = parseFloat(child.rate);
		var amount = qty * rate;
		frappe.model.set_value(cdt, cdn, 'amount', amount);
		refresh_field('amount');
	}
});

frappe.ui.form.on('Diseal Sale Item', {
    item_code: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        frm.call({
            method: 'get_item_rate',
            args:{
                item_code:child.item_code,
                index:child.idx
            },
            doc:frm.doc
        });
    }
});



frappe.ui.form.on('Diesel Sale', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});



frappe.ui.form.on('Diesel Sale', {
    transporter: function(frm) {
		frm.set_query("contract_id", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
				    ["H and T Contract", "docstatus", '=', 1],
				    // ["H and T Contract", "company_name", '=', frm.doc.company],
                    ["H and T Contract", "season", '=', frm.doc.season],
                    ["H and T Contract", "plant", '=', frm.doc.plant],
				]
			};
		});
	},
    harvester: function(frm) {
		frm.set_query("contract_id", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
				    ["H and T Contract", "docstatus", '=', 1],
				    // ["H and T Contract", "company_name", '=', frm.doc.company],
                    ["H and T Contract", "season", '=', frm.doc.season],
                    ["H and T Contract", "plant", '=', frm.doc.plant],
				]
			};
		});
	},
});

frappe.ui.form.on('Diesel Sale', {	      
    transporter: function(frm,cdt,cdn) {  
        frappe.call({
            method: 'get_contract_list',
			doc:frm.doc,
            callback: function(r) {
                if (r.message) {
					frm.set_query("contract_id",function(doc, cdt, cdn) {	    
						let d = locals[cdt][cdn];
						return {
							filters: [
								['H and T Contract', 'name','in', r.message],     
							]
						};
					});
                }
            }
        });	
        
    }
});


frappe.ui.form.on('Diesel Sale', {	      
    harvester: function(frm,cdt,cdn) {  
        frappe.call({
            method: 'get_contract_list',
			doc:frm.doc,
            callback: function(r) {
                if (r.message) {
					frm.set_query("contract_id",function(doc, cdt, cdn) {	    
						let d = locals[cdt][cdn];
						return {
							filters: [
								['H and T Contract', 'name','in', r.message],     
							]
						};
					});
                }
            }
        });	
        
    }
});
