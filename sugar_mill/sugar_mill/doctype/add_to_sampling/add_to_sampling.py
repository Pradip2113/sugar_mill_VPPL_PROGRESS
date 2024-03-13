# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

# from datetime import datetime


class AddToSampling(Document):
    @frappe.whitelist()
    def list(self):
        crop_variety_list=[str(d.crop_variety_link) for d in self.crop_variety]
        crop_type_list=[str(d.crop_type_link) for d in self.crop_type]
        circle_office_list = [str(d.circle_office_link) for d in self.circle_office]
        village_list=[str(d.village_link) for d in self.village]
        #  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # village_items = [d.village_link for d in self.village]
        # condition_1 = "{}".format("  or  ".join(["d.area == '{}'".format(name) for name in village_items]))
        # circle_office_items = [d.circle_office_link for d in self.circle_office]
        # condition_2 = "{}".format("  or  ".join(["d.circle_office == '{}'".format(name) for name in circle_office_items]))
        # crop_variety_items = [d.crop_variety_link for d in self.crop_variety]
        # condition_3 = "{}".format("  or  ".join(["d.crop_variety == '{}'".format(name) for name in crop_variety_items]))
        # crop_type_items = [d.crop_type_link for d in self.crop_type]
        # condition_4 = "{}".format("  or  ".join(["d.crop_type == '{}'".format(name) for name in crop_type_items]))
        # if condition_1 == "" and self.select_all_records_for_sampling==0:
        #     frappe.throw("Please fill up village")
        # if condition_2 == "" and self.select_all_records_for_sampling==0:
        #     frappe.throw("Please fill up circle_office")
        # if condition_3 == "" and self.select_all_records_for_sampling==0:
        #     frappe.throw("Please fill up crop_variety")
        # if condition_4 == "" and self.select_all_records_for_sampling==0:
        #     frappe.throw("Please fill up crop_type")

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        filters={"plantation_status":"New","is_kisan_card":self.is_kisan_card}
        if circle_office_list:
            filters["circle_office"] = ["in", list(circle_office_list)]
        if village_list:
            filters["area"] = ["in", village_list]
        if crop_variety_list:
            filters["crop_variety"] = ["in", crop_variety_list]
        if crop_type_list:
            filters["crop_type"] = ["in", crop_type_list]
        if self.season:
            filters["season"]=self.season
        if self.from_date and self.to_date:
            filters["plantattion_ratooning_date"]=["between", [self.from_date, self.to_date]]
        doc = frappe.get_all(
            "Cane Master",
            filters=filters,
            fields=[
                "is_kisan_card",
                "plant_name",
                "grower_name",
                "grower_code",
                "form_number",
                "name",
                "plantattion_ratooning_date",
                "area_acrs",
                "circle_office",
                "crop_variety",
                "plantation_status",
                "season",
                "crop_type",
                "docstatus",
                "area"
                
            ],
        )   
        if not self.select_all_records_for_sampling:
            for d in doc:
                # frappe.msgprint(str(d.plantattion_ratooning_date))
                # frappe.msgprint(str(d.docstatus))
                # if (
                #     d.plantation_status == "New"
                #     # and str(d.docstatus) == "1"
                #     and (
                #         str(self.from_date)
                #         <= str(d.plantattion_ratooning_date)
                #         <= str(self.to_date)
                #     )
                #     and (self.season == d.season)
                #     and eval(condition_1)
                #     and eval(condition_2)
                #     and eval(condition_3)
                #     and eval(condition_4)
                # ):
                    # if(self.village == d.area) and (self.circle_office == d.circle_office) and (self.crop_variety == d.crop_variety):
                    self.append(
                        "cane_master_data",
                        {
                            "id": d.name,
                            "grower_name": d.grower_name,
                            "grower_code":d.grower_code,
                            "form_number": d.form_number,
                            "plantattion_ratooning_date": d.plantattion_ratooning_date,
                            "plantation_status": d.plantation_status,
                             "area_acrs": d.area_acrs,
                            "circle_office": d.circle_office,
                            "crop_variety": d.crop_variety,
                            "season": d.season,
                            "crop_type":d.crop_type,
                            "plant_name":d.plant_name
                        },
                    )
        else:
            for d in doc:
                if (
                    d.plantation_status == "New"
                    and (
                        str(self.from_date)
                        <= str(d.plantattion_ratooning_date)
                        <= str(self.to_date)
                    )
                    and (self.season == d.season)
                    ):
                    self.append(
                        "cane_master_data",
                        {
                            "id": d.name,
                            "grower_name": d.grower_name,
                            "grower_code":d.grower_code,
                            "form_number": d.form_number,
                            "plantattion_ratooning_date": d.plantattion_ratooning_date,
                            "plantation_status": d.plantation_status,
                            "area_acrs": d.area_acrs,
                            "circle_office": d.circle_office,
                            "crop_variety": d.crop_variety,
                            "season": d.season,
                            "crop_type":d.crop_type,
                            "plant_name":d.plant_name
                        },
                    )
            
        if not self.get("cane_master_data"):
            frappe.throw("The record You are looking for are not available")


    @frappe.whitelist()
    def selectall(self):
        # pass
        children = self.get("cane_master_data")
        if not children:
            return
        all_selected = all([child.check for child in children])
        value = 0 if all_selected else 1
        for child in children:
            child.check = value
            
    @frappe.whitelist()
    def before_save(self):
        for row in self.get("cane_master_data"):
            if row.check and not self.direct_for_harvesting:
                doc = frappe.get_all("Crop Sampling",filters={"id": row.id,},fields=[ "name"],)
                # frappe.throw(str(doc))
                if not doc:
# frappe.msgprint(str(row.parent))
                    doc = frappe.new_doc("Crop Sampling")
                    doc.id = row.id
                    doc.insert()
                    doc.save()
                    moc = frappe.db.get_all("Crop Sampling", fields=["name"], order_by="creation DESC", limit=1)
                    frappe.db.set_value("Crop Sampling", moc[0].name, "plantation_status","To Sampling")
                    frappe.db.set_value("Cane Master",row.id ,"plantation_status", "To Sampling")
                    
            elif row.check and self.direct_for_harvesting:
                doc = frappe.get_all("Crop Harvesting",filters={"id": row.id,},fields=[ "name"],)
                if not doc:
                    doc=frappe.new_doc('Crop Harvesting')
                    doc.brix ="0"
                    doc.crop_sample_id="Without Sampling"
                    doc.no_of_pairs="0"
                    doc.id =row.id
                    doc.insert()
                    doc.save
                    moc = frappe.db.get_all("Crop Harvesting", fields=["name"], order_by="creation DESC", limit=1)
                    frappe.db.set_value("Crop Harvesting", moc[0].name, "plantation_status","To Harvesting")
                    frappe.db.set_value("Cane Master", row.id ,"plantation_status", "To Harvesting")
                    
        # for i in self.get("cane_master_data"):
        #         if i.check:
        #             frappe.db.set_value("Cane Master", i.id ,"plantation_status", "To Sampling")
                    
                

    # def on_trash(self):
    #     for i in self.get("cane_master_data"):
    #             if i.check:
    #                 frappe.db.set_value("Cane Master", i.id ,"plantation_status", "New")
                    

    #     moc = frappe.db.get_list("Crop Sampling", fields=["id", "name"])  # fields=["plantation_status", "name","form_number"
    #     for j in self.get("cane_master_data"):
    #         if i.check:
    #             for c in moc:
    #                 if j.id == c.id:
    #                     frappe.delete_doc("Crop Sampling", c.name)
    #                     break
