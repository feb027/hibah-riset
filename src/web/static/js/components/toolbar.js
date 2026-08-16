/**
 * Toolbar Actions & Modal Controllers.
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
  const videoImg = document.getElementById('video-player-img');
  let isStreamRunning = true;

  // Jeda / Nyalakan Video Stream
  if (btnToggleStream) {
    btnToggleStream.addEventListener('click', async () => {
      isStreamRunning = !isStreamRunning;
      if (!isStreamRunning) {
        if (btnToggleStreamText) btnToggleStreamText.textContent = 'Nyalakan Video';
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

  // Mode: Tarik Garis
  const modalSource = document.getElementById('modal-source');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const btnApplySource = document.getElementById('btn-apply-source');
  const selectSourceType = document.getElementById('select-source-type');
  const inputSourceUri = document.getElementById('input-source-uri');

  // Mode: Tarik Garis
  if (btnDrawLine) {
    btnDrawLine.addEventListener('click', () => {
      const curMode = store.getState().mode;
      const newMode = curMode === 'draw_line' ? 'idle' : 'draw_line';
      store.setState({ mode: newMode, roiDraftPoints: [] });
    });
  }

  // Mode: Gambar RoI
  if (btnDrawRoi) {
    btnDrawRoi.addEventListener('click', () => {
      const curMode = store.getState().mode;
      const newMode = curMode === 'draw_roi' ? 'idle' : 'draw_roi';
      store.setState({ mode: newMode, roiDraftPoints: [] });
    });
  }

  // Selesai Gambar RoI
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

  // Hapus RoI
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

  // Balik Arah
  if (btnFlipDirection) {
    btnFlipDirection.addEventListener('click', async () => {
      await restClient.triggerAction('flip_direction');
    });
  }

  // Reset Hitungan
  if (btnReset) {
    btnReset.addEventListener('click', async () => {
      if (confirm('Reset seluruh hitungan IN/OUT ke 0?')) {
        await restClient.triggerAction('reset');
      }
    });
  }

  // Sinkronisasi status aktif tombol dengan mode store
  store.subscribe('mode', (mode) => {
    if (btnDrawLine) btnDrawLine.classList.toggle('active', mode === 'draw_line');
    if (btnDrawRoi) btnDrawRoi.classList.toggle('active', mode === 'draw_roi');
    if (btnFinishRoi) btnFinishRoi.style.display = mode === 'draw_roi' ? 'inline-flex' : 'none';
  });

  // Modal Sumber Video
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
      if (sType === 'webcam' && !sUri) sUri = '0';

      const res = await restClient.changeSource(sType, sUri);
      if (res && res.status === 'success') {
        modalSource.classList.add('hidden');
        // Refresh video image player feed
        const videoImg = document.getElementById('video-player-img');
        if (videoImg) {
          videoImg.src = `/api/stream/video_feed?t=${Date.now()}`;
        }
      } else {
        alert('Gagal mengganti sumber video. Pastikan path / URL valid.');
      }
    });
  }
}
