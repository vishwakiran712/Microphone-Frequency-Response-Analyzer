# 🎙️ Microphone Frequency Response Analyzer

> An interactive acoustic instrumentation laboratory for analyzing microphone frequency response, simulating measurement sweeps, visualizing spectral characteristics, and evaluating microphone performance across the audible frequency range.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt)
[![NumPy](https://img.shields.io/badge/Numerical-NumPy-orange?logo=numpy)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-orange?logo=matplotlib)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<img width="929" height="492" alt="image" src="https://github.com/user-attachments/assets/8e8cfb00-3ee2-431a-bc1d-d45454bea810" />


---

## 📌 Overview

**Microphone Frequency Response Analyzer** is an interactive desktop application for studying the frequency-dependent behavior of microphones.

A microphone does not necessarily respond equally to every frequency. Its output can vary across the audible spectrum depending on its transducer characteristics, acoustic design, electronics, and measurement conditions.

This simulator provides a controlled environment for exploring microphone frequency-response behavior and understanding how acoustic input is transformed into an electrical measurement.

The application focuses on:

* Microphone frequency response
* Frequency sweeps
* Spectral analysis
* Amplitude response
* Frequency-domain visualization
* Acoustic measurement concepts
* Microphone characterization
* Signal processing
* Measurement-system analysis

---

# ✨ Key Features

## 🎙️ Microphone Response Simulation

The application models the frequency-dependent response of a microphone across the acoustic spectrum.

Conceptually:

```text id="6a4m1k"
Acoustic Input
      │
      ▼
┌─────────────────┐
│   Microphone    │
│    Response     │
└────────┬────────┘
         │
         ▼
Electrical Output
         │
         ▼
Frequency Analysis
         │
         ▼
Response Curve
```

This allows users to visualize how microphone output changes as the excitation frequency changes.

---

# 📡 Frequency Sweep

The analyzer uses a frequency sweep to examine microphone behavior across a range of frequencies.

A sweep can be represented conceptually as:

```text id="n7x8m2"
Frequency
20 Hz ───────────────────────────────► 20 kHz

Amplitude
   │
   │       ╭──────╮
   │───────╯      ╰────────╮
   │                       ╰──────
   └────────────────────────────────► Frequency
```

The resulting response curve provides a visual representation of the microphone's frequency characteristics.

---

# 🎚️ Frequency Response

Frequency response describes the relative output level of a microphone as a function of frequency.

The response can be represented as:

```text id="w6e4f9"
H(f) = Output(f) / Input(f)
```

or in logarithmic form:

```text id="l0m8j2"
Response(dB) =
20 log₁₀(|Output(f)| / |Input(f)|)
```

A flat response indicates relatively uniform sensitivity across the tested frequency range, while peaks and dips indicate frequency-dependent coloration or attenuation.

---

# 🔬 Microphone Characterization

The analyzer can be used to study important characteristics of a microphone response curve.

### Flat Regions

Indicate frequencies where microphone sensitivity remains relatively consistent.

### Peaks

May indicate frequency regions where the microphone exhibits increased sensitivity.

### Dips

May indicate attenuation or reduced sensitivity.

### High-Frequency Roll-Off

Shows decreasing response at higher frequencies.

### Low-Frequency Roll-Off

Shows decreasing response toward the lower end of the spectrum.

---

# 📈 Response Curve Visualization

The primary output of the analyzer is a frequency-response curve.

A typical response can be visualized as:

```text id="o8d5pz"
 Response
   dB
    │
 +5 │          ╭─────╮
    │         ╱       ╲
  0 │────────╯         ╰──────────
    │                         ╲
 -5 │                          ╲___
    │
    └────────────────────────────────►
       20 Hz                  20 kHz
```

The frequency axis is represented logarithmically, matching the way frequency-response plots are commonly presented in audio and acoustic engineering.

---

# 🎼 Audible Frequency Range

The analyzer operates across the commonly referenced human-audible frequency range:

```text id="x7q3km"
20 Hz → 20 kHz
```

This range covers:

* Low-frequency bass
* Mid-frequency content
* Vocal frequencies
* Upper harmonics
* High-frequency acoustic content

---

# 🔊 Low-Frequency Response

The lower portion of the response curve can be used to study:

* Bass sensitivity
* Low-frequency attenuation
* Proximity-related behavior
* Low-frequency roll-off

This region is particularly important for microphones used in:

* Vocal recording
* Instrument recording
* Measurement systems
* Environmental acoustics

---

# 🗣️ Mid-Frequency Response

The mid-frequency region contains significant speech and many musical components.

Analyzing this region helps demonstrate how microphone frequency characteristics influence:

* Speech intelligibility
* Vocal coloration
* Tonal balance
* Measurement accuracy

---

# ✨ High-Frequency Response

The upper frequency range provides insight into:

* High-frequency sensitivity
* Presence characteristics
* Treble response
* High-frequency roll-off

A microphone with strong high-frequency sensitivity may produce a different perceived character from one with a smoother or attenuated high-frequency response.

---

# 📊 Spectral Analysis

The analyzer uses frequency-domain processing to evaluate microphone response.

Conceptually:

```text id="l4m5y6"
Excitation Signal
       │
       ▼
Microphone Response
       │
       ▼
      FFT
       │
       ▼
Frequency Spectrum
       │
       ▼
Response Extraction
       │
       ▼
Frequency Response Curve
```

This provides a practical demonstration of how FFT-based signal processing can be used in acoustic instrumentation.

---

# 🧮 FFT Analysis

The Fast Fourier Transform converts the sampled time-domain signal into a frequency-domain representation.

Conceptually:

```text id="t8u2pw"
x(t)
 │
 │ FFT
 ▼
X(f)
```

The magnitude spectrum provides information about the distribution of signal energy across frequency.

The analyzer uses this frequency-domain information to construct the microphone response representation.

---

# 📐 Frequency-Domain Measurement

A generalized measurement workflow can be expressed as:

```text id="s9k4ca"
Input Excitation
      │
      ▼
Reference Spectrum
      │
      │
      ▼
Measured Spectrum
      │
      ▼
Ratio / Normalization
      │
      ▼
Magnitude Response
      │
      ▼
dB Frequency Response
```

Normalization is important because the objective is to study the microphone's relative frequency behavior rather than simply the absolute amplitude of the excitation signal.

---

# 🧪 Example Experiments

## Experiment 1 — Flat Microphone Response

Generate a microphone with an approximately flat response.

Observe the response curve across:

```text id="r5e7zq"
20 Hz → 20 kHz
```

The resulting curve should remain relatively stable across the frequency range.

---

## Experiment 2 — Low-Frequency Roll-Off

Configure a microphone response with reduced sensitivity at low frequencies.

Observe:

```text id="6a6s6n"
Low Frequency
      ↓
Reduced Response
      ↓
Gradual Recovery
      ↓
Midband
```

This demonstrates the concept of low-frequency attenuation.

---

## Experiment 3 — Presence Peak

Simulate increased microphone sensitivity within a mid/high-frequency region.

Observe how the response curve develops a peak.

This can be used to understand how microphone response contributes to perceived tonal character.

---

## Experiment 4 — High-Frequency Roll-Off

Introduce high-frequency attenuation.

Observe how the response decreases toward the upper end of the spectrum.

---

## Experiment 5 — Microphone Comparison

Create different response profiles and compare them.

For example:

```text id="6m8w9j"
Microphone A
Flat Response

Microphone B
Bass Roll-Off

Microphone C
Presence Peak

Microphone D
High-Frequency Roll-Off
```

This demonstrates why microphone selection matters in acoustic measurement and audio recording.

---

# 🧠 Microphone Characterization Pipeline

```text id="5m2c9e"
┌──────────────────────────────┐
│       Test Configuration     │
│                              │
│ Frequency Range              │
│ Excitation                   │
│ Response Characteristics     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Frequency Excitation    │
│                              │
│       Sweep Generation       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Microphone Model       │
│                              │
│ Frequency-Dependent Response │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Signal Analysis        │
│                              │
│          FFT                 │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Response Extraction      │
│                              │
│      Magnitude vs f          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Frequency Response       │
│          Plot                │
└──────────────────────────────┘
```

---

# 🖥️ Application Interface

The application uses a technical laboratory-style desktop interface designed around acoustic measurement.

Conceptually:

```text id="j5n2q7"
┌──────────────────────────────────────────────────────────────┐
│             MICROPHONE FREQUENCY RESPONSE ANALYZER          │
├──────────────────────┬───────────────────────────────────────┤
│                      │                                       │
│  MEASUREMENT SETUP   │       SYSTEM STATUS                   │
│                      │                                       │
│  Frequency Range     ├───────────────────────────────────────┤
│  Sweep Parameters    │                                       │
│  Microphone Model    │       FREQUENCY RESPONSE             │
│                      │                                       │
│                      │                                       │
│  ANALYSIS CONTROLS   │       SPECTRAL ANALYSIS              │
│                      │                                       │
└──────────────────────┴───────────────────────────────────────┘
```

The GUI is implemented using **PyQt5**, while NumPy and Matplotlib provide the numerical and visualization components.

---

# 🎓 Educational Applications

This project can be used to demonstrate:

* Microphone Characterization
* Frequency Response
* Acoustic Instrumentation
* Transducer Behavior
* Frequency Sweeps
* FFT
* Frequency-Domain Analysis
* Spectral Analysis
* Audio Engineering
* Acoustic Measurement
* Signal Processing
* Measurement-System Calibration
* Microphone Selection
* Acoustic Testing

---

# 🛠️ Technology Stack

| Technology     | Purpose                          |
| -------------- | -------------------------------- |
| **Python**     | Core application                 |
| **NumPy**      | Numerical computation and FFT    |
| **PyQt5**      | Desktop graphical interface      |
| **Matplotlib** | Frequency-response visualization |

---

# 🚀 Installation

### 1. Clone the repository

```bash id="u4q1z8"
git clone https://github.com/vishwakiran712/Microphone-Frequency-Response-Analyzer.git
cd Microphone-Frequency-Response-Analyzer
```

### 2. Install dependencies

```bash id="x3p6yb"
pip install numpy matplotlib PyQt5
```

### 3. Run the analyzer

```bash id="k9c2vf"
python app.py
```

---

# 📂 Project Structure

```text id="n8w1rx"
Microphone-Frequency-Response-Analyzer/
│
├── app.py
├── README.md
└── LICENSE
```

---

# 🔭 Possible Future Enhancements

Potential extensions include:

* Real microphone input
* Audio-interface integration
* Frequency-sweep measurement using physical hardware
* Logarithmic sine sweep
* Exponential sine sweep
* MLS-based measurement
* Reference microphone correction
* Microphone calibration files
* Sensitivity measurement in mV/Pa
* Absolute SPL calibration
* THD analysis
* Signal-to-noise ratio
* Dynamic range analysis
* Polar-pattern measurement
* Multi-angle microphone characterization
* 1/3-octave response
* Waterfall plots
* Spectrogram
* Phase response
* Group delay
* Multiple microphone comparison
* CSV export
* Measurement report generation
* Automated response flatness metrics

---

# ⚠️ Simulation Notice

This application is intended for **education, experimentation, and acoustic/DSP research**.

A simulated frequency response should not be interpreted as a calibrated specification for a physical microphone. Accurate microphone characterization requires controlled acoustic excitation, calibrated reference equipment, appropriate measurement geometry, and controlled environmental conditions.

---

# 📜 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

# 👨‍💻 Author

**Vishwakiran B.V.S.**

Engineering • Sports Technology • Product Research • Scientific Computing • Acoustics • Signal Processing

GitHub: [@vishwakiran712](https://github.com/vishwakiran712)

---

# ⭐ Project

If you find this project useful for learning, acoustic experimentation, or signal-processing research, consider giving the repository a ⭐.

**Repository:**
https://github.com/vishwakiran712/Microphone-Frequency-Response-Analyzer
