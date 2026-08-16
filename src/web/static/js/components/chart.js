/**
 * Real-Time SVG Traffic Timeline Chart Component.
 */
import { store } from '../store.js';

export function initTrafficChart() {
  const chartSvg = document.getElementById('traffic-chart-svg');
  if (!chartSvg) return;

  store.subscribe('telemetry', (telemetry) => {
    const history = telemetry.recent_traffic || [];
    if (history.length < 2) return;

    const w = 400;
    const h = 100;
    const padding = 10;

    const maxVal = Math.max(
      10,
      ...history.map(d => Math.max(d.count_in, d.count_out, d.occupancy))
    );

    const pointsIn = [];
    const pointsOut = [];

    history.forEach((d, i) => {
      const x = padding + (i / (history.length - 1)) * (w - 2 * padding);
      const yIn = h - padding - (d.count_in / maxVal) * (h - 2 * padding);
      const yOut = h - padding - (d.count_out / maxVal) * (h - 2 * padding);

      pointsIn.push(`${x.toFixed(1)},${yIn.toFixed(1)}`);
      pointsOut.push(`${x.toFixed(1)},${yOut.toFixed(1)}`);
    });

    const lineIn = chartSvg.querySelector('.chart-line-in');
    const lineOut = chartSvg.querySelector('.chart-line-out');

    if (lineIn) lineIn.setAttribute('d', `M ${pointsIn.join(' L ')}`);
    if (lineOut) lineOut.setAttribute('d', `M ${pointsOut.join(' L ')}`);
  });
}
