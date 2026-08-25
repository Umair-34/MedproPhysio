(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var header = document.querySelector('.mp-header');
    if (header) {
      var syncHeaderScroll = function () {
        var scrolled = window.scrollY > 10;
        header.classList.toggle('is-scrolled', scrolled);
        document.documentElement.classList.toggle('is-header-scrolled', scrolled);
      };
      syncHeaderScroll();
      window.addEventListener('scroll', syncHeaderScroll, { passive: true });
    }

    var navToggle = document.querySelector('[data-mp-nav-toggle]');
    var nav = document.getElementById('mp-main-nav');
    if (navToggle && nav) {
      navToggle.addEventListener('click', function () {
        var open = nav.classList.toggle('is-open');
        navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }

    document.querySelectorAll('.mp-nav__has-dropdown > a').forEach(function (link) {
      link.addEventListener('click', function (event) {
        if (!window.matchMedia('(max-width: 900px)').matches) {
          return;
        }
        var item = link.closest('.mp-nav__has-dropdown');
        if (!item || !item.querySelector('.mp-nav__dropdown')) {
          return;
        }
        event.preventDefault();
        item.classList.toggle('is-open');
      });
    });

    document.querySelectorAll('[data-mp-process]').forEach(function (root) {
      var steps = root.querySelectorAll('[data-mp-process-step]');
      var panels = root.querySelectorAll('[data-mp-process-panel]');
      var progress = root.querySelector('[data-mp-process-progress]');
      if (!steps.length || !panels.length) {
        return;
      }

      var activateStep = function (index) {
        var safeIndex = Math.max(0, Math.min(index, steps.length - 1));

        steps.forEach(function (step, stepIndex) {
          var isActive = stepIndex === safeIndex;
          step.classList.toggle('is-active', isActive);
          step.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });

        panels.forEach(function (panel, panelIndex) {
          var isActive = panelIndex === safeIndex;
          panel.classList.toggle('is-active', isActive);
          if (isActive) {
            panel.removeAttribute('hidden');
          } else {
            panel.setAttribute('hidden', '');
          }
        });

        if (progress) {
          progress.style.width = ((safeIndex + 1) / steps.length * 100) + '%';
        }
      };

      steps.forEach(function (step, index) {
        step.addEventListener('click', function () {
          activateStep(index);
        });

        step.addEventListener('keydown', function (event) {
          if (event.key === 'ArrowDown' || event.key === 'ArrowRight') {
            event.preventDefault();
            activateStep(index + 1);
            steps[Math.min(index + 1, steps.length - 1)].focus();
          } else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') {
            event.preventDefault();
            activateStep(index - 1);
            steps[Math.max(index - 1, 0)].focus();
          }
        });
      });

      activateStep(0);
    });

    document.querySelectorAll('[data-mp-about]').forEach(function (root) {
      var tabs = root.querySelectorAll('[data-mp-about-tab]');
      var panels = root.querySelectorAll('[data-mp-about-panel]');
      if (!tabs.length || !panels.length) {
        return;
      }

      var activateTab = function (index) {
        var safeIndex = Math.max(0, Math.min(index, tabs.length - 1));

        tabs.forEach(function (tab, tabIndex) {
          var isActive = tabIndex === safeIndex;
          tab.classList.toggle('is-active', isActive);
          tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
          tab.setAttribute('tabindex', isActive ? '0' : '-1');
        });

        panels.forEach(function (panel, panelIndex) {
          var isActive = panelIndex === safeIndex;
          panel.classList.toggle('is-active', isActive);
          if (isActive) {
            panel.removeAttribute('hidden');
          } else {
            panel.setAttribute('hidden', '');
          }
        });
      };

      tabs.forEach(function (tab, index) {
        tab.addEventListener('click', function () {
          activateTab(index);
        });

        tab.addEventListener('keydown', function (event) {
          if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
            event.preventDefault();
            activateTab(index + 1);
            tabs[Math.min(index + 1, tabs.length - 1)].focus();
          } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
            event.preventDefault();
            activateTab(index - 1);
            tabs[Math.max(index - 1, 0)].focus();
          }
        });
      });

      activateTab(0);
    });

    document.querySelectorAll('[data-mp-faq-page]').forEach(function (root) {
      var searchInput = root.querySelector('[data-mp-faq-search]');
      var filters = root.querySelectorAll('[data-mp-faq-filter]');
      var items = root.querySelectorAll('[data-mp-faq-item]');
      var emptyState = root.querySelector('[data-mp-faq-empty]');
      var countEl = root.querySelector('[data-mp-faq-count]');
      var expandBtn = root.querySelector('[data-mp-faq-expand]');
      var collapseBtn = root.querySelector('[data-mp-faq-collapse]');
      var activeCategory = 'all';

      var updateCount = function (visibleCount) {
        if (!countEl) {
          return;
        }
        countEl.textContent = visibleCount + ' question' + (visibleCount === 1 ? '' : 's');
      };

      var applyFilters = function () {
        var query = (searchInput && searchInput.value ? searchInput.value : '').trim().toLowerCase();
        var visibleCount = 0;

        items.forEach(function (item) {
          var category = item.getAttribute('data-category') || '';
          var text = item.textContent.toLowerCase();
          var matchesCategory = activeCategory === 'all' || category === activeCategory;
          var matchesQuery = !query || text.indexOf(query) !== -1;
          var isVisible = matchesCategory && matchesQuery;

          item.hidden = !isVisible;
          if (!isVisible) {
            item.removeAttribute('open');
          }
          if (isVisible) {
            visibleCount += 1;
          }
        });

        if (emptyState) {
          emptyState.hidden = visibleCount > 0;
        }
        updateCount(visibleCount);
      };

      filters.forEach(function (filter) {
        filter.addEventListener('click', function () {
          activeCategory = filter.getAttribute('data-mp-faq-filter') || 'all';
          filters.forEach(function (btn) {
            var isActive = btn === filter;
            btn.classList.toggle('is-active', isActive);
            btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
          });
          applyFilters();
        });
      });

      if (searchInput) {
        searchInput.addEventListener('input', applyFilters);
      }

      if (expandBtn) {
        expandBtn.addEventListener('click', function () {
          items.forEach(function (item) {
            if (!item.hidden) {
              item.setAttribute('open', '');
            }
          });
        });
      }

      if (collapseBtn) {
        collapseBtn.addEventListener('click', function () {
          items.forEach(function (item) {
            item.removeAttribute('open');
          });
        });
      }

      applyFilters();
    });

    if (typeof Swiper !== 'undefined') {
      document.querySelectorAll('[data-mp-swiper]').forEach(function (el) {
        var opts = {
          loop: true,
          autoplay: { delay: 5000, disableOnInteraction: false },
          pagination: { el: el.querySelector('.swiper-pagination'), clickable: true },
        };
        if (el.dataset.mpSwiper === 'hero') {
          opts.effect = 'fade';
          opts.fadeEffect = { crossFade: true };
          opts.autoplay = { delay: 5500, disableOnInteraction: false };
          opts.speed = 900;
        } else if (el.dataset.mpSwiper === 'testimonials') {
          opts.slidesPerView = 1;
          opts.spaceBetween = 14;
          opts.autoplay = { delay: 6000, disableOnInteraction: false };
          opts.navigation = {
            nextEl: el.querySelector('.swiper-button-next'),
            prevEl: el.querySelector('.swiper-button-prev'),
          };
          opts.breakpoints = {
            768: { slidesPerView: 2, spaceBetween: 16 },
          };
        }
        new Swiper(el, opts);
      });
    }
  });
})();
