/**
 * Interactive Drag-and-Drop & Polygon Drawing Handler.
 */
import { store } from '../store.js';
import { restClient } from '../network/rest_client.js';

export class CanvasInteraction {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.isDragging = false;
    this.dragTarget = null; // 'line_start' | 'line_end' | 'line_new'
    this.tempStart = null;
    this.tempEnd = null;

    this.bindEvents();
  }

  getNormalizedPos(e) {
    const rect = this.canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const x = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
    const y = Math.max(0, Math.min(1, (clientY - rect.top) / rect.height));
    return { x: Number(x.toFixed(4)), y: Number(y.toFixed(4)) };
  }

  bindEvents() {
    const onStart = (e) => {
      const { mode, line } = store.getState();
      const pos = this.getNormalizedPos(e);

      if (mode === 'draw_line') {
        this.isDragging = true;
        this.tempStart = pos;
        this.tempEnd = pos;
      } else if (mode === 'draw_roi') {
        const { roiDraftPoints } = store.getState();
        const updated = [...roiDraftPoints, pos];
        store.setState({ roiDraftPoints: updated });
      } else {
        // Cek apakah mengklik handle garis yang sudah ada
        const dStart = Math.hypot(pos.x - line.start.x, pos.y - line.start.y);
        const dEnd = Math.hypot(pos.x - line.end.x, pos.y - line.end.y);
        if (dStart < 0.05) {
          this.isDragging = true;
          this.dragTarget = 'line_start';
        } else if (dEnd < 0.05) {
          this.isDragging = true;
          this.dragTarget = 'line_end';
        }
      }
    };

    const onMove = (e) => {
      if (!this.isDragging) return;
      const pos = this.getNormalizedPos(e);
      const { mode, line } = store.getState();

      if (mode === 'draw_line') {
        this.tempEnd = pos;
      } else if (this.dragTarget === 'line_start') {
        store.setState({ line: { ...line, start: pos } });
      } else if (this.dragTarget === 'line_end') {
        store.setState({ line: { ...line, end: pos } });
      }
    };

    const onEnd = async () => {
      if (!this.isDragging) return;
      this.isDragging = false;
      const { mode, line } = store.getState();

      if (mode === 'draw_line' && this.tempStart && this.tempEnd) {
        const dist = Math.hypot(this.tempEnd.x - this.tempStart.x, this.tempEnd.y - this.tempStart.y);
        if (dist > 0.03) {
          store.setState({
            mode: 'idle',
            line: { start: this.tempStart, end: this.tempEnd, orientation: 'custom' }
          });
          await restClient.updateLine(this.tempStart, this.tempEnd, 'custom');
        }
        this.tempStart = null;
        this.tempEnd = null;
      } else if (this.dragTarget) {
        await restClient.updateLine(line.start, line.end, line.orientation);
        this.dragTarget = null;
      }
    };

    this.canvas.addEventListener('mousedown', onStart);
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onEnd);

    this.canvas.addEventListener('touchstart', onStart, { passive: true });
    window.addEventListener('touchmove', onMove, { passive: true });
    window.addEventListener('touchend', onEnd);
  }
}
