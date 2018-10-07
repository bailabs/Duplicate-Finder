# coding: utf-8
# Copyright (c) 2018, pcmata@bai.ph and contributors
# For license information, please see license.txt


import sys

# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
import json

import frappe

from frappe.model.rename_doc import rename_doc

from difflib import SequenceMatcher

@frappe.whitelist()
def duplicate_checker(doc, event):
    duplicate_customer = detect_duplicate_customer(doc)

    duplicate_contact = detect_duplicate_contact(doc)

    duplicate_customer += duplicate_contact

    duplicate_customer = list(set(duplicate_customer))

    for i in duplicate_customer:
        duplicate=[]

        duplicate=new_detect_or_not(doc,duplicate,i)

        duplicate.insert(ignore_permissions=True)

def new_detect_or_not(doc,duplicate,i):
    if len(frappe.db.sql(
            """Select name from `tabDuplicate Finder List` where  source_customer=%s""",
            (i))) == 0 and len(frappe.db.sql(
        """Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s """,
        (i))) == 0:
        duplicate = frappe.get_doc({'doctype': "Duplicate Finder List"})

        duplicate.source_customer = doc.name

        duplicate.detected_duplicate_customer = i

        link = frappe.db.sql("""Select parent from `tabDynamic Link` where link_name=%s""", (i))

        for l in link:
            email_id = frappe.db.sql("""Select email_id from `tabContact` where name=%s""", (l[0]))

            for e in email_id:
                if e[0] and e[0] != None:
                    duplicate.email_address = e[0]

            if not duplicate.email_address or duplicate.email_address == None:
                duplicate.email_address = "No Email Address"


    elif len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where source_customer=%s""",
                           (i))) != 0 or len(
        frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s""",
                      (i))) != 0:

        duplicate = frappe.get_doc({'doctype': "Duplicate Finder List"})

        if len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s""",
                             (i))):
            duplicate.source_customer = frappe.db.sql(
                """Select source_customer from `tabDuplicate Finder List` where detected_duplicate_customer=%s""",
                (i))[0][0]

        else:
            duplicate.source_customer = i

        duplicate.detected_duplicate_customer = doc.name

        link = frappe.db.sql("""Select parent from `tabDynamic Link` where link_name=%s""", (doc.name))

        for l in link:
            email_id = frappe.db.sql("""Select email_id from `tabContact` where name=%s""", (l[0]))

            for e in email_id:
                if e[0] and e[0] != None:
                    duplicate.email_address = e[0]

            if not duplicate.email_address or duplicate.email_address == None:
                duplicate.email_address = "No Email Address"

    return duplicate
@frappe.whitelist()
def detect_duplicate_customer(doc):
    customer_fields = frappe.db.sql(
        """Select fieldname from `tabDocField` where parent='Customer' and fieldtype!='Section Break' and fieldtype!='HTML' and fieldtype!='Attach Image' and fieldtype!='Column Break' and fieldtype!='Table'""")
    existing_customers = frappe.db.sql("""Select name from tabCustomer where name!=%s""", (doc.name))

    no_of_values_source_doc = 0

    for field in customer_fields:
        if doc.get(field[0]) or doc.get(field[0]) != None:
            no_of_values_source_doc += 1

    fifty_percent = no_of_values_source_doc / 2

    duplicate_customer = []

    not_allowed_fields=[
        "is_frozen",
        "disabled",
        "is_internal_customer",
        "credit_limit",
        "bypass_credit_limit_check_at_sales_order",
        "loyalty_program",
        "default_commission_rate",
        "bypass_credit_limit_check_at_sales_order",
        "customer_group",
        "customer_type",
        "disabled",
        "docstatus",
        "doctype",
        "is_internal_customer",
        "language",
        "naming_series",
        "owner",
        "territory"
        ]

    for customer in existing_customers:
        number_of_equal_values = 0

        for field in customer_fields:
            if field[0] not in not_allowed_fields:
                value = frappe.get_all('Customer', filters={'name': customer[0]}, fields=[field[0]])

                if similar(str(value[0][field[0]]).lower(),str(doc.get(field[0])).lower()) >= 0.8 and doc.get(field[0]) != None:
                    number_of_equal_values += 1

                if field[0] in "customer_name" and similar(str(value[0][field[0]]).lower(),str(doc.get(field[0])).lower()) >= 0.8 and \
                                customer[0] not in duplicate_customer:
                    duplicate_customer.append(customer[0])

        if number_of_equal_values >= fifty_percent and customer[0] not in duplicate_customer:
            duplicate_customer.append(customer[0])

    return duplicate_customer


@frappe.whitelist()
def detect_duplicate_contact(doc):
    contact_fields = frappe.db.sql(
        """Select fieldname from `tabDocField` where parent='Contact' and fieldtype!='Section Break' and fieldtype!='HTML' and fieldtype!='Attach Image' and fieldtype!='Column Break' and fieldtype!='Table'""")

    contacts_of_existing_customers = frappe.db.sql(
        """Select parent,link_name from `tabDynamic Link` where link_name!=%s and parenttype='Contact'""", (doc.name))

    no_of_values_source_contact = 0

    source_contact = frappe.db.sql(
        """Select parent from `tabDynamic Link` where link_name=%s and parenttype='Contact'""", (doc.name))

    for field in contact_fields:
        for sc in source_contact:
            sc_value = frappe.get_all('Contact', filters={'name': sc[0]}, fields=[field[0]])

            if sc_value[0][field[0]] or sc_value[0][field[0]] != None:
                no_of_values_source_contact += 1

    fifty_percent_contact = no_of_values_source_contact / 2

    duplicate_contact = []

    for customer_contact in contacts_of_existing_customers:
        number_of_equal_values_contacts = 0

        for field in contact_fields:
            value = frappe.get_all('Contact', filters={'name': customer_contact[0]}, fields=[field[0]])

            for sc in source_contact:
                sc_value = frappe.get_all('Contact', filters={'name': sc[0]}, fields=[field[0]])

                not_allowed_fields=[
                    "unsubscribed",
                    "docstatus",
                    "doctype",
                    "is_primary_contact",
                    "owner",
                    "status"
                ]

                if field[0] not in not_allowed_fields:
                    try:
                        if similar(str(value[0][field[0]]).lower(),str(sc_value[0][field[0]]).lower()) >= 0.8 and sc_value[0][
                            field[0]] != None:
                            number_of_equal_values_contacts += 1

                        if field[0] in "email_id" and similar(value[0][field[0]],sc_value[0][field[0]]) >= 0.8  and sc_value[0][
                            field[0]] != None and customer_contact[1] not in duplicate_contact:
                            duplicate_contact.append(customer_contact[1])
                    except:
                        pass


        if number_of_equal_values_contacts >= fifty_percent_contact and fifty_percent_contact != 0 and customer_contact[
            1] not in duplicate_contact:
            duplicate_contact.append(customer_contact[1])

    return duplicate_contact


@frappe.whitelist()
def detect_duplicates_through_contact(doc, event):

    link_name = frappe.db.sql("""Select link_name from `tabDynamic Link` where parent=%s""", (doc.name))

    for i in link_name:
        doc = frappe.get_doc("Customer", {'name': i[0]})

    duplicate_checker(doc,event)

@frappe.whitelist()
def delete_customer(doc, event):

    if len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where source_customer=%s""", (doc.name))) != 0:
        duplicates_for_this_source = frappe.db.sql(
            """Select detected_duplicate_customer from `tabDuplicate Finder List` where source_customer=%s""",
            (doc.name))

        new_source = ""

        for i in duplicates_for_this_source:
            new_source = i[0]

        frappe.db.sql("""Update from `tabDuplicate Finder List` set source_customer=%s where source_customer=%s""",
                      (new_source, doc.name))
    else:
        frappe.db.sql("""Delete from `tabDuplicate Finder List` where detected_duplicate_customer=%s""", (doc.name))




@frappe.whitelist()
def merge(key, duplicates):
    old_key = key

    for dup in sorted(json.loads(duplicates)[key], reverse=True):
        rename_doc("Customer", old_key, dup['customer'], merge=True)

        old_key = dup['customer']

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
