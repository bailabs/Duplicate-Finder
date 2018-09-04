# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bai Web and Mobile Lab and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DuplicateFinder(Document):
	pass

@frappe.whitelist()
def get_duplicates():
	sources=frappe.db.sql("""Select source_customer from `tabDuplicate Finder List`""")
	data={}
	data2={}
	for source in sources:
		duplicate=frappe.db.sql("""Select detected_duplicate_customer,email_address from `tabDuplicate Finder List` where source_customer=%s""",(source[0]))
		for dup in duplicate:
			if source[0] not in data:
				data[source[0]]=[]
				data2[source[0]]=[]
			if dup[0] not in data2[source[0]]:
				data[source[0]].append({'customer':dup[0],'email':dup[1]})
				data2[source[0]].append(dup[0])


	return data