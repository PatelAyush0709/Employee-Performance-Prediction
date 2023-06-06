# importing dependencies
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
from preprocessing import Preprocessing


class Model:
    def __init__(self):
        self.data = None
        self.x, self.y, self.xtest, self.xtrain, self.ytrain, self.ytest, self.predict = None, None, None, None, None, None, None
        self.model = None

    def split_data(self, data):

        self.data = data
        self.data.drop(['Technical Skills'], axis=1, inplace=True)

        # split data into target and feature
        self.x = self.data.drop('Performance', axis=1)
        self.x = self.x[
            ['Education Level', 'Department', 'Debugging_Skills', 'Learning_Growth', 'Quality_of_Work', 'Workload',
             'Code_Quality', 'Time_Management', 'Job Tenure', 'Peer_Feedback', 'Project_Completion_Rate', 'Skill_1',
             'Skill_2', 'Skill_3', 'Skill_4', 'Skill_5', 'Skill_6', 'Skill_7', 'Skill_8', 'Skill_9', 'Skill_10',
             'Skill_11']]
        self.y = self.data['Performance']

        # Split dataset into train and test data
        self.xtrain, self.xtest, self.ytrain, self.ytest = train_test_split(self.x, self.y, test_size=0.3)

    def Randomforest_model(self):

        # model call
        self.model = RandomForestClassifier()

        # model fitting
        self.model.fit(self.xtrain, self.ytrain)

        # prediction of the model
        self.predict = self.model.predict(self.xtest)
        print('predicted value: ', self.predict)

    def result(self):
        # accuracy of the model
        accuracy = accuracy_score(self.predict, self.ytest)
        print('Accuracy of the Model: ', accuracy * 100)

        # check matrix of the model
        matrix = confusion_matrix(self.predict, self.ytest)
        print('confusion matrix: ', matrix)

        # check report of the dataset
        report = classification_report(self.predict, self.ytest)
        print('classification report: ', report)

    def pickle_file(self):
        pkl_file = open("model.pkl", "wb")
        pickle.dump(self.model, pkl_file)
        pkl_file.close()
        print('---> Model is saved in Pickle File and Now its Ready to Use')



    # take User Input
    def predict_real(self, tech_dict, encode_dict):
        # create an empty list
        r_data = []

        # take user inputs
        education_level = input("Enter Education Level (Masters,Bachelors, PhD) : ")
        department = input("Enter Department (Python & ML, Database, Mobile, Devops, .Net, Frontend) : ")
        debugging_skills = input("Enter Debugging skills excellent, good, poor :")
        learning_rate = input("Enter learning Rate (yes/no) : ")
        quality_of_work = input("Enter Quality of work excellent, good, poor: ")
        workload = input("Enter workload high low medium : ")
        code_quality = input("Enter code quality excellent, good, poor : ")
        time_management = input("Enter Time management skills excellent, good: ")

        # perform label encoding on below columns
        inp_list = [education_level, department, debugging_skills, learning_rate, quality_of_work, workload,
                    code_quality, time_management]
        for count, ele in enumerate(inp_list):
            for key, value in encode_dict[count].items():
                if key == ele:
                    # now append this encoded values in empty list
                    r_data.append(value)
                    break

        # this is already in numeric form so append directly into the empty list
        job_tenure = int(input("Enter your Job Tenure : "))
        peer_feedback = int(input("Enter peer feedback from the range of 1 to 10 : "))
        project_completion_rate = int(input("Enter Project Completion Rate in percentage : "))

        r_data.append(job_tenure)
        r_data.append(peer_feedback)
        r_data.append(project_completion_rate)

        # technical skills field contain comma separated values
        skills = input("Enter skills (for example: python,html,mysql,csharp,android,git,etc): ")

        # separated values by comma using split function
        inp_list = [skill for skill in skills.split(',')]

        # now compare this values with unique values dictionary
        for ele in inp_list:
            for key, value in tech_dict.items():
                if key == ele:
                    # append numeric values into the empty list
                    r_data.append(value)
                    break

        # now here we have total 11 skills column so replace values upto 11 skills
        if len(inp_list) == 1 and inp_list == ['']:
            r_data.extend(11 * [0])
        else:
            r_data.extend((11 - len(inp_list)) * [0])


        # now predict the r_data list
        ans = self.model.predict([r_data])[0]

        # now compare this numeric answer with target column
        for key, value in encode_dict[len(encode_dict) - 1].items():
            if value == ans:
                ans = key

        print(ans)
