/**
 * Metrics Component for Updating Numeric Telemetry Indicators & Real-Time Activity Log.
 */
import { store } from '../store.js';

export function initMetrics() {
  const elTotal = document.getElementById('metric-total');
  const elIn = document.getElementById('metric-in');
  const elOut = document.getElementById('metric-out');
  const elOccupancy = document.getElementById('metric-occupancy');
  const elFps = document.getElementById('header-fps');
  const elLatency = document.getElementById('header-latency');
  const elSource = document.getElementById('header-source');
  const elModel = document.getElementById('header-model');
  const elStatusDot = document.getElementById('status-dot');
  const elStatusText = document.getElementById('status-text');
  const logList = document.getElementById('activity-log-list');

  let prevIn = 0;
  let prevOut = 0;
  let hasInit = false;

  function addLog(text, type) {
    if (!logList) return;
    const emptyMsg = logList.querySelector('.log-empty');
    if (emptyMsg) emptyMsg.remove();

    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;

    const item = document.createElement('div');
    item.className = `log-item ${type === 'in' ? 'in-event' : 'out-event'}`;
    item.innerHTML = `<span>${text}</span><span class="log-time">${timeStr}</span>`;

    logList.insertBefore(item, logList.firstChild);

    // Batasi log maksimal 15 baris
    while (logList.children.length > 15) {
      logList.removeChild(logList.lastChild);
    }
  }

  store.subscribe('telemetry', (telemetry) => {
    if (elTotal) elTotal.textContent = telemetry.total_count;
    if (elIn) elIn.textContent = telemetry.count_in;
    if (elOut) elOut.textContent = telemetry.count_out;
    if (elOccupancy) elOccupancy.textContent = telemetry.live_occupancy;

    const fpsVal = typeof telemetry.fps === 'number' ? telemetry.fps.toFixed(1) : '0.0';
    const latVal = typeof telemetry.latency_ms === 'number' ? telemetry.latency_ms.toFixed(1) : '0.0';
    if (elFps) elFps.textContent = `${fpsVal} FPS`;
    if (elLatency) elLatency.textContent = `${latVal} ms`;
    if (elSource) elSource.textContent = telemetry.source_name;
    if (elModel) elModel.textContent = telemetry.model_name;

    if (!hasInit) {
      prevIn = telemetry.count_in;
      prevOut = telemetry.count_out;
      hasInit = true;
    } else {
      if (telemetry.count_in > prevIn) {
        const delta = telemetry.count_in - prevIn;
        addLog(`+${delta} Orang Melintas MASUK (IN)`, 'in');
        prevIn = telemetry.count_in;
      }
      if (telemetry.count_out > prevOut) {
        const delta = telemetry.count_out - prevOut;
        addLog(`+${delta} Orang Melintas KELUAR (OUT)`, 'out');
        prevOut = telemetry.count_out;
      }
    }
  });

  store.subscribe('connectionStatus', (status) => {
    if (!elStatusDot || !elStatusText) return;
    if (status === 'connected') {
      elStatusDot.classList.remove('disconnected');
      elStatusText.textContent = 'LIVE';
    } else if (status === 'connecting') {
      elStatusDot.classList.remove('disconnected');
      elStatusText.textContent = 'CONNECTING';
    } else {
      elStatusDot.classList.add('disconnected');
      elStatusText.textContent = 'OFFLINE';
    }
  });
}
