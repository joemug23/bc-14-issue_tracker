$('document').ready(function(){

	
    $.ajax({
        method: 'GET',
        url: '/get_open_issues',
        success: function(res){
        	//check if res is not empty
            for(var k in res){
                $('#open').append('<div class="mycards col-md-5" id="'+ res[k] +'" draggable="true" ondragstart="drag(event)"><div class="card_title">'
                							+ res[k].department +' <span class="label label-warning">'+res[k].priority+'</span></div>'
                							+'<div class="card_content"><p><small><em>By: '+ res[k].raise_person +'</em></small></p>'+ res[k].description+'<p><small><em>Assigned to: '+ res[k].assigned_to +'</em></small></p></div>'
                							+'<div class="card_controls"><a href="/delete_issue/'+ k +'"><span class="glyphicon glyphicon-trash">Delete</span></a>  <button class="btn btn-info" data-toggle="modal" data-target="#assign_user_modal"><span class="glyphicon glyphicon-user"></span>Assign</button></div>'
                							+'<div class="modal fade" id="assign_user_modal" tabindex="-1" role="dialog">'
											  +'<div class="modal-dialog" role="document">'
											    +'<div class="modal-content">'
								
											      +'<div class="modal-body">'
											        +'<form action="/assign_user/'+ k +'" method="POST">'
											           +'<div class="form-group">'
											           		+'<label for="staffname" class="col-sm-3" control-label>Staff Name</label>'
											           		+'<div class="col-sm-9">'
											           			+'<input type="text" class="form-control" id="staffname" name="staffname" placeholder="Enter name of staff to assign">'
											           			
											           		+'</div>'
											           +'</div>'

											 		   +'<div class="modal-footer" style="margin: 10px;">'
											              +'<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'
											              +'<button type="submit" class="btn btn-success">Save changes</button>'
											           +'<div>'
											       

											        +'</form>'
											      +'</div>'
											      
											    +'</div>'
											  +'</div>'
											+'</div>'
                							+'</div>');
            }

        }
    });

    $.ajax({
        method: 'GET',
        url: '/get_closed_issues',
        success: function(res){
        	// check if res is not empty
            for(var k in res){
                $('#closed').append('<div class="mycards col-md-5" id="'+ res[k] +'" draggable="true" ondragstart="drag(event)"><div class="card_title">'
                							+ res[k].department +' <span class="label label-warning">'+res[k].priority+'</span></div>'
                							+'<div class="card_content"><p><small><em>By: '+ res[k].raise_person +'</em></small></p>'+ res[k].description+'<p><small><em>Assigned to: '+ res[k].assigned_to +'</em></small></p></div>'
                							+'<div class="card_controls"><a href="/delete_issue/'+ k +'"><span class="glyphicon glyphicon-trash">Delete</span></a>  <button class="btn btn-info" data-toggle="modal" data-target="#assign_user_modal"><span class="glyphicon glyphicon-user"></span>Assign</button></div>'
                							+'<div class="modal fade" id="assign_user_modal" tabindex="-1" role="dialog">'
											  +'<div class="modal-dialog" role="document">'
											    +'<div class="modal-content">'
								
											      +'<div class="modal-body">'
											        +'<form action="/assign_user/'+ k +'" method="POST">'
											           +'<div class="form-group">'
											           		+'<label for="staffname" class="col-sm-3" control-label>Staff Name</label>'
											           		+'<div class="col-sm-9">'
											           			+'<input type="text" class="form-control" id="staffname" name="staffname" placeholder="Enter name of staff to assign">'
											           			
											           		+'</div>'
											           +'</div>'

											 		   +'<div class="modal-footer" style="margin: 10px;">'
											              +'<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'
											              +'<button type="submit" class="btn btn-success">Save changes</button>'
											           +'<div>'
											       

											        +'</form>'
											      +'</div>'
											      
											    +'</div>'
											  +'</div>'
											+'</div>'
                							+'</div>');
            }

        }
    });
});

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.append(document.getElementById(data));
    var target = ev.target.id
    var data_id = data.id

    $.ajax({
    	method: 'POST',
    	url: '/update_issue_status',
    	data: {target: target, data_id: data_id}
    })
}