# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "duplicate_finder"
app_title = "Duplicate Finder"
app_publisher = "Bai Web and Mobile Lab"
app_description = "fetches duplicate data and let the user to merge it."
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "pcmata@bai.ph"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/duplicate_finder/css/duplicate_finder.css"
# app_include_js = "/assets/duplicate_finder/js/duplicate_finder.js"

# include js, css files in header of web template
# web_include_css = "/assets/duplicate_finder/css/duplicate_finder.css"
# web_include_js = "/assets/duplicate_finder/js/duplicate_finder.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "duplicate_finder.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "duplicate_finder.install.before_install"
# after_install = "duplicate_finder.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "duplicate_finder.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Customer": {
		"on_update": "duplicate_finder.methods.duplicate_checker",
	},

	"Contact": {
		"on_update": "duplicate_finder.methods.detect_duplicates_through_contact"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"duplicate_finder.tasks.all"
# 	],
# 	"daily": [
# 		"duplicate_finder.tasks.daily"
# 	],
# 	"hourly": [
# 		"duplicate_finder.tasks.hourly"
# 	],
# 	"weekly": [
# 		"duplicate_finder.tasks.weekly"
# 	]
# 	"monthly": [
# 		"duplicate_finder.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "duplicate_finder.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "duplicate_finder.event.get_events"
# }

