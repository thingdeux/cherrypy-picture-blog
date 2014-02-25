$(document).ready(function() {	
	$("#manage_tabs").tabs();
	$(".ui_menu").menu();
	$("#tags_selection").hide();

	function silentlySendDataWithPost(location, data) {				
		var data = $.ajax({
						type: "POST",
						url: location,
						data: data,								
						contentType: 'application/x-www-form-urlencoded',
						responseType: 'XMLHttpRequestResponseType'
						});
			
		return (data);
	}

	function parseTagsReceived(uiObj) {

			var tags_to_submit = {
				main_tag: $(uiObj).attr('main'),
				sub_tag: $(uiObj).attr('sub'),
				event_tag: $(uiObj).attr('event')
			}
		return (  tags_to_submit  );
	}
	
	//Reset the width on event and sub tags (they're typically longer) - wordwrap looks wrong
	$(".long_sub_tag").width(150);
	$(".long_event_tag").width(200);	

	//JQUERY UI Handler for 'images tab'
	$(".ui-menu").on( "menuselect", function(event, ui) {

		if ( $(this).is('#image_tag_menu') ) {
			var parsedTags = parseTagsReceived( $(ui).attr('item') );
			var returnedTemplate = silentlySendDataWithPost("/getPictures/", parsedTags);

			returnedTemplate.done (function (response, textStatus, jqXHR) {			
				$("#image_picture_menu").html(response);		
			});

			$("#selected_picture").html('');			
		}
		else if (  $(this).is('#tags_menu')  ) {			
			var data = {
						tag_type: $(ui).attr('item').attr('dataTagType'),
						main_tag: $(ui).attr('item').attr('dataSubQuery'),
						sub_tag: $(ui).attr('item').attr('dataEventQuery')
						}		

			if (data['tag_type']) {		
				var returnedTemplate = silentlySendDataWithPost("/manageTags/", data);
				returnedTemplate.done (function (response, textStatus, jqXHR) {
					$('#tags_selection').html(response);
				});
			}
		}
		else if (  $(this).is('#blogs_menu')  ) {			
			var data = {
						blog_id: $(ui).attr('item').attr('dataBlogId'),						
						perform_action: "display"
						}			
			
			if (data['blog_id']) {				
				var returnedTemplate = silentlySendDataWithPost("/manageBlogs/", data);				
				returnedTemplate.done (function (response, textStatus, jqXHR) {
					$('#blogs_selection').html(response);								
				});
			}
		}

	});

	

});