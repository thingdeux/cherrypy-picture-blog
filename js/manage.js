$(document).ready(function() {	
	function silentlySendDataWithPost(location, data) {				
		$.post(location, data);
	}

	function parseTagsReceived(uiObj) {
		
		//console.log( $(uiObj).attr('main') );
		//console.log( $(uiObj).attr('sub') );
		//console.log( $(uiObj).attr('event') );

			var tags_to_submit = {
				main_tag: $(uiObj).attr('main'),
				sub_tag: $(uiObj).attr('sub'),
				event_tag: $(uiObj).attr('event')
			}

		return (  tags_to_submit  );
	}

	$("#manage_tabs").tabs();
	$(".ui_menu").menu();
	$(".long_event_tag").width(200);




	$(".ui-menu").on( "menuselect", function(event, ui) {					
		var parsedTags = parseTagsReceived( $(ui).attr('item') );		

		silentlySendDataWithPost("/getPictures", parsedTags);
	});


});