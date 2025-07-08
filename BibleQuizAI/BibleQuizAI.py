import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class BibleQuizAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bible Quiz AI")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Sample Bible questions (you can expand this)
        self.questions = [
            {
                "question": "Who built the ark according to the Bible?",
                "options": ["Moses", "Noah", "Abraham", "David"],
                "correct": 1,
                "explanation": "Noah built the ark as instructed by God to save his family and animals from the flood."
            },
            {
                "question": "How many days and nights did Jesus fast in the wilderness?",
                "options": ["30 days", "40 days", "50 days", "60 days"],
                "correct": 1,
                "explanation": "Jesus fasted for 40 days and 40 nights in the wilderness, being tempted by Satan."
            },
            {
                "question": "Who was the first king of Israel?",
                "options": ["David", "Solomon", "Saul", "Samuel"],
                "correct": 2,
                "explanation": "Saul was the first king of Israel, anointed by Samuel."
            },
            {
                "question": "What is the shortest verse in the Bible?",
                "options": ["Jesus wept", "Rejoice always", "Pray continually", "Love one another"],
                "correct": 0,
                "explanation": "John 11:35 - 'Jesus wept' is the shortest verse in the Bible."
            },
            {
                "question": "How many disciples did Jesus have?",
                "options": ["10", "11", "12", "13"],
                "correct": 2,
                "explanation": "Jesus had 12 disciples, also known as the Twelve Apostles."
            }
        ]
        
        self.current_question = 0
        self.score = 0
        self.selected_answer = tk.IntVar()
        
        self.setup_ui()
        self.load_question()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Bible Quiz AI",
            font=("Arial", 24, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Score display
        self.score_label = tk.Label(
            self.root,
            text="Score: 0/0",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#34495e'
        )
        self.score_label.pack(pady=10)
        
        # Question frame
        self.question_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.question_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Question text
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=("Arial", 14),
            bg='#f0f0f0',
            fg='#2c3e50',
            wraplength=700,
            justify='left'
        )
        self.question_label.pack(pady=20)
        
        # Options frame
        self.options_frame = tk.Frame(self.question_frame, bg='#f0f0f0')
        self.options_frame.pack(pady=20)
        
        # Radio buttons for options
        self.option_labels = []
        for i in range(4):
            option = tk.Radiobutton(
                self.options_frame,
                text="",
                variable=self.selected_answer,
                value=i,
                font=("Arial", 12),
                bg='#f0f0f0',
                fg='#34495e',
                selectcolor='#ecf0f1'
            )
            option.pack(anchor='w', pady=5)
            self.option_labels.append(option)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        # Submit button
        self.submit_button = tk.Button(
            button_frame,
            text="Submit Answer",
            command=self.check_answer,
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.submit_button.pack(side='left', padx=10)
        
        # Next button
        self.next_button = tk.Button(
            button_frame,
            text="Next Question",
            command=self.next_question,
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            state='disabled'
        )
        self.next_button.pack(side='left', padx=10)
        
        # Restart button
        self.restart_button = tk.Button(
            button_frame,
            text="Restart Quiz",
            command=self.restart_quiz,
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.restart_button.pack(side='left', padx=10)
        
        # Explanation label
        self.explanation_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11, "italic"),
            bg='#f0f0f0',
            fg='#7f8c8d',
            wraplength=700,
            justify='left'
        )
        self.explanation_label.pack(pady=10)
    
    def load_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=f"Question {self.current_question + 1}: {question_data['question']}")
            
            for i, option in enumerate(question_data['options']):
                self.option_labels[i].config(text=f"{chr(65 + i)}. {option}")
            
            self.selected_answer.set(-1)
            self.explanation_label.config(text="")
            self.submit_button.config(state='normal')
            self.next_button.config(state='disabled')
        else:
            self.show_final_results()
    
    def check_answer(self):
        if self.selected_answer.get() == -1:
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        question_data = self.questions[self.current_question]
        user_answer = self.selected_answer.get()
        correct_answer = question_data['correct']
        
        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "Great job! That's the right answer.")
        else:
            correct_option = chr(65 + correct_answer)
            messagebox.showerror("Incorrect", f"Sorry, that's not correct. The right answer is {correct_option}.")
        
        self.explanation_label.config(text=f"Explanation: {question_data['explanation']}")
        self.score_label.config(text=f"Score: {self.score}/{self.current_question + 1}")
        
        self.submit_button.config(state='disabled')
        self.next_button.config(state='normal')
    
    def next_question(self):
        self.current_question += 1
        self.load_question()
    
    def restart_quiz(self):
        self.current_question = 0
        self.score = 0
        self.score_label.config(text="Score: 0/0")
        self.load_question()
    
    def show_final_results(self):
        percentage = (self.score / len(self.questions)) * 100
        
        result_text = f"Quiz Complete!\n\nFinal Score: {self.score}/{len(self.questions)}\nPercentage: {percentage:.1f}%\n\n"
        
        if percentage >= 80:
            result_text += "Excellent! You have a great knowledge of the Bible!"
        elif percentage >= 60:
            result_text += "Good job! You have a solid understanding of the Bible."
        elif percentage >= 40:
            result_text += "Not bad! Keep studying to improve your knowledge."
        else:
            result_text += "Keep studying the Bible to improve your knowledge!"
        
        messagebox.showinfo("Quiz Results", result_text)
        self.restart_quiz()

def main():
    root = tk.Tk()
    app = BibleQuizAI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 