###########################################Kahoot!
#shahar avramov to:Eran Bineth
###########################################
from socket import *
import threading
import thread
import time
import random
import Kahoot_db

class player:#class who save the client details
    def __init__(self,time_come,clientsock,name):
        self.time_come=time_come#save the time the client joined
        self.sock=clientsock#save his socket
        self.points=0#save his points
        self.name=name#save his name

    def getclientsock(self):#return socket
        return self.sock

    def gettime_come(self):#return time
        return self.time_come
    def getpoints(self):#return points
        return self.points
    def addPoints(self,add):#return add points
        self.points=self.points+add
    def getName(self):#return name
        return self.name
    def setName(self,new_name):#change name
        self.name=new_name
    def update_hasAnswer(self,has):#return if the client has answered
        self.has_answer=has
    def getHasAnswer(self):#return if the client answered
        return self.has_answer

class game:#class who is charge about whole the game progress
    def __init__(self):
        self.clients=[]#list of the clients
        self.quiz=analayze_questionsText(open(self.random_quiz(),"rb"))#send the quiz file and get class of the questions and answers of the quiz
        self.numOfAnswers=0#save the number of answers he got from the clients
        self.num_deleted=0

    def random_quiz(self):#choose on quiz from the free he have
        name_quiz="quiz"+str(random.randint(1,3))+'.txt'
        print name_quiz
        #return name_quiz
        return 'quiz2.txt'

    def add_client(self,client):#add client to the list
       self.clients.append(client)

    def game_progress(self):#def which pass the questions,send the and than send the score of every player
        for i in range(5):
            questions = self.quiz.get_question()[i]#get the questions according to the number
            answers = self.quiz.get_answers()[i]#same with answers
            random.shuffle(answers)
            self.send_questions(questions,answers,self.quiz.get_true_answers()[i])#
            if len(self.clients) ==0:#check if there is a problem
                return 0#if there is finish working
            self.num_deleted=0

        points_lst=[]
        for j in range(len(self.clients)):#get the points
            points_lst.append(self.clients[j].getpoints())

        points_lst.sort()#sort the list from small to big
        points_lst.reverse()

        for i in self.clients:#send to every client his score
            for j in range(len(points_lst)):
                if i.getpoints()==points_lst[j]:
                    msg="%i,%i,%s"%(i.getpoints(),(j+1),i.getName())
                    i.getclientsock().send(msg)
                    break

    def send_questions(self,question,answers,true_answer):
        quiters=[]#save the quiter
        for i in range(len(self.clients)):
            msg=question+','+answers[0]+','+answers[1]+','+answers[2]+','+answers[3]+','+true_answer#build the quiz
            try:#try to send the quiz
                self.clients[i].getclientsock().send(msg)#send the quiz
                thread.start_new_thread(self.take_answers, (self.clients[i],time.clock(),true_answer,i))#open thread which get the client's answer

            except:#if doesnt work
                quiters.append(i)#add the bad client to the list

        for i in quiters:#pass the quiters and kick out them
            self.clients.pop(i)

        while 1:#check if whole the people answered
            if self.numOfAnswers==len(self.clients):
                if len(self.clients) == 0:
                    return 0
                self.numOfAnswers=0
                break

        quiters = []#reset
        for i in range(len(self.clients)):#send to every player if he answered or he missed the chance
            try:
                if not self.clients[i].getHasAnswer():
                    self.clients[i].getclientsock().send("time out")
                else:
                    self.clients[i].getclientsock().send("every_one_answer")
            except:
                quiters.append(i)#if he have a probel he kick the player out

        for i in quiters:
            self.clients.pop(i)
        time.sleep(2)

    def take_answers(self,client,time_ask,true_answer,index_to_remove):#take answer from the player
        answer="nope"
        while 1:
            try:#try to recieve the question
                answer=client.getclientsock().recv(1024)
            except timeout:#if time out
                if answer == "nope":
                    if time.clock() - time_ask >= 20:#check if the player passed the time he can answer
                        client.update_hasAnswer(False)#if he passed update his answer to false
                        self.numOfAnswers = self.numOfAnswers + 1
                        return 0
                else:
                    client.update_hasAnswer(True)#if he answered uptade his answer to true
                    break
            except:#if another problem, kick the player out
                deleted=self.num_deleted
                while not deleted==0:
                    index_to_remove = index_to_remove - 1
                    deleted=deleted-1

                self.clients.pop(index_to_remove)
                self.num_deleted=self.num_deleted+1

                return 0

        if answer==true_answer:#if he has answered correctly +20
            client.addPoints(20)
        self.numOfAnswers = self.numOfAnswers + 1
        return 0

class analayze_questionsText:#get quiz file and build list of questions,answer and true answers

    def __init__(self,questions):
        self.quiz=questions
        self.lines=self.quiz.readlines()

    def get_question(self):
        return [self.lines[0],self.lines[5],self.lines[10],self.lines[15],self.lines[20]]
        #get the questions from the text file
    def get_answers(self):
        return [[self.lines[1],self.lines[2],self.lines[3],self.lines[4]],[self.lines[6],self.lines[7],self.lines[8],self.lines[9]],[self.lines[11],self.lines[12],self.lines[13],self.lines[14]],[self.lines[16],self.lines[17],self.lines[18],self.lines[19]],[self.lines[21],self.lines[22],self.lines[23],self.lines[24]]]
        #get answers
    def get_true_answers(self):
        return [self.lines[4],self.lines[9],self.lines[14],self.lines[19],self.lines[24]]

global game_kahoot
BUFSIZ = 1024

def collect_to_game(serversock):#collect the people to the game
    global game_kahoot
    clients=game_kahoot.clients
    if len(clients)>=2:#check if alredy 2 player
        return True

    time_player=clients[0].gettime_come()
    clientsock, addr="no","no"
    while time.clock()-time_player<10:#wait 10 seconds and add clients
        try:
            clientsock, addr = serversock.accept()
        except:
            pass
        if (not clientsock == "no") and (not addr == "no"):
            print '...connected from:', addr
            name = clientsock.recv(1024)

            if name == "admin":
                admin_action(serversock,clientsock)
                exit()
            game_kahoot.add_client(player(time.clock(), clientsock, name))
            clientsock.settimeout(1)
        clients = game_kahoot.clients
        clientsock, addr = "no", "no"
        if len(clients) == 4:
            return True

    if len(clients)>=2:
        return True

    serversock.setblocking(1)#wait for last player to join
    clientsock, addr = serversock.accept()
    print '...connected from:', addr
    name = clientsock.recv(1024)
    if name == "admin":
        admin_action(serversock,clientsock)
        exit()
    clientsock.settimeout(1)
    game_kahoot.add_client(player(time.clock(), clientsock, name))
    clients = game_kahoot.clients
    return True

def admin_action(serversock,clientsock):
    global game_kahoot

    for i in game_kahoot.clients:
        i.getclientsock().close()
    serversock.close()
if __name__ == '__main__':
    while 1:
        game_kahoot=game()

        HOST = 'localhost'
        PORT = 50008
        ADDR = (HOST, PORT)
        serversock = socket(AF_INET, SOCK_STREAM)
        serversock.bind(ADDR)
        serversock.listen(2)

        status = Kahoot_db.update("Shahar", HOST, PORT)["status"]

        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        name=clientsock.recv(1024)
        if name=="admin":
            admin_action(serversock,clientsock)
            exit()

        game_kahoot.add_client(player(time.clock(), clientsock,name))#add the client to the clients list

        clientsock.settimeout(1)
        serversock.settimeout(5)

        collect_to_game(serversock)#coolect minimum 2 player to the game(maximum 4)
        game_kahoot.game_progress()#start the game
