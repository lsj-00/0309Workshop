import argparse
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from statsmodels.api import OLS
from statsmodels.tools import add_constant
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from joblib import dump, load

logging.basicConfig(level=logging.INFO)

features = ['Age','KM','FuelType','HP','MetColor', 'Automatic', 'CC', 'Doors','Weight']
numeric_features = ['Age','KM','HP','MetColor', 'Automatic', 'CC', 'Doors','Weight']
categorical_features = ['FuelType']
label = 'Price'

def run(data_path, model_path):
    # Read the CSV file
    df = pd.read_csv(data_path)

    numeric_transformer = MinMaxScaler()
    categorical_transformer = OneHotEncoder()
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    # Set initial seed for reproducibility
    np.random.seed(123)
    logging.info('Start Train-Test Split...')
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(df[features], \
                                                        df[label], \
                                                        test_size=0.2, \
                                                        random_state=0)
                                                        
    X_train = preprocessor.fit_transform(X_train)
    # Initial linear regression model
    logging.info('Start Training...')
    

    model = OLS(y_train, X_train).fit()

    # Evaluate and Deploy
    logging.info('Evaluate...')
    X_test = preprocessor.transform(X_test)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    logging.info(model.summary())
    logging.info("\nMean Squared Error on Test Set: {}".format(mse))
    
    logging.info('Deploy...')
    dump(model, model_path+'mdl.joblib')
    dump(features, model_path+'raw_features.joblib')
    
    logging.info('Training completed.')
    return None

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_path", type=str)
    argparser.add_argument("--model_path", type=str)
    args = argparser.parse_args()
    run(args.data_path, args.model_path)

