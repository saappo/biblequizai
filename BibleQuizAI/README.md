# BibleQuizAI

A simple Bible quiz application built with Python and Tkinter that runs locally on your computer.

## Features

- Interactive Bible quiz with multiple choice questions
- Real-time score tracking
- Explanations for each answer
- Modern, user-friendly interface
- No internet connection required

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python installation)

## Installation

1. Make sure you have Python installed on your system
2. Clone or download this project to your local machine
3. Navigate to the project directory

## Running the Application

### Method 1: Direct Python execution
```bash
python BibleQuizAI.py
```

### Method 2: Using Python module
```bash
python -m BibleQuizAI
```

### Method 3: Double-click (Windows)
- Navigate to the project folder
- Double-click on `BibleQuizAI.py`

## How to Play

1. The application will open with a graphical interface
2. Read each question carefully
3. Select your answer by clicking on one of the radio buttons
4. Click "Submit Answer" to check your response
5. Read the explanation for the correct answer
6. Click "Next Question" to continue
7. At the end, you'll see your final score and percentage
8. Click "Restart Quiz" to play again

## Sample Questions

The application includes questions about:
- Biblical characters (Noah, Jesus, Saul, etc.)
- Biblical events (the flood, Jesus' fasting, etc.)
- Bible trivia (shortest verse, number of disciples, etc.)

## Customization

You can easily add more questions by editing the `questions` list in the `BibleQuizAI.py` file. Each question should follow this format:

```python
{
    "question": "Your question here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0,  # Index of correct answer (0-3)
    "explanation": "Explanation of the correct answer."
}
```

## Troubleshooting

### If the application doesn't start:
1. Make sure Python is installed and in your system PATH
2. Verify that Tkinter is available (it's included with most Python installations)
3. Try running from the command line to see any error messages

### If you get a "tkinter not found" error:
- On Ubuntu/Debian: `sudo apt-get install python3-tk`
- On CentOS/RHEL: `sudo yum install tkinter`
- On macOS: Tkinter should be included with Python
- On Windows: Tkinter should be included with Python

## Future Enhancements

Potential improvements for the application:
- Add more questions and categories
- Implement difficulty levels
- Add timer functionality
- Save high scores
- Connect to Bible APIs for dynamic content
- Add AI-powered question generation

## License

This project is open source and available under the MIT License. 