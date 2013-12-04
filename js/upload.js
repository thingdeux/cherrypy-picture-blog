function sayHi()
{
	alert("hi")
}

function hide_dropzone_junk()
{
  $(".dz-success-mark").hide();
  $(".dz-error-mark").hide();
  $(".dz-size").hide();
}

function modify_upload_button(show_or_hide)
{
  if (show_or_hide === "hide")
  {
    $("#picture_upload_button").hide();
  }
  else 
  {
    $("#picture_upload_button").show();
  }
  
}


$(document).ready(function() {	
	// --- Index Page --- //
	//Handler for queue button being clicked on index page.
  modify_upload_button("hide")
	$("#picture_upload_button").click(function() {				
	});
  
	
});


//Dropzone Global Configuration
Dropzone.options.uploadDropzone = {

  // Prevents Dropzone from uploading dropped files immediately
  autoProcessQueue: false,  
  dictDefaultMessage: "",  
  acceptedFiles: "image/*",
  thumbnailWidth: 75,
  thumbnailHeight: 75,
  uploadMultiple: true,
  parallelUploads: 20,



  init: function() {

    var upload_button = document.querySelector("#picture_upload_button")
        uploadDropzone = this; // closure


    upload_button.addEventListener("click", function() {
      uploadDropzone.processQueue(); // Tell Dropzone to process all queued files.      
      modify_upload_button("hide")
    }); 

    //Run when the added file event happens
    this.on("addedfile", function() {      
      hide_dropzone_junk()
      modify_upload_button("show")

    });

    this.on("uploadprogress", function(self, progress) {
      $("#statistics").html(progress)
      //console.log(progress)
    });    

  }
};