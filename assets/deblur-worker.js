// Browser-side deblur preview. Classic image processing, no AI model:
// Richardson-Lucy deconvolution on luminance with a Gaussian (focus blur)
// or line (motion blur) PSF, or an unsharp mask + contrast curve for text.

function clampIdx(v, max) { return v < 0 ? 0 : v > max ? max : v; }

function gaussKernel(sigma) {
  var r = Math.max(1, Math.ceil(sigma * 3));
  var k = new Float32Array(r * 2 + 1), sum = 0;
  for (var i = -r; i <= r; i++) { k[i + r] = Math.exp(-(i * i) / (2 * sigma * sigma)); sum += k[i + r]; }
  for (i = 0; i < k.length; i++) k[i] /= sum;
  return k;
}

function gaussBlur(src, w, h, k, tmp, dst) {
  var r = (k.length - 1) >> 1, x, y, i, s, row;
  for (y = 0; y < h; y++) {
    row = y * w;
    for (x = 0; x < w; x++) {
      s = 0;
      for (i = -r; i <= r; i++) s += src[row + clampIdx(x + i, w - 1)] * k[i + r];
      tmp[row + x] = s;
    }
  }
  for (y = 0; y < h; y++) {
    for (x = 0; x < w; x++) {
      s = 0;
      for (i = -r; i <= r; i++) s += tmp[clampIdx(y + i, h - 1) * w + x] * k[i + r];
      dst[y * w + x] = s;
    }
  }
  return dst;
}

function lineTaps(len, angleDeg) {
  var n = Math.max(3, Math.round(len)), a = angleDeg * Math.PI / 180, taps = [];
  for (var k = 0; k < n; k++) {
    var t = (k / (n - 1) - 0.5) * len;
    taps.push([t * Math.cos(a), t * Math.sin(a)]);
  }
  return taps;
}

function lineBlur(src, w, h, taps, dst) {
  var n = taps.length, inv = 1 / n, x, y, k, sx, sy, x0, y0, fx, fy, x1, y1, s;
  for (y = 0; y < h; y++) {
    for (x = 0; x < w; x++) {
      s = 0;
      for (k = 0; k < n; k++) {
        sx = x + taps[k][0]; sy = y + taps[k][1];
        x0 = Math.floor(sx); y0 = Math.floor(sy); fx = sx - x0; fy = sy - y0;
        x1 = clampIdx(x0 + 1, w - 1); y1 = clampIdx(y0 + 1, h - 1);
        x0 = clampIdx(x0, w - 1); y0 = clampIdx(y0, h - 1);
        s += (src[y0 * w + x0] * (1 - fx) + src[y0 * w + x1] * fx) * (1 - fy) +
             (src[y1 * w + x0] * (1 - fx) + src[y1 * w + x1] * fx) * fy;
      }
      dst[y * w + x] = s * inv;
    }
  }
  return dst;
}

// Both PSFs are symmetric, so the adjoint equals the forward blur.
function richardsonLucy(obs, w, h, blur, iters, progress) {
  var n = w * h, est = new Float32Array(obs), conv = new Float32Array(n), ratio = new Float32Array(n), corr = new Float32Array(n), i, it, r;
  for (it = 0; it < iters; it++) {
    blur(est, conv);
    for (i = 0; i < n; i++) {
      r = obs[i] / (conv[i] + 1e-3);
      ratio[i] = r < 0.4 ? 0.4 : r > 2.5 ? 2.5 : r; // damping limits ringing
    }
    blur(ratio, corr);
    for (i = 0; i < n; i++) est[i] *= corr[i];
    progress((it + 1) / iters);
  }
  return est;
}

function unsharp(src, w, h, sigma, amount) {
  var n = w * h, k = gaussKernel(sigma), tmp = new Float32Array(n), low = new Float32Array(n), out = new Float32Array(n);
  gaussBlur(src, w, h, k, tmp, low);
  for (var i = 0; i < n; i++) out[i] = src[i] + (src[i] - low[i]) * amount;
  return out;
}

self.onmessage = function (e) {
  var d = e.data, w = d.width, h = d.height, px = d.data, n = w * h, i;
  var Y = new Float32Array(n), Cb = new Float32Array(n), Cr = new Float32Array(n);
  for (i = 0; i < n; i++) {
    var r = px[i * 4], g = px[i * 4 + 1], b = px[i * 4 + 2];
    var yv = 0.299 * r + 0.587 * g + 0.114 * b;
    Y[i] = yv + 1; Cb[i] = b - yv; Cr[i] = r - yv;
  }
  var s = d.strength / 100, out;
  function progress(p) { self.postMessage({ type: 'progress', value: p }); }

  if (d.mode === 'text') {
    out = unsharp(Y, w, h, 1.0 + s * 1.5, 0.8 + s * 2.2);
    progress(0.6);
    var lo = 255, hi = 0;
    for (i = 0; i < n; i++) { if (out[i] < lo) lo = out[i]; if (out[i] > hi) hi = out[i]; }
    // Stretch contrast a little so faint print becomes readable.
    var mid = (lo + hi) / 2, gain = 1 + s * 0.5;
    for (i = 0; i < n; i++) out[i] = mid + (out[i] - mid) * gain;
    progress(1);
  } else {
    var blur, iters = 12;
    if (d.mode === 'motion') {
      var taps = lineTaps(3 + s * 27, d.angle || 0);
      blur = function (src, dst) { return lineBlur(src, w, h, taps, dst); };
      iters = 10;
    } else {
      var k = gaussKernel(0.6 + s * 3.4), tmp = new Float32Array(n);
      blur = function (src, dst) { return gaussBlur(src, w, h, k, tmp, dst); };
    }
    out = richardsonLucy(Y, w, h, blur, iters, progress);
    out = unsharp(out, w, h, 0.8, 0.25);
  }

  var res = new Uint8ClampedArray(n * 4);
  for (i = 0; i < n; i++) {
    var yy = out[i] - 1, rr = yy + Cr[i], bb = yy + Cb[i];
    res[i * 4] = rr;
    res[i * 4 + 1] = (yy - 0.299 * rr - 0.114 * bb) / 0.587;
    res[i * 4 + 2] = bb;
    res[i * 4 + 3] = 255;
  }
  self.postMessage({ type: 'done', width: w, height: h, data: res }, [res.buffer]);
};
