import pandas as pd
# from models import Department, Employee


data = pd.read_csv("./MOCK_DATA.csv")

for i in range(data.shape[0]):
    row = data.loc[i]
    name = row.name
    address = row.address
    dept = row.Department
    salary = random.randint(1000, 43000)

    #print(data.loc[i])
