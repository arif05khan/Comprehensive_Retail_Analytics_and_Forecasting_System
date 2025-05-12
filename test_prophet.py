import sys
import traceback
try:
    from prophet import Prophet
    import pandas as pd

    df = pd.DataFrame({
        'ds': pd.date_range(start='2020-01-01', periods=10, freq='D'),
        'y': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    })
    model = Prophet()
    model.fit(df)
    print("Prophet model created successfully!")
except Exception as e:
    print("Error:", e)
    traceback.print_exc(file=sys.stdout)