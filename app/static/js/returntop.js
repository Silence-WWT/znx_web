/**
 * Created by tangwei on 2014/10/28.
 */
(function($) {
    $.fn.goup = function(options) {
        $.fn.goup.defaultOpts = {
            appear: 200,
            scrolltime: 800,
            imgsrc: "../images/top_arrow.png",
            width: 90,
            place: "bottom-right",
            fadein: 500,
            fadeout: 500,
            opacity: 0.5
        };
        var opts = $.extend({}, $.fn.goup.defaultOpts, options);
        return this.each(function() {
            var goup = $(this);
            goup.html("<a><img /></a>");
            var goupa = $("#goup a");
            var goupimg = $("#goup a img");
            goup.css({
                "position": "fixed",
                "display": "block",
                "width": "'" + opts.width + "px'",
                "z-index": "9"
            });
            goupa.css("opacity", opts.opacity);
            goupimg.attr("src", opts.imgsrc);
            goupimg.width(opts.width);
            goupimg.hide();
            $(function() {
                $(window).scroll(function() {
                    if ($(this).scrollTop() > opts.appear) goupimg.fadeIn(opts.fadein);
                    else goupimg.fadeOut(opts.fadeout)
                });
                $(goupa).hover(function() {
                    $(this).css("opacity", "1.0");
                    $(this).css("cursor", "pointer")
                }, function() {
                    $(this).css("opacity", opts.opacity)
                });
                $(goupa).click(function() {
                    $("body,html").animate({
                        scrollTop: 0
                    }, opts.scrolltime);
                    return false
                })
            });
            if (opts.place === "top-right") goup.css({
                "top": "2%",
                "right": "2%"
            });
            else if (opts.place === "top-left") goup.css({
                "top": "2%",
                "left": "2%"
            });
            else if (opts.place === "bottom-right") goup.css({
                "bottom": "2%",
                "right": "2%"
            });
            else if (opts.place === "bottom-left") goup.css({
                "bottom": "2%",
                "left": "2%"
            });
            else goup.css({
                    "bottom": "2%",
                    "right": "2%"
                })
        })
    }
})(jQuery);

$(document).ready(function() {
    $('#goup').goup();
    $('#goup').goup({
        width: "40px",
        scrolltime: 800,
        appear: 600,
        imgsrc: '../images/top_arrow.png',
        place: "bottom-right",
        fadein: 300,
        fadeout: 500,
        opacity: "1"
    });
    var h = $(window).height();
    $('#scroll a').click(function() {
        $("html, body").animate({
            scrollTop: h
        }, 900);
        return false;
    });
    $('#divheader').height(h);

    var h6 = parseInt(h / 6);
    $('#title').height(h6);
    $('#twitter').height(h6);
    $('#downloadbuttons').height(h6);
    $('#scroll').height(h6);
});