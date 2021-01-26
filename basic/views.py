from django.shortcuts import render
from firebase_admin import firestore
import firestoreInitApp
import sys
import datetime
import bcrypt
import json


# Create your views here.

def home(request):
    return render(request,'index.html')



def quiz(request):
    if(request.method == 'GET'):
        return render(request , 'home.html')
    else :
        ## get all the details and the question set :

        question_set = int(request.POST['question_set'])
        qa_set = getQA(question_set)
        question_list = qa_set['questions']
        answer_list = qa_set['answers']
        number = int(request.POST['question_number'])
        print(number)


        if(number ==0):
            participant_data ={}
            name = request.POST['name']
            registration_number = request.POST['reg_no']
            start_time  = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

            participant_data['name'] = name
            participant_data['registration_number'] = registration_number
            participant_data['start_time'] = start_time

            db = firestore.client()
            db_ref = db.collection('participants')
            
            participant_doc = db_ref.document()
            participant_data['participant_id'] = participant_doc.id

            participant_doc.set(participant_data)


            context ={
                'question_set' : question_set,
                'question' : question_list[number],
                'question_number' : number + 1,
                'name' : name
            }

        elif(number == len(question_list)):
            answer = request.POST['answer']
            name = request.POST['name']
            if(answer == answer_list[number-1]):
                ### all answers are correct save the reponse here

                db = firestore.client()
                db_ref = db.collection('participants')
                db_document = db_ref.where('name','==',name).stream()
                last_time = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"))
                for d in db_document :
                    dict = d.to_dict()
                   
                    participant_id = dict['participant_id']
                    secret_key = participant_id
                    dict['end_time'] = last_time
                    db_ref.document(participant_id).set(dict)
                
                context  = {
                    'secret_key'  : secret_key,
                    'answer_list' : answer_list,
                    'name' : name,

                }
                print(question_set)
                return render(request,'ty.html' ,context)
            else :
                
                context ={
                    'question_set' : question_set,
                    'question' : question_list[number-1],
                    'question_number' : number,
                    'incorrect_answer' : 1,
                    'name' : name
                }
                return render(request , 'main.html' , context)
        else :
            ## get answer for previous question
            answer = request.POST['answer']
            name = request.POST['name']
            print(answer)
            if(answer == answer_list[number-1]):
                context ={
                    'question_set' : question_set,
                    'question' : question_list[number],
                    'question_number' : number +1,
                    'name' : name
                }

            else :
                context ={
                    'question_set' : question_set,
                    'question' : question_list[number-1],
                    'question_number' : number,
                    'incorrect_answer' : 1,
                    'name' : name
                }

        return render(request , 'main.html' , context)

def getQA(question_set):
    QA_Master_Set = {
        1 : {
            'questions' : ['Q1','Q2','Q3','Q4','Q5'],
            'answers' : ['A1','A2','A3','A4','A5']
        },

    }

    return QA_Master_Set[int(question_set)]
