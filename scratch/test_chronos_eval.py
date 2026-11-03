import sys
print(f"Python: {sys.version}")

try:
    import chronos
    print("chronos package is directly available:", chronos)
except Exception as e:
    print("chronos import:", e)

try:
    import torch
    print("torch:", torch.__version__)
except Exception as e:
    print("torch import:", e)

try:
    import transformers
    print("transformers:", transformers.__version__)
except Exception as e:
    print("transformers import:", e)
