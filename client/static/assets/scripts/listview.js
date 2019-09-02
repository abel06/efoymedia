$.fn.isInViewport = function () {
    var elementTop = $(this).offset().top;
    var elementBottom = elementTop + $(this).outerHeight();
    var viewportTop = $(window).scrollTop();
    var viewportBottom = viewportTop + $(window).height();
    return elementBottom > viewportTop && elementTop < viewportBottom;
};

$.fn.isInViewSidePort = function () {
    var elementLeft = $(this).offset().left;
    var elementRight = elementLeft + $(this).outerWidth()
    var viewportLeft = $(window).offset().left;
    var viewportRight = viewportLeft + $(window).outerWidth()

    return elementRight > viewportLeft && elementLeft < viewportRight;
    // && elementTop < viewportBottom;
};
page = 1
var cat = "{{cat}}";
$(window).on('load', function () {
    defferImages()
    var processing = false
    var x = 30
    $(window).on('resize scroll', function () {
        var scrollAmount = $(window).scrollTop();
        var documentHeight = $(document).height();
        defferImages()

        var scrollPercent = (scrollAmount / documentHeight) * 100;

        if (scrollPercent > x) {
            page = page + 1
            if (!processing) {
                processing = true

                console.log(category)
                callAjax();

            }
        }
        function callAjax() {

            $.ajax({
                url: "http://127.0.0.1:8000/listview?page=" + page + "&category=" + category,

                success: function (result) {
                    processing = false;

                    $('.row.movie-list').append(result)


                },
                error: function (request, error) {
                    "Request: " + JSON.stringify(request);
                }
            });

        }
        // defferImages()

    });


    // $(".regular").on('afterChange', function (event, slick, direction) {
    //     defferImages($(this))
    // });

    function defferImages(element) {

        var sliderImgDeffer = $(".slider_img")
        var src = sliderImgDeffer[0].getAttribute('data-src')
        // var src2 = sliderImgDeffer[0].getAttribute('data-src2')
        sliderImgDeffer[0].setAttribute('src', src)
        // $(".slider_img").css("height", screen.height);
        // $(".slider_img").css("width", screen.width);



        if (element) {
            element.find('.single-vid-container').each(function () {
                if ($(this).isInViewport() && $(this).isInViewSidePort()) {
                    img = $(this).find('img')
                    if (img.hasClass("unloaded")) {
                        console.log(img)
                        imgDefer = img[0]
                        imgDefer.setAttribute('src', imgDefer.getAttribute('data-src'))
                        img.removeClass("unloaded")
                        img.addClass("loaded")
                    }
                }
            });
        } else {
            $('.single-vid-container').each(function () {
                if ($(this).isInViewport() && $(this).isInViewSidePort()) {
                    imgDefer = $(this).find('img')[0]
                    imgDefer.setAttribute('src', imgDefer.getAttribute('data-src'))
                    $(this).find('img').removeClass("unloaded")
                    $(this).find('img').addClass("loaded")
                }
            });
        }
    }



});




function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

