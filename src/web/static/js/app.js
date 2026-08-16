/**
 * Main Application Bootstrap.
 */
import { store } from './store.js';
import { wsClient } from './network/ws_client.js';
import { restClient } from './network/rest_client.js';
import { CanvasEngine } from './canvas/engine.js';
import { CanvasInteraction } from './canvas/interaction.js';
import { initMetrics } from './components/metrics.js';
import { initTrafficChart } from './components/chart.js';
import { initToolbar } from './components/toolbar.js';

document.addEventListener('DOMContentLoaded', async () => {
  console.log('[App] Inisialisasi People Counting Dashboard...');

  // 1. Inisialisasi Komponen UI
  initMetrics();
  initTrafficChart();
  initToolbar();

  // 2. Inisialisasi Canvas
  const canvasEl = document.getElementById('canvas-overlay');
  if (canvasEl) {
    new CanvasEngine(canvasEl);
    new CanvasInteraction(canvasEl);
  }

  // 3. Muat Konfigurasi Awal dari REST API
  const config = await restClient.getConfig();
  if (config) {
    store.setState({
      line: config.line,
      roi: config.roi,
    });
  }

  // 4. Hubungkan WebSocket Telemetri
  wsClient.connect();
});
