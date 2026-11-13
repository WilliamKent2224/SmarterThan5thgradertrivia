# Commenting this out until i understand it.
# set_website_title("Smarter than 5th Grader Trivia")
# set_site_information(
#    author="William Kent",
#    description="Descriptions are for the weak.",
#    sources="Thanks to the Drafter, No help from GPT",
#    planning=["None this was coded in one multi day session. 3 am hits different the third night"],
#    links=["not yet"]
# )
# hide_debug_information()
# set_website_framed(False)
#
from dataclasses import dataclass
from drafter import *

# a data class cotaining the values of questions, including the question itself, the answers to choose from, and the correct answer amongst them.
@dataclass
class Question:
    question: str # the question, in string format.
    answers: list[str] # the possible answers to the question
    correct_answer: str # the correct answer.
    
# the state dataclass, used to keep track of:
# the trivia takers score, current question, previous score, and whether or not they have played.
@dataclass
class State:
    question_index: int # the index which determins the current question
    current_score: int # the current score of the player.
    last_score: int # the score fo the player the final round
    has_played: bool # a boolean that tracks whether or not the user has taken the trivia quiz before

# a dataclass defined that contains all the questions, answers, and correct answer. See question dataclass for more information
questions = [
    Question(
        question="1. What is 2 to the power of 8?",
        answers=["1024", "2048", "4096", "256"],
        correct_answer="1024", ),
    Question(
        question="2. Which is better?",
        answers=["Pancakes", "Waffles", "Bagel", "Toast"],
        correct_answer="Waffles", ),
    Question(
        question="3. What is the word 'cheese'",
        answers=["Noun", "Verb", "Adverb", "Adjective"],
        correct_answer="Noun", ),
    Question(
        question="4. Which subject teaches you about world history?",
        answers=["Math", "English", "Spanish", "Social Studies"],
        correct_answer="Social Studies", ),
    Question(
        question="5. What Color is the sky in Colorodo America at 12:01 pm January the 3rd?",
        answers=["Blue", "Black*", "Red", "What kind of question is this??????"],
        correct_answer="Blue", ), ]
# the index function, a common fundemental function used to generate the page. By default it generates the main page
@route
def index(state: State) -> Page:
    content = [
        # a header of the page, used to query the user to identify if the user wishes to start the quiz
        Header("5th Grade Knowledge Trivia Quiz"), "Would you like to start the 5-question quiz?",
    ]
    # an if statement that tracks if the user has played the game yet. If they have it will difplay their score out of 5
    if state.has_played:
        score_text = f"Last attempt score: {state.last_score} / {len(questions)}"
    # upon the situation that there is no previous playthrough it will show this text instead.
    else:
        score_text = "Last attempt score: No attempts yet."
    # a set of appends that add the score and buttons, should be self explanatory honestly. 
    content.append(score_text)
    content.append(Button("Start Quiz", "start_quiz"))
    content.append(Button("Credits", "credits"))
    return Page(state, content) # returns the page.
# a function that starts the quiz, upon the press of the button from the main page of course. of course.
@route
def start_quiz(state: State) -> Page:
    state.question_index = 0 # defines the default index upon starting.
    state.current_score = 0 # score start at 0, gains 1 point for question.
    return show_question(state) # returns new page.
# a function that shows the current question after the quiz has started, also updates the old score information.
@route
def show_question(state: State) -> Page:
    if state.question_index >= len(questions):
        state.last_score = state.current_score # same reason as has_played notation on the line bellow.
        state.has_played = True # updates this so that the main screen knows to display the last score 
        return results(state)
    
    current_question = questions[state.question_index] # keeps track of the current question being ask. 
    content = [
        Header(f"Question {state.question_index + 1} of {len(questions)}"),
        current_question.question,
    ]
    # uses a temporary variable to assist in submitting the selected choice.
    # sets up the button to submit the answer, did not plan for this in the design but stuff had to change. A lot.
    # will be relavent when the submit answer function is done being coded.
    # Note: update this documentation when that is working. 
    for choice in current_question.answers:
        content.append(
            Button(choice, "submit_answer", arguments={"selected": choice})
        )
    # return statement bellow updates the page
    return Page(state, content) # if you don't know what this return statement does at this point, give up understanding the code
# holy hell this is function is gonna be the death of me debugging this crap has taken until 1:06 pm the day its due FAH.
# submit answer function was created so that if a person missclick the wrong answer it would not automatically submit it. 
@route
def submit_answer(state: State, selected: str) -> Page:
    current_question = questions[state.question_index] # gets and updates the current question 
    
    if selected == current_question.correct_answer: # checks to see if the answer selected is the correct one
        state.current_score += 1 # adds to the score if it does
        
    state.question_index += 1 # to be honest even i don't know why this fixed my code but i am not touching it. neither should you.
    return show_question(state) # updates the page
# the function for the results screen (god i am gonna lose so many points because none of this is to my original design)
# Note: delete complaints before upload
# The function results takes control of the results page, it displays the score as a value of correct answers (int -> str) out
# of the length of the quiz.
# made it like this so i can add questions if needed later.
@route
def results(state: State) -> Page:
    return Page(
        state,
        [
            Header("Quiz Complete!"),
            f"You scored {state.current_score} out of {len(questions)}.",
            Button("Back to Main Page", "index"),
        ],
    )
# credits page. I shouldn't have to document this but there are instructions on soap bottles soooooo
# this function comes from the main page and displays credits to who spent hours on this god forsaken code.
# gave credit to the python language and the drafter liabrary.
# If i have to use Chat GPT later to debug because it is getting god awefully close to the deadline (11:43 am the day its due), i will credit it
@route
def credits(state: State) -> Page:
    return Page(
        state,
        [
            Header("Credits"),
            "Created by: William Kent",
            "Built with the Python Drafter Library.",
            Button("Back to Main Page", "index"),
        ],
    )
# please work this time
# start server call.
# OH MY GOD IT WORKS THANK JESUS
start_server(State(question_index=0, current_score=0, last_score=0, has_played=False))
