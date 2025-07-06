console.log("🟢 image_search.js file is loaded and running at all");

function waitForJQuery(callback) {
    if (typeof window.jQuery !== 'undefined') {
        callback(window.jQuery);
    } else {
        setTimeout(function () {
            waitForJQuery(callback);
        }, 50);
    }
}

waitForJQuery(function ($) {
    console.log("✅ jQuery is ready, search image JS running!");

    $(document).ready(function () {
        $(document).on('input', '#id_image_search', function () {
            var query = $(this).val();
            if (query.length < 3) return;

            console.log("🔎 Searching for:", query);

            var searchUrl = '/image-search/?q=' + encodeURIComponent(query);

            $.getJSON(searchUrl, function (data) {
                var images = data.images || [];
                var container = $('<div class="image-results"></div>').css({
                    marginTop: '10px',
                    display: 'flex',
                    flexWrap: 'wrap'
                });

                images.slice(0, 10).forEach(function (img) {
                    var imageTag = $('<img>').attr('src', img.thumbnail).css({
                        width: '120px',
                        margin: '5px',
                        cursor: 'pointer'
                    });

                    imageTag.on('dblclick', function() {
                    var imageUrl = img.original;
                    var objIdMatch = window.location.pathname.match(/\/(\d+)\/change\/$/);
                    var objId = objIdMatch ? objIdMatch[1] : null;
                    var modelType = 'word';
                    if (window.location.href.includes('/category/')) {
                        modelType = 'category';
                    } else if (window.location.href.includes('/subcategory/')) {
                        modelType = 'subcategory';
                    }

                    if (!objId) {
                        alert('⚠️ Please save this object first before assigning an image!');
                        return;
                    }

    $.get('/download-image/', {url: imageUrl, id: objId, type: modelType}, function(response) {
        if (response.success) {
            alert('Image successfully assigned and saved! The page will now reload.');
            location.reload();
        } else {
            alert('Error: ' + response.error);
        }
    });
});

                    container.append(imageTag);
                });

                $('.image-results').remove();
                $(this).after(container);
            }.bind(this));
        });
    });
});