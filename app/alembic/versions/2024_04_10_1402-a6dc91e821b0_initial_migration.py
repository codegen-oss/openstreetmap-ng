"""Initial migration

Revision ID: a6dc91e821b0
Revises:
Create Date: 2024-04-10 14:02:55.421038+00:00

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Text
from sqlalchemy.dialects import postgresql

import app.models.element_member_ref
import app.models.geometry

# revision identifiers, used by Alembic.
revision: str = 'a6dc91e821b0'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('acl_domain',
    sa.Column('domain', sa.Unicode(), nullable=False),
    sa.Column('restrictions', sa.ARRAY(sa.Unicode(), dimensions=1), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('acl_inet',
    sa.Column('inet', postgresql.CIDR(), nullable=False),
    sa.Column('restrictions', sa.ARRAY(sa.Unicode(), dimensions=1), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('acl_mx',
    sa.Column('mx', sa.Unicode(), nullable=False),
    sa.Column('restrictions', sa.ARRAY(sa.Unicode(), dimensions=1), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('note',
    sa.Column('point', app.models.geometry.PointType(), nullable=False),
    sa.Column('closed_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('hidden_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth1_nonce',
    sa.Column('nonce', sa.Unicode(length=255), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('nonce', 'created_at')
    )
    op.create_table('user',
    sa.Column('email', sa.Unicode(length=254), nullable=False),
    sa.Column('display_name', sa.Unicode(length=255), nullable=False),
    sa.Column('password_hashed', sa.Unicode(), nullable=False),
    sa.Column('created_ip', postgresql.INET(), nullable=False),
    sa.Column('status', sa.Enum('pending_terms', 'pending_activation', 'active', name='userstatus'), nullable=False),
    sa.Column('auth_provider', sa.Enum('openid', 'google', 'facebook', 'microsoft', 'github', 'wikipedia', name='authprovider'), nullable=True),
    sa.Column('auth_uid', sa.Unicode(), nullable=True),
    sa.Column('language', sa.Unicode(length=15), nullable=False),
    sa.Column('activity_tracking', sa.Boolean(), nullable=False),
    sa.Column('crash_reporting', sa.Boolean(), nullable=False),
    sa.Column('password_changed_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=True),
    sa.Column('password_salt', sa.Unicode(), nullable=True),
    sa.Column('roles', sa.ARRAY(sa.Enum('moderator', 'administrator', name='userrole'), dimensions=1), server_default='{}', nullable=False),
    sa.Column('description', sa.UnicodeText(), server_default='', nullable=False),
    sa.Column('description_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('editor', sa.Enum('id', 'rapid', 'remote', name='editor'), nullable=True),
    sa.Column('avatar_type', sa.Enum('default', 'gravatar', 'custom', name='avatartype'), server_default='default', nullable=False),
    sa.Column('avatar_id', sa.Unicode(length=64), nullable=True),
    sa.Column('home_point', app.models.geometry.PointType(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('user_display_name_idx', 'user', ['display_name'], unique=True)
    op.create_index('user_email_idx', 'user', ['email'], unique=True)
    op.create_table('changeset',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('closed_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('size', sa.Integer(), server_default='0', nullable=False),
    sa.Column('bounds', app.models.geometry.PolygonType(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diary',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.Unicode(length=255), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('language_code', sa.Unicode(length=15), nullable=False),
    sa.Column('point', app.models.geometry.PointType(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('friendship',
    sa.Column('from_user_id', sa.BigInteger(), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['from_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('from_user_id', 'to_user_id')
    )
    op.create_table('issue',
    sa.Column('report_type', sa.Enum('diary', 'diary_comment', 'note', 'user', name='reporttype'), nullable=False),
    sa.Column('report_id', sa.Unicode(length=32), nullable=False),
    sa.Column('assigned_role', sa.Enum('moderator', 'administrator', name='userrole'), nullable=False),
    sa.Column('status', sa.Enum('open', 'resolved', 'ignored', name='issuestatus'), server_default='open', nullable=False),
    sa.Column('updated_user_id', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['updated_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mail',
    sa.Column('source', sa.Enum('system', 'message', 'diary_comment', name='mailsource'), nullable=False),
    sa.Column('from_user_id', sa.BigInteger(), nullable=True),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('subject', sa.UnicodeText(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('ref', sa.UnicodeText(), nullable=True),
    sa.Column('priority', sa.SmallInteger(), nullable=False),
    sa.Column('processing_counter', sa.SmallInteger(), server_default='0', nullable=False),
    sa.Column('processing_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['from_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('from_user_id', sa.BigInteger(), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('subject', sa.UnicodeText(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('is_read', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('from_hidden', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('to_hidden', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['from_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('note_comment',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('user_ip', postgresql.INET(), nullable=True),
    sa.Column('note_id', sa.BigInteger(), nullable=False),
    sa.Column('event', sa.Enum('opened', 'closed', 'reopened', 'commented', 'hidden', name='noteevent'), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('body_tsvector', postgresql.TSVECTOR(), sa.Computed("to_tsvector('simple', body)", persisted=True), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['note_id'], ['note.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth1_application',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.Column('consumer_key', sa.Unicode(length=40), nullable=False),
    sa.Column('consumer_secret_encrypted', sa.LargeBinary(), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', name='scope'), dimensions=1), nullable=False),
    sa.Column('application_url', sa.Unicode(), nullable=False),
    sa.Column('callback_url', sa.Unicode(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth2_application',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.Column('client_id', sa.Unicode(length=50), nullable=False),
    sa.Column('client_secret_encrypted', sa.LargeBinary(), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', name='scope'), dimensions=1), nullable=False),
    sa.Column('is_confidential', sa.Boolean(), nullable=False),
    sa.Column('redirect_uris', sa.ARRAY(sa.Unicode(), dimensions=1), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('client_id_idx', 'oauth2_application', ['client_id'], unique=True)
    op.create_table('trace',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Unicode(length=255), nullable=False),
    sa.Column('description', sa.Unicode(length=255), nullable=False),
    sa.Column('visibility', sa.Enum('identifiable', 'public', 'trackable', 'private', name='trace_visibility'), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('start_point', app.models.geometry.PointType(), nullable=False),
    sa.Column('file_id', sa.Unicode(length=64), nullable=False),
    sa.Column('tags', sa.ARRAY(sa.Unicode(length=40), dimensions=1), server_default='{}', nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_block',
    sa.Column('from_user_id', sa.BigInteger(), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('acknowledged', sa.Boolean(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('revoked_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('revoked_user_id', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['from_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['revoked_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_pref',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('app_id', sa.BigInteger(), nullable=True),
    sa.Column('key', sa.Unicode(length=255), nullable=False),
    sa.Column('value', sa.Unicode(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'app_id', 'key')
    )
    op.create_table('user_token_account_confirm',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_token_email_change',
    sa.Column('from_email', sa.Unicode(), nullable=False),
    sa.Column('to_email', sa.Unicode(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_token_email_reply',
    sa.Column('mail_source', sa.Enum('system', 'message', 'diary_comment', name='mailsource'), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['to_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_token_session',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('changeset_comment',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('changeset_id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['changeset_id'], ['changeset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('changeset_subscription',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('changeset_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['changeset_id'], ['changeset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('changeset_id', 'user_id')
    )
    op.create_table('diary_comment',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('diary_id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['diary_id'], ['diary.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diary_subscription',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('diary_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['diary_id'], ['diary.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('diary_id', 'user_id')
    )
    op.create_table('element',
    sa.Column('sequence_id', sa.BigInteger(), sa.Identity(always=True, minvalue=1), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('changeset_id', sa.BigInteger(), nullable=False),
    sa.Column('type', sa.Enum('node', 'way', 'relation', name='element_type'), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('version', sa.BigInteger(), nullable=False),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('point', app.models.geometry.PointType(), nullable=True),
    sa.Column('members', app.models.element_member_ref.ElementMemberRefJSONB(astext_type=Text()), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('superseded_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['changeset_id'], ['changeset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('type', 'id', 'version', name='element_pkey')
    )
    op.create_table('issue_comment',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('issue_id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth1_token',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('application_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('token_secret', sa.LargeBinary(length=40), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', name='scope'), dimensions=1), nullable=False),
    sa.Column('callback_url', sa.Unicode(), nullable=True),
    sa.Column('verifier', sa.Unicode(), nullable=True),
    sa.Column('authorized_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['oauth1_application.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth2_token',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('application_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', name='scope'), dimensions=1), nullable=False),
    sa.Column('redirect_uri', sa.Unicode(), nullable=True),
    sa.Column('code_challenge_method', sa.Enum('plain', 'S256', name='oauth2codechallengemethod'), nullable=True),
    sa.Column('code_challenge', sa.Unicode(), nullable=True),
    sa.Column('authorized_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['oauth2_application.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('report',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('issue_id', sa.BigInteger(), nullable=False),
    sa.Column('category', sa.Enum('spam', 'offensive', 'threat', 'vandal', 'personal', 'abusive', 'other', name='reportcategory'), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trace_point',
    sa.Column('trace_id', sa.BigInteger(), nullable=False),
    sa.Column('track_idx', sa.SmallInteger(), nullable=False),
    sa.Column('captured_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('point', app.models.geometry.PointType(), nullable=False),
    sa.Column('elevation', sa.Float(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.ForeignKeyConstraint(['trace_id'], ['trace.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trace_point')
    op.drop_table('report')
    op.drop_table('oauth2_token')
    op.drop_table('oauth1_token')
    op.drop_table('issue_comment')
    op.drop_table('element')
    op.drop_table('diary_subscription')
    op.drop_table('diary_comment')
    op.drop_table('changeset_subscription')
    op.drop_table('changeset_comment')
    op.drop_table('user_token_session')
    op.drop_table('user_token_email_reply')
    op.drop_table('user_token_email_change')
    op.drop_table('user_token_account_confirm')
    op.drop_table('user_pref')
    op.drop_table('user_block')
    op.drop_table('trace')
    op.drop_index('client_id_idx', table_name='oauth2_application')
    op.drop_table('oauth2_application')
    op.drop_table('oauth1_application')
    op.drop_table('note_comment')
    op.drop_table('message')
    op.drop_table('mail')
    op.drop_table('issue')
    op.drop_table('friendship')
    op.drop_table('diary')
    op.drop_table('changeset')
    op.drop_index('user_email_idx', table_name='user')
    op.drop_index('user_display_name_idx', table_name='user')
    op.drop_table('user')
    op.drop_table('oauth1_nonce')
    op.drop_table('note')
    op.drop_table('acl_mx')
    op.drop_table('acl_inet')
    op.drop_table('acl_domain')
    # ### end Alembic commands ###