import time
start_time = time.time()
import pandas as pd
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time for reading aussen.parquet: {execution_time:.4f} seconds")
#aussen_df = pd.read_parquet('aussen.parquet', engine='pyarrow')
print("hallo")