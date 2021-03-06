"""Data Models

Revision ID: 63f487313801
Revises: 
Create Date: 2020-09-23 22:14:45.451894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63f487313801'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('education',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course', sa.String(), nullable=False),
    sa.Column('school', sa.String(), nullable=False),
    sa.Column('date_started', sa.DateTime(), nullable=False),
    sa.Column('date_end', sa.DateTime(), nullable=True),
    sa.Column('degree_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_education_course'), 'education', ['course'], unique=False)
    op.create_index(op.f('ix_education_id'), 'education', ['id'], unique=False)
    op.create_index(op.f('ix_education_school'), 'education', ['school'], unique=False)
    op.create_table('experience',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.Column('date_started', sa.DateTime(), nullable=False),
    sa.Column('date_end', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_experience_company'), 'experience', ['company'], unique=False)
    op.create_index(op.f('ix_experience_id'), 'experience', ['id'], unique=False)
    op.create_index(op.f('ix_experience_title'), 'experience', ['title'], unique=False)
    op.create_table('hobbies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hobbies_id'), 'hobbies', ['id'], unique=False)
    op.create_index(op.f('ix_hobbies_name'), 'hobbies', ['name'], unique=True)
    op.create_table('languages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_languages_id'), 'languages', ['id'], unique=False)
    op.create_index(op.f('ix_languages_name'), 'languages', ['name'], unique=True)
    op.create_table('skill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_skill_id'), 'skill', ['id'], unique=False)
    op.create_index(op.f('ix_skill_name'), 'skill', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('about_me', sa.Text(), nullable=True),
    sa.Column('current_job', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_firstname'), 'user', ['firstname'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_lastname'), 'user', ['lastname'], unique=False)
    op.create_table('users_educations',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('education_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['education_id'], ['education.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('users_hobbies',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('hobbie_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hobbie_id'], ['hobbies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('users_jobs',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['experience.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('users_languages',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['language_id'], ['languages.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('users_skills',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_skills')
    op.drop_table('users_languages')
    op.drop_table('users_jobs')
    op.drop_table('users_hobbies')
    op.drop_table('users_educations')
    op.drop_index(op.f('ix_user_lastname'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_firstname'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_skill_name'), table_name='skill')
    op.drop_index(op.f('ix_skill_id'), table_name='skill')
    op.drop_table('skill')
    op.drop_index(op.f('ix_languages_name'), table_name='languages')
    op.drop_index(op.f('ix_languages_id'), table_name='languages')
    op.drop_table('languages')
    op.drop_index(op.f('ix_hobbies_name'), table_name='hobbies')
    op.drop_index(op.f('ix_hobbies_id'), table_name='hobbies')
    op.drop_table('hobbies')
    op.drop_index(op.f('ix_experience_title'), table_name='experience')
    op.drop_index(op.f('ix_experience_id'), table_name='experience')
    op.drop_index(op.f('ix_experience_company'), table_name='experience')
    op.drop_table('experience')
    op.drop_index(op.f('ix_education_school'), table_name='education')
    op.drop_index(op.f('ix_education_id'), table_name='education')
    op.drop_index(op.f('ix_education_course'), table_name='education')
    op.drop_table('education')
    # ### end Alembic commands ###
