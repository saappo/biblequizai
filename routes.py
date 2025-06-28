from flask import render_template, request, redirect, url_for, flash, session, jsonify, make_response, get_flashed_messages
from flask_login import login_required, current_user
from models import User, Quiz, Question, UserResponse, Suggestion, db, ContactMessage
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

# Define sample questions if not already defined
SAMPLE_QUESTIONS = {
    'Easy': [
        {
            'text': 'Who built the ark?',
            'options': ['Noah', 'Moses', 'Abraham', 'David'],
            'correct_answer': 'Noah',
            'category': 'Old Testament'
        },
        {
            'text': 'How many disciples did Jesus have?',
            'options': ['10', '12', '13', '14'],
            'correct_answer': '12',
            'category': 'New Testament'
        },
        {
            'text': 'Who was the first man created by God?',
            'options': ['Adam', 'Eve', 'Noah', 'Abraham'],
            'correct_answer': 'Adam',
            'category': 'Old Testament'
        },
        {
            'text': 'What was the first miracle Jesus performed?',
            'options': ['Walking on water', 'Turning water into wine', 'Feeding 5000', 'Raising Lazarus'],
            'correct_answer': 'Turning water into wine',
            'category': 'New Testament'
        },
        {
            'text': 'Who was thrown into the lion\'s den?',
            'options': ['David', 'Daniel', 'Joseph', 'Jonah'],
            'correct_answer': 'Daniel',
            'category': 'Old Testament'
        },
        {
            'text': 'What was the name of Jesus\' mother?',
            'options': ['Mary', 'Elizabeth', 'Sarah', 'Rebecca'],
            'correct_answer': 'Mary',
            'category': 'New Testament'
        },
        {
            'text': 'Which book comes first in the Bible?',
            'options': ['Genesis', 'Exodus', 'Matthew', 'Psalms'],
            'correct_answer': 'Genesis',
            'category': 'Old Testament'
        }
    ],
    'Medium': [
        {
            'text': 'What was the name of Abraham\'s wife?',
            'options': ['Sarah', 'Rebecca', 'Rachel', 'Leah'],
            'correct_answer': 'Sarah',
            'category': 'Old Testament'
        },
        {
            'text': 'How many days was Jonah in the belly of the fish?',
            'options': ['1', '2', '3', '4'],
            'correct_answer': '3',
            'category': 'Old Testament'
        },
        {
            'text': 'Who denied Jesus three times?',
            'options': ['Peter', 'John', 'James', 'Andrew'],
            'correct_answer': 'Peter',
            'category': 'New Testament'
        },
        {
            'text': 'What was the name of the river where Jesus was baptized?',
            'options': ['Jordan', 'Nile', 'Euphrates', 'Tigris'],
            'correct_answer': 'Jordan',
            'category': 'New Testament'
        },
        {
            'text': 'How many books are in the New Testament?',
            'options': ['27', '39', '66', '73'],
            'correct_answer': '27',
            'category': 'General'
        },
        {
            'text': 'Who was the first king of Israel?',
            'options': ['Saul', 'David', 'Solomon', 'Samuel'],
            'correct_answer': 'Saul',
            'category': 'Old Testament'
        },
        {
            'text': 'What was the name of the place where Jesus was born?',
            'options': ['Bethlehem', 'Nazareth', 'Jerusalem', 'Galilee'],
            'correct_answer': 'Bethlehem',
            'category': 'New Testament'
        }
    ],
    'Hard': [
        {
            'text': 'What was the name of the high priest who questioned Jesus?',
            'options': ['Caiaphas', 'Annas', 'Pilate', 'Herod'],
            'correct_answer': 'Caiaphas',
            'category': 'New Testament'
        },
        {
            'text': 'How many years did the Israelites wander in the wilderness?',
            'options': ['30', '40', '50', '60'],
            'correct_answer': '40',
            'category': 'Old Testament'
        },
        {
            'text': 'What was the name of the place where Jesus was crucified?',
            'options': ['Golgotha', 'Gethsemane', 'Bethlehem', 'Nazareth'],
            'correct_answer': 'Golgotha',
            'category': 'New Testament'
        },
        {
            'text': 'Who was the father of John the Baptist?',
            'options': ['Zechariah', 'Joseph', 'Eli', 'Joachim'],
            'correct_answer': 'Zechariah',
            'category': 'New Testament'
        },
        {
            'text': 'What was the name of the mountain where Moses received the Ten Commandments?',
            'options': ['Mount Sinai', 'Mount Horeb', 'Mount Ararat', 'Mount Moriah'],
            'correct_answer': 'Mount Sinai',
            'category': 'Old Testament'
        },
        {
            'text': 'How many days was Jesus in the tomb before His resurrection?',
            'options': ['1', '2', '3', '4'],
            'correct_answer': '3',
            'category': 'New Testament'
        },
        {
            'text': 'What was the name of the prophet who was taken to heaven in a chariot of fire?',
            'options': ['Elijah', 'Elisha', 'Isaiah', 'Jeremiah'],
            'correct_answer': 'Elijah',
            'category': 'Old Testament'
        }
    ]
}

def register_routes(app):
    @app.login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def home():
        return redirect(url_for('welcome'))

    @app.route('/submit', methods=['GET', 'POST'])
    def submit_suggestion():
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            location = request.form.get('location')
            
            if not title or not content:
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('submit_suggestion'))
            
            suggestion = Suggestion(
                title=title,
                content=content,
                location=location,
                user_id=current_user.id if current_user.is_authenticated else None
            )
            
            db.session.add(suggestion)
            db.session.commit()
            
            flash('Thank you for your suggestion!', 'success')
            return redirect(url_for('home'))
        
        return render_template('submit.html')

    @app.route('/suggestions')
    def view_suggestions():
        suggestions = Suggestion.query.filter_by(status='approved').order_by(Suggestion.created_at.desc()).all()
        return render_template('suggestions.html', suggestions=suggestions)

    @app.route('/admin')
    @login_required
    def admin():
        if not current_user.is_admin:
            flash('Access denied', 'error')
            return redirect(url_for('home'))
        
        suggestions = Suggestion.query.order_by(Suggestion.created_at.desc()).all()
        return render_template('admin.html', suggestions=suggestions)

    @app.route('/admin/suggestion/<int:id>/<action>')
    @login_required
    def admin_action(id, action):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        suggestion = Suggestion.query.get_or_404(id)
        if action == 'approve':
            suggestion.status = 'approved'
        elif action == 'reject':
            suggestion.status = 'rejected'
        
        db.session.commit()
        return redirect(url_for('admin'))

    @app.route('/admin/generate-questions', methods=['POST'])
    @login_required
    def admin_generate_questions():
        """Admin route to manually trigger question generation"""
        if not current_user.is_admin:
            flash('Access denied', 'error')
            return redirect(url_for('home'))
        
        try:
            from question_generator import generate_daily_questions
            success = generate_daily_questions()
            if success:
                flash('Questions generated successfully!', 'success')
            else:
                flash('Error generating questions. Check the logs for details.', 'error')
        except Exception as e:
            logger.error(f"Error in manual question generation: {str(e)}")
            flash('Error generating questions. Check the logs for details.', 'error')
        
        return redirect(url_for('admin'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        logger.debug('Accessing login page')
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'error')
        
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        logger.debug('Accessing register page')
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('register'))
            
            new_user = User(
                email=email,
                password_hash=generate_password_hash(password)
            )
            
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                logger.error(f'Error during registration: {str(e)}')
                db.session.rollback()
                flash('An error occurred during registration', 'error')
        
        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard():
        logger.debug('Accessing dashboard')
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        return render_template('dashboard.html', user=user)

    @app.route('/quiz/<difficulty>', methods=['GET', 'POST'])
    def take_quiz(difficulty):
        logger.debug(f'Accessing quiz with difficulty {difficulty}')
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            flash('Invalid difficulty level', 'error')
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            try:
                answer = request.form.get('answer')
                if not answer:
                    flash('Please select an answer', 'error')
                    return redirect(url_for('take_quiz', difficulty=difficulty))
                
                if 'answers' not in session:
                    session['answers'] = []
                session['answers'].append(answer)
                session.modified = True
                
                logger.info(f"Answer submitted for difficulty {difficulty}")
                
                if len(session['answers']) >= len(session['questions']):
                    logger.info("Quiz completed, redirecting to results")
                    return redirect(url_for('results'))
                
                current_question = session['questions'][len(session['answers'])]
                return render_template('quiz.html',
                                    question=current_question,
                                    difficulty=difficulty,
                                    current_question=len(session['answers']) + 1,
                                    total_questions=len(session['questions']))
            except Exception as e:
                logger.error(f"Error in quiz submission: {str(e)}")
                flash('An error occurred. Please try again.', 'error')
                return redirect(url_for('home'))
        
        try:
            if 'questions' not in session or 'difficulty' not in session or session['difficulty'] != difficulty:
                # Get questions from database based on difficulty
                questions = Question.query.filter_by(difficulty=difficulty).order_by(db.func.random()).limit(5).all()
                if not questions:
                    flash('No questions available for this difficulty level', 'error')
                    return redirect(url_for('home'))
                
                # Convert questions to session-friendly format
                session_questions = []
                for q in questions:
                    session_questions.append({
                        'text': q.text,
                        'options': q.options,
                        'correct_answer': q.correct_answer,
                        'category': q.category if hasattr(q, 'category') else 'General'
                    })
                
                session['questions'] = session_questions
                session['answers'] = []
                session['difficulty'] = difficulty
                session.modified = True
                logger.info(f"New quiz initialized with {len(session_questions)} questions")
            
            current_question_index = len(session.get('answers', []))
            if current_question_index >= len(session['questions']):
                return redirect(url_for('results'))
                
            current_question = session['questions'][current_question_index]
            return render_template('quiz.html',
                                question=current_question,
                                difficulty=difficulty,
                                current_question=current_question_index + 1,
                                total_questions=len(session['questions']))
        except Exception as e:
            logger.error(f"Error in quiz initialization: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('home'))

    @app.route('/results')
    def results():
        if 'questions' not in session or 'answers' not in session:
            flash('No quiz in progress', 'error')
            return redirect(url_for('home'))
        
        try:
            correct_answers = sum(1 for q, a in zip(session['questions'], session['answers'])
                                if a == q['correct_answer'])
            total_questions = len(session['questions'])
            score = int((correct_answers / total_questions) * 100)
            
            questions = []
            for q, a in zip(session['questions'], session['answers']):
                questions.append({
                    'text': q['text'],
                    'user_answer': a,
                    'correct_answer': q['correct_answer']
                })
            
            session.pop('questions', None)
            session.pop('answers', None)
            session.pop('difficulty', None)
            
            return render_template('results.html',
                                score=score,
                                correct_answers=correct_answers,
                                total_questions=total_questions,
                                questions=questions)
        except Exception as e:
            logger.error(f"Error in results calculation: {str(e)}")
            flash('An error occurred while calculating results.', 'error')
            return redirect(url_for('home'))

    @app.route('/logout')
    def logout():
        logger.debug('User logging out')
        session.clear()
        return redirect(url_for('home'))

    @app.errorhandler(404)
    def not_found_error(error):
        logger.error(f'404 error: {str(error)}')
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'500 error: {str(error)}')
        db.session.rollback()
        return render_template('500.html'), 500

    @app.route('/welcome')
    def welcome():
        return render_template('welcome.html')

    @app.route('/public-quiz/<difficulty>', methods=['GET', 'POST'])
    def public_quiz(difficulty):
        """Non-login-required quiz route"""
        logger.debug(f'Accessing public quiz with difficulty {difficulty}')
        
        # Validate difficulty level
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            flash('Invalid difficulty level', 'error')
            return redirect(url_for('welcome'))
        
        # Clear any existing quiz session data when starting a new quiz
        if request.method == 'GET':
            session.clear()  # Clear all session data
            session.modified = True
        
        if request.method == 'POST':
            try:
                answer = request.form.get('answer')
                if not answer:
                    flash('Please select an answer', 'error')
                    return redirect(url_for('public_quiz', difficulty=difficulty))
                
                # Initialize session data if not present
                if 'questions' not in session or 'answers' not in session:
                    session['questions'] = []
                    session['answers'] = []
                    session['difficulty'] = difficulty
                
                # Add the answer to the session
                session['answers'].append(answer)
                session.modified = True
                
                logger.info(f"Answer submitted for public quiz difficulty {difficulty}: {answer}")
                
                # Check if quiz is complete
                if len(session['answers']) >= len(session['questions']):
                    logger.info("Public quiz completed, redirecting to results")
                    return redirect(url_for('public_quiz_results'))
                
                # Get the next question
                current_question = session['questions'][len(session['answers'])]
                response = make_response(render_template('quiz.html',
                                    question=current_question,
                                    difficulty=difficulty,
                                    current_question=len(session['answers']) + 1,
                                    total_questions=len(session['questions'])))
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                return response
            except Exception as e:
                logger.error(f"Error in public quiz submission: {str(e)}")
                flash('An error occurred. Please try again.', 'error')
                return redirect(url_for('welcome'))
        
        try:
            # Initialize a new quiz with 5 questions
            questions = random.sample(SAMPLE_QUESTIONS[difficulty], min(5, len(SAMPLE_QUESTIONS[difficulty])))
            session['questions'] = questions
            session['answers'] = []
            session['difficulty'] = difficulty
            session.modified = True
            logger.info(f"New public quiz initialized with {len(questions)} questions")
            
            # Get first question
            current_question = session['questions'][0]
            logger.info(f"Displaying first question of {len(session['questions'])}")
            
            response = make_response(render_template('quiz.html',
                                question=current_question,
                                difficulty=difficulty,
                                current_question=1,
                                total_questions=len(session['questions'])))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        except Exception as e:
            logger.error(f"Error in public quiz initialization: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('welcome'))

    @app.route('/public-quiz-results')
    def public_quiz_results():
        """Results page for non-login-required quiz"""
        if 'questions' not in session or 'answers' not in session:
            flash('No quiz in progress', 'error')
            return redirect(url_for('welcome'))
        
        try:
            correct_answers = sum(1 for q, a in zip(session['questions'], session['answers'])
                                if a == q['correct_answer'])
            total_questions = len(session['questions'])
            score = int((correct_answers / total_questions) * 100)
            
            questions = []
            for q, a in zip(session['questions'], session['answers']):
                questions.append({
                    'text': q['text'],
                    'user_answer': a,
                    'correct_answer': q['correct_answer']
                })
            
            session.pop('questions', None)
            session.pop('answers', None)
            session.pop('difficulty', None)
            
            return render_template('results.html',
                                score=score,
                                correct_answers=correct_answers,
                                total_questions=total_questions,
                                questions=questions)
        except Exception as e:
            logger.error(f"Error in public quiz results calculation: {str(e)}")
            flash('An error occurred while calculating results.', 'error')
            return redirect(url_for('welcome'))

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        # Clear any quiz-related session data
        session.pop('questions', None)
        session.pop('answers', None)
        session.pop('difficulty', None)
        
        if request.method == 'POST':
            try:
                logger.info("Processing contact form submission")
                name = request.form.get('name')
                email = request.form.get('email')
                subject = request.form.get('subject')
                message = request.form.get('message')
                
                logger.info(f"Form data received - Name: {name}, Email: {email}, Subject: {subject}")
                
                if not all([name, email, subject, message]):
                    logger.warning("Missing required fields in contact form")
                    flash('All fields are required', 'error')
                    return redirect(url_for('contact'))
                
                try:
                    # Create and save the contact message using the model
                    logger.info("Creating new ContactMessage object")
                    contact_message = ContactMessage(
                        name=name,
                        email=email,
                        subject=subject,
                        message=message
                    )
                    logger.info("Adding contact message to database session")
                    db.session.add(contact_message)
                    
                    # Log the current database state
                    logger.info(f"Database URI: {db.engine.url}")
                    logger.info(f"Database tables: {db.engine.table_names()}")
                    
                    try:
                        logger.info("Attempting to commit database transaction")
                        db.session.commit()
                        logger.info("Contact message saved successfully")
                    except Exception as commit_error:
                        logger.error(f"Error during commit: {str(commit_error)}", exc_info=True)
                        db.session.rollback()
                        raise
                    
                    flash('Thank you for your message! We will get back to you soon.', 'success')
                    return redirect(url_for('welcome'))
                except Exception as db_error:
                    logger.error(f"Database error in contact form submission: {str(db_error)}", exc_info=True)
                    db.session.rollback()
                    raise
            except Exception as e:
                logger.error(f"Error in contact form submission: {str(e)}", exc_info=True)
                flash('An error occurred while sending your message. Please try again.', 'error')
                return redirect(url_for('contact'))
        
        # Clear any existing flash messages before rendering the contact form
        get_flashed_messages()
        
        return render_template('contact.html') 