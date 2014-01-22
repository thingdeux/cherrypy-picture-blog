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
		var tagName = optionJQueryObject.value;

		function findAndShowRelatedTag(tag_selection_box, tag_value_name) {		
			var builtQuery = tag_value_name + ":" + 'contains("' + tagName + '"' + ")"		
			selectedTable.find(builtQuery).show();
			selectedTable.find(tag_selection_box).show(200);
		}

		if (tagType == "tag_selection") {		
			findAndShowRelatedTag(".sub_tag_info", ".sub_tag_values")
		}
		else if (tagType == "sub_tag_selection") {	
			var splitTags = tagName.split(";");
			tagName = splitTags[1];

			findAndShowRelatedTag(".event_tag_info", ".event_tag_values");
		}
	}

	function fadeFormAndReplaceWithProcessing(jQueryTableObject) {
		//Fade the block to .50 opacity
		jQueryTableObject.parentsUntil('#process_files').fadeTo(300, .50);				
		
		var processingText = jQueryTableObject.closest('div').after('<span class = "proccesingText">Processing ...</span>');
		processingText = processingText.next('.proc');			
	}

	function checkProcessingQueue(image_id, isCleared, jQueryObject) {		

		if (isCleared == 1)
		{										
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
		jQueryTableObject.parentsUntil('#process_files').hide();
	}


	hideAllTagBoxes();
	
	//Handler for any button being clicked - will pass the form data over to cherrypy.		
	$(":button").click(function() {
		
		//'process' button
		if ( $(this).is("#process_picture_button") )
		{
			var data_array = $(this.form).serializeArray()
			var buttonObject = $(this); //Have to declare this in order to pass it in settimeout
			silentlySendDataWithPost("/processPicture", data_array );
			fadeFormAndReplaceWithProcessing( $(this) );

			//In one second check to see if the queue is cleared
			setTimeout(function() { checkProcessingQueue( data_array[0].value, 1, buttonObject) }, 1000);

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

	//Hanlder for when any tag option is selected
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