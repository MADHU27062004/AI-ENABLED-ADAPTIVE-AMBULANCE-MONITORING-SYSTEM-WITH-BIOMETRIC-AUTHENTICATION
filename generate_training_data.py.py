import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment

# Create training dataset
np.random.seed(42)

# Normal readings
normal_data = {
    'spo2': np.random.randint(96, 100, 200),
    'heart': np.random.randint(60, 91, 200),
    'sys': np.random.randint(100, 121, 200),
    'dia': np.random.randint(60, 81, 200),
    'ecg': np.random.randint(0, 701, 200),
    'mmhg': np.random.uniform(3, 5, 200),
    'label': ['Normal'] * 200
}

# Abnormal readings
abnormal_data = {
    'spo2': list(np.random.randint(80, 96, 100)) + list(np.random.randint(100, 101, 100)),
    'heart': list(np.random.randint(40, 60, 50)) + list(np.random.randint(100, 150, 150)),
    'sys': list(np.random.randint(70, 100, 50)) + list(np.random.randint(140, 180, 150)),
    'dia': list(np.random.randint(30, 60, 50)) + list(np.random.randint(90, 120, 150)),
    'ecg': list(np.random.randint(700, 1000, 100)) + list(np.random.randint(1000, 2000, 100)),
    'mmhg': list(np.random.uniform(0.5, 2.9, 100)) + list(np.random.uniform(5.1, 8, 100)),
    'label': ['Abnormal'] * 200
}

# Combine
df_normal = pd.DataFrame(normal_data)
df_abnormal = pd.DataFrame(abnormal_data)
df_train = pd.concat([df_normal, df_abnormal], ignore_index=True)

# Shuffle
df_train = df_train.sample(frac=1).reset_index(drop=True)

# Save to Excel
df_train.to_excel('training_data.xlsx', index=False, sheet_name='Training Data')

print("✅ Training data Excel created: training_data.xlsx")
print(f"📊 Total samples: {len(df_train)}")
print(f"📈 Normal: {len(df_normal)}, Abnormal: {len(df_abnormal)}")
