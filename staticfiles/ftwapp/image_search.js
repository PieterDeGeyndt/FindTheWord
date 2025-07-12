function waitForJQuery(callback) {
    if (typeof window.jQuery !== 'undefined') {
        callback(window.jQuery);
    } else {
        setTimeout(function() {
            waitForJQuery(callback);
        }, 50);
    }
}

waitForJQuery(function($) {
    console.log("🟢 image_search.js loaded and running");

    $(document).ready(function() {
        // ✅ Check if success message exists, if not create it
        if (!$('#image_success_message').length) {
        var successMsg = $('<div id="image_success_message">✅ Image saved! Reloading...</div>').css({
            display: 'none',
            position: 'fixed',
            top: '20px',
            right: '20px',
            backgroundColor: '#28a745',
            color: 'white',
            padding: '10px 20px',
            borderRadius: '5px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
            zIndex: 9999,
            fontSize: '14px'
        });
        $('body').append(successMsg);
        }

        // ✅ Check if field exists and button is not already added
        if ($('#id_image_search').length && !$('#image_search_button').length) {
            // Create button
            var button = $('<button type="button" id="image_search_button" class="button">Search Images</button>').css({
                marginLeft: '10px',
                verticalAlign: 'top'
            }); 
            // Insert button after input field
            $('#id_image_search').after(button);
            
            if (!$('#image_search_spinner').length) {
            var spinner = $('<span id="image_search_spinner" style="display:none; margin-left:10px;">⏳ Loading...</span>');
            $('#image_search_button').after(spinner);
            }
        }


    // ✅ Add click handler for button
    $(document).on('click', '#image_search_button', function() {
        var query = $('#id_image_search').val();
        console.log("🔎 Search button clicked, value:", query);

            if (query.length < 3) {
                alert('⚠️ Type at least 3 characters to search.');
                return;
            }

            var searchUrl = '/image-search/?q=' + encodeURIComponent(query);

            $('#image_search_spinner').show();
  
            $.getJSON(searchUrl, function(data) {
                // ✅ Hide spinner when done
                $('#image_search_spinner').hide();

                // --- continue building image cards here ---
                var images = data.images || [];
                var container = $('<div class="image-results"></div>').css({
                    marginTop: '10px',
                    display: 'flex',
                    flexWrap: 'wrap'
                });

                images.slice(0, 10).forEach(function(img) {
                    var imageTag = $('<img>').attr('src', img.thumbnail).css({
                        width: '120px',
                        margin: '5px',
                        border: '2px solid #eee',
                        borderRadius: '4px',
                        transition: 'all 0.3s',
                        cursor: 'pointer'
                    });
                    
                    imageTag.hover(
                        function() { $(this).css({ borderColor: '#2a6496', transform: 'scale(1.05)' }); },
                        function() { $(this).css({ borderColor: '#eee', transform: 'scale(1)' }); }
                    );
                    
                    imageTag.on('dblclick', function() {
                        var imageUrl = img.original;
                        var objIdMatch = window.location.pathname.match(/\/(\d+)\/change\/$/);
                        var objId = objIdMatch ? objIdMatch[1] : null;

                        var modelType = 'null';
                        if (window.location.href.includes('/category/')) {
                            modelType = 'category';
                        } else if (window.location.href.includes('/subcategory/')) {
                            modelType = 'subcategory';
                        } else if (window.location.href.includes('/word/')) {
                            modelType = 'word';
                        }

                        if (!modelType) {
                            alert('Error: Could not detect model type from URL.');
                            return;
                        }

                        if (!objId) {
                            alert('⚠️ Please save this object first before assigning an image!');
                            return;
                        }

                        $.get('/download-image/', {url: imageUrl, id: objId, type: modelType}, function(response) {
                            if (response.success) {
                                $('#image_success_message').fadeIn(300).delay(1000).fadeOut(300, function() {
                                    location.reload();
                                });
                            } else {
                                alert('Error: ' + response.error);
                            }
                        });
                    });
                    
                    imageTag.hide().fadeIn(300);
                    container.append(imageTag);
                });

                $('.image-results').remove();
                $('#image_search_button').after(container);
            });
        });
    });
});
