/**
 * High-Performance Layered Canvas Renderer.
 */
import { store } from '../store.js';

export class CanvasEngine {
  constructor(canvasElement) {
    this.canvas = canvasElement;
    this.ctx = this.canvas.getContext('2d');
    this.animationFrameId = null;

    this.resize();
    window.addEventListener('resize', () => this.resize());
    this.startLoop();
  }

  resize() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    if (this.canvas.width !== rect.width || this.canvas.height !== rect.height) {
      this.canvas.width = rect.width;
      this.canvas.height = rect.height;
    }
  }

  startLoop() {
    const render = () => {
      this.render();
      this.animationFrameId = requestAnimationFrame(render);
    };
    render();
  }

  stopLoop() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
  }

  render() {
    const w = this.canvas.width;
    const h = this.canvas.height;
    const ctx = this.ctx;
    const state = store.getState();

    ctx.clearRect(0, 0, w, h);

    // 1. Gambar Zona RoI
    if (state.roi.enabled && state.roi.points.length >= 3) {
      this.drawPolygon(ctx, state.roi.points, w, h, 'rgba(56, 189, 248, 0.12)', '#38bdf8');
    }

    // 2. Gambar Draft RoI jika dalam mode gambar
    if (state.mode === 'draw_roi' && state.roiDraftPoints.length > 0) {
      this.drawPolygon(ctx, state.roiDraftPoints, w, h, 'rgba(245, 158, 11, 0.15)', '#f59e0b', true);
      // Gambar titik-titik sudut
      state.roiDraftPoints.forEach((pt, i) => {
        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(pt.x * w, pt.y * h, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.font = '11px monospace';
        ctx.fillText(`P${i+1}`, pt.x * w + 8, pt.y * h - 4);
      });
    }

    // 3. Gambar Garis Virtual Counting
    const { line } = state;
    if (line && line.start && line.end) {
      const p1x = line.start.x * w;
      const p1y = line.start.y * h;
      const p2x = line.end.x * w;
      const p2y = line.end.y * h;

      // Garis utama amber tegas
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(p1x, p1y);
      ctx.lineTo(p2x, p2y);
      ctx.stroke();

      // Handle titik awal & akhir
      this.drawHandle(ctx, p1x, p1y, '#f59e0b');
      this.drawHandle(ctx, p2x, p2y, '#f59e0b');

      // Teks label garis
      const midX = (p1x + p2x) / 2;
      const midY = (p1y + p2y) / 2;
      ctx.fillStyle = '#f59e0b';
      ctx.font = '11px monospace';
      ctx.fillText('GARIS COUNTING', midX + 8, midY - 6);
    }

    // 4. Petunjuk mode aktif di pojok canvas
    if (state.mode === 'draw_line') {
      this.drawModeBadge(ctx, 'MODE: TARIK GARIS (Klik & Seret di Layar)');
    } else if (state.mode === 'draw_roi') {
      this.drawModeBadge(ctx, 'MODE: GAMBAR RoI (Klik titik-titik poligon. Klik tombol Selesai jika sudah)');
    }
  }

  drawHandle(ctx, x, y, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }

  drawPolygon(ctx, points, w, h, fillStyle, strokeStyle, isDraft = false) {
    if (points.length < 2) return;
    ctx.fillStyle = fillStyle;
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = isDraft ? 1.5 : 2;
    if (isDraft) ctx.setLineDash([4, 4]);
    else ctx.setLineDash([]);

    ctx.beginPath();
    ctx.moveTo(points[0].x * w, points[0].y * h);
    for (let i = 1; i < points.length; i++) {
      ctx.lineTo(points[i].x * w, points[i].y * h);
    }
    if (!isDraft || points.length >= 3) {
      ctx.closePath();
      ctx.fill();
    }
    ctx.stroke();
    ctx.setLineDash([]);
  }

  drawModeBadge(ctx, text) {
    ctx.fillStyle = '#18181b';
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 1;
    ctx.fillRect(12, 12, 380, 26);
    ctx.strokeRect(12, 12, 380, 26);
    ctx.fillStyle = '#f4f4f5';
    ctx.font = '11px sans-serif';
    ctx.fillText(text, 20, 29);
  }
}
