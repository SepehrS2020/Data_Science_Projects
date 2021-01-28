import requests
import pandas as pd
url='https://hooks.bluebrain.xyz/api/v1/za/sales?start=2020-1-27&end=2020-11-28'
r = requests.get(url, headers={'Authorization': '6SIFsKEjeHe214NDy2lNeDP39BRzHUpzZI6t5R214NDy26TkrwuErQ8mbw2yVzMMatJbZe51VCzYCSyM1kvoe1qWhbE7xPSwdDeA'})

data= pd.DataFrame(r.json())
data=data[data['object_sale_datePurchase'<'2020-1-27']]
data=data[data['object_pur_datePayment']<'2019']


cur.executescript(
'''
INSERT INTO Sales (vendor_name, model_name, object_pur_articlePrice,
object_sale_datePurchase, object_sale_articlePriceTotal, caseMaterial, cycleTime)
VALUES (?, ?, ?, ?, ?, ?, ?) ''',
(
item['vendor_name'], item['model_name'],item['object_pur_articlePrice'],
item['object_sale_datePurchase'], item['object_sale_articlePriceTotal'],
item['caseMaterial'], item['cycleTime']   )
)
conn.close()
