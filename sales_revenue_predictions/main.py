import pandas as pd
import numpy as np 
dataset = pd.read_csv('ventes_dataset_sale.csv')
#nettoyage des données 
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
dataset.loc[(dataset['customer_age'] < 18) | (dataset['customer_age'] > 80), 'customer_age'] = np.nan
dataset.loc[(dataset['quantity'] < 1) | (dataset['quantity'] > 20), 'quantity'] = np.nan
dataset.loc[(dataset['unit_price'] < 0) | (dataset['unit_price'] > 1000), 'unit_price'] = np.nan
dataset.loc[(dataset['delivery_days'] < 0) | (dataset['delivery_days'] > 30), 'delivery_days'] = np.nan
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
dataset['customer_type'] = dataset['customer_type'].replace(cust_type)
#codage et entrainement 
from sklearn.model_selection import train_test_split
x = dataset.drop(columns=['order_id','month'])
y = dataset['revenue']
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)
numeric_columns = [
    "quantity",
    "unit_price",
    "discount",
    "delivery_days",
    "customer_age",
]
categorical_columns = [
    "product_category",
    "region",
    "payment_method",
    "customer_gender",
    "customer_type"
]
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(drop='first',handle_unknown='ignore'))
])
preprocessor = ColumnTransformer([
    ('num',numerical_pipeline,numeric_columns),
    ('cat',categorical_pipeline,categorical_columns)
])
from sklearn.linear_model import LinearRegression
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])
model.fit(x_train,y_train)
y_pred = model.predict(x_test)
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print(mae)
print(rmse)
print(r2)
x_predict = pd.DataFrame({
    'product_category': ['Food', 'Electronics', 'Books'],
    'region': ['Conakry', 'Nzerekore', 'Labe'],
    'payment_method': ['Cash', 'Card', 'Mobile money'],
    'quantity': [5, 2, 10],
    'unit_price': [20.0, 150.0, 15.0],
    'discount': [10, 20, 5],
    'delivery_days': [3, 5, 2],
    'customer_age': [30, 45, 25],
    'customer_gender': ['Male', 'Female', 'Female'],
    'customer_type': ['New', 'Returning', 'New']
})
y_predict = model.predict(x_predict)
for i, pred in enumerate(y_predict):
    print(f"Prediction for input {i+1}: {pred:.2f}")
print(x_predict)