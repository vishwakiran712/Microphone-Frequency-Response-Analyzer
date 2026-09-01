import sys
import csv
import numpy as np
from scipy import signal as sp_signal

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QDoubleSpinBox, QComboBox, QGroupBox,
    QFrame, QSplitter, QScrollArea, QPushButton, QFileDialog, QCheckBox
)
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# -------------------------------------------------------------------------
# UI Styling (Dark Theme)
# -------------------------------------------------------------------------
DARK_STYLE = """
QMainWindow {
    background-color: #0D1117;
}
QWidget {
    color: #C9D1D9;
    font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 11px;
}
QGroupBox {
    border: 1px solid #21262D;
    border-radius: 6px;
    margin-top: 10px;
    font-weight: bold;
    color: #58A6FF;
    background-color: #161B22;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    background-color: #161B22;
    border-radius: 3px;
}
QLabel {
    color: #8B949E;
}
QDoubleSpinBox, QComboBox {
    background-color: #0D1117;
    border: 1px solid #30363D;
    border-radius: 4px;
    padding: 4px 6px;
    color: #58A6FF;
    font-weight: bold;
}
QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #58A6FF;
}
QComboBox QAbstractItemView {
    background-color: #161B22;
    color: #58A6FF;
    selection-background-color: #21262D;
}
QPushButton {
    background-color: #238636;
    color: #FFFFFF;
    border: 1px solid #2EA043;
    border-radius: 4px;
    padding: 6px 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2EA043;
}
QPushButton:pressed {
    background-color: #1A7F37;
}
QCheckBox {
    color: #C9D1D9;
    font-weight: bold;
}
QFrame#metricCard {
    background-color: #0D1117;
    border: 1px solid #21262D;
    border-radius: 6px;
}
"""

# Microphone Profiles Parameter Constants
MIC_PROFILES = {
    "Measurement Microphone": {
        "color": "#3FB950",
        "sensitivity_offset": 0.0,    # dB baseline sensitivity
        "bass_cutoff": 15.0,          # Hz
        "hf_cutoff": 24000.0,         # Hz
        "resonances": [
            {"freq": 18000, "q": 3.0, "gain": 1.2}  # Subtle diaphragm resonance
        ]
    },
    "Consumer Microphone": {
        "color": "#58A6FF",
        "sensitivity_offset": -2.5,   # dB sensitivity
        "bass_cutoff": 70.0,          # Bass roll-off
        "hf_cutoff": 15000.0,         # High-frequency roll-off
        "resonances": [
            {"freq": 4500, "q": 2.5, "gain": 3.5},   # Presence peak for voice clarity
            {"freq": 11000, "q": 4.0, "gain": -2.0}  # Mild high notch
        ]
    },
    "Low-Cost Microphone": {
        "color": "#F85149",
        "sensitivity_offset": -8.0,   # Low sensitivity
        "bass_cutoff": 150.0,         # Steep bass roll-off
        "hf_cutoff": 9000.0,          # Band-limited high roll-off
        "resonances": [
            {"freq": 2800, "q": 1.8, "gain": 6.0},   # Sharp body resonance peak
            {"freq": 6500, "q": 3.0, "gain": -5.0},  # Capsule absorption dip
            {"freq": 8200, "q": 4.5, "gain": 4.0}    # Sibilance peak
        ]
    }
}


class MicAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Microphone Frequency Response Analyzer")
        self.resize(1400, 850)
        self.setMinimumSize(1024, 720)

        # Analysis State
        self.freqs = np.zeros(1)
        self.responses = {}

        self.init_ui()
        self.recalculate_curves()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # -----------------------------------------------------------------
        # LEFT PANEL: Controls & Configuration
        # -----------------------------------------------------------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        ctrl_layout = QVBoxLayout(scroll_content)

        # 1. Microphone Selection Controls
        group_select = QGroupBox("1. MICROPHONE SELECTION")
        grid_sel = QGridLayout(group_select)
        grid_sel.setSpacing(6)

        grid_sel.addWidget(QLabel("Active Microphone:"), 0, 0)
        self.combo_mic = QComboBox()
        self.combo_mic.addItems([
            "Measurement Microphone",
            "Consumer Microphone",
            "Low-Cost Microphone"
        ])
        self.combo_mic.currentIndexChanged.connect(self.recalculate_curves)
        grid_sel.addWidget(self.combo_mic, 0, 1)

        grid_sel.addWidget(QLabel("Reference Microphone:"), 1, 0)
        self.combo_ref = QComboBox()
        self.combo_ref.addItems([
            "Measurement Microphone",
            "Consumer Microphone",
            "Low-Cost Microphone"
        ])
        self.combo_ref.setCurrentIndex(0)
        self.combo_ref.currentIndexChanged.connect(self.recalculate_curves)
        grid_sel.addWidget(self.combo_ref, 1, 1)

        self.chk_compare_all = QCheckBox("Overlay All Microphones")
        self.chk_compare_all.setChecked(True)
        self.chk_compare_all.stateChanged.connect(self.recalculate_curves)
        grid_sel.addWidget(self.chk_compare_all, 2, 0, 1, 2)

        ctrl_layout.addWidget(group_select)

        # 2. Measurement Parameters
        group_params = QGroupBox("2. ANALYSIS PARAMETERS")
        grid_params = QGridLayout(group_params)
        grid_params.setSpacing(6)

        grid_params.addWidget(QLabel("Start Frequency (Hz):"), 0, 0)
        self.spin_fmin = self.create_spinbox(10.0, 1000.0, 20.0, grid_params, 0, 1, step=5.0)

        grid_params.addWidget(QLabel("End Frequency (Hz):"), 1, 0)
        self.spin_fmax = self.create_spinbox(1000.0, 48000.0, 20000.0, grid_params, 1, 1, step=1000.0)

        grid_params.addWidget(QLabel("Measurement Noise (dB):"), 2, 0)
        self.spin_noise = self.create_spinbox(0.0, 10.0, 0.5, grid_params, 2, 1, step=0.1)

        ctrl_layout.addWidget(group_params)

        # 3. Data Export
        group_export = QGroupBox("3. DATA EXPORT")
        vbox_export = QVBoxLayout(group_export)
        self.btn_export = QPushButton("Export Curves to CSV")
        self.btn_export.clicked.connect(self.export_csv)
        vbox_export.addWidget(self.btn_export)

        ctrl_layout.addWidget(group_export)
        ctrl_layout.addStretch()

        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)

        # -----------------------------------------------------------------
        # RIGHT PANEL: Plots & Electroacoustic Indicators
        # -----------------------------------------------------------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Performance Indicator Cards
        metrics_group = QGroupBox("ELECTROACOUSTIC PERFORMANCE METRICS")
        grid_metrics = QGridLayout(metrics_group)
        grid_metrics.setSpacing(6)

        self.lbl_peak_freq = self.create_metric_card("Peak Frequency", "0 Hz", grid_metrics, 0, 0)
        self.lbl_bandwidth = self.create_metric_card("-3 dB Bandwidth", "0 Hz", grid_metrics, 0, 1)
        self.lbl_max_dev = self.create_metric_card("Max Deviation (vs Ref)", "0.0 dB", grid_metrics, 0, 2)
        self.lbl_avg_dev = self.create_metric_card("Avg Deviation (vs Ref)", "0.0 dB", grid_metrics, 0, 3)

        right_layout.addWidget(metrics_group)

        # Matplotlib Plots
        plots_group = QGroupBox("FREQUENCY RESPONSE & DEVIATION ANALYSIS")
        layout_plots = QVBoxLayout(plots_group)

        self.fig = Figure(figsize=(9, 6), facecolor='#161B22')
        self.canvas = FigureCanvas(self.fig)
        layout_plots.addWidget(self.canvas)

        right_layout.addWidget(plots_group, stretch=1)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([350, 1030])

    def create_spinbox(self, min_val, max_val, val, layout, row, col, step=0.1):
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(val)
        spin.setSingleStep(step)
        spin.valueChanged.connect(self.recalculate_curves)
        layout.addWidget(spin, row, col)
        return spin

    def create_metric_card(self, title, default_val, layout, row, col):
        card = QFrame()
        card.setObjectName("metricCard")
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(6, 4, 6, 4)

        lbl_title = QLabel(title.upper())
        lbl_title.setStyleSheet("color: #8B949E; font-size: 10px; font-weight: bold;")
        lbl_val = QLabel(default_val)
        lbl_val.setStyleSheet("color: #58A6FF; font-size: 12px; font-weight: bold;")

        vbox.addWidget(lbl_title)
        vbox.addWidget(lbl_val)
        layout.addWidget(card, row, col)
        return lbl_val

    def generate_mic_response(self, mic_name, freqs, noise_std):
        """Generates synthetic frequency response curve (in dB) using high/low pass filters & resonant peaks."""
        profile = MIC_PROFILES[mic_name]
        w = 2 * np.pi * freqs

        # 1. Base High-Pass (Bass roll-off) & Low-Pass (HF roll-off)
        wb = 2 * np.pi * profile["bass_cutoff"]
        wh = 2 * np.pi * profile["hf_cutoff"]

        # High-pass filter magnitude response (2nd order Butterworth-like)
        hp_mag = (w**2) / np.sqrt((w**2 - wb**2)**2 + (wb * w)**2)
        # Low-pass filter magnitude response (2nd order Butterworth-like)
        lp_mag = (wh**2) / np.sqrt((w**2 - wh**2)**2 + (wh * w)**2)

        resp_db = 20.0 * np.log10(np.maximum(1e-6, hp_mag * lp_mag)) + profile["sensitivity_offset"]

        # 2. Add Parametric Resonance Peaks / Dips (Peaking EQ filters)
        for res in profile["resonances"]:
            f0 = res["freq"]
            q = res["q"]
            gain_db = res["gain"]

            # Peaking EQ approximation in dB domain
            bw = f0 / q
            res_shape = np.exp(-0.5 * ((freqs - f0) / (bw / 2.0))**2)
            resp_db += gain_db * res_shape

        # 3. Measurement Noise
        if noise_std > 0.0:
            # Reproducible random state seed mapped to frequency grid
            np.random.seed(42)
            resp_db += np.random.normal(0, noise_std, len(freqs))

        return resp_db

    def recalculate_curves(self):
        fmin = self.spin_fmin.value()
        fmax = self.spin_fmax.value()

        if fmin >= fmax:
            return

        # Logarithmically spaced frequency array (500 points)
        self.freqs = np.logspace(np.log10(fmin), np.log10(fmax), 500)
        noise_level = self.spin_noise.value()

        # Compute curves for all microphones
        self.responses = {}
        for mic_name in MIC_PROFILES.keys():
            self.responses[mic_name] = self.generate_mic_response(mic_name, self.freqs, noise_level)

        active_mic = self.combo_mic.currentText()
        ref_mic = self.combo_ref.currentText()

        active_resp = self.responses[active_mic]
        ref_resp = self.responses[ref_mic]

        # Electroacoustic Performance Indicators
        # 1. Peak Frequency
        peak_idx = np.argmax(active_resp)
        peak_freq = self.freqs[peak_idx]

        # 2. -3 dB Bandwidth relative to 1 kHz level
        idx_1k = np.argmin(np.abs(self.freqs - 1000.0))
        ref_1k_val = active_resp[idx_1k]
        threshold = ref_1k_val - 3.0

        passband_indices = np.where(active_resp >= threshold)[0]
        if len(passband_indices) > 0:
            bw_low = self.freqs[passband_indices[0]]
            bw_high = self.freqs[passband_indices[-1]]
            bandwidth = bw_high - bw_low
            bw_str = f"{bandwidth:.0f} Hz ({bw_low:.0f}-{bw_high:.0f} Hz)"
        else:
            bw_str = "N/A"

        # 3. Deviation vs Reference
        diff = active_resp - ref_resp
        max_dev = np.max(np.abs(diff))
        avg_dev = np.mean(np.abs(diff))

        # Update Metrics GUI
        self.lbl_peak_freq.setText(f"{peak_freq:.0f} Hz ({active_resp[peak_idx]:.1f} dB)")
        self.lbl_bandwidth.setText(bw_str)
        self.lbl_max_dev.setText(f"{max_dev:.2f} dB")
        self.lbl_avg_dev.setText(f"{avg_dev:.2f} dB")

        # Plot Graphs
        self.plot_visuals(active_mic, ref_mic)

    def plot_visuals(self, active_mic, ref_mic):
        self.fig.clear()
        grid_c = '#21262D'
        text_c = '#8B949E'

        # Subplot 1: Frequency Response Magnitude Graph
        ax1 = self.fig.add_subplot(211)
        ax1.set_facecolor('#0D1117')

        if self.chk_compare_all.isChecked():
            for name, resp in self.responses.items():
                color = MIC_PROFILES[name]["color"]
                lw = 2.0 if name == active_mic else 1.0
                alpha = 1.0 if name == active_mic else 0.6
                ax1.semilogx(self.freqs, resp, color=color, linewidth=lw, alpha=alpha, label=name)
        else:
            color = MIC_PROFILES[active_mic]["color"]
            ax1.semilogx(self.freqs, self.responses[active_mic], color=color, linewidth=2.0, label=active_mic)
            if ref_mic != active_mic:
                ref_color = MIC_PROFILES[ref_mic]["color"]
                ax1.semilogx(self.freqs, self.responses[ref_mic], color=ref_color, linestyle='--', linewidth=1.2, label=f"Ref: {ref_mic}")

        ax1.set_title("Microphone Frequency Response (dB re 1V/Pa)", color='#58A6FF', fontsize=9, fontweight='bold', loc='left')
        ax1.set_ylabel("Sensitivity (dB)", color=text_c, fontsize=8)
        ax1.tick_params(colors=text_c, labelsize=7)
        ax1.grid(True, which="both", linestyle='--', alpha=0.3, color=grid_c)
        ax1.legend(facecolor='#161B22', edgecolor=grid_c, labelcolor=text_c, fontsize=7, loc='lower right')

        # Subplot 2: Difference Curve vs Reference Microphone
        ax2 = self.fig.add_subplot(212, sharex=ax1)
        ax2.set_facecolor('#0D1117')

        diff = self.responses[active_mic] - self.responses[ref_mic]
        ax2.semilogx(self.freqs, diff, color='#E3B341', linewidth=1.5, label=f"{active_mic} - {ref_mic}")
        ax2.axhline(0, color='#8B949E', linestyle=':', linewidth=1.0)

        ax2.set_title(f"Difference Curve Relative to {ref_mic}", color='#E3B341', fontsize=9, fontweight='bold', loc='left')
        ax2.set_xlabel("Frequency (Hz)", color=text_c, fontsize=8)
        ax2.set_ylabel("Difference (dB)", color=text_c, fontsize=8)
        ax2.tick_params(colors=text_c, labelsize=7)
        ax2.grid(True, which="both", linestyle='--', alpha=0.3, color=grid_c)
        ax2.legend(facecolor='#161B22', edgecolor=grid_c, labelcolor=text_c, fontsize=7, loc='upper right')

        for ax in [ax1, ax2]:
            for spine in ax.spines.values():
                spine.set_color(grid_c)

        self.fig.tight_layout()
        self.canvas.draw()

    def export_csv(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Frequency Response Data", "mic_frequency_response.csv", "CSV Files (*.csv)")
        if not filePath:
            return

        with open(filePath, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ["Frequency_Hz", "Measurement_Mic_dB", "Consumer_Mic_dB", "LowCost_Mic_dB"]
            writer.writerow(header)

            for i in range(len(self.freqs)):
                row = [
                    f"{self.freqs[i]:.2f}",
                    f"{self.responses['Measurement Microphone'][i]:.3f}",
                    f"{self.responses['Consumer Microphone'][i]:.3f}",
                    f"{self.responses['Low-Cost Microphone'][i]:.3f}"
                ]
                writer.writerow(row)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(DARK_STYLE)

    window = MicAnalyzerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()