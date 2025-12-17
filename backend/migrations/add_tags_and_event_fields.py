"""Add tags system and expand event model

Revision ID: add_tags_and_event_fields
Revises: 
Create Date: 2025-12-17

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'add_tags_and_event_fields'
down_revision = None  # Update this with your latest migration
branch_labels = None
depends_on = None


def upgrade():
    # Create tags table
    op.create_table('tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=True)
    
    # Create recipe_tags association table
    op.create_table('recipe_tags',
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
        sa.PrimaryKeyConstraint('recipe_id', 'tag_id')
    )
    
    # Add new columns to events table
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('client_company', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('contact_name', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('contact_email', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('contact_phone', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('event_end_time', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('event_type', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('service_type', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('adult_count', sa.Integer(), nullable=True, server_default='0'))
        batch_op.add_column(sa.Column('minor_count', sa.Integer(), nullable=True, server_default='0'))
        batch_op.add_column(sa.Column('special_diets', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('venue_city', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('venue_state', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('venue_zip', sa.String(length=20), nullable=True))
    
    # Add new columns to proposals table
    with op.batch_alter_table('proposals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('client_snapshot', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('event_snapshot', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('menu_snapshot', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('subtotal', sa.Float(), nullable=True, server_default='0.0'))
        batch_op.add_column(sa.Column('discount_amount', sa.Float(), nullable=True, server_default='0.0'))
        batch_op.add_column(sa.Column('notes', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # Remove columns from proposals
    with op.batch_alter_table('proposals', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('notes')
        batch_op.drop_column('discount_amount')
        batch_op.drop_column('subtotal')
        batch_op.drop_column('menu_snapshot')
        batch_op.drop_column('event_snapshot')
        batch_op.drop_column('client_snapshot')
    
    # Remove columns from events
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('venue_zip')
        batch_op.drop_column('venue_state')
        batch_op.drop_column('venue_city')
        batch_op.drop_column('special_diets')
        batch_op.drop_column('minor_count')
        batch_op.drop_column('adult_count')
        batch_op.drop_column('service_type')
        batch_op.drop_column('event_type')
        batch_op.drop_column('event_end_time')
        batch_op.drop_column('contact_phone')
        batch_op.drop_column('contact_email')
        batch_op.drop_column('contact_name')
        batch_op.drop_column('client_company')
    
    # Drop tables
    op.drop_table('recipe_tags')
    op.drop_index(op.f('ix_tags_name'), table_name='tags')
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
