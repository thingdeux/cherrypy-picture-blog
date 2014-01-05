function silentlySendDataWithPost(location, data)
{				
	$.post(location, data);
}


$(document).ready(function() {
		
	//Handler for 'process' button being clicked - will pass the form data over to cherrypy.
	$("#process_picture_button").click(function() {																				
		silentlySendDataWithPost("/processPicture", $(this.form).serializeArray() );				
	});

	//Prevent enter from causing submission
	$("#process_picture_button").keypress(function( event ){
			if (event.which == 13)
			{				
				event.preventDefault();
			}
	});

})