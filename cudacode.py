import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np

N = 10**8

# Host (CPU) vectors
a = np.random.randn(N).astype(np.float32)
b = np.random.randn(N).astype(np.float32)
c = np.empty_like(a)  # Result vector on host (CPU)

# Allocate memory on the device (GPU)
a_gpu = cuda.mem_alloc(a.nbytes)
b_gpu = cuda.mem_alloc(b.nbytes)
c_gpu = cuda.mem_alloc(c.nbytes)

# Transfer data from host (CPU) to device (GPU)
for i in range(10*100):
    print(f"Iteration: {i+1}")
    cuda.memcpy_htod(a_gpu, a)
    cuda.memcpy_htod(b_gpu, b)

    alpha = np.float32(1.0)
    beta = np.float32(1.0)

print("Result from GPU (CuBLAS):", c[:10])
print("Expected result (CPU):", (a + b)[:10])

# import os
# print(os.getcwd())