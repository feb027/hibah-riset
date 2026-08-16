/**
 * Metrics Component for Updating Numeric Telemetry Indicators.
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

  store.subscribe('telemetry', (telemetry) => {
    if (elTotal) elTotal.textContent = telemetry.total_count;
    if (elIn) elIn.textContent = telemetry.count_in;
    if (elOut) elOut.textContent = telemetry.count_out;
    if (elOccupancy) elOccupancy.textContent = telemetry.live_occupancy;
    if (elFps) elFps.textContent = `${telemetry.fps} FPS`;
    if (elLatency) elLatency.textContent = `${telemetry.latency_ms} ms`;
    if (elSource) elSource.textContent = telemetry.source_name;
    if (elModel) elModel.textContent = telemetry.model_name;
  });

  store.subscribe('connectionStatus', (status) => {
    if (!elStatusDot || !elStatusText) return;
    if (status === 'connected') {
      elStatusDot.classList.remove('disconnected');
      elStatusText.textContent = 'TERHUBUNG';
    } else if (status === 'connecting') {
      elStatusDot.classList.remove('disconnected');
      elStatusText.textContent = 'MENGHUBUNGKAN';
    } else {
      elStatusDot.classList.add('disconnected');
      elStatusText.textContent = 'TERPUTUS';
    }
  });
}
