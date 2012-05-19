// Generated by CoffeeScript 1.3.1
(function() {
  var $;

  $ = jQuery;

  $(document).ready(function() {
    var images;
    images = $(".post-image a");
    return images.imageFader();
  });

  $.fn.imageFader = function(options) {
    var imgClass;
    imgClass = "post-image-full";
    return this.each(function() {
      return $(this).click(function() {
        var $el, img, thumbHeight, thumbHref;
        $el = $(this);
        $("." + imgClass).each(function() {
          return $el.fadeOut(function() {
            return $el.remove();
          });
        });
        thumbHref = $el.attr("href");
        thumbHeight = $("img", this).height();
        img = $("<img>").attr("src", thumbHref).addClass(imgClass);
        $(img).appendTo($(this).parent()).load(function() {
          var fullImgHeight, offset;
          $el = $(this);
          fullImgHeight = $el.height();
          offset = fullImgHeight / 2;
          offset -= thumbHeight / 2;
          $el.css("top", -offset + "px");
          $el.fadeIn();
          return $el.click(function() {
            return $(this).fadeOut(function() {
              return $(this).remove();
            });
          });
        });
        return false;
      });
    });
  };

}).call(this);