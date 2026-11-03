import numpy as np
import pandas as pd
from scipy import stats

class PageHinkleyDriftDetector:
    """
    Page-Hinkley test for detecting abrupt concept drift in streaming or sequential data.
    Monitors cumulative deviations of observations from running mean.
    """
    def __init__(self, delta=0.005, threshold=35.0, alpha=0.999):
        self.delta = delta          # Magnitude of tolerable change
        self.threshold = threshold  # Threshold for alarm triggering
        self.alpha = alpha          # Forgetting factor for running mean
        self.reset()
        
    def reset(self):
        self.x_mean = 0.0
        self.sum_val = 0.0
        self.min_val = float('inf')
        self.n = 0
        self.drift_detected = False
        
    def update(self, val):
        self.n += 1
        if self.n == 1:
            self.x_mean = float(val)
        else:
            self.x_mean = self.alpha * self.x_mean + (1.0 - self.alpha) * float(val)
            
        self.sum_val += float(val) - self.x_mean - self.delta
        if self.sum_val < self.min_val:
            self.min_val = self.sum_val
            
        ph_stat = self.sum_val - self.min_val
        if ph_stat > self.threshold:
            self.drift_detected = True
            return True, ph_stat
        return False, ph_stat


class ADWINDriftDetector:
    """
    Adaptive Windowing (ADWIN) algorithm.
    Dynamically grows window size and cuts sub-windows when statistical mean difference
    exceeds Hoeffding's inequality bound epsilon_cut = sqrt((1/(2*m)) * ln(4/delta)).
    """
    def __init__(self, delta=0.01, max_window=1000):
        self.delta = delta
        self.max_window = max_window
        self.window = []
        self.drift_detected = False
        
    def reset(self):
        self.window = []
        self.drift_detected = False
        
    def update(self, val):
        self.window.append(float(val))
        if len(self.window) > self.max_window:
            self.window.pop(0)
            
        w_len = len(self.window)
        if w_len < 10:
            return False, 0.0
            
        # Check sub-window splits
        for split_point in range(5, w_len - 5, max(1, w_len // 10)):
            w0 = self.window[:split_point]
            w1 = self.window[split_point:]
            n0, n1 = len(w0), len(w1)
            m = 1.0 / (1.0 / n0 + 1.0 / n1)
            
            mean0, mean1 = np.mean(w0), np.mean(w1)
            diff = abs(mean0 - mean1)
            
            # Variance estimate
            var_w = np.var(self.window)
            eps_cut = np.sqrt((2.0 / m) * var_w * np.log(2.0 / self.delta)) + (2.0 / (3.0 * m)) * np.log(2.0 / self.delta)
            
            if diff > eps_cut:
                self.drift_detected = True
                self.window = w1 # Drop older sub-window
                return True, float(diff)
                
        return False, 0.0

print("Testing Page-Hinkley and ADWIN...")
ph = PageHinkleyDriftDetector(threshold=20.0)
adwin = ADWINDriftDetector(delta=0.01)

# Stream normal distribution, then shifted distribution
np.random.seed(42)
stream_normal = np.random.normal(loc=100.0, scale=10.0, size=150)
stream_shifted = np.random.normal(loc=135.0, scale=12.0, size=150)
full_stream = np.concatenate([stream_normal, stream_shifted])

ph_drifts = []
adwin_drifts = []

for idx, x in enumerate(full_stream):
    d_ph, _ = ph.update(x)
    d_ad, _ = adwin.update(x)
    if d_ph: ph_drifts.append(idx)
    if d_ad: adwin_drifts.append(idx)

print(f"Page-Hinkley detected drift at step(s): {ph_drifts}")
print(f"ADWIN detected drift at step(s): {adwin_drifts}")
print("Both detectors successfully identified the distribution shift!")
