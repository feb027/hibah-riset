import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.counting.models import Point, Line
from core.counting.counter import PeopleCounter
from core.counting.detector import LineCrossDetector

class NaiveCounter:
    def __init__(self, virtual_line: Line):
        self.virtual_line = virtual_line
        self.count_in = 0
        self.count_out = 0
        self.history = {}

    def update(self, track_id: int, current_centroid: Point):
        if track_id not in self.history:
            self.history[track_id] = current_centroid
            return
        
        previous = self.history[track_id]
        traj = Line(previous, current_centroid)
        intersects, direction = LineCrossDetector.check_crossing(self.virtual_line, traj)
        
        # NAIVE LOGIC: Hitung setiap kali garis terpotong (sangat rentan over-counting jika jitter)
        if intersects:
            if direction == "IN":
                self.count_in += 1
            else:
                self.count_out += 1
                
        self.history[track_id] = current_centroid

def run_synthetic_ablation():
    print("Memulai eksperimen ablasi (Ablation Study) Logika Hitung secara terisolasi...")
    print("Menggunakan data sintetik lintasan tracker dengan 'Jitter' (gangguan/noise) untuk menguji ketahanan debouncing.")
    
    # Garis virtual vertikal di x=500
    virtual_line = Line(Point(500, 0), Point(500, 1000))
    
    naive_counter = NaiveCounter(virtual_line)
    state_machine_counter = PeopleCounter(virtual_line, cooldown_threshold=30)
    
    max_frames = 200
    naive_history = []
    state_history = []
    
    # Skenario: 3 Orang menyeberang garis. 
    # Orang 1 (ID=1) menyeberang dengan mulus.
    # Orang 2 (ID=2) mondar-mandir / tracking jitter di sekitar garis (x=500) selama 40 frame.
    # Orang 3 (ID=3) menyeberang dengan mulus di akhir.
    
    for frame in range(max_frames):
        # Orang 1: Mulus dari kiri ke kanan (IN)
        if 10 <= frame <= 50:
            x1 = 400 + (frame - 10) * (200 / 40)
            naive_counter.update(1, Point(x1, 200))
            state_machine_counter.update(1, Point(x1, 200))
            
        # Orang 2: Oklusi / Jitter parah di sekitar garis
        if 60 <= frame <= 140:
            # Base movement from left to right
            base_x = 450 + (frame - 60) * (100 / 80)
            # Add severe noise that makes it cross back and forth across 500
            noise = np.sin(frame * 0.5) * 30  
            x2 = base_x + noise
            
            naive_counter.update(2, Point(x2, 500))
            state_machine_counter.update(2, Point(x2, 500))
            
        # Orang 3: Mulus dari kanan ke kiri (OUT)
        if 150 <= frame <= 190:
            x3 = 600 - (frame - 150) * (200 / 40)
            naive_counter.update(3, Point(x3, 800))
            state_machine_counter.update(3, Point(x3, 800))
            
        naive_history.append(naive_counter.count_in + naive_counter.count_out)
        state_history.append(state_machine_counter.count_in + state_machine_counter.count_out)

    plt.figure(figsize=(10, 6))
    plt.plot(range(max_frames), naive_history, label='Model A (Naive Line Crossing)', color='red', linestyle='--')
    plt.plot(range(max_frames), state_history, label='Model B (State Machine + Debouncing)', color='blue', linewidth=2)
    
    plt.title('Ablation Study Skenario C: Over-Counting akibat Tracking Jitter')
    plt.xlabel('Frame ke-')
    plt.ylabel('Total Orang Dihitung (Masuk + Keluar)')
    plt.legend()
    plt.grid(True)
    
    # Highlight the jitter area
    plt.axvspan(60, 140, color='yellow', alpha=0.3, label='Periode Jitter / Oklusi (Orang 2)')
    plt.legend()
    
    os.makedirs('experiments', exist_ok=True)
    chart_path = 'experiments/ablation_counting.png'
    plt.savefig(chart_path)
    
    print(f"Selesai! Grafik komparasi tersimpan di {chart_path}")
    print(f"Hasil Akhir Model A (Naive): {naive_history[-1]} orang (OVER-COUNT SANGAT PARAH)")
    print(f"Hasil Akhir Model B (State Machine): {state_history[-1]} orang (AKURAT!)")

if __name__ == "__main__":
    run_synthetic_ablation()
