$(document).ready(function() {
	
	//Keep all elements from query in variable so DOM does not need to be crawled again.
	var main_tags = $('.tag_preview_image');
	//Pick a random number between 0 and length of all main_tags - display it first
	var tag_length = main_tags.length;	
	var selected_random_tag = Math.floor(( Math.random()*tag_length));

	main_tags.each( function(index) {
		function shiftPortraitImage(image) {
			var image_width = parseInt($(image).prop('width') );			

			if (image_width < 720) {			
				var moveDistance = 720 - image_width;	
				var transformStatement = "translate(" + moveDistance + "px,0px)";				
				$(image).css('transform', transformStatement);
			}
		}

		//Make sure images that are in portrait orientation align properly with the tag nav
		shiftPortraitImage( $(this) );
		
		//Hide all other images except the randomly selected image
		if ( index != selected_random_tag ) {
			$(this).hide();
		}
		
	});

	function hideOrShowPreviewImageByName(name) {		
		main_tags.each(function () {
			if ($(this).attr('id') == name) {				
				$(this).show();
			}
			else {				
				$(this).hide();
			}
		});
	}

	$('.tag').hover(function () {			
		hideOrShowPreviewImageByName( $(this).attr('name')  )
	});

	$('a').click(function(event) {
		event.preventDefault();
		//Post here
	});


});