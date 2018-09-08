import frappe
import json
@frappe.whitelist()
def duplicate_checker(doc,event):
    customer_fields=frappe.db.sql("""Select fieldname from `tabDocField` where parent='Customer' and fieldtype!='Section Break' and fieldtype!='HTML' and fieldtype!='Attach Image' and fieldtype!='Column Break' and fieldtype!='Table'""")
    existing_customers=frappe.db.sql("""Select name from tabCustomer where name!=%s""",(doc.name))
    print(existing_customers)
    no_of_values_source_doc=0
    for field in customer_fields:

        print(doc.get(field[0]))
        if doc.get(field[0]) or doc.get(field[0])!=None:
            no_of_values_source_doc+=1
    fifty_percent=no_of_values_source_doc/2
    print("50 percent "+str(fifty_percent))
    duplicate_customer=[]
    for customer in existing_customers:
        number_of_equal_values = 0


        for field in customer_fields:
            if field[0] not in "bypass_credit_limit_check_at_sales_order" and field[0] not in "customer_group" and field[0] not in "customer_type" and field[0] not in "disabled" and field[0] not in "docstatus" and field[0] not in "doctype" and field[0] not in "is_internal_customer" and field[0] not in "language" and field[0] not in "naming_series" and field[0] not in "owner" and field[0] not in "territory":
                value=frappe.get_all('Customer', filters={'name': customer[0]}, fields=[field[0]])


                for val in value:
                    if str(val[field[0]]).lower()==str(doc.get(field[0])).lower() and doc.get(field[0])!=None:
                        number_of_equal_values+=1
                        print(value)
                        print(field)
                        print(doc.get(field[0]))
                    if field[0] in "customer_name" and str(val[field[0]]).lower()==str(doc.get(field[0])).lower() and customer[0] not in duplicate_customer:
                        print("the same name")
                        duplicate_customer.append(customer[0])



        print("number of equal values "+str(number_of_equal_values))
        if number_of_equal_values>=fifty_percent and customer[0] not in duplicate_customer:
            duplicate_customer.append(customer[0])
            print("customer "+doc.name+" is duplicate to customer "+customer[0])

    contact_fields=frappe.db.sql("""Select fieldname from `tabDocField` where parent='Contact' and fieldtype!='Section Break' and fieldtype!='HTML' and fieldtype!='Attach Image' and fieldtype!='Column Break' and fieldtype!='Table'""")
    contacts_of_existing_customers=frappe.db.sql("""Select parent,link_name from `tabDynamic Link` where link_name!=%s and parenttype='Contact'""",(doc.name))
    no_of_values_source_contact=0
    source_contact=frappe.db.sql("""Select parent from `tabDynamic Link` where link_name=%s and parenttype='Contact'""",(doc.name))

    for field in contact_fields:

        print(doc.get(field[0]))
        for sc in source_contact:
            sc_value = frappe.get_all('Contact', filters={'name': sc[0]}, fields=[field[0]])
            for val2 in sc_value:

                if val2[field[0]] or val2[field[0]]!=None:
                    no_of_values_source_contact+=1
    fifty_percent_contact=no_of_values_source_contact/2
    print(no_of_values_source_contact)
    print(fifty_percent_contact)
    duplicate_contact=[]
    for customer_contact in contacts_of_existing_customers:
        number_of_equal_values_contacts = 0

        for field in contact_fields:
            value=frappe.get_all('Contact', filters={'name': customer_contact[0]}, fields=[field[0]])
            for sc in source_contact:
                sc_value=frappe.get_all('Contact', filters={'name': sc[0]}, fields=[field[0]])

                for val in value:
                    for val2 in sc_value:
                        if field[0] not in "docstatus" and field[0] not in "doctype" and field[0] not in "is_primary_contact" and field[0] not in "owner" and field[0] not in "status":
                            if str(val[field[0]]).lower()==str(val2[field[0]]).lower() and val2[field[0]]!=None:
                                number_of_equal_values_contacts+=1
                                print(value)
                                print(field)
                                print(val2[field[0]])
                            if field[0] in "email_id" and val[field[0]]==val2[field[0]] and val2[field[0]]!=None and customer_contact[1] not in duplicate_contact:
                                duplicate_contact.append(customer_contact[1])

        print("number of equal values of contacts " + str(number_of_equal_values_contacts))
        if number_of_equal_values_contacts >= fifty_percent_contact and customer_contact[1] not in duplicate_contact:
            duplicate_contact.append(customer_contact[1])

            for sc in source_contact:
                print("customer " + sc[0] + " is duplicate to customer " + customer_contact[1])


    print (duplicate_customer)
    for i in range(len(duplicate_customer)):
        print(i)
        if duplicate_customer[i] not in duplicate_contact:
            duplicate_customer.append(duplicate_customer[i])
    print("this customer is duplicated with "+str(duplicate_customer))
    for i in duplicate_customer:
        if len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s and source_customer=%s""",(i,doc.name)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s and source_customer=%s""",(doc.name,i)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s""",(i)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s""",(doc.name)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where source_customer=%s""",(i)))==0:
            duplicate = frappe.get_doc({'doctype':"Duplicate Finder List"})
            duplicate.source_customer=doc.name
            duplicate.detected_duplicate_customer=i
            link=frappe.db.sql("""Select parent from `tabDynamic Link` where link_name=%s""",(i))
            for l in link:
                email_id=frappe.db.sql("""Select email_id from `tabContact` where name=%s""",(l[0]))
                for e in email_id:
                    if e[0] and e[0]!=None:
                        duplicate.email_address=e[0]
                if not duplicate.email_address or duplicate.email_address==None:
                    duplicate.email_address="No Email Address"

            duplicate.insert(ignore_permissions=True)
        elif len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where source_customer=%s""",(i)))!=0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s and source_customer=%s""",(i,doc.name)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s and source_customer=%s""",(doc.name,i)))==0:
            duplicate = frappe.get_doc({'doctype':"Duplicate Finder List"})
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

            duplicate.insert(ignore_permissions=True)

@frappe.whitelist()
def detect_duplicates_through_contact(doc,event):
    link_name=frappe.db.sql("""Select link_name from `tabDynamic Link` where parent=%s""",(doc.name))
    for ln in link_name:

        doc=frappe.get_doc("Customer",{'name':ln[0]})
    customer_fields = frappe.db.sql(
        """Select fieldname from `tabDocField` where parent='Customer' and fieldtype!='Section Break' and fieldtype!='HTML' and fieldtype!='Attach Image' and fieldtype!='Column Break' and fieldtype!='Table'""")
    existing_customers = frappe.db.sql("""Select name from tabCustomer where name!=%s""", (doc.name))
    print(existing_customers)
    no_of_values_source_doc = 0
    for field in customer_fields:

        print(doc.get(field[0]))
        if doc.get(field[0]) or doc.get(field[0]) != None:
            no_of_values_source_doc += 1
    fifty_percent = no_of_values_source_doc / 2
    print("50 percent " + str(fifty_percent))
    duplicate_customer = []
    for customer in existing_customers:
        number_of_equal_values = 0

        for field in customer_fields:
            if field[0] not in "bypass_credit_limit_check_at_sales_order" and field[0] not in "customer_group" and \
                            field[0] not in "customer_type" and field[0] not in "disabled" and field[
                0] not in "docstatus" and field[0] not in "doctype" and field[0] not in "is_internal_customer" and \
                            field[0] not in "language" and field[0] not in "naming_series" and field[
                0] not in "owner" and field[0] not in "territory":
                value = frappe.get_all('Customer', filters={'name': customer[0]}, fields=[field[0]])

                for val in value:
                    if str(val[field[0]]).lower() == str(doc.get(field[0])).lower() and doc.get(field[0]) != None:
                        number_of_equal_values += 1
                        print(value)
                        print(field)
                        print(doc.get(field[0]))
                    if field[0] in "customer_name" and str(val[field[0]]).lower() == str(doc.get(field[0])).lower() and customer[
                        0] not in duplicate_customer:
                        duplicate_customer.append(customer[0])

        print("number of equal values " + str(number_of_equal_values))
        if number_of_equal_values >= fifty_percent and customer[0] not in duplicate_customer:
            duplicate_customer.append(customer[0])
            print("customer " + doc.name + " is duplicate to customer " + customer[0])

    contact_fields = frappe.db.sql(
        """Select fieldname from `tabDocField` where parent='Contact' and fieldtype!='Section Break' and fieldtype!='HTML' and fieldtype!='Attach Image' and fieldtype!='Column Break' and fieldtype!='Table'""")
    contacts_of_existing_customers = frappe.db.sql(
        """Select parent,link_name from `tabDynamic Link` where link_name!=%s and parenttype='Contact'""", (doc.name))
    no_of_values_source_contact = 0
    source_contact = frappe.db.sql(
        """Select parent from `tabDynamic Link` where link_name=%s and parenttype='Contact'""", (doc.name))

    for field in contact_fields:

        print(doc.get(field[0]))
        for sc in source_contact:
            sc_value = frappe.get_all('Contact', filters={'name': sc[0]}, fields=[field[0]])
            for val2 in sc_value:

                if val2[field[0]] or val2[field[0]] != None:
                    no_of_values_source_contact += 1
    fifty_percent_contact = no_of_values_source_contact / 2
    print(no_of_values_source_contact)
    print(fifty_percent_contact)
    duplicate_contact = []
    for customer_contact in contacts_of_existing_customers:
        number_of_equal_values_contacts = 0

        for field in contact_fields:
            value = frappe.get_all('Contact', filters={'name': customer_contact[0]}, fields=[field[0]])
            for sc in source_contact:
                sc_value = frappe.get_all('Contact', filters={'name': sc[0]}, fields=[field[0]])

                for val in value:
                    for val2 in sc_value:
                        if field[0] not in "docstatus" and field[0] not in "doctype" and field[
                            0] not in "is_primary_contact" and field[0] not in "owner" and field[0] not in "status":
                            if str(val[field[0]]).lower() == str(val2[field[0]]).lower() and val2[field[0]] != None:
                                number_of_equal_values_contacts += 1
                                print(value)
                                print(field)
                                print(val2[field[0]])
                            if field[0] in "email_id" and val[field[0]] == val2[field[0]] and val2[field[0]] != None and \
                                            customer_contact[1] not in duplicate_contact:
                                duplicate_contact.append(customer_contact[1])

        print("number of equal values of contacts " + str(number_of_equal_values_contacts))
        if number_of_equal_values_contacts >= fifty_percent_contact and customer_contact[1] not in duplicate_contact:
            duplicate_contact.append(customer_contact[1])

            for sc in source_contact:
                print("customer " + sc[0] + " is duplicate to customer " + customer_contact[1])

    for i in range(len(duplicate_customer)):
        print(i)
        if duplicate_customer[i] not in duplicate_contact:
            duplicate_customer.append(duplicate_customer[i])
    print("this customer is duplicated with " + str(duplicate_customer))
    for i in duplicate_customer:
        if len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s and source_customer=%s""",(i,doc.name)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s and source_customer=%s""",(doc.name,i)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s""",(i)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s""",(doc.name)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where source_customer=%s""",(i)))==0:
            duplicate=frappe.get_doc("Duplicate Finder List")
            duplicate.source_customer=doc.name
            duplicate.detected_duplicate_customer=i
            link=frappe.db.sql("""Select parent from `tabDynamic Link` where link_name=%s""",(i))
            for l in link:
                email_id=frappe.db.sql("""Select email_id from `tabContact` where name=%s""",(l[0]))
                for e in email_id:
                    if e[0] and e[0]!=None:
                        duplicate.email_address=e[0]
                if not duplicate.email_address or duplicate.email_address==None:
                    duplicate.email_address="No Email Address"

            duplicate.save()
        elif  len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where source_customer=%s""",(i)))!=0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s and source_customer=%s""",(i,doc.name)))==0 and len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where detected_duplicate_customer=%s and source_customer=%s""",(doc.name,i)))==0:
            duplicate = frappe.new_doc("Duplicate Finder List")
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

            duplicate.save()


@frappe.whitelist()
def delete_customer(doc,event):
    if len(frappe.db.sql("""Select name from `tabDuplicate Finder List` where source_customer=%s""",(doc.name)))!=0:
        duplicates_for_this_source=frappe.db.sql("""Select detected_duplicate_customer from `tabDuplicate Finder List` where source_customer=%s""",(doc.name))
        new_source=""
        for i in duplicates_for_this_source:
            new_source=i[0]
        frappe.db.sql("""Update from `tabDuplicate Finder List` set source_customer=%s where source_customer=%s""",(new_source,doc.name))
    else:
        frappe.db.sql("""Delete from `tabDuplicate Finder List` where detected_duplicate_customer=%s""",(doc.name))


from frappe.model.rename_doc import rename_doc
@frappe.whitelist()
def test(key,duplicates):
    print("sorted")
    print(sorted(json.loads(duplicates)[key],reverse=True))
    old_key=key
    for dup in sorted(json.loads(duplicates)[key],reverse=True):
        print(dup['customer'])
        print("old")
        print(old_key)
        print("new")
        print(dup['customer'])
        rename_doc("Customer", old_key, dup['customer'], merge=True)

        # if len(frappe.db.sql("""Select name from `tabCustomer` where name=%s""",(dup['customer'])))==0:
        #     rename_doc("Customer",old_key,dup['customer'],1)
        # else:
        #     rename_doc("Customer", old_key, dup['customer']+"("+str(len(frappe.db.sql("""Select name from `tabCustomer` where name=%s""",(dup['customer']))))+")", 1)
        old_key=dup['customer']