$(document).ready(function() {	

	function shiftPortraitImage(image) {
		var image_width = image.attr("dataWidth");		

		console.log(image)

		if (image_width < 720) {	
			var moveDistance = 720 - image_width;			
			var transformStatement = "translate(" + moveDistance + "px,0px)";			
			//$(image).css('transform', transformStatement);
		}		
	}

	function hideOrShowPreviewImageByName(name) {		
		main_tags.each(function () {
			if ($(this).attr('id') == name) {									
				$(this).show();
				shiftPortraitImage( $(this) );				
			}
			else {				
				$(this).hide();
			}
		});
	}

	function hideAllPreviewImages() {
		main_tags.each( function(index) {						
			$(this).hide();
		});
	}
	
	//Keep all elements from query in variable so DOM does not need to be crawled again.
	var main_tags = $('.tag_preview_image');
	//Pick a random number between 0 and length of all main_tags - display it first
	var tag_length = main_tags.length;
	var selected_random_tag = Math.floor(( Math.random()*tag_length));	
	//var nav_x = $("#tag_nav").position().left	

	hideAllPreviewImages();

	//Make sure all of the images have loaded before adjusting them and showing them
	$(window).load(function() {

		main_tags.each( function(index) {												
			//Hide all other images except the randomly selected image
			if ( index == selected_random_tag ) {
				$(this).show();
				shiftPortraitImage( $(this) );
			}					
		});

	});
	
	
	$('.tag').hover(function () {			
		hideOrShowPreviewImageByName( $(this).attr('name')  )
	});

	$('a').click(function(event) {
		event.preventDefault();
		//Post here
	});


});