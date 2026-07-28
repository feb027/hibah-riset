import matplotlib.pyplot as plt
import os

# Data
labels_pemotongan = ['Utuh dalam bingkai', 'Terpotong tepi']
sizes_pemotongan = [84.7, 15.3]
colors_pemotongan = ['#4CAF50', '#F44336']

labels_oklusi = ['Terlihat penuh', 'Teroklusi sebagian', 'Teroklusi berat']
sizes_oklusi = [63.2, 22.5, 14.3]
colors_oklusi = ['#2196F3', '#FFC107', '#FF5722']

labels_ukuran = ['Besar (>=150 px)', 'Sedang (50-150 px)', 'Kecil (<50 px)']
sizes_ukuran = [53.0, 36.7, 10.3]
colors_ukuran = ['#9C27B0', '#00BCD4', '#795548']

# Create figure
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Sebaran Karakteristik Target (99.481 kotak)', fontsize=16, fontweight='bold', y=1.05)

# Plot 1
ax1.pie(sizes_pemotongan, labels=labels_pemotongan, autopct='%1.1f%%', startangle=90, colors=colors_pemotongan, textprops={'fontsize': 11})
ax1.set_title('1. Pemotongan Bingkai', pad=15, fontweight='bold')

# Plot 2
ax2.pie(sizes_oklusi, labels=labels_oklusi, autopct='%1.1f%%', startangle=90, colors=colors_oklusi, textprops={'fontsize': 11})
ax2.set_title('2. Tingkat Oklusi', pad=15, fontweight='bold')

# Plot 3
ax3.pie(sizes_ukuran, labels=labels_ukuran, autopct='%1.1f%%', startangle=90, colors=colors_ukuran, textprops={'fontsize': 11})
ax3.set_title('3. Jarak / Ukuran Objek', pad=15, fontweight='bold')

# Layout
plt.tight_layout()

# Save
output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'experiments')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'sebaran_target.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Graph saved to {output_path}")
