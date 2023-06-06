# importing dependencies
import warnings

import pandas as pd

from model import Model
from preprocessing import Preprocessing


class MainClass:
    def __ini__(self):
        self.data = pd.DataFrame()

    def main(self):
        preprocess = Preprocessing()
        # fetch data from the dataset
        self.data = preprocess.read_data()

        # preprocessing steps
        self.data = preprocess.preprocessing(data=self.data)

        # encode technical skills column which contain comma separated values
        self.data = preprocess.technical_skills_encoding(data=self.data)

        # encoding all categorical values
        self.data = preprocess.encode_categorical(data=self.data)

        # call function where unique values of technical skills store in dictionary
        tech_dict = preprocess.ret_uni()

        # call all encoded values stored in functiom
        encode_dict = preprocess.ret_encode()


        # model function stored in variable
        modelobj = Model()

        # splitting dataset into train and test data
        modelobj.split_data(data=self.data)

        # call model and perform further steps
        modelobj.Randomforest_model()

        # result contain accuracy,matrix,classification_report
        modelobj.result()

        # now make a pickle file of our mode named as model.pkl
        # modelobj.pickle_file()

        # Take user input for prediction
        # modelobj.predict_real(tech_dict=tech_dict, encode_dict=encode_dict)



if __name__ == "__main__":

    warnings.filterwarnings('ignore')

    # OBJ OF CLASS
    obj = MainClass()
    obj.main()
