/**
 * Interactive Drag-and-Drop & Polygon Drawing Handler (Live Visual Feedback & Touch-Optimized).
 */
import { store } from '../store.js';
import { restClient } from '../network/rest_client.js';
import { getVideoRenderBox } from './engine.js';

export class CanvasInteraction {
  constructor(canvas) {
    this.canvas = canvas;
    this.isDragging = false;
    this.dragTarget = null;
    this.tempStart = null;
    this.tempEnd = null;

    this.bindEvents();
  }

  getNormalizedPos(e) {
    const rect = this.canvas.getBoundingClientRect();
    const clientX = e.touches && e.touches.length > 0 ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches && e.touches.length > 0 ? e.touches[0].clientY : e.clientY;
    const rawX = clientX - rect.left;
    const rawY = clientY - rect.top;

    const box = getVideoRenderBox(this.canvas);
    const x = Math.max(0, Math.min(1, (rawX - box.x) / box.w));
    const y = Math.max(0, Math.min(1, (rawY - box.y) / box.h));
    return { x: Number(x.toFixed(4)), y: Number(y.toFixed(4)) };
  }

  bindEvents() {
    const onStart = (e) => {
      const { mode, line } = store.getState();
      const pos = this.getNormalizedPos(e);

      if (mode === 'draw_line') {
        if (e.cancelable) e.preventDefault();
        this.isDragging = true;
        this.tempStart = pos;
        this.tempEnd = pos;
        store.setState({ lineDraft: { start: pos, end: pos } });
      } else if (mode === 'draw_roi') {
        if (e.cancelable) e.preventDefault();
        const { roiDraftPoints } = store.getState();
        const updated = [...roiDraftPoints, pos];
        store.setState({ roiDraftPoints: updated });
      } else {
        // Cek klik/sentuh handle garis
        const dStart = Math.hypot(pos.x - line.start.x, pos.y - line.start.y);
        const dEnd = Math.hypot(pos.x - line.end.x, pos.y - line.end.y);
        if (dStart < 0.09) {
          if (e.cancelable) e.preventDefault();
          this.isDragging = true;
          this.dragTarget = 'line_start';
        } else if (dEnd < 0.09) {
          if (e.cancelable) e.preventDefault();
          this.isDragging = true;
          this.dragTarget = 'line_end';
        }
      }
    };

    const onMove = (e) => {
      if (!this.isDragging) return;
      if (e.cancelable) e.preventDefault();
      const pos = this.getNormalizedPos(e);
      const { mode, line } = store.getState();

      if (mode === 'draw_line') {
        this.tempEnd = pos;
        store.setState({ lineDraft: { start: this.tempStart, end: pos } });
      } else if (this.dragTarget === 'line_start') {
        store.setState({ line: { ...line, start: pos } });
      } else if (this.dragTarget === 'line_end') {
        store.setState({ line: { ...line, end: pos } });
      }
    };

    const onEnd = async (e) => {
      if (!this.isDragging) return;
      if (e && e.cancelable) e.preventDefault();
      this.isDragging = false;
      const { mode, line } = store.getState();

      if (mode === 'draw_line' && this.tempStart && this.tempEnd) {
        const dist = Math.hypot(this.tempEnd.x - this.tempStart.x, this.tempEnd.y - this.tempStart.y);
        if (dist > 0.02) {
          const newLine = { start: this.tempStart, end: this.tempEnd, orientation: 'custom' };
          store.setState({
            mode: 'idle',
            line: newLine,
            lineDraft: null
          });
          await restClient.updateLine(this.tempStart, this.tempEnd, 'custom');
        } else {
          store.setState({ lineDraft: null });
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

    this.canvas.addEventListener('touchstart', onStart, { passive: false });
    window.addEventListener('touchmove', onMove, { passive: false });
    window.addEventListener('touchend', onEnd);
    window.addEventListener('touchcancel', onEnd);
  }
}
