$ = jQuery

$(document).ready ->
    hljs.initHighlightingOnLoad();
    images = $(".post-image a")
    images.imageFader()

$.fn.imageFader = (options) ->
    imgClass = "post-image-full"

    @each () -> 
        $(this).click -> 
            $el = $(this)
            $("."+imgClass).each -> $el.fadeOut -> $el.remove()
            thumbHref = $el.attr("href")
            thumbHeight = $("img", this).height()

            img = $("<img>")
                .attr("src", thumbHref)
                .addClass(imgClass)

            $(img).appendTo($(this).parent()).load ->
                $el = $(this)
                fullImgHeight = $el.height()
                offset = fullImgHeight/2
                offset -= thumbHeight/2
                $el.css("top", -offset+"px")
                $el.fadeIn()
                $el.click ->
                    $(this).fadeOut -> $(this).remove()
            return false

            
