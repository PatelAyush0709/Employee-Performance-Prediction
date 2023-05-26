import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns


class Preprocessing():
    def __init__(self):
        self.unique_values_ret = {}
        self.encode_dict = []

    # Reading data
    def read_data(self):
        return pd.read_csv('../Data/EmployeeData.csv')

    # covert values into lower
    def convert_to_lower(self, data, cols):
        for col in cols:
            data[col] = data[col].apply(lambda x: x.lower())
        return data

    # data preprocessing
    def preprocessing(self, data):
        # drop unused column
        data = data.drop(['Employee Id'], axis=1)

        cols_to_convert = ['Education Level', 'Department', 'Debugging_Skills', 'Learning_Growth', 'Quality_of_Work',
                           'Workload', 'Code_Quality',
                           'Time_Management', 'Technical Skills']

        data = self.convert_to_lower(data, cols_to_convert)

        # replace poor by good in Time_Management column
        data['Time_Management'] = data['Time_Management'].str.replace('poor', 'good')

        # drop low value column from dataset because we don't require according to documentation
        data = data[(data.Code_Quality != 'low') & (data.Quality_of_Work != 'low') & (data.Debugging_Skills != 'low')]

        # replace c# by csharp because # is a symbol that's why it is not count
        data['Technical Skills'] = data['Technical Skills'].str.replace('#', 'sharp')

        # remove white spaces
        data['Technical Skills'] = data['Technical Skills'].str.replace(' ', '')

        # check correlation between features
        print('\n\nCorrelation matrix: \n', data.corr())
        plt.figure(figsize=(20, 10))
        sns.heatmap(data.corr(), annot=True)
        plt.show()

        # Plot graphs
        print('count plot of target column: ')
        sns.countplot(x=data['Performance'])
        plt.show()
        return data

    def technical_skills_encoding(self, data):
        # split values by comma using split function
        values = data['Technical Skills'].str.split(',')

        unique_values = {}
        for index, value in enumerate(set([value.strip() for sublist in values for value in sublist])):
            unique_values[value] = index
        self.unique_values_ret = unique_values
        print(self.unique_values_ret)

        # place above unique values into dataset using apply method
        data['Technical Skills'] = data['Technical Skills'].apply(
            lambda row: [unique_values[value.strip()] for value in row.split(',')])

        # find max. length in technical skills column
        max_length = values.apply(len).max()

        # create new columns for max length skills
        data['Technical Skills'] = data['Technical Skills'].astype(str)
        for i in range(max_length):
            data[f'Skill_{i + 1}'] = data['Technical Skills'].str.split(',').str.get(i)

        # cleaning technical skills column
        data = data.applymap(
            lambda x: x.replace('[', '').replace(']', '').replace("'", '') if isinstance(x, str) else x)

        # fill NAN values by 0
        data.fillna(-1, inplace=True)
        print('After Filling NaN values: \n', data.head())

        return data

    def label_encode(self, data, cols):
        lencode = LabelEncoder()
        for col in cols:
            data[col] = lencode.fit_transform(data[col])
            print('Mapping of  ', col, ':', dict(zip(lencode.classes_, lencode.transform(lencode.classes_))))
            temp = dict(zip(lencode.classes_, lencode.transform(lencode.classes_)))
            self.encode_dict.append(temp)
        return data

    # Encoding Categorical
    def encode_categorical(self, data):

        cols_to_encode = ['Education Level', 'Department', 'Debugging_Skills', 'Learning_Growth', 'Quality_of_Work',
                          'Workload',
                          'Code_Quality',
                          'Time_Management', 'Performance']

        data = self.label_encode(data, cols_to_encode)
        return data

    def ret_uni(self):
        return self.unique_values_ret

    def ret_encode(self):
        return self.encode_dict
