"""add day and question type columns

Revision ID: add_day_and_type_columns
Revises: add_question_hash
Create Date: 2024-12-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_day_and_type_columns'
down_revision = 'add_question_hash'
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns
    op.add_column('questions', sa.Column('day', sa.Integer(), nullable=True))
    op.add_column('questions', sa.Column('question_type', sa.String(50), nullable=True))
    
    # Add admin column to users table
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True, default=False))
    
    # Set default values for existing questions
    connection = op.get_bind()
    connection.execute('UPDATE questions SET day = 1, question_type = \'Factual\' WHERE day IS NULL')
    
    # Make columns non-nullable after setting default values
    op.alter_column('questions', 'day', nullable=False)
    op.alter_column('questions', 'question_type', nullable=False)
    
    # Remove quiz_id column if it exists
    try:
        op.drop_column('questions', 'quiz_id')
    except:
        pass  # Column might not exist
    
    # Drop quizzes table if it exists
    try:
        op.drop_table('quizzes')
    except:
        pass  # Table might not exist

def downgrade():
    # Recreate quizzes table
    op.create_table('quizzes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('difficulty', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add quiz_id column back
    op.add_column('questions', sa.Column('quiz_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'questions', 'quizzes', ['quiz_id'], ['id'])
    
    # Remove new columns
    op.drop_column('questions', 'question_type')
    op.drop_column('questions', 'day')
    op.drop_column('users', 'is_admin') 