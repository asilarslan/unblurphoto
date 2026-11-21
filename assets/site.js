// Before/after slider, sticky mobile CTA and language switcher.
(function () {
  function setPos(el, pct) {
    pct = Math.max(0, Math.min(100, pct));
    el.style.setProperty('--pos', pct + '%');
    var knob = el.querySelector('.ba-knob');
    if (knob) knob.setAttribute('aria-valuenow', Math.round(pct));
  }

  function initSlider(el) {
    if (el.dataset.ready) return;
    el.dataset.ready = '1';
    var dragging = false;
    function fromEvent(e) {
      var r = el.getBoundingClientRect();
      setPos(el, ((e.clientX - r.left) / r.width) * 100);
    }
    el.addEventListener('pointerdown', function (e) {
      dragging = true;
      el.dataset.touched = '1';
      fromEvent(e);
    });
    window.addEventListener('pointermove', function (e) { if (dragging) fromEvent(e); });
    window.addEventListener('pointerup', function () { dragging = false; });
    window.addEventListener('pointercancel', function () { dragging = false; });
    var knob = el.querySelector('.ba-knob');
    if (knob) {
      knob.addEventListener('keydown', function (e) {
        var cur = parseFloat(getComputedStyle(el).getPropertyValue('--pos')) || 50;
        if (e.key === 'ArrowLeft') { setPos(el, cur - 5); e.preventDefault(); }
        if (e.key === 'ArrowRight') { setPos(el, cur + 5); e.preventDefault(); }
      });
    }
    // One gentle sweep so visitors notice the slider can be dragged.
    if (el.hasAttribute('data-hint') && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
      var start = null;
      var frames = [50, 82, 18, 50];
      function step(t) {
        if (el.dataset.touched) return;
        if (start === null) start = t;
        var p = (t - start) / 2400;
        if (p >= 1) { setPos(el, 50); return; }
        var seg = Math.min(2, Math.floor(p * 3));
        var local = p * 3 - seg;
        var ease = local < .5 ? 2 * local * local : 1 - Math.pow(-2 * local + 2, 2) / 2;
        setPos(el, frames[seg] + (frames[seg + 1] - frames[seg]) * ease);
        requestAnimationFrame(step);
      }
      setTimeout(function () { requestAnimationFrame(step); }, 900);
    }
  }

  window.UBSlider = { init: initSlider, set: setPos };
  document.querySelectorAll('.ba').forEach(initSlider);

  // Mobile sticky App Store button: only after the hero, and never on top of the tool.
  var sticky = document.querySelector('.sticky-cta');
  var hero = document.querySelector('[data-hero]');
  var tool = document.querySelector('[data-tool]');
  if (sticky && hero && 'IntersectionObserver' in window) {
    var heroVisible = true, toolVisible = false;
    var update = function () { sticky.classList.toggle('show', !heroVisible && !toolVisible); };
    new IntersectionObserver(function (e) { heroVisible = e[0].isIntersecting; update(); }).observe(hero);
    if (tool) new IntersectionObserver(function (e) { toolVisible = e[0].isIntersecting; update(); }).observe(tool);
  }

  var lang = document.querySelector('.lang');
  if (lang) lang.addEventListener('change', function () { location.href = lang.value; });
})();
