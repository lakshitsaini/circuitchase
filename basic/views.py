from django.shortcuts import render
from firebase_admin import firestore
import firestoreInitApp
import sys
import datetime
import bcrypt
import json
import random
import pytz
IST = pytz.timezone('Asia/Kolkata') 
# Create your views here.

def home(request):
    return render(request,'index.html')

#-------------------load test view-------------------------
def loaderio(request):
    return render(request,'loaderio-f3c731dc5ea8a201c360f115e6bedceb.html')


def getSet(reg_no):
    db = firestore.client()
    db_ref = db.collection('participants')
    db_document = db_ref.where('registration_number','==',reg_no).stream()
    
    if(len(list(db_document))):
        print("hi")
        db_document2 = db_ref.where('registration_number','==',reg_no).stream()
        for d in db_document2 :
            dict = d.to_dict()
            print(dict)
            return(dict['question_set'])
    else:
        return random.randint(1,4)


def quiz(request):
    if(request.method == 'GET'):
        return render(request , 'home.html')
    else :
        ## get all the details and the question set :

        
        

        number = int(request.POST['question_number'])
        temp_question_list = getQA(1)['questions']
        if(number ==0):

        
            
            participant_data ={}
            name = request.POST['name']
            registration_number = request.POST['reg_no']
            question_set = int(getSet(registration_number))
            qa_set = getQA(question_set)
            question_list = qa_set['questions']
            answer_list = qa_set['answers']
            hint_list = qa_set['hints']
            print(question_set)
            start_time  = datetime.datetime.now(IST).strftime("%Y-%m-%dT%H:%M:%S.%f")

            participant_data['name'] = name
            participant_data['registration_number'] = registration_number
            participant_data['start_time'] = start_time

            db = firestore.client()
            db_ref = db.collection('participants')
            
            participant_doc = db_ref.document()
            participant_data['participant_id'] = participant_doc.id
            participant_data['question_set'] = question_set
            participant_doc.set(participant_data)


            context ={
                'question_set' : question_set,
                'question' : question_list[number],
                'question_number' : number + 1,
                'name' : name,
                'hint' : hint_list[number]
            }

        elif(number == len(temp_question_list)):
            question_set = int(request.POST['question_set'])
            qa_set = getQA(question_set)
            question_list = qa_set['questions']
            answer_list = qa_set['answers']
            hint_list = qa_set['hints']
            number = int(request.POST['question_number'])
            answer = request.POST['answer'].lower()
            name = request.POST['name']
            if(answer == answer_list[number-1].lower()):
                ### all answers are correct save the reponse here
                circuit_clue = {
                    1 : 'Connect the components such that you see green light but not red light. But when you reverse the polarity of the battery while keeping the remaining circuit the same, you will see red light but not green light. This is a game of polarities, take utmost care! Don’t forget to support the LEDs with one resistor each. You will need: 1 battery (9V), 2 LEDs (one red and one green), 2 resistors (1k ohm each), 1 switch, connecting wires.',
                    2 : 'Good work! Now make a circuit which mimics the OR logic. Use the components you hunted for and take care of polarities! Let your LED glow in 3 out of 4 cases of a 2 input OR logic. If you are successful, then congratulations! You just simulated an OR logic gate! You will need: 1 battery (9V), 1 LED, 2 resistors (1k ohm each), 2 switches, connecting wires. ',
                    3 : 'Now this is a stubborn circuit! It mimics an AND logic gate and it wants both inputs high. Use your LED to indicate the high output in that one special case out of all the four. Because the AND logic says: Im logical and quite demanding, I want both this and that. Solve this circuit and simulate the working of AND gate! You will need: 1 battery (9V), 1 LED, 1 resistor (1k ohm), 2 switches, connecting wires.',
                    4 : 'Get three LEDs: Red, Green, Yellow and get a pair of resistor-switch for each LED. What do these colours prompt you for making? Join the components in such a way that you control the traffic!You will need: 1 battery (9V), 3 LEDs (one red, one yellow and one green), 3 resistors (1k ohm each), 3 switches, connecting wires. '
                }
                db = firestore.client()
                db_ref = db.collection('participants')
                db_document = db_ref.where('name','==',name).stream()
                last_time = str(datetime.datetime.now(IST).strftime("%Y-%m-%dT%H:%M:%S.%f"))
                for d in db_document :
                    dict = d.to_dict()
                   
                    participant_id = dict['participant_id']
                    secret_key = participant_id
                    dict['end_time'] = last_time
                    db_ref.document(participant_id).set(dict)
                
                context  = {
                    'secret_key'  : "qJJVd3sYHsj9bxf6mvNt",
                    'answer_list' : answer_list,
                    'name' : name,
                    'circuit_clue' : circuit_clue[question_set]

                }
                print(question_set)
                return render(request,'ty.html' ,context)
            else :
                
                context ={
                    'question_set' : question_set,
                    'question' : question_list[number-1],
                    'question_number' : number,
                    'incorrect_answer' : 1,
                    'name' : name,
                    'hint' : hint_list[number-1]
                }
                return render(request , 'main.html' , context)
        else :
            ## get answer for previous question
            question_set = int(request.POST['question_set'])
            qa_set = getQA(question_set)
            question_list = qa_set['questions']
            answer_list = qa_set['answers']
            hint_list = qa_set['hints']
            number = int(request.POST['question_number'])
            answer = request.POST['answer'].lower()
            name = request.POST['name']
            print(answer)
            if(answer == answer_list[number-1].lower()):
                context ={
                    'question_set' : question_set,
                    'question' : question_list[number],
                    'question_number' : number +1,
                    'name' : name,
                    'hint' : hint_list[number]
                }

            else :
                context ={
                    'question_set' : question_set,
                    'question' : question_list[number-1],
                    'question_number' : number,
                    'incorrect_answer' : 1,
                    'name' : name,
                    'hint' : hint_list[number-1]

                }

        return render(request , 'main.html' , context)

def getQA(question_set):
    QA_Master_Set = {
        1 : {
            'questions' : ['Clue 1: I glow with happiness when you choose to travel in the right direction.',
            'Clue 2: I am the traffic light of your circuit, but I don’t have colours. I give signals equivalent to only red or green. When my mood is off, you call me open. When my mood is on, you call me closed.',
            'Clue 3: I alone can decide the power dissipated in the circuit. Oh also, Mr. B.B.Roy from Great Britain is my very good friend.',
            'Clue 4: I am worth 9 mitochondria. Behold! If your circuit is the cell then I am the mitochondria.',
            'Clue 5: If the circuit is a prom night for the components, then I am their tinder. My purpose is to connect two lovers with least resistance.'],
            'answers' : ['LED','Switch','Resistor','Battery','Wire'],
            'hints' : ['Hint 1','Hint 2','Hint 3','Hint 4','Hint 5']
        },
        2 : {
            'questions' : ['Clue 1:  I am the most disappointed one among all components because everyone calls me by my 3-lettered acronym instead of my full name, yet I provide your lives with a bright light of hope.',
            'Clue 2: I have 2 heads, one is optimistic and the other pessimistic. I must surely use both of them to serve the purpose of my life. Without me, all other components could be useless.',
            'Clue 3: I am the simplest component of your circuit, yet your circuit won’t work without me. I wear clothes of various colours, but only one colour at a time. Do you remember matching my colours in the game of ‘Among Us’?',
            "Clue 4: George Simon Ohm's constant which is a building block for all the circuits around us.",
            'Clue 5: My position decides the fate of your circuit. I decide whether the circuit is on or off.'],
            'answers' : ['LED','Battery','Wire','resistor','switch'],
            'hints' : ['Hint 1','Hint 2','Hint 3','Hint 4','Hint 5']
        },
        3 : {
            'questions' : ['Clue 1 : I am the stored version of electric poles. I give life to your circuit.',
            'Clue 2: I have a longer lifespan and two legs (one longer than the other). Recombination of electrons and holes is something on which I live.',
            'CLue 3: I am like a bridge between two paths, if you want to pass I need to be closed. If I open my mouth, your circuit will not work.',
            'Clue 4: What do you call your female sibling trapped between two ‘R’s?',
            'Clue 5:  I am the one who keeps everyone connected, but I am often taken for granted. I know my electrons respect me, because I provide them a path to run.'],
            'answers' : ['Battery','LED','Switch','Resistor','Wire'],
            'hints' : ['Hint 1','Hint 2','Hint 3','Hint 4','Hint 5']
        },
        4 : {
            'questions' : ["Clue 1: I am the god of all components in a circuit, if you have contact with my both hands I'll provide constant blessings.",
            'Clue 2: All stars are born in the dark and all darkness dies because of me.',
            'Clue 3: I have two moods. When my mood is off, you call me open. When my mood is on, you call me closed.',
            'Clue 4: Assume you are swimming in a river and the flow of water is in the opposite direction. I do the same work as flow of water is doing. Who am I?',
            'CLue 5: You have the battery and bulb, but they are not talking to each other. I can establish their friendship by joining their hands and they will provide you with the light of friendship. Who am I?'],
            'answers' : ['Battery','LED','Switch','Resistor','Wire'],
            'hints' : ['Hint 1','Hint 2','Hint 3','Hint 4','Hint 5']
        },
    }

    return QA_Master_Set[int(question_set)]
