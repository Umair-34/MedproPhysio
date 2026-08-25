(function () {
  'use strict';

  var copyBtn = document.querySelector('.mp-visit-copy-btn');
  var feedback = document.getElementById('visitCopyFeedback');

  function showFeedback(message) {
    if (!feedback) {
      return;
    }
    feedback.textContent = message;
    feedback.hidden = false;
    window.setTimeout(function () {
      feedback.hidden = true;
    }, 2600);
  }

  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      var text = copyBtn.getAttribute('data-copy-text') || '';
      if (!text) {
        return;
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          showFeedback('Address copied to clipboard.');
        }).catch(fallbackCopy);
        return;
      }

      fallbackCopy();

      function fallbackCopy() {
        var textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'absolute';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand('copy');
          showFeedback('Address copied to clipboard.');
        } catch (error) {
          showFeedback('Could not copy address. Please copy it manually.');
        }
        document.body.removeChild(textarea);
      }
    });
  }

  document.querySelectorAll('[data-visit-action]').forEach(function (link) {
    link.addEventListener('click', function () {
      link.classList.add('is-pressed');
      window.setTimeout(function () {
        link.classList.remove('is-pressed');
      }, 180);
    });
  });
})();
