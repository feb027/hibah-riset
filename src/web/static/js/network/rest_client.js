/**
 * REST API Client for System Mutations.
 */
export class RestClient {
  constructor(baseUrl = '') {
    this.baseUrl = baseUrl;
  }

  async getConfig() {
    try {
      const res = await fetch(`${this.baseUrl}/api/config`);
      if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
      return await res.json();
    } catch (err) {
      console.error('[RestClient] Gagal memuat config:', err);
      return null;
    }
  }

  async updateLine(start, end, orientation = 'custom') {
    try {
      const res = await fetch(`${this.baseUrl}/api/config/line`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start, end, orientation })
      });
      return await res.json();
    } catch (err) {
      console.error('[RestClient] Gagal update garis:', err);
      return null;
    }
  }

  async updateRoi(points, enabled = true) {
    try {
      const res = await fetch(`${this.baseUrl}/api/config/roi`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ points, enabled })
      });
      return await res.json();
    } catch (err) {
      console.error('[RestClient] Gagal update RoI:', err);
      return null;
    }
  }

  async triggerAction(action) {
    try {
      const res = await fetch(`${this.baseUrl}/api/control/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action })
      });
      return await res.json();
    } catch (err) {
      console.error(`[RestClient] Gagal aksi '${action}':`, err);
      return null;
    }
  }

  async changeSource(sourceType, uri) {
    try {
      const res = await fetch(`${this.baseUrl}/api/control/source`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source_type: sourceType, uri })
      });
      return await res.json();
    } catch (err) {
      console.error('[RestClient] Gagal ganti sumber:', err);
      return null;
    }
  }
}

export const restClient = new RestClient();
