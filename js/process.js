function silentlySendDataWithPost(data)
{		
	//var form_data = $("#queued_file_form").val();
	//var form_data = $(data).val();
	console.log(data);
	//$.post("/processPicture", form_data);	
}


$(document).ready(function() {
		
	//Handler for queue button being clicked on index page.
	$("#process_picture_button").click(function() {
		button = $(this);
		console.log(button.val());
		silentlySendDataWithPost(  );				
	});



	//Handler for enter being pressed after inputting url
	$("#process_picture_button").keypress(function( event ){
			if (event.which == 13)
			{
				//Stop enter from doing what it normally does
				event.preventDefault();				
			}
	});

})