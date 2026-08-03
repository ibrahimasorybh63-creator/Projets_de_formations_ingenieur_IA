import pandas as pd 
import numpy as np
dataset = pd.read_csv('ventes_dataset_sale.csv')
#nettoyage de données
print(f"Nombre de lignes : {dataset.shape[0]}")
print(f"Nombre de colonnes : {dataset.shape[1]}")

dataset.info()
dataset.isna().sum().sort_values(ascending=False)

dataset.duplicated().sum()

dataset.describe()

dataset.describe(include="object")
dataset = dataset.drop_duplicates(keep='first')
dataset['product_category'].unique()
dataset['product_category'].value_counts()
dataset['product_category'] = dataset['product_category'].str.strip().str.lower()
correction_map = {
    'foood': 'food',
    'toy': 'toys',
    'book': 'books',
    'beuty': 'beauty',
    'cloting': 'clothing',
    'hom': 'home',
    'sport': 'sports',
    'eletronics': 'electronics',
    'electronic': 'electronics',
}
dataset['product_category'] = dataset['product_category'].replace(correction_map).str.capitalize()
dataset['region'] = dataset['region'].str.strip().str.capitalize()
correction_region = {
    'Conakri' : 'Conakry',
    'Labé' : 'Labe',
    "N'zerekore" : "Nzerekore"
}
dataset['region'] = dataset['region'].replace(correction_region)
dataset['region'].value_counts()
dataset['payment_method'] = dataset['payment_method'].str.strip().str.capitalize()
correction_paiement = {
    "Credit card" : "Card",
    "Cash payment" : "Cash",
    "Mobilemoney" : "Mobile money"
}
dataset['payment_method'] = dataset['payment_method'].replace(correction_paiement)
dataset.loc[(dataset['customer_age'] < 18) | (dataset['customer_age'] > 80), 'customer_age'] = None
mediane = dataset['customer_age'].median()
dataset['customer_age'] =  dataset['customer_age'].fillna(mediane)
dataset.loc[(dataset['quantity'] < 1) | (dataset['quantity'] > 20), 'quantity'] = None
dataset['quantity'] = dataset.groupby('product_category')['quantity'].transform(
    lambda x: x.fillna(x.median())
)
Q1 = dataset.groupby('product_category')['unit_price'].transform(lambda x: x.quantile(0.25))
Q3 = dataset.groupby('product_category')['unit_price'].transform(lambda x: x.quantile(0.75))
IQR = Q3 - Q1
borne_basse = Q1 - 1.5 * IQR
borne_haute = Q3 + 1.5 * IQR

dataset.loc[(dataset['unit_price'] < borne_basse) | (dataset['unit_price'] > borne_haute), 'unit_price'] = None
dataset['unit_price'] = dataset.groupby('product_category')['unit_price'].transform(
    lambda x: x.fillna(x.median())
)
Q1 = dataset.groupby('region')['delivery_days'].transform(lambda x: x.quantile(0.25))
Q3 = dataset.groupby('region')['delivery_days'].transform(lambda x: x.quantile(0.75))
IQR = Q3 - Q1
borne_basse = Q1 - 1.5 * IQR
borne_haute = Q3 + 1.5 * IQR

dataset.loc[(dataset['delivery_days'] < borne_basse) | (dataset['delivery_days'] > borne_haute), 'delivery_days'] = None
dataset['delivery_days'] = dataset.groupby('region')['delivery_days'].transform(
    lambda x: x.fillna(x.median())
)
dataset['discount'] = dataset.groupby('product_category')['discount'].transform(
    lambda x: x.fillna(x.median())
).clip(0, 100)
mode = dataset['payment_method'].mode()
dataset['payment_method'] = dataset['payment_method'].fillna(mode[0])
dataset['payment_method'].isna().sum()
gender = {
    "F":"Female",
    "M":"Male",
    "female":"Female",
    "male":"Male",
    "MALE":"Male",
    "FEMALE":"Female"
}
dataset['customer_gender'] = dataset['customer_gender'].replace(gender)
cust_type = {
    "NEW":"New",
    "new":"New",
    "Returing":"Returning",
    "RETURNING":"Returning",
    "returning":"Returning"
}
#encodage 
dataset['customer_type'] = dataset['customer_type'].replace(cust_type)
dataset = pd.get_dummies(dataset, columns=['product_category','region','payment_method','customer_gender','customer_type'], drop_first=True)
dataset['month'].unique()
#mise en forme du mois sous format cyclique (cohérence des saisons de ventes)
mois_numero = dataset['month'].map({'January':0, 'February':1, 'March':2,'April':3,'May':4,'June':5,'July':6,'August':7,'September':8,'October':9,'November':10 , 'December':11})
dataset['month_sin'] = np.sin(2 * np.pi * mois_numero / 12)
dataset['month_cos'] = np.cos(2 * np.pi * mois_numero / 12)
mois_numero.isna().sum()
dataset = dataset.drop(columns=['month'])
#predictions
from sklearn.model_selection import train_test_split
X = dataset.drop(columns=['order_id', 'revenue'])
y = dataset['revenue']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train,y_train)
y_pred = model.predict(X_test)
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print(mae, rmse, r2)