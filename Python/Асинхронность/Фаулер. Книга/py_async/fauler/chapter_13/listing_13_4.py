import sys


[sys.stdout.buffer.write(b'HI!!\n') for _ in range(1000000)]
sys.stdout.flush()
