mw.require('icon_selector.js');

mw.require('fonts.js');
mw.lib.require('bootstrap3');

mw.iconLoader()
   .addIconSet('SVGIcons')
   .addIconSet('iconsMindLine')
   .addIconSet('iconsMindSolid')
   .addIconSet('mwIcons')
   .addIconSet('materialDesignIcons')
   .addIconSet('materialIcons');

mw.templateFont = mw.templateFont || new mw.font();
mw.templateTopFixed = '.nav-bar.nav--fixed';



$(document).ready(function() {
   var $window = $(window);
   var $navBar = $('nav');
   var navHeight = $navBar.outerHeight(true);
 
   // Set the height of full-height sections to fill the window, minus the height of the navigation bar
   var setFullHeightSectionHeight = function() {
     var windowHeight = $window.height();
     var $fullHeightSections = $('.full-height-section');
     $fullHeightSections.css('height', windowHeight - navHeight);
   };
 
   // Call the function initially and on window resize
   setFullHeightSectionHeight();
   $window.on('resize', setFullHeightSectionHeight);
 });
 
$(document).ready(function () {
   var $window = $(window);
   var windowWidth = $window.width();
   var windowHeight = $window.height();
   var navHeight = $('nav').outerHeight(true);

   // Disable parallax on mobile
   if ((/Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i).test(navigator.userAgent || navigator.vendor || window.opera)) {
      $('section[data-parallax="true"]').addClass('not-parallaxed');
      $('div[data-parallax="true"]').addClass('not-parallaxed');
   } else {
      $('section[data-parallax="true"]').each(function () {
         $(this).parallax('50%', 0.5);
      });

      $('div[data-parallax="true"]').each(function () {
         $(this).parallax('50%', 0.5);
      });
   }

   // Full height section with 100% width
   var $fullHeightSection = $('.full-height-section');
   $fullHeightSection.css({
      'height': windowHeight - navHeight
   });
   $window.resize(function () {
      $fullHeightSection.css({
         'height': $window.height() - navHeight
      });
   });

   // Tabs
   var $tabs = $('.tabs');
   $tabs.find('.tabs__tabs a').on('click', function () {
      var $tab = $(this);
      var $tabPanel = $($tab.attr('href'));
      $tabs.find('.tabs__tabs a').removeClass('active');
      $tab.addClass('active');
      $tabs.find('.tabs__panel').removeClass('active');
      $tabPanel.addClass('active');
      return false;
   });

   // Mobile menu
   var $mobileMenu = $('#mobile-menu');
   $mobileMenu.on('click', function () {
      $(this).toggleClass('active');
      $('.nav-main').toggleClass('active');
      return false;
   });

   $('.nav-main').find('.dropdown-toggle').on('click', function (e) {
      if ($(this).parent('.dropdown').hasClass('show')) {
         e.stopPropagation();
      }
   });

   $('.nav-main').find('.dropdown-menu').on('click', function (e) {
      e.stopPropagation();
   });

   $window.on('resize', function () {
      if (windowWidth != $window.width()) {
         windowWidth = $window.width();
         $mobileMenu.removeClass('active');
         $('.nav-main').removeClass('active');
      }
   });

   // Init Swiper
   var swiper = new Swiper('.swiper-container', {
      direction: 'horizontal',
      speed: 800,
      pagination: {
         el: '.swiper-pagination',
         type: 'bullets',
         clickable: true
      },
      navigation: {
         nextEl: '.swiper-button-next',
         prevEl: '.swiper-button-prev',
      },
   });

   // Blog feed
   var $blogFeed = $('.blog-feed');
   var $blogFeedList = $blogFeed.find('.blog-feed__list');
   var $blogFeedItem = $blogFeed.find('.blog-feed__item');
   var $blogFeedButton = $blogFeed.find('.blog-feed__button');
   var blogFeedCount = 6;

   $blogFeedList.find('.blog-feed__item:lt(' + blogFeedCount + ')').addClass('shown');
   if ($blogFeedItem.length <= blogFeedCount) {
      $blogFeedButton.hide();
   }

   $blogFeedButton.on('click', function () {
      var $blogFeedItemShown = $blogFeedList.find('.blog-feed__item')
   })
});

mw.on('ready', function () {
   var header = mw.$('#header').get(0);
   var content = mw.$('#content').get(0);
   var footer = mw.$('#footer').get(0);
   var stickyNav = mw.$('.sticky-nav').get(0);
   var stickyHeader = mw.$('.sticky-header').get(0);
   var stickyFooter = mw.$('.sticky-footer').get(0);
   var stickyElements = [stickyNav, stickyHeader, stickyFooter];
   var resizeStickyElements = function () {
      var contentHeight = content.offsetHeight;
      var windowHeight = window.innerHeight;
      var headerHeight = header ? header.offsetHeight : 0;
      var footerHeight = footer ? footer.offsetHeight : 0;
      var heightOffset = headerHeight + footerHeight + stickyNav.offsetHeight + stickyHeader.offsetHeight + stickyFooter.offsetHeight;
      var contentMinHeight = windowHeight - heightOffset;
      content.style.minHeight = contentMinHeight + 'px';
      stickyElements.forEach(function (el) {
         if (el) {
            el.style.width = content.offsetWidth + 'px';
         }
      });
   };
   resizeStickyElements();
   mw.$(window).resize(function () {
      resizeStickyElements();
   });
});
$(document).ready(function () {
   mw.$('#blog-posts-5').find('a[data-page-number]').unbind('click');
   mw.$('#blog-posts-5').find('a[data-page-number]').click(function (e) {
      var pn = $(this).attr('data-page-number');
      mw.$('#blog-posts-5').attr('paging_param', 'current_page');
      mw.$('#blog-posts-5').attr('current_page', pn)
      mw.reload_module('#blog-posts-5');
      return false;
   });
});
mw.$(document).ready(function () {
   mr.sliders.documentReady($)
})
mw.require('events.js', true);
mw.require("url.js", true);
//mw.require("tools.js", true);
mw.require("forms.js", true);
mw.search_settings = {
   content_type: 'all',
   limit: 5,
   ajax_paging: true,
   template: 'default',
   done: false,
   hide_paging: true
}
mw.search = function (key, holder, obj) {
   if (typeof key === 'undefined' || typeof holder === 'undefined') return false;
   var opt = $.extend(mw.search_settings, obj, {});
   var holder = $(holder);
   holder
      .attr('keyword', key)
      .attr('content_type', opt.content_type)
      .attr('hide_paging', opt.hide_paging)
      .attr('limit', opt.limit)
      .attr('ajax_paging', opt.ajax_paging)
      .attr('search_global', true)

      .attr('template', opt.template)
      .show();

   mw.load_module('posts', holder, function () {
      if (typeof opt.done === 'function') {
         opt.done.call(this);
      }
   });
}
$(document).ready(function () {

   $('#loginModal').on('show.bs.modal', function (e) {
      $('#loginModalModuleLogin').reload_module();
      $('#loginModalModuleRegister').reload_module();
   });


   $('#shoppingCartModal').on('show.bs.modal', function (e) {
      $('#js-ajax-cart-checkout-process').reload_module();
   });


   mw.on('mw.cart.add', function (event, data) {
      $('#shoppingCartModal').modal('show');


   });


   $('body').on('click', '.js-show-register-window', function (e) {
      $('#loginModal').modal('show');
      $('.js-login-window').hide();
      $('.js-register-window').show();
      e.preventDefault();
      e.stopPropagation();
   });

   $('.js-show-login-window').on('click', function (e) {

      $('.js-register-window').hide();
      $('.js-login-window').show();
      e.preventDefault();
      e.stopPropagation();
   });
});
mw.lib.require('collapse_nav');
$(document).ready(function () {
   $('.nav-main .menu').collapseNav({
      responsive: 1,
      mobile_break: 991,
      li_class: 'dropdown',
      li_a_class: '',
      li_ul_class: '',
      caret: '<span class="caret"></span>' //Element append immediately after the More text
   });
})
checkFirstSectionForNav = function () {
   var firstSectionHas = $('.main-container section').first().hasClass('imagebg');

   var skip = $('.main-container section').first().hasClass('background-image-holder');

   if (!skip && firstSectionHas == true) {
      $('nav .nav-bar').addClass('nav--absolute nav--transparent');
   } else {
      $('nav .nav-bar').removeClass('nav--absolute nav--transparent');
   }
}

$(document).ready(function () {
   checkFirstSectionForNav();

   $(window).on('moduleLoaded', function () {
      checkFirstSectionForNav();
   });
});
mw.lib.require('fitty');

mw.$(document).ready(function () {
   //fitty(document.getElementById('fitty-logo-1'));
   //fitty(document.getElementById('fitty-logo-2'));
});
mw.require('tools.js', true);
mw.require('ui.css', true);
mw.$(document).ready(function () {
   mr.sliders.documentReady($)
})
$(document).ready(function () {
   mw.$('#recent-news-14').find('a[data-page-number]').unbind('click');
   mw.$('#recent-news-14').find('a[data-page-number]').click(function (e) {
      var pn = $(this).attr('data-page-number');
      mw.$('#recent-news-14').attr('paging_param', 'current_page');
      mw.$('#recent-news-14').attr('current_page', pn)
      mw.reload_module('#recent-news-14');
      return false;
   });
});
// Get the search bar element
var searchBar = document.querySelector('.inline-search');

// Get the button or icon element that will toggle the search bar
var toggleButton = document.querySelector('.search-toggle');

// Add a click event listener to the toggle button or icon
toggleButton.addEventListener('click', function() {
  // Toggle the display of the search bar
  searchBar.style.display = (searchBar.style.display === 'none') ? 'block' : 'none';
});
