$(document).ready(function() {
			

	$('.tag_preview_image').each( function() {
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
		$(this).hide();
	});

	$('.tag').hover(function () {		
		var selected_tag = $(this).attr('name');

		$(".tag_preview_image").each(function () {
			if ($(this).attr('id') == selected_tag) {
				$(this).show();
			}
		});

	},
	//Hides image after mouse leaves
	function() {		
		var selected_tag = $(this).attr('name');

		$(".tag_preview_image").each(function () {
			if ($(this).attr('id') == selected_tag) {
				$(this).hide();				
			}
		});
	});


});