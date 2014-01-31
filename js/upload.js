function hide_dropzone_junk()
{
  //Hide the  default dropzone checkmarks that I won't be using
  $(".dz-success-mark").hide();
  $(".dz-error-mark").hide();
  $(".dz-size").hide();
  $(".dz-filename").hide();
  $(".dropzone-previews > .dz-error").hide();  //Hide all previews that caused  
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
  //Hide upload button on page load, unhide after a file is queued	
  modify_upload_button("hide")
	$("#picture_upload_button").click(function() {				
	});
  
	
});


//Dropzone Global Configuration
Dropzone.options.uploadDropzone = {

  // Prevents Dropzone from uploading dropped files immediately, waits for click of upload button
  autoProcessQueue: false,    
  dictDefaultMessage: "",  
  acceptedFiles: "image/*",
  thumbnailWidth: 75,
  thumbnailHeight: 75,
  uploadMultiple: true,
  createImageThumbnails: true,
  maxFiles: 30,
  parallelUploads: 30,
  maxThumbnailFilesize: 2,
  maxFilesize: 4, //In MB
  previewsContainer: "#dropzonePreview",



  init: function() {

    var upload_button = document.querySelector("#picture_upload_button")
        uploadDropzone = this;

    //Hide upload button and upload files when 'upload' button is clicked
    upload_button.addEventListener("click", function() {
      uploadDropzone.processQueue(); // Tell Dropzone to process all queued files.      
      modify_upload_button("hide");
    }); 

    //Run when the added file event happens
    this.on("addedfile", function() {   
      hide_dropzone_junk();
      modify_upload_button("show");           
    });

    //Kickoff event after all files finish uploading
    this.on("complete", function(self) {          
      //Return array of all queued files for length checking
      queued_files = this.getQueuedFiles();      

      //If the queue is empty and the complete event fires set upload progress text to 'complete'
      if (queued_files.length < 1)
      {        
        $("#dropzone_upload_progress").html("Upload Progress: Complete");
        $(".dropzone-previews > .dz-image-preview").hide();  //Hide all previews that caused                  
        //Clean up queue files (though there should be none....dropzone problem)
        this.removeAllFiles();
      }      


    }); 

    //Catch Dropzone upload error
    this.on("error", function(self, error) {      
      console.log("Dropzone Error: " + error);      
    });

    //Update html for upload progress with current upload status [1-100]
    this.on("totaluploadprogress", function(upload_progress) {      
      //Total progress in 1-100 - can be used to show upload status of all pictures
      $("#dropzone_upload_progress").html("Upload Progress: " + parseInt(upload_progress) + "%");
    });
    
  }
};


