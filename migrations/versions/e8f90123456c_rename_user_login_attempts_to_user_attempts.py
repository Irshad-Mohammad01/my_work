"""Rename user_login_attempts to user_attempts and add OTP rate limit fields

Revision ID: e8f90123456c
Revises: c7f89123456b
Create Date: 2026-08-08 23:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8f90123456c'
down_revision = 'c7f89123456b'
branch_labels = None
depends_on = None


def upgrade():
    # Rename table user_login_attempts -> user_attempts
    op.rename_table('user_login_attempts', 'user_attempts')
    
    # Rename column failed_attempts -> failed_login_attempts
    with op.batch_alter_table('user_attempts', schema=None) as batch_op:
        batch_op.alter_column('failed_attempts', new_column_name='failed_login_attempts', existing_type=sa.Integer())
        batch_op.add_column(sa.Column('otp_request_attempts', sa.Integer(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('first_otp_request_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_otp_request_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('reason', sa.String(length=50), nullable=True))


def downgrade():
    with op.batch_alter_table('user_attempts', schema=None) as batch_op:
        batch_op.drop_column('reason')
        batch_op.drop_column('last_otp_request_at')
        batch_op.drop_column('first_otp_request_at')
        batch_op.drop_column('otp_request_attempts')
        batch_op.alter_column('failed_login_attempts', new_column_name='failed_attempts', existing_type=sa.Integer())
        
    op.rename_table('user_attempts', 'user_login_attempts')
