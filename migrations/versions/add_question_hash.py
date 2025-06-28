"""add question hash

Revision ID: add_question_hash
Revises: 
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_question_hash'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add question_hash column
    op.add_column('questions', sa.Column('question_hash', sa.String(64), nullable=True))
    
    # Create unique index
    op.create_index('uq_questions_hash', 'questions', ['question_hash'], unique=True)
    
    # Generate hashes for existing questions
    connection = op.get_bind()
    questions = connection.execute('SELECT id, text, options, correct_answer FROM questions').fetchall()
    
    for q in questions:
        # Parse options from JSON string if needed
        options = q[2]
        if isinstance(options, str):
            import json
            options = json.loads(options)
        
        # Generate hash
        from models import Question
        question_hash = Question.generate_hash(q[1], options, q[3])
        
        # Update the row
        connection.execute(
            'UPDATE questions SET question_hash = %s WHERE id = %s',
            (question_hash, q[0])
        )
    
    # Make the column non-nullable after populating it
    op.alter_column('questions', 'question_hash',
                    existing_type=sa.String(64),
                    nullable=False)

def downgrade():
    # Remove the unique index
    op.drop_index('uq_questions_hash', table_name='questions')
    
    # Remove the column
    op.drop_column('questions', 'question_hash') 