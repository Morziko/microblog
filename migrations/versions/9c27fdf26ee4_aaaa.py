"""AAaa

Revision ID: 9c27fdf26ee4
Revises: 
Create Date: 2019-06-24 20:53:04.260559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c27fdf26ee4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('preambul',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('len_post', sa.Integer(), nullable=True),
    sa.Column('preamble_id', sa.Integer(), nullable=True),
    sa.Column('last_message_read_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=40), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency', sa.String(length=40), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('history_city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=40), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('history_currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency', sa.String(length=40), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('len_message', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_timestamp'), 'message', ['timestamp'], unique=False)
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_name'), 'notification', ['name'], unique=False)
    op.create_index(op.f('ix_notification_timestamp'), 'notification', ['timestamp'], unique=False)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=240), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('FileContent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['message.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_timestamp'), 'comment', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_timestamp'), table_name='comment')
    op.drop_table('comment')
    op.drop_table('FileContent')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_notification_timestamp'), table_name='notification')
    op.drop_index(op.f('ix_notification_name'), table_name='notification')
    op.drop_table('notification')
    op.drop_index(op.f('ix_message_timestamp'), table_name='message')
    op.drop_table('message')
    op.drop_table('history_currency')
    op.drop_table('history_city')
    op.drop_table('followers')
    op.drop_table('currency')
    op.drop_table('city')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('preambul')
    ### end Alembic commands ###
