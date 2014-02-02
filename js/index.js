$(document).ready(function() {
	//Hide the latest 8 pictures
	$('.thumbnail_scroller').hide();
			

	$('.thumbnail_scroller').each(function(i) {
	    $(this).next().delay(200*i).fadeOut('fast', function() {
	        //$(this).fadeIn('slow');
	        $(this).slideDown(200);
    	});
	});

});