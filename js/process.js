function silentlySendDataWithPost(location, data) {				
	$.post(location, data);
}

function hideUnusedTagBoxes() {
	$(".sub_tag_info").hide();
	$(".event_tag_info").hide();
	$(".sub_tag_values").hide();
	$(".event_tag_values").hide();
}

function hideOrShowTagBoxes(selectedTable, tagType, optionJQueryObject) {	
	var tagName = optionJQueryObject.value;

	if (tagType == "tag_selection")
	{		
		//selectedTable.find(".sub_tag_values").hide();
		selectedTable.find(".sub_tag_values:contains(" + tagName + ")").show();
		selectedTable.find(".sub_tag_info").show(200);

	}
	else if (tagType == "sub_tag_selection")
	{	
		var splitTags = tagName.split(";");		

		//selectedTable.find(".event_tag_values").hide();
		selectedTable.find(".event_tag_values:contains(" + splitTags[1] + ")").show();
		selectedTable.find(".event_tag_info").show(200);
	}
}




$(document).ready(function() {
	hideUnusedTagBoxes();
	

	//Handler for any button being clicked - will pass the form data over to cherrypy.		
	$(":button").click(function() {
		
		//'process' button
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
			}

		}	
	});


	//When a tag option box is selected
	$("select").change(function() {
		
		//Iterate over each of the selected boxes
		$( "select option:selected" ).each(function() {
			//Walk up the DOM and find the main table
			var tagType = $(this).parents("select").attr("name");
			var selectedOptionsTable = $(this).parentsUntil("table");
			
			//Walk back down and find the tag box to unhide		 			
			hideOrShowTagBoxes( selectedOptionsTable, tagType, this );
		});

	});




})