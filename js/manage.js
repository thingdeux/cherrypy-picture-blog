$(document).ready(function() {	
	$("#manage_tabs").tabs();
	$(".ui_menu").menu();

	function silentlySendDataWithPost(location, data) {				
		var returnedData = $.ajax({
								type: "POST",
								url: location,
								data: data,								
								contentType: 'application/x-www-form-urlencoded',
								responseType: 'XMLHttpRequestResponseType'
								});
			
		returnedData.done (function (response, textStatus, jqXHR) {			
			$("#image_picture_menu").html(response);		
		});
	}

	function parseTagsReceived(uiObj) {

			var tags_to_submit = {
				main_tag: $(uiObj).attr('main'),
				sub_tag: $(uiObj).attr('sub'),
				event_tag: $(uiObj).attr('event')
			}
		return (  tags_to_submit  );
	}
	
	//Reset the width on event tags (they're typically longer) - wordwrap looks wrong
	$(".long_event_tag").width(200);

	//JQUERY UI Handler for 'images tab'
	$(".ui-menu").on( "menuselect", function(event, ui) {					
		var parsedTags = parseTagsReceived( $(ui).attr('item') );
		silentlySendDataWithPost("/getPictures/", parsedTags);
		$("#selected_picture").html('');
	});
	

});