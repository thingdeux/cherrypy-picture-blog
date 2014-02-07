$(document).ready(function() {	

	//  --Global Variables-- //
	//Keep all elements from query in variable so DOM does not need to be crawled again.
	var main_tags = $('.tag_preview_image');	
	//Global var for determining when the preview image is animating.
	var isTransitioning = false;

	function hideOrShowPreviewImageByName(name) {		
		
		if (isTransitioning == false) {
			main_tags.each(function () {			
				if ( $(this).is(":visible") ) {					
					$(this).fadeOut(200);			
				}										
				if ($(this).attr('id') == name) {
					$(this).delay(200).show(150);
				}		
			});
			//Prevent multiple images from hiding/fading out at the same time.
			setTransitioning()
			window.setTimeout(function() { setTransitioning() }, 500);
		}

		
	}
	
	function setTransitioning() {
		isTransitioning = !isTransitioning;		
	}

	function hideAllPreviewImages() {
		main_tags.each( function(index) {					
			$(this).hide();
		});
	}

	function getRandomPreviewImage(){
		//Pick a random number between 0 and length of all main_tags - display it first
		var tag_length = main_tags.length;
		var selected_random_tag = Math.floor(( Math.random()*tag_length));
		return (selected_random_tag)
	}
	
	
	hideAllPreviewImages();

	//Make sure all of the images have loaded before showing them
	$(window).load(function() {
		randomSelection = getRandomPreviewImage()
		main_tags.each( function(index) {												
			//Hide all other images except the randomly selected image
			if ( index == randomSelection ) {
				$(this).show();			
			}					
		});

	});
	
	
	$('.tag').hover(function () {			
		hideOrShowPreviewImageByName( $(this).attr('name')  )
	},
	function() {
		//Do nothing on unhover				
	});

	$('a').click(function(event) {
		event.preventDefault();
		//Post here
	});


});