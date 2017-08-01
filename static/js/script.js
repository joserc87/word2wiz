$(function(){

    var numSuccess = 0;
    var numError = 0;
    var failedFiles = [];
    var dataListFail = [];

    var ul = $('#upload ul');

    $('#drop a').click(function(){
        // Simulate a click on the file input button
        // to show the file browser dialog
        $(this).parent().find('input').click();
    });

    // jquery dialog
    $( "#error-dialog" ).dialog({
        autoOpen: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            Ok: function() {
            $( this ).dialog( "close" );
            }
        }
    });


    // Initialize the jQuery File Upload plugin
    $('#upload').fileupload({

        // This element will accept file drag/drop uploading
        dropZone: $('#drop'),

        // This function is called when a file is added to the queue;
        // either via the browse button, or via drag/drop:
        add: function (e, data) {

            var tpl = $('<li class="working"><input type="text" value="0" data-width="48" data-height="48"'+
                ' data-fgColor="#0788a5" data-readOnly="1" data-bgColor="#3e4043" /><p></p><span></span></li>');

            // Append the file name and file size
            tpl.find('p').text(data.files[0].name)
                         .append('<i>' + formatFileSize(data.files[0].size) + '</i>');

            // Add the HTML to the UL element
            data.context = tpl.appendTo(ul);

            // Initialize the knob plugin
            tpl.find('input').knob();

            // Listen for clicks on the cancel icon
            tpl.find('span').click(function(){

                if(tpl.hasClass('working')){
                    jqXHR.abort();
                }

                tpl.fadeOut(function(){
                    tpl.remove();
                });

            });

            // Automatically upload the file once it is added to the queue
            var jqXHR = data.submit().success(function(result, textStatus, jqXHR){

                var json = JSON.parse(result);
                var status = json['status'];
                var file = json['file'];

                if(status == 'error'){
                    errorMessage = json['message'];
                    if (errorMessage == null || errorMessage == '') {
                        errorMessage = 'Unknown error';
                    }
                    data.context.addClass('error');
                    numError++;
                    failedFiles.push(data.files[0].name);
                    dataListFail.push(data);
                    tpl.find('p').append('<a id="show-errors-' + numError + '" class="browse-button">SHOW ERRORS</a>');
                    $("#show-errors-" + numError).click(function() {
                        // Show the error message in a dialog:
                        var obj = $("#error-dialog").find('p').text(errorMessage);
                        obj.html(obj.html().replace(/\n/g,'<br/>'));
                        $("#error-dialog").dialog("open");
                    });

                }else{
                    numSuccess++;
                    tpl.find('p').append('<a class="browse-button" href="' + file + '">Download</a>');
                }

                updateNote();

                // setTimeout(function(){
                // 	//data.context.fadeOut('slow');
                // },3000);
            });
        },

        progress: function(e, data){

            // Calculate the completion percentage of the upload
            var progress = parseInt(data.loaded / data.total * 100, 10);

            // Update the hidden input field and trigger a change
            // so that the jQuery knob plugin knows to update the dial
            data.context.find('input').val(progress).change();

            if(progress == 100){
                data.context.removeClass('working');
            }
        },

        fail:function(e, data){
            // Something has gone wrong!
            data.context.addClass('error');
            numError++;
            updateNote();
            dataListFail.push (data);
        }

    });


    // Prevent the default action when a file is dropped on the window
    $(document).on('drop dragover', function (e) {
    	  if(failedFiles.length > 0)
            e.preventDefault();
    });
    
    // Show the upload failed files
    $(document).on('click', '#note-error', function (e) {
        if(failedFiles.length > 0)
            alert(failedFiles.join("\n"));
    });
	
    // Retry all fails
    $(document).on('click', '#btn-retry', function (e) {
    	  e.preventDefault();
    	  failedFiles.length = 0;
    	  numError = 0;
    	  if($('#note').length)
    	      $('#note').html('');
    	  var dataListFailClone = dataListFail.slice();
    	  dataListFail.length = 0;
    	  $.each(dataListFailClone, function() {
    	      if (this.context != null)
    	          this.context.remove();
      		  $('#upload').fileupload('add', this);
    	  });
    });
    
    // Update the note
    function updateNote() {
    	if($('#note').length)
			  $('#note').html('<span>' + numSuccess + '</span> successfully uploaded.<br /><span id="note-error">' + numError + '</span> failed uploaded.' + (numError > 0 ? ' <a href="#" id="btn-retry"> (Retry all)</a>' : ''));
    }
    
    // Helper function that formats the file sizes
    function formatFileSize(bytes) {
        if (typeof bytes !== 'number') {
            return '';
        }

        if (bytes >= 1000000000) {
            return (bytes / 1000000000).toFixed(2) + ' GB';
        }

        if (bytes >= 1000000) {
            return (bytes / 1000000).toFixed(2) + ' MB';
        }

        return (bytes / 1000).toFixed(2) + ' KB';
    }

});
