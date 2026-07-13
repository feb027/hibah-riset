import pandas as pd
import matplotlib.pyplot as plt
import os

csv_path = "experiments/yolo_comparison_results.csv"

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found. Run compare_yolo_models.py first.")
    exit(1)

df = pd.read_csv(csv_path)

# Set up the matplotlib figure
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('YOLO Models Comparison on CPU (Laptop i5-5200U)', fontsize=16)

# Plot 1: FPS comparison
axes[0].bar(df['Model'], df['Avg_FPS'], color=['#4C72B0', '#DD8452', '#55A868'])
axes[0].set_title('Average FPS (Higher is better)')
axes[0].set_ylabel('Frames Per Second')
for i, v in enumerate(df['Avg_FPS']):
    axes[0].text(i, v + 0.1, f"{v:.2f}", ha='center')

# Plot 2: Average Confidence comparison
axes[1].bar(df['Model'], df['Avg_Confidence'], color=['#4C72B0', '#DD8452', '#55A868'])
axes[1].set_title('Average Detection Confidence (Higher is better)')
axes[1].set_ylabel('Confidence Score (0-1)')
axes[1].set_ylim(0, 1.0)
for i, v in enumerate(df['Avg_Confidence']):
    axes[1].text(i, v + 0.02, f"{v:.4f}", ha='center')

plt.tight_layout()

# Save the plot
output_img = "experiments/output-i5-5200u.png"
os.makedirs("experiments", exist_ok=True)
plt.savefig(output_img, dpi=300)
print(f"Plot saved to {output_img}")
