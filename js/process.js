$(document).ready(function() {
	function silentlySendDataWithPost(location, data) {				
		$.post(location, data);
	}

	function hideAllTagBoxes() {
		$(".sub_tag_info").hide();
		$(".event_tag_info").hide();
		$(".sub_tag_values").hide();
		$(".event_tag_values").hide();
	}

	function hideAllTagOptions(optionJQueryObject) {	
		var selectedTable = $(optionJQueryObject).parentsUntil("table");
		selectedTable.find(".sub_tag_values").hide();
		selectedTable.find(".event_tag_values").hide();
	}

	function hideOrShowTagBoxes(selectedTable, tagType, optionJQueryObject) {			
		function findAndShowRelatedTag(tag_selection_box, tag_value_name, mainTag, subTag) {			
			//build a jQuery find statement to only display event tags that pertain to the passed tag_value	
			if (tag_value_name == ".sub_tag_values") {
				var builtQuery = tag_value_name + ":" + 'contains("' + mainTag + '"' + ")";
				selectedTable.find(builtQuery).show();			
			}
			else if (tag_value_name == ".event_tag_values") {
				var subTagQuery = tag_value_name + ":" + 'contains("' + subTag + '"' + ")";
				var mainTagQuery = ":" + 'contains("' + mainTag + '"' + ")";										
				
				selectedTable.find(subTagQuery + mainTagQuery).show();
			}

			selectedTable.find(tag_selection_box).show(200);
		}
		
		if (tagType == "tag_selection") {					
			findAndShowRelatedTag(".sub_tag_info", ".sub_tag_values", optionJQueryObject.value, undefined);
		}
		else if (tagType == "sub_tag_selection") {
			//The passed name of the option selected tag 
			var splitTags = optionJQueryObject.value.split(";");
			//Split the built string of tag hierarchy that was passed so that the 2nd element (sub_tag) is used
			var parentTagName = splitTags[0];			
			var subTagName = splitTags[1];								

			//Return every event tag that matches the sub
			findAndShowRelatedTag(".event_tag_info", ".event_tag_values", parentTagName, subTagName);
		}		
	}

	function fadeFormAndReplaceWithProcessing(jQueryTableObject) {
		//Fade the block to .50 opacity
		jQueryTableObject.parentsUntil('#process_files').fadeTo(300, .50);				
		
		//Pop the word processing in front of the current block of content
		var processingText = jQueryTableObject.closest('div').after('<span class = "proccesingText">Processing ...</span>');				
	}

	function checkProcessingQueue(image_id, isCleared, jQueryObject) {		

		if (isCleared == 1) 	{										
			$.get( ("/checkProcessingQueue" + "/" + image_id), function ( data ) {								
				var isQueueClear = Number(data);

				if (isQueueClear == 1)  {
					setTimeout(function() { checkProcessingQueue(image_id, 1, jQueryObject) }, 2000);
				}
				else  {					
					hideQueueBox(jQueryObject);					
				}
			
			});									
		}

	}

	function hideQueueBox(jQueryTableObject) {		
		//Hides the whole block
		jQueryTableObject.parentsUntil('#process_files').hide(300);
		$('.proccesingText').hide(300);									
	}

	function verifyRequiredFields(data) {		
		var image_name = "";
		var  main_tag = "";
		var sub_tag = "";

		for (i=0; i < data.length;i++) {
			if (data[i].name == "picture_name") {
				image_name = data[i].value;			
			}
			else if (data[i].name == "tag_selection") {
				main_tag = data[i].value;
			}
			else if (data[i].name == "sub_tag_selection") {
				sub_tag = data[i].value;
			}
		}
		


		if (image_name.length > 0 && main_tag.length > 0 && sub_tag.length > 0) {
			return(true);
		}

		return(false);
	}

	//To implement later possibly
	function prettifyTagsByStrippingParents(jQueryObject)
	{			
		var split_tag = $(jQueryObject).text().split('->');
		if (split_tag.length > 1) {								
			$(jQueryObject).text(split_tag[split_tag.length - 1]);
		}		
		
	}


	hideAllTagBoxes();
	
	//Handler for any button being clicked - will pass the form data over to cherrypy.		
	$(":button").click(function() {
		
		//'process' button
		if ( $(this).is("#process_picture_button") )	{
			var data_array = $(this.form).serializeArray()

			//Verify that 3 required fields are populated before submission (name | main tags | sub_tags)
			if ( verifyRequiredFields(data_array) ) {		
				var buttonObject = $(this); //Have to declare this in order to pass it in settimeout
				silentlySendDataWithPost("/processPicture", data_array );
				fadeFormAndReplaceWithProcessing( $(this) );

				//In one second check to see if the queue is cleared --recursively perform this check
				setTimeout(function() { checkProcessingQueue( data_array[0].value, 1, buttonObject) }, 1000);
			}
			else {
				alert("You must fill out/select all required fields");
			}

		}
		else if ( $(this).is("#delete_picture_button") )	{			
			var verifyDelete = confirm("Delete this file without processing?");
			if (verifyDelete)
			{
				silentlySendDataWithPost("/deletePicture", $(this.form).serializeArray() );
			}

		}	
	});

	//Handler for when any tag option is selected
	$("select").change(function() {
		//Hide all tag options - (see below)
		hideAllTagOptions(this);		
		
		//Re-evaluate the current selection boxes highlighted options and only show the sub or event tags that match selections
		$( "select option:selected" ).each(function() {			
			var tagType = $(this).parents("select").attr("name");
			//Walk up the DOM and find the main table for the selected option
			var selectedOptionsTable = $(this).parentsUntil("table");					
			hideOrShowTagBoxes( selectedOptionsTable, tagType, this );			
		});		
	});

})