$(document).ready(function() {	

	//  --Global Variables-- //
	//Keep all elements from query in variable so DOM does not need to be crawled again.
	var main_tags = $('.tag_preview_image');

	var nav_tag_list = $('#tag_nav').find('.tag');
	//Global var for determining when the preview image is animating.
	var isTransitioning = false;	
	//Slideshow Transition speed
	var slideshowShuffleSpeed = 4000;
	var shuffleTimeOutObject = 0;
	var allowHoverBuffer = false;

	window.setTimeout(function() { allowHoverBuffer = true; }, 1000);

	function showPreviewImageByName(name) {
		
		if (isAPreviewImageAnimating() == false && isTransitioning == false && allowHoverBuffer == true) {
			main_tags.each(function () {
				if ( $(this).is(":visible") ) {
					$(this).fadeOut(200, 'swing');
				}
				if ($(this).attr('id') == name) {
					$(this).delay(200).fadeIn(150, 'swing');
				}
			});
			//Prevent multiple images from hiding/fading out at the same time.
			setTransitioning()
			window.setTimeout(function() { setTransitioning() }, 450);
		}
	}

	function shufflePreviewImage() {
			randomSelection = getRandomPreviewImage();
			fadeAllPreviewImagesOut(300);

			main_tags.each(function (index) {
				if (index == randomSelection) {					
					$(this).delay(300).fadeIn(300, 'swing');				
				}
			});			
			
			shuffleTimeOutObject = window.setTimeout(function() { shufflePreviewImage() }, slideshowShuffleSpeed);
	}
		
	function setTransitioning() {
		isTransitioning = !isTransitioning;	
	}

	function isAPreviewImageAnimating() {
		var is_an_image_animating = false;
		
		main_tags.each(function() {
			if ( $(this).is(':animated') ) {				
				is_an_image_animating = true;
			}
		});
				
		return (is_an_image_animating)
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

	function getRandomPreviewImage() {				
		//Pick a random number between 0 and length of all main_tags - display it first
		var tag_length = main_tags.length;
		var selected_random_tag = Math.floor(( Math.random()*tag_length));						
		return (selected_random_tag)
	}

	function silentlySendDataWithPost(location, data) {				
		var data = $.ajax({
						type: "POST",
						url: location,
						data: data,								
						contentType: 'application/x-www-form-urlencoded',
						responseType: 'XMLHttpRequestResponseType'
						});
			
		return (data);
	}

	hideAllPreviewImages();

	//Make sure all of the images have loaded before showing them
	$(window).load(function() {
		randomSelection = getRandomPreviewImage();

		main_tags.each( function(index) {												
			//Hide all other images except the randomly selected image
			if ( index == randomSelection ) {
				$(this).show();

				//Start slideshow if there are at least 2 categories
				if (main_tags.length > 1 ) {				
					shuffleTimeOutObject = window.setTimeout(function() { shufflePreviewImage() }, slideshowShuffleSpeed);
				}
			}					
		});

	});

	//No need to shuffle and/or move image on rollover if there's just one tag
	if (main_tags.length > 1) {
		$('.tag').hover(function () {
			showPreviewImageByName( $(this).attr('name')  )		
			//Stop slideshow on hover
			clearTimeout(shuffleTimeOutObject);	
		},
		function() {
			//Start slideshow
			shuffleTimeOutObject = window.setTimeout(function() { shufflePreviewImage() }, slideshowShuffleSpeed);
		});	
	}

});