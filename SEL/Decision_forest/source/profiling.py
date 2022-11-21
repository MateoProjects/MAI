from pandas_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("DESK.csv")
profile = ProfileReport(df, title="balance Profiling Report")
profile.to_file("balance.html")

