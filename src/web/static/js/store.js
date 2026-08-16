/**
 * Reactive State Store with Publisher-Subscriber Pattern.
 */
class StateStore {
  constructor() {
    this.state = {
      mode: 'idle', // 'idle' | 'draw_line' | 'draw_roi'
      connectionStatus: 'connecting', // 'connecting' | 'connected' | 'disconnected'
      telemetry: {
        fps: 0,
        latency_ms: 0,
        total_count: 0,
        count_in: 0,
        count_out: 0,
        live_occupancy: 0,
        source_name: 'Menghubungkan...',
        model_name: 'YOLO26-S + Deep-OC-SORT',
        recent_traffic: []
      },
      line: {
        start: { x: 0.33, y: 0.0 },
        end: { x: 0.33, y: 1.0 },
        orientation: 'v'
      },
      roi: {
        enabled: false,
        points: []
      },
      roiDraftPoints: []
    };
    this.listeners = new Map();
  }

  getState() {
    return this.state;
  }

  setState(partialState) {
    const prevState = { ...this.state };
    this.state = { ...this.state, ...partialState };

    // Notifikasi listener jika key tertentu berubah
    for (const [key, value] of Object.entries(partialState)) {
      if (this.listeners.has(key)) {
        this.listeners.get(key).forEach(cb => cb(value, prevState[key], this.state));
      }
    }

    if (this.listeners.has('*')) {
      this.listeners.get('*').forEach(cb => cb(this.state, prevState));
    }
  }

  subscribe(key, callback) {
    if (!this.listeners.has(key)) {
      this.listeners.set(key, new Set());
    }
    this.listeners.get(key).add(callback);
    return () => this.listeners.get(key).delete(callback);
  }
}

export const store = new StateStore();
