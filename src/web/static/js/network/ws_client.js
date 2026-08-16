/**
 * WebSocket Telemetry Client with Heartbeat & Automatic Reconnection.
 */
import { store } from '../store.js';

export class WsClient {
  constructor(path = '/ws/telemetry') {
    this.path = path;
    this.ws = null;
    this.reconnectTimer = null;
    this.isExplicitlyClosed = false;
  }

  connect() {
    this.isExplicitlyClosed = false;
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}${this.path}`;

    store.setState({ connectionStatus: 'connecting' });

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('[WsClient] Terhubung ke telemetry hub');
        store.setState({ connectionStatus: 'connected' });
        if (this.reconnectTimer) {
          clearTimeout(this.reconnectTimer);
          this.reconnectTimer = null;
        }
      };

      this.ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          store.setState({
            telemetry: {
              fps: payload.fps,
              latency_ms: payload.latency_ms,
              total_count: payload.total_count,
              count_in: payload.count_in,
              count_out: payload.count_out,
              live_occupancy: payload.live_occupancy,
              source_name: payload.source_name,
              model_name: payload.model_name,
              recent_traffic: payload.recent_traffic || []
            },
            line: payload.line || store.getState().line,
            roi: payload.roi || store.getState().roi
          });
        } catch (err) {
          console.error('[WsClient] Gagal parsing telemetry JSON:', err);
        }
      };

      this.ws.onclose = () => {
        store.setState({ connectionStatus: 'disconnected' });
        if (!this.isExplicitlyClosed) {
          console.warn('[WsClient] Terputus. Menghubungkan kembali dalam 2 detik...');
          this.reconnectTimer = setTimeout(() => this.connect(), 2000);
        }
      };

      this.ws.onerror = (err) => {
        console.error('[WsClient] WebSocket error:', err);
        store.setState({ connectionStatus: 'disconnected' });
      };
    } catch (err) {
      console.error('[WsClient] Gagal inisialisasi WebSocket:', err);
      store.setState({ connectionStatus: 'disconnected' });
      this.reconnectTimer = setTimeout(() => this.connect(), 2000);
    }
  }

  disconnect() {
    this.isExplicitlyClosed = true;
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export const wsClient = new WsClient();
