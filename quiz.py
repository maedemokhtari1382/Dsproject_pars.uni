import random
import sqlite3

# Connect to the database
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Create the table to store questions and answers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        choices TEXT,
        answer INTEGER
    )
''')
conn.commit()

# Function to add a question to the database
def add_question(question, choices, answer):
    cursor.execute('''
        INSERT INTO questions (question, choices, answer)
        VALUES (?, ?, ?)
    ''', (question, choices, answer))
    conn.commit()

# Add sample questions to the database
add_question("کدام یک از موارد زیر نوعی پایتون نیست؟",
              "۱. CPython\n۲. Jython\n۳. IPython\n۴. PyPy", 4)
add_question("پایتون به کدام دسته‌ی زبان‌ها تعلق دارد؟",
              "۱. زبان‌های برنامه‌نویسی\n۲. زبان‌های ترجمه‌شونده\n۳. زبان‌های اسکریپت\n۴. زبان‌های ماشین", 3)
# Add more questions...

# Function to generate a quiz
def generate_quiz(num_questions):
    cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT ?', (num_questions,))
    quiz_questions = cursor.fetchall()

    quiz = []
    for question in quiz_questions:
        question_text = question[1]
        choices_text = question[2]
        answer_index = question[3]

        choices = choices_text.split('\n')
        quiz.append((question_text, choices, answer_index))

    return quiz

# Function to display a quiz
def display_quiz(quiz):
    for i, question in enumerate(quiz):
        print(f"\nسوال {i+1}: {question[0]}")
        for j, choice in enumerate(question[1]):
            print(f"{j+1}. {choice}")

# Function to take user input for quiz answers
def take_quiz(quiz):
    score = 0
    for i, question in enumerate(quiz):
        print(f"\nسوال {i+1}: {question[0]}")
        for j, choice in enumerate(question[1]):
            print(f"{j+1}. {choice}")

        user_answer = int(input("لطفاً پاسخ خود را انتخاب کنید: "))
        if user_answer == question[2]:
            score += 1

    return score

# Generate a quiz with 5 questions
quiz = generate_quiz(5)
display_quiz(quiz)
user_score = take_quiz(quiz)

print(f"\nامتیاز شما: {user_score}/{len(quiz)}")

# Close the database connection
conn.close()
