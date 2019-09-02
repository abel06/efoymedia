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


// $.ajax({
//     url: "http://127.0.0.1:8000/api/videos?category=News_Politics",
//     success: function (result) {
//         console.log(result)
//     },
//     error: function (request, error) {
//         "Request: " + JSON.stringify(request);
//     }
// });
// });

$(window).on('load', function () {
    var sliderImgDeffer = $(".slider-img")


    defferImages()
    $(".slick-dots").on("click", function () {
        $(this).parent().on('afterChange', function (event, slick, currentSlide) {
            defferImages($(this))
        });
    })
    $(window).on('resize scroll', function () {
        defferImages()

    });
    $(".regular").on('afterChange', function (event, slick, direction) {
        defferImages($(this))
    });

    function defferImages(element) {
        if (element) {
            element.find('.slick-slide').each(function () {
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
            $('.slick-slide').each(function () {
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

