/**
 * High-Performance Layered Canvas Renderer (Live Line Preview & Letterbox Aware).
 */
import { store } from '../store.js';

export function getVideoRenderBox(canvas) {
  const videoImg = document.getElementById('video-player-img');
  const w = canvas.width;
  const h = canvas.height;
  if (!videoImg || !videoImg.naturalWidth || !videoImg.naturalHeight) {
    return { x: 0, y: 0, w, h };
  }

  const naturalRatio = videoImg.naturalWidth / videoImg.naturalHeight;
  const canvasRatio = w / h;

  let renderW, renderH, offsetX, offsetY;
  if (naturalRatio > canvasRatio) {
    renderW = w;
    renderH = w / naturalRatio;
    offsetX = 0;
    offsetY = (h - renderH) / 2;
  } else {
    renderH = h;
    renderW = h * naturalRatio;
    offsetX = (w - renderW) / 2;
    offsetY = 0;
  }
  return { x: offsetX, y: offsetY, w: renderW, h: renderH };
}

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
    if (this.canvas.width !== Math.round(rect.width) || this.canvas.height !== Math.round(rect.height)) {
      this.canvas.width = Math.round(rect.width);
      this.canvas.height = Math.round(rect.height);
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

    const box = getVideoRenderBox(this.canvas);

    // 1. Gambar Zona RoI Aktif
    if (state.roi && state.roi.enabled && state.roi.points.length >= 3) {
      this.drawPolygon(ctx, state.roi.points, box, 'rgba(56, 189, 248, 0.12)', '#38bdf8');
    }

    // 2. Gambar Draft RoI jika sedang dalam mode penarikan
    if (state.mode === 'draw_roi' && state.roiDraftPoints.length > 0) {
      this.drawPolygon(ctx, state.roiDraftPoints, box, 'rgba(245, 158, 11, 0.15)', '#f59e0b', true);
      state.roiDraftPoints.forEach((pt, i) => {
        const px = box.x + pt.x * box.w;
        const py = box.y + pt.y * box.h;
        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(px, py, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.font = '10px monospace';
        ctx.fillText(`P${i+1}`, px + 8, py - 4);
      });
    }

    // 3. Gambar Garis Live Saat Ditarik (Line Draft Preview)
    if (state.lineDraft && state.lineDraft.start && state.lineDraft.end) {
      const p1x = box.x + state.lineDraft.start.x * box.w;
      const p1y = box.y + state.lineDraft.start.y * box.h;
      const p2x = box.x + state.lineDraft.end.x * box.w;
      const p2y = box.y + state.lineDraft.end.y * box.h;

      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 3;
      ctx.setLineDash([6, 4]);
      ctx.beginPath();
      ctx.moveTo(p1x, p1y);
      ctx.lineTo(p2x, p2y);
      ctx.stroke();
      ctx.setLineDash([]);

      this.drawHandle(ctx, p1x, p1y, '#10b981');
      this.drawHandle(ctx, p2x, p2y, '#10b981');

      const midX = (p1x + p2x) / 2;
      const midY = (p1y + p2y) / 2;
      ctx.fillStyle = '#10b981';
      ctx.font = '11px monospace';
      ctx.fillText('LEPASKAN UNTUK MENYIMPAN', midX + 8, midY - 6);
    }
    // 4. Gambar Garis Virtual Counting Standar
    else if (state.line && state.line.start && state.line.end) {
      const p1x = box.x + state.line.start.x * box.w;
      const p1y = box.y + state.line.start.y * box.h;
      const p2x = box.x + state.line.end.x * box.w;
      const p2y = box.y + state.line.end.y * box.h;

      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(p1x, p1y);
      ctx.lineTo(p2x, p2y);
      ctx.stroke();

      this.drawHandle(ctx, p1x, p1y, '#f59e0b');
      this.drawHandle(ctx, p2x, p2y, '#f59e0b');

      const midX = (p1x + p2x) / 2;
      const midY = (p1y + p2y) / 2;
      ctx.fillStyle = '#f59e0b';
      ctx.font = '10px monospace';
      ctx.fillText('GARIS COUNTING', midX + 8, midY - 6);
    }

    // 5. Badge Mode Aktif
    if (state.mode === 'draw_line') {
      this.drawModeBadge(ctx, 'MODE: TARIK GARIS (Sentuh & Geser Jari)');
    } else if (state.mode === 'draw_roi') {
      this.drawModeBadge(ctx, 'MODE: GAMBAR RoI (Ketuk titik sudut)');
    }
  }

  drawHandle(ctx, x, y, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  drawPolygon(ctx, points, box, fillStyle, strokeStyle, isDraft = false) {
    if (points.length < 2) return;
    ctx.fillStyle = fillStyle;
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = isDraft ? 1.5 : 2;
    if (isDraft) ctx.setLineDash([4, 4]);
    else ctx.setLineDash([]);

    ctx.beginPath();
    ctx.moveTo(box.x + points[0].x * box.w, box.y + points[0].y * box.h);
    for (let i = 1; i < points.length; i++) {
      ctx.lineTo(box.x + points[i].x * box.w, box.y + points[i].y * box.h);
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
    ctx.fillRect(8, 8, 300, 24);
    ctx.strokeRect(8, 8, 300, 24);
    ctx.fillStyle = '#f4f4f5';
    ctx.font = '11px sans-serif';
    ctx.fillText(text, 14, 24);
  }
}
