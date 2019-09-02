var $navbar_toggler = $(".navbar-toggler"),
    $navbar_collapse = $(".collapse");
$navbar_toggler.on("click", function (a) {
    "none" == $navbar_collapse.css("display") ? ($navbar_collapse.slideDown("slow"), $(".cart-popup-container").hide(), $(".cart-popup-container").removeClass("cart-popup-open")) : $navbar_collapse.slideUp("slow")
}), $(".star").on("click", function (a) {
    $navbar_collapse.hide(), console.log("worked"), console.log("active", active)
}), $(".close-icon").on("click", function (a) {
    $(".cart-popup-container").removeClass("cart-popup-open"), $(".cart-popup-container").toggle("slide")
}), $(document).on("click", function (a) {
    var o = $(a.target);
    "block" != $navbar_collapse.css("display") || o.hasClass("navbar-toggler-icon") || o.hasClass("navbar-toggler") || o.hasClass("fa") || o.hasClass("star") || o.hasClass("dropdown") || o.hasClass("dropdown-toggle") || o.hasClass("form-inline") || o.hasClass("autocomplete") || o.hasClass("go_button") || o.hasClass("go") || o.hasClass("search_box") || $navbar_collapse.slideUp("slow")
}), $("#navbarDropdownMenuLink").on("click", function (a) {
    $(".dropdown-menu").toggle()
}), "" != active && $("#" + active).addClass("active"), "song" != active && "rchannel" != active || $("#religious").addClass("active"), "home" == active && $("#home").addClass("active");