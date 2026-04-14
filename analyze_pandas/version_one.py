import pandas as pd

name = ["Lucas","Isadora","Julia","Monica"]
age = [25,24,23,22]
sex = ["M","F","F","F"]

df = pd.DataFrame({"name":name,"age":age,"sex":sex})

print(df)