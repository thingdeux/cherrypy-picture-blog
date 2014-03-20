$(document).ready(function() {

	function getModal(data) {
		var returnedData = $.ajax({
			type: "GET",
			url: '/getModalPicture',
			data: { 
				image_id: data[0],
				onIndex: data[1]
			}			
		});

		returnedData.done(function ( response, textStatus, jqXHR) {						
			$("#modal").html( response );
		});		
	}

	$( ".nav_image" ).tooltip({ track: true });	

	$(".nav_image").click(function () {		
		var image_id = $(this).children().find('img').prop('id');
		var onIndex = undefined

		//Ended up reusing this functionality (yay) so this is a 'hack' (boo) to make it work on the index page		
		if (typeof image_id == 'undefined') {				
			var image_id = $(this).attr('id')
			var onIndex = true
		}
		
		getModal( [image_id, onIndex] );	
	});	

});