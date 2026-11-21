// Free in-browser unblur preview. Photos never leave the device.
(function () {
  var root = document.querySelector('[data-tool]');
  if (!root) return;
  var T = JSON.parse(root.querySelector('.tool-i18n').textContent);
  var MAX_SIDE = 1000;
  var $ = function (s) { return root.querySelector(s); };
  var drop = $('[data-drop]'), input = drop.querySelector('input'), start = $('[data-start]'), work = $('[data-work]');
  var slider = $('[data-result]'), imgBefore = slider.querySelector('.ba-before'), imgAfter = slider.querySelector('.ba-after');
  var strength = $('[data-strength]'), strengthVal = $('[data-strength-val]'), angle = $('[data-angle]'), angleVal = $('[data-angle-val]'), angleRow = $('[data-angle-row]');
  var status = $('[data-status]'), bar = $('.bar i'), dl = $('[data-download]');
  var mode = (root.querySelector('[data-mode][aria-pressed="true"]') || {}).dataset.mode || 'focus', source = null, worker = null, timer = null, afterUrl = null, beforeUrl = null;

  function setStatus(msg, p) { status.textContent = msg; bar.style.width = Math.round((p || 0) * 100) + '%'; }

  function loadImage(src) {
    return new Promise(function (resolve, reject) {
      var img = new Image();
      img.onload = function () { resolve(img); };
      img.onerror = reject;
      img.src = src;
    });
  }

  function useImage(src) {
    loadImage(src).then(function (img) {
      var scale = Math.min(1, MAX_SIDE / Math.max(img.naturalWidth, img.naturalHeight));
      var c = document.createElement('canvas');
      c.width = Math.round(img.naturalWidth * scale);
      c.height = Math.round(img.naturalHeight * scale);
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      source = c;
      c.toBlob(function (b) {
        if (beforeUrl) URL.revokeObjectURL(beforeUrl);
        beforeUrl = URL.createObjectURL(b);
        imgBefore.src = beforeUrl;
        imgAfter.src = beforeUrl;
      }, 'image/jpeg', 0.92);
      drop.hidden = true; start.hidden = true; work.hidden = false;
      window.UBSlider.init(slider);
      window.UBSlider.set(slider, 50);
      run();
    }).catch(function () { setStatus(T.error, 0); work.hidden = true; drop.hidden = false; start.hidden = false; alert(T.error); });
  }

  function onFile(file) {
    if (!file || !/^image\//.test(file.type)) { alert(T.error); return; }
    useImage(URL.createObjectURL(file));
  }

  function run() {
    if (!source) return;
    if (worker) worker.terminate();
    worker = new Worker(root.dataset.worker);
    var ctx = source.getContext('2d');
    var data = ctx.getImageData(0, 0, source.width, source.height);
    setStatus(T.processing.replace('{p}', '0'), 0);
    dl.setAttribute('aria-disabled', 'true');
    worker.onmessage = function (e) {
      if (e.data.type === 'progress') { setStatus(T.processing.replace('{p}', Math.round(e.data.value * 100)), e.data.value); return; }
      var out = document.createElement('canvas');
      out.width = e.data.width; out.height = e.data.height;
      var octx = out.getContext('2d');
      octx.putImageData(new ImageData(e.data.data, e.data.width, e.data.height), 0, 0);
      var fs = Math.max(12, Math.round(out.width / 40));
      octx.font = '600 ' + fs + 'px -apple-system, Segoe UI, sans-serif';
      octx.textAlign = 'right'; octx.textBaseline = 'bottom';
      octx.fillStyle = 'rgba(0,0,0,.45)';
      octx.fillText('unblurphoto.app · preview', out.width - fs * 0.6 + 1, out.height - fs * 0.5 + 1);
      octx.fillStyle = 'rgba(255,255,255,.85)';
      octx.fillText('unblurphoto.app · preview', out.width - fs * 0.6, out.height - fs * 0.5);
      out.toBlob(function (b) {
        if (afterUrl) URL.revokeObjectURL(afterUrl);
        afterUrl = URL.createObjectURL(b);
        imgAfter.src = afterUrl;
        dl.href = afterUrl;
        dl.removeAttribute('aria-disabled');
        setStatus(T.done, 1);
      }, 'image/jpeg', 0.9);
      worker.terminate(); worker = null;
    };
    worker.postMessage({ width: data.width, height: data.height, data: data.data, mode: mode, strength: +strength.value, angle: +angle.value }, [data.data.buffer]);
  }

  function schedule() { clearTimeout(timer); timer = setTimeout(run, 350); }

  drop.addEventListener('click', function () { input.click(); });
  drop.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
  input.addEventListener('change', function () { onFile(input.files[0]); input.value = ''; });
  ['dragenter', 'dragover'].forEach(function (t) { drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.add('over'); }); });
  ['dragleave', 'drop'].forEach(function (t) { drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.remove('over'); }); });
  drop.addEventListener('drop', function (e) { onFile(e.dataTransfer.files[0]); });
  document.addEventListener('paste', function (e) {
    var item = [].find.call(e.clipboardData ? e.clipboardData.items : [], function (i) { return i.type.indexOf('image/') === 0; });
    if (item) onFile(item.getAsFile());
  });
  $('[data-sample]').addEventListener('click', function () { useImage(root.dataset.sample); });
  $('[data-new]').addEventListener('click', function () {
    if (worker) worker.terminate();
    source = null; work.hidden = true; drop.hidden = false; start.hidden = false;
    root.scrollIntoView({ block: 'start' });
  });
  root.querySelectorAll('[data-mode]').forEach(function (b) {
    b.addEventListener('click', function () {
      mode = b.dataset.mode;
      root.querySelectorAll('[data-mode]').forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
      angleRow.hidden = mode !== 'motion';
      schedule();
    });
  });
  strength.addEventListener('input', function () { strengthVal.textContent = strength.value; schedule(); });
  angle.addEventListener('input', function () { angleVal.textContent = angle.value + '°'; schedule(); });
  dl.addEventListener('click', function (e) { if (dl.getAttribute('aria-disabled') === 'true') e.preventDefault(); });
})();
