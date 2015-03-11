var modal = (function(){
    var method = {}, $overlay, $modal, $content, $close, closeCallback;

    // Center the modal in the viewport
    method.center = function () {
        var top, left;

        top = Math.max($(window).height() - $modal.outerHeight(), 0) / 2;
        left = Math.max($(window).width() - $modal.outerWidth(), 0) / 2;

        $modal.css({
            top:top + $(window).scrollTop(),
            left:left + $(window).scrollLeft()
        });
    };

    // Open the modal
    method.open = function (settings) {
        closeCallback = settings.closeCallback;
        $content.empty().append(settings.content);

        $modal.css({
            width: settings.width || 'auto',
            height: settings.height || 'auto'
        });

        method.center();
        $(window).bind('resize.modal', method.center);
        $modal.show();
        $overlay.show();
    };

    // Close the modal
    method.close = function () {
        $modal.hide();
        $overlay.hide();
        $content.empty();
        $(window).unbind('resize.modal');
        if(closeCallback) closeCallback();
    };

    // Generate the HTML and add it to the document
    $overlay = $('<div id="overlay"></div>');
    $modal = $('<div id="overlayModal"></div>');
    $content = $('<div id="overlayContent"></div>');
    $close = $('<a id="overlayClose" href="#">close</a>');

    $modal.hide();
    $overlay.hide();
    $modal.append($content, $close);

    $(document).ready(function(){
        $('body').append($overlay, $modal);
    });

    $close.click(function(e){
        e.preventDefault();
        method.close();
    });

    $overlay.click(function(e){
        method.close();
    });

    return method;
}());
