###########################################Kahoot!
#shahar avramov to:Eran Bineth
###########################################
import socket as s
import os
from Tkinter import *
import tkFont
import threading
import thread
import time
import Kahoot_db


class tkinter_questions:#build the whole GUI
    def __init__(self):
        self.chosen_ans=""#give a default value in case the player doesn't answer

    def update_q_a(self,question,answers,true_answer):#update the variables
        self.question = question
        self.answers = answers
        self.true_answer = true_answer


    def build_root(self):#buld screen
        self.screen = Tk()
        for i in range(6):  # make the weight to 1
            self.screen.columnconfigure(i, weight=1)

        self.screen.title("Kahoot!!")  # his title
        self.screen.geometry('600x430')  # his size
        self.screen.resizable(width=FALSE, height=FALSE)
        self.screen["background"] = "#0085E5"

    def build_QuestionScreen(self):#build the questions screen
        font_question = tkFont.Font(weight=tkFont.BOLD, size=25)


        self.q_label=Label(self.screen,fg="black",text=self.question,font=font_question,bg="#0085E5",wraplength=580)
        self.q_label.grid(row=0,column=0,columnspan=6)
        font_answers = tkFont.Font(weight=tkFont.BOLD, size=15)

        self.a1_bth = Button(self.screen, text=self.answers[0], bg="red", height=2, width=8, command=self.action_bth1,font=font_answers)#every button get one answer
        self.a1_bth.grid(row=1, column=0, columnspan=6, pady=2, sticky="wens")
        self.a2_bth = Button(self.screen, text=self.answers[1], bg="green", height=2, width=8, command=self.action_bth2,font=font_answers)
        self.a2_bth.grid(row=2, column=0, columnspan=6, pady=2, sticky="wens")
        self.a3_bth = Button(self.screen, text=self.answers[2], bg="blue", height=2, width=8, command=self.action_bth3, font=font_answers)
        self.a3_bth.grid(row=3, column=0, columnspan=6, pady=2, sticky="wens")
        self.a4_bth = Button(self.screen, text=self.answers[3], bg="yellow", height=2, width=8, command=self.action_bth4,font=font_answers)
        self.a4_bth.grid(row=4, column=0, columnspan=6, pady=2, sticky="wens")
        self.screen.mainloop()

        self.q_label.destroy()#clean the screen for the next screen
        self.a1_bth.destroy()
        self.a2_bth.destroy()
        self.a3_bth.destroy()
        self.a4_bth.destroy()

        self.buildWait_screen()#build the screen which show the correct answer

    def action_bth1(self):
        print 'll'
        self.chosen_ans = self.a1_bth["text"]#take the chosen answer
        client_sock.getSocket().send( self.chosen_ans)#send it to check if correct

        while 1:#check if every one answered
            if answer_all:
                break

        self.screen.quit()#if yes stop the question screen

    def action_bth2(self):
        self.chosen_ans = self.a2_bth["text"]
        client_sock.getSocket().send(self.chosen_ans)

        while 1:
            if answer_all:
                break

        self.screen.quit()

    def action_bth3(self):
        self.chosen_ans = self.a3_bth["text"]
        client_sock.getSocket().send(self.chosen_ans)

        while 1:
            if answer_all:
                break

        self.screen.quit()
    def action_bth4(self):
        self.chosen_ans = self.a4_bth["text"]
        client_sock.getSocket().send(self.chosen_ans)

        while 1:
            if answer_all:
                break

        self.screen.quit()

    def build_collect_screen(self):#appear when there is not anoughf players
        font_question = tkFont.Font(weight=tkFont.BOLD, size=25)

        self.collect_label = Label(self.screen, fg="white", text="Waiting for players...", font=font_question, bg="#0085E5")
        self.collect_label.grid(row=0, column=0, columnspan=6,pady=100)

        self.screen.mainloop()
        self.collect_label.destroy()
    def buildWait_screen(self):#correct answer screen
        font_question = tkFont.Font(weight=tkFont.BOLD, size=15)
        if self.chosen_ans==self.true_answer:#check if the answer is true or false
            self.screen["background"] = "green"
            self.label = Label(self.screen, fg="blue", text="correct\n+20", font=font_question, bg="#5FC536")
            self.label.grid(row=0, column=0, columnspan=6,pady=100)
        else:
            self.screen["background"] = "red"
            self.label = Label(self.screen, fg="blue", text=("Error\nTrue Answer: %s"%self.true_answer), font=font_question, bg="#C70039")
            self.label.grid(row=0, column=0, columnspan=6,pady=100)
        self.screen.after(2000,lambda:self.screen.quit())#wait 2 seconds and than close the main loop
        self.screen.mainloop()
        self.label.destroy()

        self.screen["background"] = "#0085E5"#return the screen to his original color

    def build_scoreScreen(self):#the last screen with the player score
        global client_sock

        self.screen_score = Tk()
        for i in range(6):  # make the weight to 1
            self.screen_score.columnconfigure(i, weight=1)

        self.screen_score.title("Kahoot!!")  # his title
        self.screen_score.geometry('450x400')  # his size
        self.screen_score.resizable(width=FALSE, height=FALSE)
        self.screen_score["background"] = "#0085E5"
        font_score = tkFont.Font(weight=tkFont.BOLD, size=20)
        self.label_score = Label(self.screen_score, fg="white", text=("Well played %s\nYou got %s points\n(Place:%s)"%(client_sock.score[2],client_sock.score[0],client_sock.score[1])),font=font_score, bg="#0085E5")
        self.label_score.grid(row=0, column=0, columnspan=6, pady=100,sticky="wens")
        self.done_score = Button(self.screen_score, text="Bye", bg="white", height=2, width=8,command=self.close_score_screen)
        self.done_score.grid(row=1, column=0, columnspan=6, pady=2)
        self.screen_score.mainloop()

    def close_score_screen(self):
        self.screen_score.destroy()

    def close_screen(self):
        self.screen.quit()

    def destroy_screen(self):
        self.screen.destroy()


class socket_details:#save the server location and the player's name
    def __init__(self,HOST,PORT):
        self.ADDR = (HOST, PORT)
        self.tcpCliSock = s.socket(s.AF_INET, s.SOCK_STREAM)

    def getADDR(self):
        return self.ADDR
    def getSocket(self):
        return self.tcpCliSock

    def update_score(self,new_score):
        self.score=new_score

HOST='localhost'
PORT=50008

def send_bth():#connect to the server and send the player's,start the game
    global client_sock,q_a,q_screen

    try:
        client_sock.getSocket().connect(client_sock.getADDR())
    except:
        print "there is no server please try again later"
        exit()


    if take_name.get()=="":#change to a default name if the player didn't entered name
        client_sock.getSocket().send("guest")
    else:
        client_sock.getSocket().send(take_name.get())

    first_sc.destroy()
    q_screen=tkinter_questions()#build the root
    q_screen.build_root()

    thread.start_new_thread(get_serverMSG,())#open a thread which get data from the server
    q_screen.build_collect_screen()
    build_TK()

def get_serverMSG():#get the data rom the server
    global client_sock,q_a,answer_all,q_screen

    time.sleep(0.5)
    first_time=True

    while 1:
        data=client_sock.getSocket().recv(1024)

        if first_time:#check if this is the first question
            q_screen.close_screen()#if yes, close the waiting screen
            first_time=False
        try:
            int(data[0])#check if the data is  number
            details_end=data.split(',')
            client_sock.update_score(details_end)#if yes update the scoe of the client and quit
            break

        except:#check if there is a special data from the server
            if data=="every_one_answer":#if every one answered
                answer_all=True

            if data=="time out":#if 20 passed and the client didn't answer
                q_screen.close_screen()



            time.sleep(0.5)
            q_a=data.split(',')
        answer_all=False
    return 0


def build_TK():#build the question screen according to the  data
    global q_a,q_screen

    for i in range(5):
        print q_a=="" or q_a==["every_one_answer"] or q_a==["time out"]
        while q_a=="" or q_a==["every_one_answer"] or q_a==["time out"]:#if the message is one of them he should'nt open the question screen
            pass


        try:#cheeck if the server sent nothing
            q_screen.update_q_a(q_a[0], [q_a[1], q_a[2], q_a[3], q_a[4]], q_a[5])#update the question and answers and open the screen
            q_screen.build_QuestionScreen()
        except:#if yes close the server
            os._exit(0)
        q_a=""

    q_screen.destroy_screen()



global client_sock ,q_a,answer_all,q_screen

q_screen=''
answer_all=False#become true when avery one answered
q_a=""#save the question and the answers

##########################################open screen

dict=Kahoot_db.get_details("Shahar")#get the location of the server
details_sock=dict.get('result')
HOST=details_sock.get('ipaddr')
PORT=details_sock.get('port')
client_sock=socket_details(HOST,PORT)
first_sc=Tk()#create him

for i in range (6):#make the weight to 1
        first_sc.columnconfigure(i,weight=1)




##############################################open screen
first_sc.title("Kahoot-Register")#his title
first_sc.geometry('350x350')#his size
first_sc.resizable(width=FALSE, height=FALSE)#enable to change the size of the window
first_sc["background"]="#0085E5"

font_kahoot_sen=tkFont.Font(weight=tkFont.BOLD,size=40)
sen1=Label(first_sc,fg="#FA8072",bg="#0085E5",text="Kahoot!!",font=font_kahoot_sen)#the instructions
sen1.grid(row=1,column=2,rowspan=1,sticky="wens",columnspan=2)

take_name=Entry(first_sc,font="Arial 18",fg="black")#entry
take_name.grid(row=2,column=2,sticky="wens",columnspan=2,pady=30)



send_bth=Button(first_sc,text="send",bg="#323E46",height=2,width=1,command=send_bth)#button to start the game
send_bth.grid(row=3,column=3,sticky="wens",columnspan=1,padx=(0,90),pady=10)



first_sc.mainloop()

q_screen.build_scoreScreen()#after whole build the score screen
client_sock.getSocket().close()
