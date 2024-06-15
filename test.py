import pandas as pd

csv_file = "C:/Users/hp/Downloads/mobil_mesin_harga.csv"
data = pd.read_csv(csv_file)

# This shows a list of all column names in a list
#print("Column Headers: ", data.columns)
for column, data_type in data.dtypes.items():
    print(f"Column: {column}, Data Type: {data_type}")
