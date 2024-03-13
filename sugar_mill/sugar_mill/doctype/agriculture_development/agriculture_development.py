import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class AgricultureDevelopment(Document):
    
    
    # /************* Vikas Work *************/

	# @frappe.whitelist()
	# def hide_child_column(self):
	# 	frappe.msgprint("Hii") 
	# 	# for row in self.get("agriculture_development_item"):
    #     # 		row.set("basel", None)
	# 	frappe.get_doc("DocType", "agriculture_development_item").get("fields", {"basel": "basel"}).hidden = 1
    
    
	# @frappe.whitelist()
	# def hide_basel_column(self):
	# 	# Get the parent document
	# 	parent_doc = frappe.get_doc("Agriculture Development", self)

	# 	# Check the value of the 'sales_type' field
	# 	sales_type = self.sales_type

	# 	# Check if the 'sales_type' field matches the condition to hide the 'Basel' column
	# 	if sales_type != "Fertilizer":  # Replace 'YourCondition' with your specific condition
	# 		# Set the 'hidden' property of the 'Basel' field to 1 in the child table
	# 		for row in parent_doc.get("agriculture_development_item"):  # Replace 'child_table_name' with the actual child table name
	# 			row.basel.hidden = 1

	# 		# Save the parent document to apply the changes
	# 		parent_doc.save()
	# 		frappe.msgprint("The 'Basel' column is now hidden.")
	# 	else:
	# 		frappe.msgprint("The 'Basel' column is not hidden.")

	# Call the function to hide the 'basel' column
	# hide_basel_column()

    
    # myapp/my_module/my_module/doctype/agriculture_development/agriculture_development.py


	# @frappe.whitelist()
	# def hide_child_column(self):
	# 	# agriculture_dev = frappe.get_doc(doctype, docname)
		
	# 	# Loop through child table and set the column value to None
	# 	for row in agriculture_dev.get("agriculture_development_item"):
	# 		row.basel = None

	# 	agriculture_dev.save()

# Remember to define the method in hooks.py as well

				
# /********** Vikas Work *******************/
	def warehouse(self,item_code):
			doc =frappe.db.get_all('Item Default', filters={'parent':item_code}, fields={'name','default_warehouse','parent'})
			if doc:
				return doc[0].get("default_warehouse")
			else:
				return None

	def get_actual_qty(self,item_code):
		warehouse=self.warehouse(item_code)
		bin_data = frappe.get_all(
			"Bin",
			filters={"item_code": item_code,"warehouse":warehouse},
			fields=["actual_qty", "warehouse"]
		)
		if bin_data:
			return bin_data[0].get("actual_qty")
		else:
			return 0

	def tax_template(self,item_code):
		doc =frappe.db.get_all('Item Tax', filters={'parent':item_code}, fields={'name','item_tax_template','parent'})
		if doc:
			return str(doc[0].get("item_tax_template"))
		else:
			return None

  
	@frappe.whitelist()
	def area_val(self):
		if (self.area < self.development_area):
			frappe.throw("Enter Valid Development Area......")
    
	@frappe.whitelist()
	def before_save(self):
		for i in self.get("agriculture_development_item"):
			doc =frappe.db.get_all('Item Tax', filters={'parent':i.item_code}, fields={'name','item_tax_template','parent'})
			for m in doc:
				i.item_tax_temp = m.item_tax_template
		
		if (self.area < self.development_area):
			frappe.throw("Enter Valid Development Area......")

	@frappe.whitelist()
	def Calculate_Fertilizer(self,doctype,basel,preeathing,earth,rainy,ratoon1,ratoon2,area,croptype,cropvariety,areafixed,areagunta):
		
		data = frappe.db.sql("""
                      select tabitem.item_code 'ItemCode',tabitem.standard_rate 'Rate',tabitem.weight_per_unit 'Weight',tabitem.item_name 'ItemName',tabitem.item_group 'Itemgroup',tabitem.name  , ceiling(ifnull(tabdose.quantity,0)* %(areagunta)s) 'Baselqty',
					  ceiling(ifnull(tabPreEarth.quantity,0) * %(areagunta)s)  'preearthqty',ceiling(ifnull(tabEarthing.quantity,0)* %(areagunta)s)  'earthingqty',ceiling(ifnull(tabRainy.quantity,0) * %(areagunta)s)  'Rainyqty',
     	              ceiling(ifnull(tabRatoon1.quantity,0) * %(areagunta)s)  'Ratoon1qty',	ceiling(ifnull(tabRatoon2.quantity,0) * %(areagunta)s)  'Ratoon2qty'
					from `tabItem` tabitem 
					left join
					(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
						from `tabDose Type` tabDosetype
						inner join `tabDose Type Item` tabDosetypeItem
						on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(basel)s and  tabDosetype.crop_type = %(croptype)s  
					) tabdose on tabdose.fertilize_name = tabitem.item_code
					left join
					(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
						from `tabDose Type` tabDosetype
						inner join `tabDose Type Item` tabDosetypeItem
						on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(preearth)s and  tabDosetype.crop_type = %(croptype)s  
					) tabPreEarth on tabPreEarth.fertilize_name = tabitem.item_code
					left join
						(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
					from `tabDose Type` tabDosetype
					inner join `tabDose Type Item` tabDosetypeItem
					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(earthing)s and  tabDosetype.crop_type = %(croptype)s 
						) tabEarthing on tabEarthing.fertilize_name = tabitem.item_code
					left join
						(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
					from `tabDose Type` tabDosetype
					inner join `tabDose Type Item` tabDosetypeItem
					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(rainy)s and  tabDosetype.crop_type = %(croptype)s  
						) tabRainy on tabRainy.fertilize_name = tabitem.item_code
                    left join
						(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
					from `tabDose Type` tabDosetype
					inner join `tabDose Type Item` tabDosetypeItem
					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(ratoon1)s and  tabDosetype.crop_type = %(croptype)s   
						) tabRatoon1 on tabRatoon1.fertilize_name = tabitem.item_code
							left join
						(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
					from `tabDose Type` tabDosetype
					inner join `tabDose Type Item` tabDosetypeItem
					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(ratoon2)s and  tabDosetype.crop_type = %(croptype)s   
						) tabRatoon2 on tabRatoon2.fertilize_name = tabitem.item_code					
                       where tabitem.item_group = 'AGRICULRE FERTLZER & CHIMECAL'  AND (
        IFNULL(tabdose.quantity, 0) <> 0
        OR IFNULL(tabPreEarth.quantity, 0) <> 0
        OR IFNULL(tabEarthing.quantity, 0) <> 0 
        OR IFNULL(tabRainy.quantity, 0) <> 0 
        OR IFNULL(tabRatoon1.quantity, 0) <> 0 
        OR IFNULL(tabRatoon2.quantity, 0) <> 0 
    ) order by  tabitem.item_code
										""",{
							'basel': basel	,	'preearth': preeathing,'earthing': earth, 'rainy': rainy,'area' : area ,'ratoon1' : ratoon1,'ratoon2' : ratoon2, 'croptype' : croptype,'areagunta':areagunta
						},  as_dict=1)	
		if data:
			# frappe.msgprint(str(data))
			for row in data:
				
				self.append("agriculture_development_item",{
								"item_code":row.ItemCode,
								"item_name":row.ItemName,
								"basel":row.Baselqty,
								"pre_earthing":row.preearthqty,
								"earth":row.earthingqty,
								"rainy":row.Rainyqty,
        						"ratoon_1":row.Ratoon1qty,
                                "ratoon_2":row.Ratoon2qty,
								"qty": float(row.Baselqty) + float(row.preearthqty) + float(row.earthingqty) +  float(row.Rainyqty) + float(row.Ratoon1qty) +float(row.Ratoon2qty),
								"item_tax_temp":self.tax_template(row.ItemCode),
								"actual_qty":str(self.get_actual_qty(row.ItemCode)),
								"rate":row.Rate,
								"weight_per_unit":row.Weight
								}
								)	
		else :
			return 0
		return data

	@frappe.whitelist()
	def get_item_pricelist_rate(self,item_code):
		item_price = frappe.get_all(
			"Item Price",
			filters={"item_code": item_code},
			fields=["price_list_rate"],
			order_by="creation desc",  # Add this to get the latest price
			limit=1  # Add this to get only the latest price
		)
		if item_price:
			return item_price[0].get("price_list_rate", 0)
		else:
			return 0.0


	@frappe.whitelist()
	def set_price_in_child_table(self):
		table = self.get('agriculture_development_item2')
		for d in  table:
			if d.item_code:
				d.rate = self.get_item_pricelist_rate(d.item_code)
	# @frappe.whitelist()
	# def Calculate_Fertilizer(self,doctype,basel,preeathing,earth,rainy,ratoon1,ratoon2,area,croptype,cropvariety,areafixed,areagunta):
		
	# 	data = frappe.db.sql("""
    #                   select tabitem.item_code 'ItemCode',tabitem.item_name 'ItemName',tabitem.item_group 'Itemgroup',tabitem.name  , ceiling(ifnull(tabdose.quantity,0)* %(areagunta)s) 'Baselqty',
	# 				  ceiling(ifnull(tabPreEarth.quantity,0) * %(areagunta)s)  'preearthqty',ceiling(ifnull(tabEarthing.quantity,0)* %(areagunta)s)  'earthingqty',ceiling(ifnull(tabRainy.quantity,0) * %(areagunta)s)  'Rainyqty',
    #  	              ceiling(ifnull(tabRatoon1.quantity,0) * %(areagunta)s)  'Ratoon1qty',	ceiling(ifnull(tabRatoon2.quantity,0) * %(areagunta)s)  'Ratoon2qty'
	# 				from `tabItem` tabitem 
	# 				left join
	# 				(
	# 					select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
	# 					from `tabDose Type` tabDosetype
	# 					inner join `tabDose Type Item` tabDosetypeItem
	# 					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(basel)s and  tabDosetype.crop_type = %(croptype)s  
	# 				) tabdose on tabdose.fertilize_name = tabitem.item_code
	# 				left join
	# 				(
	# 					select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
	# 					from `tabDose Type` tabDosetype
	# 					inner join `tabDose Type Item` tabDosetypeItem
	# 					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(preearth)s and  tabDosetype.crop_type = %(croptype)s  
	# 				) tabPreEarth on tabPreEarth.fertilize_name = tabitem.item_code
	# 				left join
	# 					(
	# 					select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
	# 				from `tabDose Type` tabDosetype
	# 				inner join `tabDose Type Item` tabDosetypeItem
	# 				on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(earthing)s and  tabDosetype.crop_type = %(croptype)s 
	# 					) tabEarthing on tabEarthing.fertilize_name = tabitem.item_code
	# 				left join
	# 					(
	# 					select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
	# 				from `tabDose Type` tabDosetype
	# 				inner join `tabDose Type Item` tabDosetypeItem
	# 				on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(rainy)s and  tabDosetype.crop_type = %(croptype)s  
	# 					) tabRainy on tabRainy.fertilize_name = tabitem.item_code
    #                 left join
	# 					(
	# 					select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
	# 				from `tabDose Type` tabDosetype
	# 				inner join `tabDose Type Item` tabDosetypeItem
	# 				on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(ratoon1)s and  tabDosetype.crop_type = %(croptype)s   
	# 					) tabRatoon1 on tabRatoon1.fertilize_name = tabitem.item_code
	# 						left join
	# 					(
	# 					select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
	# 				from `tabDose Type` tabDosetype
	# 				inner join `tabDose Type Item` tabDosetypeItem
	# 				on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(ratoon2)s and  tabDosetype.crop_type = %(croptype)s   
	# 					) tabRatoon2 on tabRatoon2.fertilize_name = tabitem.item_code					
    #                    where tabitem.item_group = 'AGRICULRE FERTLZER & CHIMECAL'  AND (
    #     IFNULL(tabdose.quantity, 0) <> 0
    #     OR IFNULL(tabPreEarth.quantity, 0) <> 0
    #     OR IFNULL(tabEarthing.quantity, 0) <> 0 
    #     OR IFNULL(tabRainy.quantity, 0) <> 0 
    #     OR IFNULL(tabRatoon1.quantity, 0) <> 0 
    #     OR IFNULL(tabRatoon2.quantity, 0) <> 0 
    # ) order by  tabitem.item_code
	# 									""",{
	# 						'basel': basel	,	'preearth': preeathing,'earthing': earth, 'rainy': rainy,'area' : area ,'ratoon1' : ratoon1,'ratoon2' : ratoon2, 'croptype' : croptype,'areagunta':areagunta
	# 					},  as_dict=1)	
	# 	if data:
	# 		# frappe.msgprint(str(data))
	# 		for row in data:			
	# 			self.append("agriculture_development_item",{
	# 							"item_code":row.ItemCode,
	# 							"item_name":row.ItemName,
	# 							"basel":row.Baselqty,
	# 							"pre_earthing":row.preearthqty,
	# 							"earth":row.earthingqty,
	# 							"rainy":row.Rainyqty,
    #     						"ratoon_1":row.Ratoon1qty,
    #                             "ratoon_2":row.Ratoon2qty,
	# 							"qty": float(row.Baselqty) + float(row.preearthqty) + float(row.earthingqty) +  float(row.Rainyqty) + float(row.Ratoon1qty) +float(row.Ratoon2qty)
								
	# 							}
	# 							)	
	# 	else :
	# 		return 0
	# 	return data
  
	# 	# if(basel == "True"):
	# 	# 	databasel = frappe.ge_all("Dose Type",filters={'dose': 'Basel'},fields=["*"])
	# 	# 	frappe.msgprint(str(databasel))
	# 	# 	for d in databasel:				
	# 	# 		frappe.msgprint(d.area)

	# 	# if(preeathing == "True"):
	# 	# 	datapreeathing = frappe.get_all("Dose Type",filters={'dose': 'Pre-Earth'},fields=["*"])
	# 	# 	frappe.msgprint(str(datapreeathing))
	# 	# 	for d in datapreeathing:				
	# 	# 		frappe.msgprint(d.area)
    
	# 	# if(earth == "True"):
	# 	# 	dataearth = frappe.get_all("Dose Type",filters={'dose': 'Earthing'},fields=["*"])
	# 	# 	frappe.msgprint(str(dataearth))
	# 	# 	for d in dataearth:				
	# 	# 		frappe.msgprint(d.area)

	# 	# if(rainy == "True"):
	# 	# 	datarainy = frappe.get_all("Dose Type",filters={'dose': 'Rainy'},fields=["*"])
	# 	# 	frappe.msgprint(str(datarainy))
	# 	# 	for d in datarainy:				
	# 	# 		frappe.msgprint(d.area)

@frappe.whitelist()
def make_delivery_challan(source_name,target_doc = None):
	def set_missing_values(source,target):
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item_quantity(source,target,source_parent):
		target.qty = source.qty
		target.item_code = source.item_code

	doclist = get_mapped_doc(
		"Agriculture Development",
				source_name,
		{
				"Agriculture Development":{
					"doctype": "Delivery Note",
				"field_map":{
								"supplier":"customer",
								"plant_name":"",
							},
				},
				"Agriculture Development Item":{
				"doctype":"Delivery Note Item",
				"field_map":{
                    "item_name":"item_name",
                    "stock_uom":"uom",
                    "season":"season",
				},
				"postprocess":update_item_quantity,
				},
			target_doc:
			set_missing_values,
		}
		)
	# frappe.msgprint("doclist")
	return doclist

@frappe.whitelist()
def make_sales_order(source_name,target_doc = None):
	def set_missing_values(source,target):
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item_quantity(source,target,source_parent):
		target.qty = source.qty
		target.item_code = source.item_code

	doclist = get_mapped_doc(
		"Agriculture Development",
				source_name,
		{
				"Agriculture Development":{
					"doctype": "Sales Order",
				"field_map":{
								"supplier":"customer",
								"plant_name":"",
							},
				},
				"Agriculture Development Item":{
				"doctype":"Sales Order Item",
				"field_map":{
                    "item_name":"item_name",
                    "stock_uom":"uom",
                    "season":"season",
                    "item_tax_temp":"item_tax_template"
				},
				"postprocess":update_item_quantity,
				},
			target_doc:
			set_missing_values,
		}
		)
	# frappe.msgprint("doclist")
	return doclist

@frappe.whitelist()
def make_nofarti(source_name,target_doc = None):
	def set_missing_values(source,target):
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item_quantity(source,target,source_parent):
		target.qty = source.qty
		target.item_code = source.item_code

	doclist = get_mapped_doc(
		"Agriculture Development",
				source_name,
		{
				"Agriculture Development":{
					"doctype": "Sales Order",
				"field_map":{
								"supplier":"customer",
								"plant_name":"",
							},
				},
				"Agriculture Development Item2":{
				"doctype":"Sales Order Item",
				"field_map":{
                    "item_name":"item_name",
                    "stock_uom":"uom",
                    "season":"season",
                    "item_tax_temp":"item_tax_template"
				},
				"postprocess":update_item_quantity,
				},
			target_doc:
			set_missing_values,
		}
		)
	# frappe.msgprint("doclist")
	return doclist


def warehouse(item_code):
			doc =frappe.db.get_all('Item Default', filters={'parent':item_code}, fields={'name','default_warehouse','parent'})
			if doc:
				return doc[0].get("default_warehouse")
			else:
				return None

def get_actual_qty(item_code):
	default_warehouse=warehouse(item_code)
	bin_data = frappe.get_all(
		"Bin",
		filters={"item_code": item_code,"warehouse":default_warehouse},
		fields=["actual_qty", "warehouse"]
	)
	if bin_data:
		return bin_data[0].get("actual_qty")
	else:
		return 0

def tax_template(item_code):
	doc =frappe.db.get_all('Item Tax', filters={'parent':item_code}, fields={'name','item_tax_template','parent'})
	if doc:
		return str(doc[0].get("item_tax_template"))
	else:
		return None


@frappe.whitelist()
def calculation(self,doctype,basel,preeathing,earth,rainy,ratoon1,ratoon2,area,croptype,cropvariety,areafixed,areagunta):

		data = frappe.db.sql("""
                      select tabitem.item_code 'ItemCode',tabitem.item_name 'ItemName',tabitem.standard_rate 'Rate',tabitem.weight_per_unit 'Weight',tabitem.item_group 'Itemgroup',tabitem.name  , ceiling(ifnull(tabdose.quantity,0)* %(areagunta)s) 'Baselqty',
					  ceiling(ifnull(tabPreEarth.quantity,0) * %(areagunta)s)  'preearthqty',ceiling(ifnull(tabEarthing.quantity,0)* %(areagunta)s)  'earthingqty',ceiling(ifnull(tabRainy.quantity,0) * %(areagunta)s)  'Rainyqty',
     	              ceiling(ifnull(tabRatoon1.quantity,0) * %(areagunta)s)  'Ratoon1qty',	ceiling(ifnull(tabRatoon2.quantity,0) * %(areagunta)s)  'Ratoon2qty'
					from `tabItem` tabitem 
					left join
					(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
						from `tabDose Type` tabDosetype
						inner join `tabDose Type Item` tabDosetypeItem
						on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(basel)s and  tabDosetype.crop_type = %(croptype)s  
					) tabdose on tabdose.fertilize_name = tabitem.item_code
					left join
					(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
						from `tabDose Type` tabDosetype
						inner join `tabDose Type Item` tabDosetypeItem
						on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(preearth)s and  tabDosetype.crop_type = %(croptype)s  
					) tabPreEarth on tabPreEarth.fertilize_name = tabitem.item_code
					left join
						(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
					from `tabDose Type` tabDosetype
					inner join `tabDose Type Item` tabDosetypeItem
					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(earthing)s and  tabDosetype.crop_type = %(croptype)s 
						) tabEarthing on tabEarthing.fertilize_name = tabitem.item_code
					left join
						(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
					from `tabDose Type` tabDosetype
					inner join `tabDose Type Item` tabDosetypeItem
					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(rainy)s and  tabDosetype.crop_type = %(croptype)s  
						) tabRainy on tabRainy.fertilize_name = tabitem.item_code
                    left join
						(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
					from `tabDose Type` tabDosetype
					inner join `tabDose Type Item` tabDosetypeItem
					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(ratoon1)s and  tabDosetype.crop_type = %(croptype)s   
						) tabRatoon1 on tabRatoon1.fertilize_name = tabitem.item_code
							left join
						(
						select tabDosetypeItem.fertilize_name,tabDosetypeItem.parent,tabDosetypeItem.quantity,tabDosetypeItem.uom
					from `tabDose Type` tabDosetype
					inner join `tabDose Type Item` tabDosetypeItem
					on tabDosetypeItem.parent =  tabDosetype.name  where dose = %(ratoon2)s and  tabDosetype.crop_type = %(croptype)s   
						) tabRatoon2 on tabRatoon2.fertilize_name = tabitem.item_code					
                       where tabitem.item_group = 'AGRICULRE FERTLZER & CHIMECAL'  AND (
        IFNULL(tabdose.quantity, 0) <> 0
        OR IFNULL(tabPreEarth.quantity, 0) <> 0
        OR IFNULL(tabEarthing.quantity, 0) <> 0 
        OR IFNULL(tabRainy.quantity, 0) <> 0 
        OR IFNULL(tabRatoon1.quantity, 0) <> 0 
        OR IFNULL(tabRatoon2.quantity, 0) <> 0 
    ) order by  tabitem.item_code
										""",{
							'basel': basel	,'preearth': preeathing,'earthing': earth, 'rainy': rainy,'area' : area ,'ratoon1' : ratoon1,'ratoon2' : ratoon2, 'croptype' : croptype,'areagunta':areagunta
						},  as_dict=1)
		items_data = []
		if data:
			# frappe.msgprint(str(data))
			
			for row in data:			
				item_data={
								"item_code":row.ItemCode,
								"item_name":row.ItemName,
								"baselqty":row.Baselqty,
								"preearthqty":row.preearthqty,
								"earthingqty":row.earthingqty,
								"rainyqty":row.Rainyqty,
        						"ratoon_1qty":row.Ratoon1qty,
                                "ratoon_2qty":row.Ratoon2qty,
								"qty": float(row.Baselqty) + float(row.preearthqty) + float(row.earthingqty) +  float(row.Rainyqty) + float(row.Ratoon1qty) +float(row.Ratoon2qty),
								"item_tax_temp":(tax_template(row.ItemCode)),
								"actual_qty":str(get_actual_qty(row.ItemCode)),
								"rate":row.Rate,
								"weight_per_unit":row.Weight
								}
				items_data.append(item_data)
			return items_data
								
		else :
			return 0
		
 

def get_items_data(items):
    items_data = []
    for item in items:
        item_data = {
            "name": item.name,
            "item_name": item.item_name,
            "item_code": item.item_code,
            "weight_per_unit":item.weight_per_unit,
            "item_tax_temp":str(tax_template(item.ItemCode)),
            "actual_qty": str(get_actual_qty(item.item_code)),
            "rate": item.standard_rate  # Fetch rate
        }
        items_data.append(item_data)
    return items_data


def get_item_rate(item_code):
    item_price = frappe.get_all(
        "Item Price",
        filters={"item_code": item_code},
        fields=["price_list_rate"],
        order_by="creation desc",  # Add this to get the latest price
        limit=1  # Add this to get only the latest price
    )
    if item_price:
        return item_price[0].get("price_list_rate", 0)
    else:
        return 0.0


@frappe.whitelist()
def get_fertilizeritem_list():
	items=[]
	item_list = frappe.get_list(
		"Item",
   		filters={"item_group":"AGRICULRE FERTLZER & CHIMECAL"},
		fields=["name", "item_name", "item_code","weight_per_unit","standard_rate"],
	)
	items = get_items_data(item_list)
	if items: 
	   return items

	

def get_items_format(items):
    items_data = []
    for item in items:
        item_data = {
            "name": item.name,
            "item_name": item.item_name,
            "item_code": item.item_code,
            "rate":get_item_rate(item.item_code)  # Fetch rate
        }
        items_data.append(item_data)
    return items_data


@frappe.whitelist()
def get_item_list():
	items=[]
	item_list = frappe.get_list(
		"Item",
   		filters={"item_group":"AGRICULRE FERTLZER & CHIMECAL"},
		fields=["name", "item_name", "item_code"],
	)
	items = get_items_format(item_list)
	if items: 
	   return items