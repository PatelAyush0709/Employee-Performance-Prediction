from typing import List

import pickle

from flask import Flask, render_template, request, redirect


# flask constructor
app = Flask(__name__)

# create a list of dummy values
new_list_one = [i for i in range(0, 22)]

# create dictionary of department wise skills and unique values in technical skills
skills_department = {
                    'database': {'MSSQL', 'PowerBI', 'MySQL', 'SSRS', 'MongoDB', 'DataWarehouse', 'Datamining', 'DataModelling', 'Oracle'},
                    'frontend': {'HTML', 'CSS', 'Bootstrap',  'JavaScript', 'AngularJS', 'NodeJS'},
                    'devops': {'CloudManagement',  'Git', 'Security', 'Jenkins', 'Ansible', 'Automation'},
                    '.net': {'ADO.Net', '.NetCoreFramework', 'ASP.Net', 'VisualBasic.Net', 'CSharp', 'LinQ', 'MVC', 'EntityFramework'},
                    'mobile': {'Android', 'iOS', 'Flutter', 'ReactNative'},
                    'python & ml': {'Python', 'MLModels', 'DLModels', 'TensorFlow', 'MSSQL', 'Flask', 'Django', 'Pytorch', 'Postgresql'}
                    }

# whenever you run the main file in model.pkl file this below dictionary should be changed hence copy the dictionary from terminal and paste it here

dictionary1 = {
                '.netcoreframework': 0, 'datamodelling': 1, 'mlmodels': 2, 'asp.net': 3, 'bigdata': 4, 'pytorch': 5,
                'powerbi': 6, 'visualbasic.net': 7, 'entityframework': 8, 'python': 9, 'ios': 10, 'ssis': 11, 'oracle': 12,
                'git': 13, 'mssql': 14, 'html': 15, 'datamining': 16, 'cloudmanagement': 17, 'mysql': 18, 'ansible': 19,
                'flask': 20, 'postgresql': 21, 'reactnative': 22, 'datawarehouse': 23, 'bootstrap': 24, 'automation': 25,
                'tensorflow': 26, 'ado.net': 27, 'ssrs': 28, 'csharp': 29, 'linq': 30, 'flutter': 31, 'nodejs': 32,
                'django': 33, 'javascript': 34, 'mvc': 35, 'mongodb': 36, 'android': 37, 'css': 38, 'angularjs': 39,
                'dlmodels': 40, 'vue': 41, 'jenkins': 42, 'security': 43
                }



@app.route("/", methods=['POST', 'GET'])
def page1():
    if request.method == 'POST':
        # submitting the form
        result = request.form

        # get values of education level
        education_level = result.get('Education_level')
        if education_level == 'bachelors':
            assume = 0
        elif education_level == 'masters':
            assume = 1
        else:
            assume = 2
        new_list_one[0] = assume

        # get values of department
        department = result.get('Department')

        new_list_one[1] = department

        # get values of job tenure
        job_tenure = int(result.get('Job_tenure'))
        new_list_one[8] = job_tenure


        return redirect("page2")
    return render_template('design.html')


@app.route("/page2", methods=['POST', 'GET'])
def page2():
    # find skills according to department
    skills = skills_department[new_list_one[1]]

    if request.method == 'POST':
        result = request.form

        # get values of code quality
        code_quality = result.get('Code quality')
        if code_quality == 'excellent':
            assume = 0
        elif code_quality == 'good':
            assume = 1
        else:
            assume = 2
        new_list_one[6] = assume

        # get values of quality of work
        quality_of_work = result.get('Quality of Work')
        if quality_of_work == 'excellent':
            assume = 0
        elif quality_of_work == 'good':
            assume = 1
        else:
            assume = 2
        new_list_one[4] = assume

        # get values of time management
        time_management = result.get('Time Management')
        if time_management == 'excellent':
            assume = 0
        else:
            assume = 1
        new_list_one[7] = assume

        # get values of workload
        workload = result.get('Workload')
        if workload == 'high':
            assume = 0
        elif workload == 'low':
            assume = 1
        else:
            assume = 2
        new_list_one[5] = assume

        # get values of debugging skills
        debugging_skills = result.get('Debugging Skills')
        if debugging_skills == 'excellent':
            assume = 0
        elif debugging_skills == 'good':
            assume = 1
        else:
            assume = 2
        new_list_one[2] = assume

        # get values of technical skills
        technical_skills = result.getlist('Technical Skills')
        technical_skills1 = [value.lower() for value in technical_skills]
        # inp_list = [skill for skill in technical_skills.split(',')]

        # take unique numeric values from the dictionary1
        k = 11
        for ele in technical_skills1:
            for key, value in dictionary1.items():
                if key == ele:
                    new_list_one[k] = value
                    k = k + 1
                    break

        while k:
            if k == 22:
                break
            new_list_one[k] = -1
            k = k + 1

        # getting values of department in numeric form according to label encoding in preprocessing file
        if new_list_one[1] == '.net':
            assume = 0
        elif new_list_one[1] == 'database':
            assume = 1
        elif new_list_one[1] == 'devops':
            assume = 2
        elif new_list_one[1] == 'frontend':
            assume = 3
        elif new_list_one[1] == 'mobile':
            assume = 4
        else:
            assume = 5
        new_list_one[1] = assume

        return redirect("page3")
    return render_template('design2.html', skills=skills)


@app.route("/page3", methods=['POST', 'GET'])
def page3():
    if request.method == 'POST':
        result = request.form

        # get values of project completion rate
        project_completion_rate = int(result.get('Project_Completion_rate'))
        new_list_one[10] = project_completion_rate

        # get values of learning growth
        learning_growth = result.get('Learning_Growth')
        if learning_growth == 'no':
            assume = 0
        else:
            assume = 1
        new_list_one[3] = assume

        # get values of peer feedback
        peer_feedback = int(result.get('Peer_Feedback'))
        new_list_one[9] = peer_feedback

        # print the final list of values
        print(new_list_one)

        # import model pickle file
        file = open('pickle/model.pkl', 'rb')
        model = pickle.load(file)  # Replace 'your_model.pkl' with the path to your trained model file

        # here numeric value into categorical value according to label encoding
        answer = model.predict([new_list_one])[0]
        if answer == 2:
            answer = 'Needs Improvement'
        elif answer == 1:
            answer = 'Meets Expectation'
        elif answer == 0:
            answer = 'Exceeds Expectation'

        return render_template("design3.html", answer=answer)
    return render_template("design3.html")


# Application to run
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
