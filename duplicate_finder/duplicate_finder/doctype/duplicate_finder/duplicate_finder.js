// Copyright (c) 2018, Bai Web and Mobile Lab and contributors
// For license information, please see license.txt

var duplicates={};

frappe.ui.form.on('Duplicate Finder', {
    merge: function (key) {
        console.log(duplicates[key]);
        for(var i=0;i<duplicates[key].length;i++){
            frappe.call({
                method: "duplicate_finder.duplicate_finder.doctype.duplicate_finder.duplicate_finder.delete_source",
                args:{
                 "source": key,
                    "duplicate": duplicates[key][i]['customer']
                },
                callback: function (r) {

                }
            });
 frappe.call({
        method: "frappe.model.rename_doc.rename_doc",
        args: {
            doctype: "Customer",
            old: key,
            "new": duplicates[key][i]['customer'],
            "merge": 1
        },
         callback: function (r) {
            frappe.msgprint("Successfully merged.");
         }
    });
        }
cur_frm.reload_doc();
    },

    refresh: function (frm) {
        var keys = [];

        frappe.call({
            method: 'duplicate_finder.duplicate_finder.doctype.duplicate_finder.duplicate_finder.get_duplicates',

            callback: function (r) {
                if (r.message) {

                    if (r.message.length == 0) {
                        cur_frm.set_df_property("list", "read_only", cur_frm.__islocal ? 0 : 1);

                    }
                    console.log(r.message);
                    duplicates = r.message;
                    for (var key in r.message) {
                        keys.push(key);

                    }
                    var content = "";
                    var merge_method = "cur_frm.events.merge('Customer')";
                    for (var sources = 0; sources < keys.length; sources++) {
                        content += '<div style="width:896px;  background-color: #fafbfc;padding: 10px 15px;margin: 15px 0px;border: 1px solid #d1d8dd;border-radius: 3px;font-size: 20px;">     <p class="h6">          ' + keys[sources] + '                            <a onclick=\'cur_frm.events.merge("' + keys[sources] + '")\' class="btn btn-default btn-xs pull-right" style="margin-top:-3px; margin-right: -5px;">             Merge</a>     </p>  <table style="width:100%">      '


                        for (var duplicate = 0; duplicate < r.message[keys[sources]].length; duplicate++) {
                            console.log(r.message[keys[sources]][duplicate]);
                            content += ' <tr><th>' + r.message[keys[sources]][duplicate]['customer'] + '</th><th>' + r.message[keys[sources]][duplicate]["email"] + '</th></tr>';
                        }
                        content += '</table></div>';
                    }
                    $(cur_frm.fields_dict['list'].wrapper).html(content);


                }else{
                    cur_frm.set_df_property("list", "read_only", cur_frm.__islocal ? 0 : 1);
                }
            }
        });

        // if (screen.width < 758) {
        //     $(cur_frm.fields_dict['list'].wrapper).html('<div style="  background-color: #fafbfc;padding: 10px 15px;margin: 15px 0px;border: 1px solid #d1d8dd;border-radius: 3px;font-size: 20px;">     <p class="h6">          Wa iLhi                            <a href="#Form/Address/ok-Billing" class="btn btn-default btn-xs pull-right" style="margin-top:-3px; margin-right: -5px;">             Edit</a>     </p>         <p>ok<br>ok<br>Comoros<br></p></div>')
        //
        // } else {
        //     $(cur_frm.fields_dict['list'].wrapper).html('<div style="width:860px;background-color: #fafbfc;padding: 10px 15px;margin: 15px 0px;border: 1px solid #d1d8dd;border-radius: 3px;font-size: 30px;">     <p class="h6">          Wa iLhi                            <a href="#Form/Address/ok-Billing" class="btn btn-default btn-xs pull-right" style="border: 1px solid #d1d8dd;border-radius: 3px;width:100px;margin-top:-3px; margin-right: -5px;">             Merge</a>     </p>         <p >Wa iLhi &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Wa_iLhi@nailhan.com<br>Wa iLhi &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; No Email Address<br></p></div>' +
        // 	'<div style="width:860px;  background-color: #fafbfc;padding: 10px 15px;margin: 15px 0px;border: 1px solid #d1d8dd;border-radius: 3px;font-size: 30px;">     <p class="h6">          Nail Han                            <a href="#Form/Address/ok-Billing" class="btn btn-default btn-xs pull-right" style="border: 1px solid #d1d8dd;border-radius: 3px;width:100px;margin-top:-3px; margin-right: -5px;">             Merge</a>     </p>         <p >Nail Han &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; nailhan_ko@nailhan.com<br>Nail Han &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; kinsako@akoni.com<br></p></div>')
        //
        // }
    },
    onload: function (frm) {
        var keys = [];

        frappe.call({
            method: 'duplicate_finder.duplicate_finder.doctype.duplicate_finder.duplicate_finder.get_duplicates',

            callback: function (r) {
                if (r.message) {

                    console.log(r.message);
                    if (r.message.length == 0) {
                        cur_frm.set_df_property("list", "read_only", cur_frm.__islocal ? 0 : 1);

                    }
                    for (var key in r.message) {
                        keys.push(key);

                    }
                    var content = "";
                    for (var sources = 0; sources < keys.length; sources++) {
                        content += '<div style="width:896px;  background-color: #fafbfc;padding: 10px 15px;margin: 15px 0px;border: 1px solid #d1d8dd;border-radius: 3px;font-size: 20px;">     <p class="h6">          ' + keys[sources] + '                            <a href="#" class="btn btn-default btn-xs pull-right" style="margin-top:-3px; margin-right: -5px;">             Merge</a>     </p>  <table style="width:100%">      '


                        for (var duplicate = 0; duplicate < r.message[keys[sources]].length; duplicate++) {
                            console.log(r.message[keys[sources]][duplicate]);
                            content += ' <tr><th>' + r.message[keys[sources]][duplicate]['customer'] + '</th><th>' + r.message[keys[sources]][duplicate]["email"] + '</th></tr>';
                        }
                        content += '</table></div>';
                    }
                    $(cur_frm.fields_dict['list'].wrapper).html(content);


                }else{
                    cur_frm.set_df_property("list", "read_only", cur_frm.__islocal ? 0 : 1);
                }
            }
        });

        // if (screen.width < 758) {
        //     $(cur_frm.fields_dict['list'].wrapper).html('<div style="  background-color: #fafbfc;padding: 10px 15px;margin: 15px 0px;border: 1px solid #d1d8dd;border-radius: 3px;font-size: 20px;">     <p class="h6">          Wa iLhi                            <a href="#Form/Address/ok-Billing" class="btn btn-default btn-xs pull-right" style="margin-top:-3px; margin-right: -5px;">             Edit</a>     </p>         <p>ok<br>ok<br>Comoros<br></p></div>')
        //
        // } else {
        //     $(cur_frm.fields_dict['list'].wrapper).html('<div style="width:860px;background-color: #fafbfc;padding: 10px 15px;margin: 15px 0px;border: 1px solid #d1d8dd;border-radius: 3px;font-size: 30px;">     <p class="h6">          Wa iLhi                            <a href="#Form/Address/ok-Billing" class="btn btn-default btn-xs pull-right" style="border: 1px solid #d1d8dd;border-radius: 3px;width:100px;margin-top:-3px; margin-right: -5px;">             Merge</a>     </p>         <p >Wa iLhi &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Wa_iLhi@nailhan.com<br>Wa iLhi &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; No Email Address<br></p></div>' +
        // 	'<div style="width:860px;  background-color: #fafbfc;padding: 10px 15px;margin: 15px 0px;border: 1px solid #d1d8dd;border-radius: 3px;font-size: 30px;">     <p class="h6">          Nail Han                            <a href="#Form/Address/ok-Billing" class="btn btn-default btn-xs pull-right" style="border: 1px solid #d1d8dd;border-radius: 3px;width:100px;margin-top:-3px; margin-right: -5px;">             Merge</a>     </p>         <p >Nail Han &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; nailhan_ko@nailhan.com<br>Nail Han &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; kinsako@akoni.com<br></p></div>')
        //
        // }
    }
});
