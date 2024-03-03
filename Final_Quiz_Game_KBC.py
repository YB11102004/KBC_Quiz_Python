import time
from tkinter import *
from customtkinter import *
from tkinter import font
from tkinter import messagebox
import requests
from PIL import Image,ImageTk
import webbrowser
from tkinter import ttk
import random

# When working with Python and encountering a 503 error, it usually means that an HTTP request made by your Python code received a 503 response from the server. This might occur when your Python program is trying to access a web server that is temporarily unavailable or experiencing high traffic loads.
final_score1=0
final_score2=0
final_score3=0
count=0
money=0
abc=0
quit_pressed=0
fifty_fifty_used = False
flip_used = False
count3=0
i=0
j=0
wrong_answer=0
question=[]
all_questions_together=[]

#rule_book function will show you the rules for the quiz.
# And ask for your permission to start the game
def rule_book():
    def on_click():
        if(check_var.get()==0):
           messagebox.showwarning("Warning", "Please check the terms & condition to start the game")
        else:
            root2.destroy()
            trivia_question=fetch_all_questions()
            if trivia_question:
                display_questions(trivia_question)
            
    
    # rule book on click function
    def on_link_click(event):
        webbrowser.open_new("https://www.setindia.com/pdf/KBC-Contest-T&Cs.pdf")
    
    root2=Tk()
    root2.title('KBC Rule Book')
    root2.configure(bg='#390F4E')
    frame = Frame(root2,bd=5,bg="#390F4E",highlightbackground="black",highlightthickness=10)
    frame.pack(side="top", expand=True)
    label1=Label(frame,text="Welcome to KBC by Yatra Bhimani!!\n> The Participant is of the age 8 years or above.\n> The Participant is a citizen of India & residing in India.\n> The Participant is of sound mind and health.",font=("Comic Sans MS",20,"bold"),bg="#390F4E",fg="#ffffff")
    label1.pack()
    label5=Label(frame,text="~ आपको 15 सवाल विभिन्न वर्ग के दिए जाएंगे। \n Answer as per your knowledge to Win.\n अपनी कुर्सी की पेटी बांध ले।",font=("Comic Sans MS",20,"bold"),bg="#390F4E",fg="#ffffff")
    label5.pack()
    label2=Label(frame,text="*Terms & Conditions",font=("Comic Sans MS",12),bg="#390F4E",fg="#0000FF")
    label2.bind("<Button-1>", on_link_click)
    label2.pack()
    check_var = IntVar()
    check=Checkbutton(frame,text="I agree Terms & conditions Provided here.",font=("Comic Sans MS",20,"bold"),bg="#390F4E",fg="#ffffff",variable=check_var)
    check.pack()
    start_img = Image.open('start.jpg').resize((70,70))
    image_start = ImageTk.PhotoImage(start_img)
    button=Button(frame,command=on_click,bg='#390F4E',fg="#fff",font=("Comic Sans MS", 14,"bold"),relief=SOLID,justify=CENTER,image=image_start)
    button.pack()
    root2.mainloop()

# this function will display the final_score of the game and the money amount you won as well.
def final_score_display():
    global fifty_fifty_used,flip_used
    root1=Tk()
    root1.title('Answer_table')
    root1.state('zoomed')
    root1.configure(bg='#390F4E')
    frame3 = Frame(root1,bg="#390F4E")
    frame3.pack(padx=10, pady=10)
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Custom.Horizontal.TProgressbar", background='blue')

    # Checks whether the helplines are used or not
    if fifty_fifty_used==False and flip_used==False:
        label_check=Label(frame3,text="Woo hoo!! Not used helplines",font=("Comic Sans MS",20,"bold"),bg='#390F4E',anchor="center",fg="#ffffff")
        label_check.pack()
    elif fifty_fifty_used==True and flip_used==True:
        label_check=Label(frame3,text="Oops! All Helpline used",font=("Comic Sans MS",20,"bold"),bg='#390F4E',anchor="center",fg="#ffffff")
        label_check.pack()
    elif fifty_fifty_used==True:
        label_check=Label(frame3,text="Oops! 50:50 used",font=("Comic Sans MS",20,"bold"),bg='#390F4E',anchor="center",fg="#ffffff")
        label_check.pack()
    elif flip_used==True:
        label_check=Label(frame3,text="Oops! you flipped question",font=("Comic Sans MS",20,"bold"),bg='#390F4E',anchor="center",fg="#ffffff")
        label_check.pack()

    # progress bars for the scores
    label=Label(frame3,text="Easy : ",font=("Comic Sans MS",20,"bold"),bg='#390F4E',anchor="center",fg="#ffffff")
    label.pack(side=LEFT,padx=5)
    progressbar = ttk.Progressbar(frame3, style="Custom.Horizontal.TProgressbar", orient='horizontal', mode='determinate')
    progressbar.pack(side=LEFT)
    progressbar["value"]=(final_score1/5)*100
    label1=Label(frame3,text="Medium : ",font=("Comic Sans MS",20,"bold"),bg='#390F4E',anchor="center",fg="#ffffff")
    label1.pack(side=LEFT,padx=5)
    progressbar1 = ttk.Progressbar(frame3, style="Custom.Horizontal.TProgressbar", orient='horizontal', mode='determinate')
    progressbar1.pack(side=LEFT)
    progressbar1["value"]=(final_score2/5)*100
    label2=Label(frame3,text="Hard : ",font=("Comic Sans MS",20,"bold"),bg='#390F4E',anchor="center",fg="#ffffff")
    label2.pack(side=LEFT,padx=5)
    progressbar2 = ttk.Progressbar(frame3, style="Custom.Horizontal.TProgressbar", orient='horizontal', mode='determinate')
    progressbar2.pack(side=LEFT)
    progressbar2["value"]=(final_score3/5)*100

    # Money value
    money_with_sprinkles = f"🎉🎊 Congratulations! You won ₹{money} 🎊🎉"
    label_money = Label(root1, text=money_with_sprinkles, font=("Comic Sans MS", 20, "bold"), bg='#390F4E', fg="#ffffff")
    label_money.pack()

    # Last message 
    frame = Frame(root1,bd=5,bg="#390F4E",highlightbackground="black",highlightthickness=10)
    frame.pack(side="top", expand=True)   
    start_img = Image.open('yatra.jpg')
    image_start = ImageTk.PhotoImage(start_img)
    label_img = Label(frame, image=image_start)
    label_img.pack()
    root1.mainloop()


# resolving the error 429 means too many requests to the api
def make_request(url):
    retries=3  
    delay=1
    while retries>0:
        response=requests.get(url)
        if response.status_code==200:
            return response.json()
        elif response.status_code==429:
            time.sleep(delay)
            delay*=2
            retries-=1
        else:
            return None
    return None

# sending the urls to resolve 429
def get_trivia_questions(url):
    return make_request(url) 

# To fetch the questions according to the categories from the API - Trivia
def fetch_all_questions():
    all_questions=[]
    urls = [
        "https://opentdb.com/api.php?amount=6&category=18&difficulty=easy&type=multiple",
        "https://opentdb.com/api.php?amount=6&category=18&difficulty=medium&type=multiple",
        "https://opentdb.com/api.php?amount=6&category=18&difficulty=hard&type=multiple"
    ]
    for url in urls:
        questions_response = get_trivia_questions(url)
        if questions_response:
            for question in questions_response['results']:
                question_data = {
                    'question': question['question'],
                    'correct_answer': question['correct_answer'],
                    'incorrect_answers': question['incorrect_answers']
                }
                all_questions.append(question_data)
    return all_questions

# this function will display multi optios questions and work according to the categories also gives the helplines for the same
def display_questions(questions):
    global i
    global question
    global all_questions_together
    # all_question_together takes one question from each category for fliping purpose if pressed then used accordingly
    all_questions_together = [questions[5], questions[11], questions[17]]
    for i in range(15):
        # process after the quit option
        if quit_pressed==1 or wrong_answer==1:
            break
        def on_submit():
            global money
            global count
            global wrong_answer
            global final_score1,final_score2,final_score3
            count+=1
            correct_answer = question['correct_answer'] 
            user_answer = selected_radio.get()
            f_answer=options[user_answer-1]
            if selected_radio.get() == 0:
                messagebox.showwarning("Warning", "कृपा करके एक विकल्प चुनें।")
            else:
                if f_answer == correct_answer:
                    a=(i%5)+1
                    if i>=0 and i<=4 :
                        final_score1+=1  #easy
                        money+=a*1000
                    elif i>=5 and i<=9:
                        final_score2+=1
                        money+=a*10000
                    else:
                        final_score3+=1
                        money+=a*100000
                    messagebox.showinfo("Feedback", "मुबारक हो! सही जवाब!")
                    root.destroy()
                else:
                    messagebox.showinfo("Feedback", f"माफ़ कीजियेगा पर सही जवाब है {correct_answer}\n अब आप आगे नहीं बढ़ सकते|")
                    root.destroy()
                    final_score_display()
                    wrong_answer=1

        def on_quit():
            global quit_pressed
            quit_pressed=1
            root.destroy()
            final_score_display()

        # 50:50 helpline
        def fifty():
            global count3
            count3+=1
            global fifty_fifty_used
            fifty_fifty_used = True
            if fifty_fifty_used:
                button1.config(font=("Comic Sans MS", 16, "bold", "overstrike"))
            correct_answer = question['correct_answer']
            if correct_answer==radio1.cget("text"):
                radio2.pack_forget()
                radio3.pack_forget()
            elif correct_answer==radio2.cget("text"):
                radio3.pack_forget()
                radio4.pack_forget()
            elif correct_answer==radio3.cget("text"):
                radio1.pack_forget()
                radio4.pack_forget()
            else:
                radio1.pack_forget()
                radio2.pack_forget()

        # flip the question helpline
        def flip():
            global i
            global count3
            count3+=1
            global flip_used
            flip_used = True
            if flip_used:
                button3.config(font=("Comic Sans MS", 16, "bold", "overstrike"))
            if(i>=0 and i<5):
                question=all_questions_together[0]
            elif(i>=5 and i<10):
                question=all_questions_together[1]
            elif(i>=10 and i<15):
                question=all_questions_together[2]
            oplabel.config(text=question['question'])
            options = question['incorrect_answers'] + [question['correct_answer']]
            options = [option.encode('utf-8').decode('unicode-escape') for option in options]
            random.shuffle(options)
            radio1.config(text=options[0], value=1)
            radio2.config(text=options[1], value=2)
            radio3.config(text=options[2], value=3)
            radio4.config(text=options[3], value=4)

        # question of the quizes starts here..
        question=questions[i]
        root=Tk()
        root.title('Quiz using API')
        root.configure(bg='#390F4E')
        frame1 = Frame(root,bd=5,bg="#390F4E",highlightbackground="black",highlightthickness=4,relief="sunken")
        frame1.pack(side="top", expand=True)
        a=(i%5)+1
        if i>=0 and i<=4 :
            label4=Label(frame1, text=f"{a*1000} रुपये के लिए आपकी स्क्रीन पर ये रहा सवाल", font=("Comic Sans MS",14,"bold"),bg='#390F4E',fg="#fff")
            label4.pack()
        elif i>=5 and i<=9:
            label4=Label(frame1, text=f"{a*10000} रुपये के लिए आपकी स्क्रीन पर पहला ये रहा सवाल", font=("Comic Sans MS",14,"bold"),bg='#390F4E',fg="#fff")
            label4.pack()
        else:
            label4=Label(frame1, text=f"{a*100000} रुपये के लिए आपकी स्क्रीन पर पहला ये रहा सवाल", font=("Comic Sans MS",14,"bold"),bg='#390F4E',fg="#fff")
            label4.pack()
        oplabel = Label(frame1, text=question['question'], font=("Comic Sans MS",14,"bold"),bg='#390F4E',fg="#fff",anchor="center")
        oplabel.pack()
        canvas = Canvas(frame1, width=0, height=0,highlightthickness=2,bg="#390F4E")
        canvas.pack(fill="x")
        canvas.create_line(0, 1, 200, 1, fill="black",width=2)
        selected_radio = IntVar()
        options = question['incorrect_answers'] + [question['correct_answer']]
        options = [option.encode('utf-8').decode('unicode-escape') for option in options]
        option=options
        random.shuffle(option)
        radio1=Radiobutton(frame1,text=option[0],variable=selected_radio, value=1,bg='#390F4E',fg="#fff")
        radio1.pack()
        radio2=Radiobutton(frame1,text=option[1],variable=selected_radio, value=2,bg='#390F4E',fg="#fff")
        radio2.pack()
        radio3=Radiobutton(frame1,text=option[2],variable=selected_radio, value=3,bg='#390F4E',fg="#fff")
        radio3.pack()
        radio4=Radiobutton(frame1,text=option[3],variable=selected_radio, value=4,bg='#390F4E',fg="#fff")
        radio4.pack()
        custom_font = font.Font(family="Comic Sans MS", size=16, overstrike=False)
        frame2 =Frame(frame1,bg="#390F4E")
        frame2.pack(padx=10, pady=10)
        label6=Label(frame2,text="HELP-LINES: ",font=("Comic Sans MS",14,"bold"),bg='#390F4E',fg="#fff")
        label6.pack(side=LEFT, padx=5)

        # counter of the helplines
        if(count3==2):
            label7=Label(frame2,text="Sorry! ALL USED.",font=("Comic Sans MS",14,"bold"),bg='#390F4E',fg="#fff")
            label7.pack(side=LEFT, padx=5)
        button1 = Button(frame2, text="50 : 50", command=fifty,font=custom_font)
        button1.pack(side=LEFT, padx=5)

        # process after the fifty-fifty used
        if fifty_fifty_used:
            button1.pack_forget()
        button3 = Button(frame2, text="flip Question", command=flip,font=custom_font)
        button3.pack(side=LEFT, padx=5)

        # process after the flip used
        if flip_used:
            button3.pack_forget()
        submit=Button(frame1,text="Lock किया जाये",command=on_submit, width=15, height=2,font=("Comic Sans MS", 14,"bold"),relief=SOLID,justify=CENTER)
        submit.pack(padx=5,pady=5)

        # Quitting option logic
        if(i%5==0 and i!=0):
            messagebox.showwarning("Warning", "आप अभी खेल छोड़ना चाहे तो quit दबाइये।")
            quit=Button(frame1,text="QUIT",command=on_quit, width=10, height=2,font=("Comic Sans MS", 14,"bold"),relief=SOLID,justify=CENTER)
            quit.pack(padx=5,pady=5)
        root.mainloop()


# __name__ becomes __main__ when you are running same file rather than importing it in another file ... now if you have imported in other file then you can not access the content inside this if condition but you can access rest of the content.
# execution starts of the quiz
if __name__ == "__main__":
    rule_book()
# calls the final score function when all the 15 questions are asked
    if(count==15):
        final_score_display()