from flask import Blueprint, render_template, request, redirect, url_for, session
from spellchecker import SpellChecker
from flask import flash
from collections import Counter
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ail2024",
  database="mydb"
)

mycursor = mydb.cursor()



# Load the KNN model outside the function
with open('knn_model.pkl', 'rb') as file:
    loaded_knn_model = pickle.load(file)

def get_suggestions(student_id):
    query = """
        SELECT grades.course_id, grades.grade, course.specialty, course.difficulty, grades.pass
        FROM grades
        JOIN course ON grades.course_id = course.course_id
        WHERE grades.st_id = %s;
        """
    mycursor.execute(query, (student_id,))

    results = mycursor.fetchall()


    suggestion_list = []

    for row in results:
        suggestion_data = {
            'course_id': row[0],
            'grade': row[1],
            'specialty': row[2],
            'difficulty': row[3],
            'pass': row[4]
        }
        
        suggestion_list.append(suggestion_data)

    # Create a new Label Encoder and encode 'specialty' for this function
    label_encoder_function = LabelEncoder()
    for suggestion_data in suggestion_list:
        suggestion_data['specialty'] = label_encoder_function.fit_transform([suggestion_data['specialty']])[0]

    # Use the loaded KNN model for predictions
    for suggestion_data in suggestion_list:
        input_data = [[
            suggestion_data['course_id'],
            suggestion_data['grade'],
            suggestion_data['specialty'],
            suggestion_data['difficulty'],
            suggestion_data['pass']
        ]]
        
        predictions_list = []
    for suggestion_data in suggestion_list:
        input_data = pd.DataFrame([suggestion_data]) 
        prediction = loaded_knn_model.predict(input_data)
        predictions_list.append(prediction)

    return predictions_list

def get_book_suggestions(student_id):
    query = """select * from book
            where book_id = %s"""
    suggestion_list = []

    book_ids = get_suggestions(student_id)

    for book_id in book_ids:
        mycursor.execute(query, (int(book_id[0]),))  
        results = mycursor.fetchall()
        for book in results:
            books_info ={
                "book_id": book[0],
                "book_title": book[1],
                "book_author": book[2],
                "genre": book[3],
                "available": book[4],
                "specialty": book[5],
                "difficulty": book[6],
                "book_picture_path": book[7],
                "location": book[8],
            }
            suggestion_list.append(books_info)
            
    return suggestion_list

get_book_suggestions(1001)