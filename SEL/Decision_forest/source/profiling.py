from pandas_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("./data/balance.csv", header=None)
profile = ProfileReport(df, title="balance Profiling Report")
profile.to_file("./doc/balance.html")

