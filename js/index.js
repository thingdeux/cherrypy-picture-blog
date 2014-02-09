$(document).ready(function() {	

	//  --Global Variables-- //
	//Keep all elements from query in variable so DOM does not need to be crawled again.
	var main_tags = $('.tag_preview_image');
	var nav_tag_list = $('#tag_nav').find('.tag');
	//Global var for determining when the preview image is animating.
	var isTransitioning = false;
	//Slideshow Transition speed
	var slideshowShuffleSpeed = 3500;	
	var shuffleTimeOutObject = 0;

	function showPreviewImageByName(name) {		
		
		if (isTransitioning == false) {
			main_tags.each(function () {			
				if ( $(this).is(":visible") ) {					
					$(this).fadeOut(200, 'swing');
				}									
				if ($(this).attr('id') == name) {
					$(this).delay(200).show(150, 'swing');
				}				
			});
			//Prevent multiple images from hiding/fading out at the same time.
			setTransitioning()
			window.setTimeout(function() { setTransitioning() }, 500);
		}		
	}

	function shufflePreviewImage() {
			randomSelection = getRandomPreviewImage();
			fadeAllPreviewImagesOut(300);			

			main_tags.each(function (index) {
				if (index == randomSelection) {
					var nameToHighlight = $(this).attr('id');					
					$(this).delay(300).show(300, 'swing');									
				}
			});

			shuffleTimeOutObject = window.setTimeout(function() { shufflePreviewImage() }, slideshowShuffleSpeed);	
	}

	function highlightNavTag(name) {
		nav_tag_list.each(function() {
			if ( $(this).attr('name') == name) {
				$(this).css('color', 'white')
			}
			else {
				$(this).css('color', 'black');
			}
		});
	}
	
	function setTransitioning() {
		isTransitioning = !isTransitioning;		
	}
	
	function hideAllPreviewImages(speed) {
		if (speed == null) { speed = 0; }

		main_tags.each( function(index) {					
			$(this).hide(speed);
		});
	}

	function fadeAllPreviewImagesOut(speed) {
		if (speed == null) { speed = 0; }
		
		main_tags.each( function(index) {					
			$(this).fadeOut(speed);
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
		randomSelection = getRandomPreviewImage();

		main_tags.each( function(index) {												
			//Hide all other images except the randomly selected image
			if ( index == randomSelection ) {
				$(this).show();
				//Start slideshow
				shuffleTimeOutObject = window.setTimeout(function() { shufflePreviewImage() }, slideshowShuffleSpeed);
			}					
		});

	});
	
	
	$('.tag').hover(function () {		
		showPreviewImageByName( $(this).attr('name')  )
		
		//Stop slideshow on hover
		clearTimeout(shuffleTimeOutObject);
	},
	function() {
		//Start slideshow
		shuffleTimeOutObject = window.setTimeout(function() { shufflePreviewImage() }, slideshowShuffleSpeed);
	});

	$('a').click(function(event) {
		event.preventDefault();
		//Post here
	});


});