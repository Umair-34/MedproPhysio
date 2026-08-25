(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var navToggle = document.querySelector('[data-cp-nav-toggle]');
    var nav = document.getElementById('cp-main-nav');
    if (navToggle && nav) {
      navToggle.addEventListener('click', function () {
        nav.classList.toggle('is-open');
      });
    }

    if (typeof Swiper !== 'undefined') {
      var heroEl = document.querySelector('.cp-hero-slider');
      if (heroEl) {
        new Swiper(heroEl, {
          loop: true,
          autoplay: {
            delay: 5500,
            disableOnInteraction: false,
          },
          effect: 'fade',
          fadeEffect: {
            crossFade: true,
          },
          pagination: {
            el: '.cp-hero .swiper-pagination',
            clickable: true,
          },
          navigation: {
            nextEl: '.cp-hero .swiper-button-next',
            prevEl: '.cp-hero .swiper-button-prev',
          },
        });
      }
    }

    var counterRing = document.querySelector('[data-counter-value]');
    if (counterRing) {
      var target = parseInt(counterRing.getAttribute('data-counter-value'), 10) || 95;
      var numberEl = counterRing.querySelector('.cp-counter-number');
      var start = 0;
      var duration = 1400;
      var startTime = null;

      function animateCounter(timestamp) {
        if (!startTime) {
          startTime = timestamp;
        }
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var value = Math.round(start + (target - start) * progress);
        if (numberEl) {
          numberEl.textContent = String(value);
        }
        counterRing.style.setProperty('--pct', String(value));
        if (progress < 1) {
          window.requestAnimationFrame(animateCounter);
        }
      }

      window.requestAnimationFrame(animateCounter);
    }
  });
})();
