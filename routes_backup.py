from flask import render_template, request, redirect, url_for, flash, session, jsonify, make_response, get_flashed_messages
from flask_login import login_required, current_user, login_user, AnonymousUserMixin
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
            'category': 'Old Testament',
            'explanation': 'Noah was commanded by God to build an ark to save his family and pairs of all animals from the great flood. (Genesis 6-9)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+6-9&version=NIV'
        },
        {
            'text': 'How many disciples did Jesus have?',
            'options': ['10', '12', '13', '14'],
            'correct_answer': '12',
            'category': 'New Testament',
            'explanation': 'Jesus chose twelve disciples to be His closest followers, also called apostles. (Matthew 10:1-4)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+10%3A1-4&version=NIV'
        },
        {
            'text': 'Who was the first man created by God?',
            'options': ['Adam', 'Eve', 'Noah', 'Abraham'],
            'correct_answer': 'Adam',
            'category': 'Old Testament',
            'explanation': 'Adam was the first human created by God from the dust of the ground. (Genesis 2:7)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+2%3A7&version=NIV'
        },
        {
            'text': 'What was the first miracle Jesus performed?',
            'options': ['Walking on water', 'Turning water into wine', 'Feeding 5000', 'Raising Lazarus'],
            'correct_answer': 'Turning water into wine',
            'category': 'New Testament',
            'explanation': 'Jesus turned water into wine at the wedding in Cana, His first recorded miracle. (John 2:1-11)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+2%3A1-11&version=NIV'
        },
        {
            'text': "Who was thrown into the lion's den?",
            'options': ['David', 'Daniel', 'Joseph', 'Jonah'],
            'correct_answer': 'Daniel',
            'category': 'Old Testament',
            'explanation': 'Daniel was thrown into the lion's den for praying to God, but God protected him. (Daniel 6)',
            'reference': 'https://www.biblegateway.com/passage/?search=Daniel+6&version=NIV'
        },
        {
            'text': "What was the name of Jesus' mother?",
            'options': ['Mary', 'Elizabeth', 'Sarah', 'Rebecca'],
            'correct_answer': 'Mary',
            'category': 'New Testament',
            'explanation': 'Mary was chosen by God to be the mother of Jesus. (Luke 1:26-38)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+1%3A26-38&version=NIV'
        },
        {
            'text': 'Which book comes first in the Bible?',
            'options': ['Genesis', 'Exodus', 'Matthew', 'Psalms'],
            'correct_answer': 'Genesis',
            'category': 'Old Testament',
            'explanation': 'Genesis is the first book of the Bible, describing creation and early history. (Genesis 1:1)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+1%3A1&version=NIV'
        }
    ],
    'Medium': [
        {
            'text': "What was the name of Abraham's wife?",
            'options': ['Sarah', 'Rebecca', 'Rachel', 'Leah'],
            'correct_answer': 'Sarah',
            'category': 'Old Testament',
            'explanation': 'Sarah was Abraham's wife and the mother of Isaac. (Genesis 17:15-19)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+17%3A15-19&version=NIV'
        },
        {
            'text': 'How many days was Jonah in the belly of the fish?',
            'options': ['1', '2', '3', '4'],
            'correct_answer': '3',
            'category': 'Old Testament',
            'explanation': 'Jonah was in the belly of the great fish for three days and three nights. (Jonah 1:17)',
            'reference': 'https://www.biblegateway.com/passage/?search=Jonah+1%3A17&version=NIV'
        },
        {
            'text': 'Who denied Jesus three times?',
            'options': ['Peter', 'John', 'James', 'Andrew'],
            'correct_answer': 'Peter',
            'category': 'New Testament',
            'explanation': 'Peter denied knowing Jesus three times before the rooster crowed. (Luke 22:54-62)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+22%3A54-62&version=NIV'
        },
        {
            'text': 'What was the name of the river where Jesus was baptized?',
            'options': ['Jordan', 'Nile', 'Euphrates', 'Tigris'],
            'correct_answer': 'Jordan',
            'category': 'New Testament',
            'explanation': 'Jesus was baptized by John the Baptist in the Jordan River. (Matthew 3:13-17)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+3%3A13-17&version=NIV'
        },
        {
            'text': 'How many books are in the New Testament?',
            'options': ['27', '39', '66', '73'],
            'correct_answer': '27',
            'category': 'General',
            'explanation': 'The New Testament contains 27 books, from Matthew to Revelation.',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+1&version=NIV'
        },
        {
            'text': 'Who was the first king of Israel?',
            'options': ['Saul', 'David', 'Solomon', 'Samuel'],
            'correct_answer': 'Saul',
            'category': 'Old Testament',
            'explanation': 'Saul was anointed by Samuel as the first king of Israel. (1 Samuel 10:1)',
            'reference': 'https://www.biblegateway.com/passage/?search=1+Samuel+10%3A1&version=NIV'
        },
        {
            'text': 'What was the name of the place where Jesus was born?',
            'options': ['Bethlehem', 'Nazareth', 'Jerusalem', 'Galilee'],
            'correct_answer': 'Bethlehem',
            'category': 'New Testament',
            'explanation': 'Jesus was born in Bethlehem, fulfilling prophecy. (Luke 2:1-7)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+2%3A1-7&version=NIV'
        }
    ],
    'Hard': [
        {
            'text': 'What was the name of the high priest who questioned Jesus?',
            'options': ['Caiaphas', 'Annas', 'Pilate', 'Herod'],
            'correct_answer': 'Caiaphas',
            'category': 'New Testament',
            'explanation': 'Caiaphas was the high priest who led the questioning of Jesus before His crucifixion. (Matthew 26:57-68)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+26%3A57-68&version=NIV'
        },
        {
            'text': 'How many years did the Israelites wander in the wilderness?',
            'options': ['30', '40', '50', '60'],
            'correct_answer': '40',
            'category': 'Old Testament',
            'explanation': 'The Israelites wandered in the wilderness for 40 years before entering the Promised Land. (Numbers 14:33-34)',
            'reference': 'https://www.biblegateway.com/passage/?search=Numbers+14%3A33-34&version=NIV'
        },
        {
            'text': 'What was the name of the place where Jesus was crucified?',
            'options': ['Golgotha', 'Gethsemane', 'Bethlehem', 'Nazareth'],
            'correct_answer': 'Golgotha',
            'category': 'New Testament',
            'explanation': 'Jesus was crucified at Golgotha, also called the Place of the Skull. (John 19:17-18)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+19%3A17-18&version=NIV'
        },
        {
            'text': 'Who was the father of John the Baptist?',
            'options': ['Zechariah', 'Joseph', 'Eli', 'Joachim'],
            'correct_answer': 'Zechariah',
            'category': 'New Testament',
            'explanation': 'Zechariah was a priest and the father of John the Baptist. (Luke 1:5-25)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+1%3A5-25&version=NIV'
        },
        {
            'text': 'What was the name of the mountain where Moses received the Ten Commandments?',
            'options': ['Mount Sinai', 'Mount Horeb', 'Mount Ararat', 'Mount Moriah'],
            'correct_answer': 'Mount Sinai',
            'category': 'Old Testament',
            'explanation': 'Moses received the Ten Commandments from God on Mount Sinai. (Exodus 19-20)',
            'reference': 'https://www.biblegateway.com/passage/?search=Exodus+19-20&version=NIV'
        },
        {
            'text': 'How many days was Jesus in the tomb before His resurrection?',
            'options': ['1', '2', '3', '4'],
            'correct_answer': '3',
            'category': 'New Testament',
            'explanation': 'Jesus was in the tomb for three days before rising from the dead. (Matthew 12:40)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+12%3A40&version=NIV'
        },
        {
            'text': 'What was the name of the prophet who was taken to heaven in a chariot of fire?',
            'options': ['Elijah', 'Elisha', 'Isaiah', 'Jeremiah'],
            'correct_answer': 'Elijah',
            'category': 'Old Testament',
            'explanation': 'Elijah was taken up to heaven in a whirlwind with a chariot of fire. (2 Kings 2:11)',
            'reference': 'https://www.biblegateway.com/passage/?search=2+Kings+2%3A11&version=NIV'
        }
    ]
}

class GuestUser(AnonymousUserMixin):
    is_guest = True
    username = "Guest"

def register_routes(app):
    @app.route('/')
    def home():
        return redirect(url_for('welcome'))

    @app.route('/health')
    def health_check():
        """Simple health check endpoint for Render"""
        return {'status': 'healthy', 'message': 'Bible Quiz AI is running on Render!'}

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
        """Non-login-required quiz route with feedback and scoring"""
        logger.debug(f'Accessing public quiz with difficulty {difficulty}')
        
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            flash('Invalid difficulty level', 'error')
            return redirect(url_for('welcome'))

        # Navigation (next/prev) logic
        next_q = request.args.get('next', type=int)
        prev_q = request.args.get('prev', type=int)

        # Handle navigation from template
        if next_q:
            current_idx = len(session['answers'])
            if current_idx < len(session['questions']):
                # Move to next question
                pass
            else:
                # Quiz completed, go to results
                return redirect(url_for('public_quiz_results'))
            show_feedback = False
        elif prev_q:
            current_idx = max(0, len(session['answers']) - 1)
            if session['answers']:
                session['answers'].pop()
                session['start_times'].pop()
                session.modified = True
            show_feedback = False
        else:
            # Initialize session data if not present
            if 'questions' not in session or 'answers' not in session or 'score' not in session:
                session['questions'] = []
                session['answers'] = []
                session['difficulty'] = difficulty
                session['score'] = 0
                session['start_times'] = []  # Track start time for each question
                session.modified = True

            # Start a new quiz on GET (if no questions or navigation)
            if request.method == 'GET' and not next_q and not prev_q:
                session.clear()
                questions = random.sample(SAMPLE_QUESTIONS[difficulty], min(5, len(SAMPLE_QUESTIONS[difficulty])))
                session['questions'] = questions
                session['answers'] = []
                session['difficulty'] = difficulty
                session['score'] = 0
                session['start_times'] = [datetime.utcnow().timestamp()]  # Start time for Q1
                session.modified = True
                current_idx = 0
                show_feedback = False
            else:
                # Navigation: next/prev
                current_idx = len(session['answers']) if not prev_q else len(session['answers']) - 1
                show_feedback = False

        # Handle answer submission
        if request.method == 'POST':
            answer = request.form.get('answer')
            if not answer:
                flash('Please select an answer', 'error')
                return redirect(url_for('public_quiz', difficulty=difficulty))
            # Calculate time taken for this question
            now = datetime.utcnow().timestamp()
            start_time = session['start_times'][-1] if session['start_times'] else now
            time_taken = max(1, int(now - start_time))  # At least 1 second
            # Scoring: max 20 points per question, -1 per second elapsed (min 5)
            max_points = 20
            min_points = 5
            points = max(min_points, max_points - time_taken)
            # Get current question
            current_idx = len(session['answers'])
            current_question = session['questions'][current_idx]
            is_correct = (answer == current_question['correct_answer'])
            if is_correct:
                session['score'] += points
            session['answers'].append(answer)
            session['start_times'].append(now)
            session.modified = True
            show_feedback = True
            # If last question, go to results
            if len(session['answers']) >= len(session['questions']):
                return redirect(url_for('public_quiz_results'))
        else:
            # Not POST: get current question
            current_question = session['questions'][current_idx]

        # Prepare template variables
        user_answer = session['answers'][-1] if show_feedback and session['answers'] else None
        progress_percent = int(((current_idx+1)/len(session['questions']))*100)
        
        # Add explanation and reference to question object if not present
        if 'explanation' not in current_question:
            current_question['explanation'] = f"This question tests your knowledge of {difficulty.lower()} biblical concepts. Study the relevant passages to deepen your understanding."
        if 'reference' not in current_question:
            current_question['reference'] = "https://www.biblegateway.com/"
            
        return render_template('quiz.html',
            question=current_question,
            difficulty=difficulty,
            current_question=current_idx+1,
            total_questions=len(session['questions']),
            show_feedback=show_feedback,
            user_answer=user_answer,
            score=session.get('score', 0),
            max_score=len(session['questions'])*20,
            progress_percent=progress_percent
        )

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

    @app.route('/play-as-guest')
    def play_as_guest():
        guest = User(username="Guest", is_guest=True)
        db.session.add(guest)
        db.session.commit()
        login_user(guest)
        return redirect(url_for('quiz')) 