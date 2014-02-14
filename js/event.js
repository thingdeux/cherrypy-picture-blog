$(document).ready(function() {

	function getModal(data) {
		var returnedData = $.ajax({
			type: "GET",
			url: '/getModalPicture',
			data: { image_id: data }			
		});

		returnedData.done(function ( response, textStatus, jqXHR) {						
			$("#modal").html( response );
		});		
	}

	$( ".nav_image" ).tooltip({ track: true });		

	$(".nav_image").click(function () {
		image_id = $(this).children().find('img').prop('id');
		getModal(image_id);
		
	});

});