/**
* Template Name: WeBuild - v2.2.0
* Template URL: https://bootstrapmade.com/free-bootstrap-coming-soon-template-countdwon/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
!(function($) {
  "use strict";
    window.setInterval(function(){
    var now = new Date();
    var start = new Date("January 30, 2021 18:00:00")
    var end = new Date("January 30, 2021 21:00:00")

    if(now.getTime() < start){
      $('.countdown2').remove();
      if ($('.countdown').length) {
        var count1 = $('.countdown').data('count');
        var template1 = $('.countdown').data('template');
        $('.countdown').countdown(count1, function(event) {
          $(this).html(event.strftime(template1));
        });
      }
    }
    else if ( now.getTime() < end ){
      $('.countdown').remove();
      if ($('.countdown2').length) {
      var count2 = $('.countdown2').data('count');
      var template2 = $('.countdown2').data('template');
      $('.countdown2').countdown(count2, function(event) {
        $(this).html(event.strftime(template2));
      });
      }
      var quiz = document.getElementById("quiz")
      quiz.setAttribute("href","/quiz")
    }
    else{
      $('.countdown2').remove();
      var elem = document.getElementById("start")
      elem.innerHTML = "Chase has Ended!"
      quiz.setAttribute("href","#")
    }
  },0);

  // Smooth scroll for  links with .scrollto classes
  $(document).on('click', '.scrollto', function(e) {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      e.preventDefault();
      var target = $(this.hash);
      if (target.length) {
        var scrollto = target.offset().top;
        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');
        return false;
      }
    }
  });

})(jQuery);