function silentlySendDataWithPost(location, data)
{				
	$.post(location, data);
}




$(document).ready(function() {
		
	//Handler for 'process' button being clicked - will pass the form data over to cherrypy.
	$(":button").click(function() {

		
		if ( $(this).is("#process_picture_button") )
		{
			silentlySendDataWithPost("/processPicture", $(this.form).serializeArray() );			
		}
		else if ( $(this).is("#delete_picture_button") )
		{			
			var verifyDelete = confirm("Delete this file without processing?");
			if (verifyDelete)
			{
				silentlySendDataWithPost("/deletePicture", $(this.form).serializeArray() );
			} //On cancel do nothing

		}	

		
	});

})