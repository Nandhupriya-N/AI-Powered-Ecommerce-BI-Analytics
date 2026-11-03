import torch
from chronos import ChronosPipeline
import time
import psutil

print("Testing Chronos T5 Tiny loading...")
t0 = time.time()
mem_before = psutil.virtual_memory().used / (1024**2)

try:
    pipeline = ChronosPipeline.from_pretrained(
        "amazon/chronos-t5-tiny",
        device_map="cpu",
        torch_dtype=torch.float32,
    )
    t1 = time.time()
    mem_after = psutil.virtual_memory().used / (1024**2)
    print(f"Chronos T5 Tiny loaded successfully in {t1 - t0:.2f}s!")
    print(f"Memory increase: {mem_after - mem_before:.2f} MB")
    
    # Test quick prediction on dummy tensor
    context = torch.tensor([100.0, 120.0, 115.0, 130.0, 140.0, 135.0, 150.0])
    fc = pipeline.predict(context, prediction_length=3, num_samples=20)
    print("Forecast shape:", fc.shape)
    print("Forecast samples median:", torch.median(fc[0], dim=0).values.tolist())
except Exception as e:
    print("Failed to load Chronos T5 Tiny:", e)
