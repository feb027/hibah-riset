/**
 * Toolbar Actions & Camera Stream Controller (Optimized Anti-Stutter & True Aspect Ratio).
 */
import { store } from '../store.js';
import { restClient } from '../network/rest_client.js';

export function initToolbar() {
  const btnDrawLine = document.getElementById('btn-draw-line');
  const btnDrawRoi = document.getElementById('btn-draw-roi');
  const btnFinishRoi = document.getElementById('btn-finish-roi');
  const btnClearRoi = document.getElementById('btn-clear-roi');
  const btnFlipDirection = document.getElementById('btn-flip-direction');
  const btnReset = document.getElementById('btn-reset');
  const btnToggleStream = document.getElementById('btn-toggle-stream');
  const btnToggleStreamText = document.getElementById('btn-toggle-stream-text');
  const btnChangeSource = document.getElementById('btn-change-source');

  const videoImg = document.getElementById('video-player-img');
  let isStreamRunning = true;

  // Modal elements
  const modalSource = document.getElementById('modal-source');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const btnApplySource = document.getElementById('btn-apply-source');
  const selectSourceType = document.getElementById('select-source-type');
  const inputSourceUri = document.getElementById('input-source-uri');

  // 1. Jeda / Nyalakan Video Stream
  if (btnToggleStream) {
    btnToggleStream.addEventListener('click', async () => {
      isStreamRunning = !isStreamRunning;
      if (!isStreamRunning) {
        if (btnToggleStreamText) btnToggleStreamText.textContent = 'Nyalakan';
        btnToggleStream.classList.add('active');
        if (videoImg) videoImg.src = '';
        await restClient.triggerAction('pause');
      } else {
        if (btnToggleStreamText) btnToggleStreamText.textContent = 'Jeda Video';
        btnToggleStream.classList.remove('active');
        if (videoImg) videoImg.src = `/api/stream/video_feed?t=${Date.now()}`;
        await restClient.triggerAction('resume');
      }
    });
  }

  // 2. Mode: Tarik Garis
  if (btnDrawLine) {
    btnDrawLine.addEventListener('click', () => {
      const curMode = store.getState().mode;
      const newMode = curMode === 'draw_line' ? 'idle' : 'draw_line';
      store.setState({ mode: newMode, roiDraftPoints: [] });
    });
  }

  // 3. Mode: Gambar RoI
  if (btnDrawRoi) {
    btnDrawRoi.addEventListener('click', () => {
      const curMode = store.getState().mode;
      const newMode = curMode === 'draw_roi' ? 'idle' : 'draw_roi';
      store.setState({ mode: newMode, roiDraftPoints: [] });
    });
  }

  // 4. Selesai Gambar RoI
  if (btnFinishRoi) {
    btnFinishRoi.addEventListener('click', async () => {
      const { roiDraftPoints } = store.getState();
      if (roiDraftPoints.length >= 3) {
        store.setState({
          mode: 'idle',
          roi: { enabled: true, points: roiDraftPoints },
          roiDraftPoints: []
        });
        await restClient.updateRoi(roiDraftPoints, true);
      } else {
        alert('Minimal tentukan 3 titik sudut poligon untuk RoI');
      }
    });
  }

  // 5. Hapus RoI
  if (btnClearRoi) {
    btnClearRoi.addEventListener('click', async () => {
      store.setState({
        mode: 'idle',
        roi: { enabled: false, points: [] },
        roiDraftPoints: []
      });
      await restClient.updateRoi([], false);
    });
  }

  // 6. Balik Arah
  if (btnFlipDirection) {
    btnFlipDirection.addEventListener('click', async () => {
      await restClient.triggerAction('flip_direction');
    });
  }

  // 7. Reset Hitungan
  if (btnReset) {
    btnReset.addEventListener('click', async () => {
      if (confirm('Reset seluruh hitungan IN/OUT ke 0?')) {
        await restClient.triggerAction('reset');
      }
    });
  }

  // 8. Sinkronisasi status aktif tombol dengan mode store
  store.subscribe('mode', (mode) => {
    if (btnDrawLine) btnDrawLine.classList.toggle('active', mode === 'draw_line');
    if (btnDrawRoi) btnDrawRoi.classList.toggle('active', mode === 'draw_roi');
    if (btnFinishRoi) btnFinishRoi.style.display = mode === 'draw_roi' ? 'inline-flex' : 'none';
  });

  // 9. Streaming Kamera Browser / HP Teroptimasi (Anti-Gepeng & Anti-Patah-Patah)
  let clientCameraStream = null;
  let isCameraActive = false;

  async function startClientCamera() {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert(
          'Browser HP memblokir kamera jika dibuka via HTTP biasa.\n\n' +
          'SOLUSI PILIHAN:\n' +
          '1. Buka via HTTPS: https://100.108.28.69:8050\n' +
          '2. ATAU gunakan aplikasi "IP Webcam" di HP, lalu masukkan URL streaming (http://100.x.x.x:8080/video) di menu RTSP / IP Camera.'
        );
        return false;
      }

      if (clientCameraStream) {
        clientCameraStream.getTracks().forEach(t => t.stop());
      }
      isCameraActive = false;

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: { ideal: 'environment' }
        },
        audio: false
      });
      clientCameraStream = stream;
      isCameraActive = true;

      const hiddenVideo = document.createElement('video');
      hiddenVideo.srcObject = stream;
      hiddenVideo.muted = true;
      hiddenVideo.playsInline = true;
      await hiddenVideo.play();

      const offscreenCanvas = document.createElement('canvas');
      const offCtx = offscreenCanvas.getContext('2d');

      await restClient.changeSource('client_upload', 'Kamera Browser / HP');

      // Loop adaptif berurutan (Sequential Async Loop) untuk mencegah penumpukan paket jaringan
      let isUploading = false;

      async function uploadFrameLoop() {
        if (!isCameraActive) return;

        if (hiddenVideo.readyState >= 2 && !isUploading) {
          const naturalW = hiddenVideo.videoWidth || 640;
          const naturalH = hiddenVideo.videoHeight || 480;

          // Jaga rasio aspek alami tanpa distorsi gepeng (Max resolusi 640px)
          const maxDim = 640;
          let targetW = naturalW;
          let targetH = naturalH;
          if (naturalW > maxDim || naturalH > maxDim) {
            if (naturalW >= naturalH) {
              targetW = maxDim;
              targetH = Math.round((naturalH * maxDim) / naturalW);
            } else {
              targetH = maxDim;
              targetW = Math.round((naturalW * maxDim) / naturalH);
            }
          }

          if (offscreenCanvas.width !== targetW || offscreenCanvas.height !== targetH) {
            offscreenCanvas.width = targetW;
            offscreenCanvas.height = targetH;
          }

          offCtx.drawImage(hiddenVideo, 0, 0, targetW, targetH);
          isUploading = true;

          offscreenCanvas.toBlob(async (blob) => {
            if (blob && isCameraActive) {
              try {
                await fetch('/api/stream/upload_frame', {
                  method: 'POST',
                  body: blob
                });
              } catch (e) {}
            }
            isUploading = false;
            if (isCameraActive) setTimeout(uploadFrameLoop, 25);
          }, 'image/jpeg', 0.65);
        } else {
          if (isCameraActive) setTimeout(uploadFrameLoop, 30);
        }
      }

      uploadFrameLoop();

      if (videoImg) {
        videoImg.src = `/api/stream/video_feed?t=${Date.now()}`;
      }
      return true;
    } catch (err) {
      console.error('Gagal membuka kamera:', err);
      alert('Gagal membuka kamera perangkat: ' + (err.message || err.name));
      return false;
    }
  }

  // 10. Modal Sumber Video
  if (btnChangeSource && modalSource) {
    btnChangeSource.addEventListener('click', () => {
      modalSource.classList.remove('hidden');
    });
  }

  if (btnCloseModal && modalSource) {
    btnCloseModal.addEventListener('click', () => {
      modalSource.classList.add('hidden');
    });
  }

  if (btnApplySource && modalSource) {
    btnApplySource.addEventListener('click', async () => {
      const sType = selectSourceType.value;
      let sUri = inputSourceUri.value.trim();

      if (sType === 'client_camera') {
        const ok = await startClientCamera();
        if (ok && modalSource) modalSource.classList.add('hidden');
        return;
      }

      // Jika beralih dari kamera client ke server, hentikan streaming client
      if (clientCameraStream) {
        clientCameraStream.getTracks().forEach(t => t.stop());
        clientCameraStream = null;
        isCameraActive = false;
      }

      if (sType === 'webcam' && !sUri) sUri = '0';

      const res = await restClient.changeSource(sType, sUri);
      if (res && res.status === 'success') {
        modalSource.classList.add('hidden');
        if (videoImg) {
          videoImg.src = `/api/stream/video_feed?t=${Date.now()}`;
        }
      } else {
        alert('Gagal mengganti sumber video. Pastikan path / URL valid.');
      }
    });
  }
}
