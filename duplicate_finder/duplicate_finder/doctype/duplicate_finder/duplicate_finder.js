// Copyright (c) 2018, Bai Web and Mobile Lab and contributors
// For license information, please see license.txt

frappe.ui.form.on('Duplicate Finder', {
    refresh: function (frm) {

    },
    onload: function (frm) {
        var keys = [];

        frappe.call({
            method: 'duplicate_finder.duplicate_finder.doctype.duplicate_finder.duplicate_finder.get_duplicates',

            callback: function (r) {
                console.log(r.message);
                for (var key in r.message) {
                    keys.push(key);

                }
                var content="";
                for (var sources = 0; sources < keys.length; sources++) {
                    content+='<div style="width:896px;  background-color: #fafbfc;padding: 10px 15px;margin: 15px 0px;border: 1px solid #d1d8dd;border-radius: 3px;font-size: 20px;">     <p class="h6">          '+keys[sources]+'                            <a href="#" class="btn btn-default btn-xs pull-right" style="margin-top:-3px; margin-right: -5px;">             Merge</a>     </p>  <table style="width:100%">      '


                    for (var duplicate = 0; duplicate < r.message[keys[sources]].length; duplicate++) {
                        console.log(r.message[keys[sources]][duplicate]);
                        content+=' <tr><th>'+r.message[keys[sources]][duplicate]['customer']+'</th><th>'+r.message[keys[sources]][duplicate]["email"]+'</th></tr>';
                    }
                    content+='</table></div>';
                }
                                    $(cur_frm.fields_dict['list'].wrapper).html(content);



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
