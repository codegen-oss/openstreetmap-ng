"""Initial migration

Revision ID: 194c0c86a069
Revises:
Create Date: 2024-07-31 10:59:47.215883+00:00

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

import app.models.geometry

# revision identifiers, used by Alembic.
revision: str = '194c0c86a069'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('acl_domain',
    sa.Column('domain', sa.Unicode(), nullable=False),
    sa.Column('restrictions', sa.ARRAY(sa.Unicode(), dimensions=1), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('acl_inet',
    sa.Column('inet', postgresql.CIDR(), nullable=False),
    sa.Column('restrictions', sa.ARRAY(sa.Unicode(), dimensions=1), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('acl_mx',
    sa.Column('mx', sa.Unicode(), nullable=False),
    sa.Column('restrictions', sa.ARRAY(sa.Unicode(), dimensions=1), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('element_member',
    sa.Column('sequence_id', sa.BigInteger(), nullable=False),
    sa.Column('order', sa.SmallInteger(), nullable=False),
    sa.Column('type', sa.Enum('node', 'way', 'relation', name='element_type'), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('role', sa.Unicode(length=255), nullable=False),
    sa.PrimaryKeyConstraint('sequence_id', 'order', name='element_member_pkey')
    )
    op.create_index('element_member_idx', 'element_member', ['type', 'id', 'sequence_id'], unique=False)
    op.create_table('note',
    sa.Column('point', app.models.geometry.PointType(), nullable=False),
    sa.Column('closed_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=True),
    sa.Column('hidden_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('email', sa.Unicode(length=254), nullable=False),
    sa.Column('display_name', sa.Unicode(length=255), nullable=False),
    sa.Column('password_hashed', sa.Unicode(length=255), nullable=False),
    sa.Column('created_ip', postgresql.INET(), nullable=False),
    sa.Column('status', sa.Enum('pending_terms', 'pending_activation', 'active', name='userstatus'), nullable=False),
    sa.Column('auth_provider', sa.Enum('openid', 'google', 'facebook', 'microsoft', 'github', 'wikipedia', name='authprovider'), nullable=True),
    sa.Column('auth_uid', sa.Unicode(), nullable=True),
    sa.Column('language', sa.Unicode(length=15), nullable=False),
    sa.Column('activity_tracking', sa.Boolean(), nullable=False),
    sa.Column('crash_reporting', sa.Boolean(), nullable=False),
    sa.Column('scheduled_delete_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=True),
    sa.Column('password_changed_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=True),
    sa.Column('roles', sa.ARRAY(sa.Enum('moderator', 'administrator', name='userrole'), as_tuple=True, dimensions=1), server_default='{}', nullable=False),
    sa.Column('description', sa.UnicodeText(), server_default='', nullable=False),
    sa.Column('description_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('editor', sa.Enum('id', 'rapid', 'remote', name='editor'), nullable=True),
    sa.Column('avatar_type', sa.Enum('default', 'gravatar', 'custom', name='avatartype'), server_default='default', nullable=False),
    sa.Column('avatar_id', sa.Unicode(length=64), nullable=True),
    sa.Column('home_point', app.models.geometry.PointType(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('user_display_name_idx', 'user', ['display_name'], unique=True)
    op.create_index('user_email_idx', 'user', ['email'], unique=True)
    op.create_index('user_pending_idx', 'user', ['created_at'], unique=False, postgresql_where=sa.text("status = 'pending_activation' OR status = 'pending_terms'"))
    op.create_table('changeset',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('closed_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=True),
    sa.Column('size', sa.Integer(), server_default='0', nullable=False),
    sa.Column('union_bounds', app.models.geometry.PolygonType(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('changeset_closed_at_idx', 'changeset', ['closed_at'], unique=False, postgresql_where=sa.text('closed_at IS NOT NULL'))
    op.create_index('changeset_created_at_idx', 'changeset', ['created_at'], unique=False)
    op.create_index('changeset_empty_idx', 'changeset', ['closed_at'], unique=False, postgresql_where=sa.text('closed_at IS NOT NULL AND size = 0'))
    op.create_index('changeset_open_idx', 'changeset', ['updated_at'], unique=False, postgresql_where=sa.text('closed_at IS NULL'))
    op.create_index('changeset_union_bounds_idx', 'changeset', ['union_bounds'], unique=False, postgresql_where=sa.text('union_bounds IS NOT NULL'), postgresql_using='gist')
    op.create_index('changeset_user_idx', 'changeset', ['user_id', 'id'], unique=False, postgresql_where=sa.text('user_id IS NOT NULL'))
    op.create_table('diary',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.Unicode(length=255), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('language', sa.Unicode(length=15), nullable=False),
    sa.Column('point', app.models.geometry.PointType(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
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
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
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
    sa.Column('processing_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['from_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('mail_processing_at_idx', 'mail', ['processing_at'], unique=False)
    op.create_table('message',
    sa.Column('from_user_id', sa.BigInteger(), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('subject', sa.UnicodeText(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('is_read', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('from_hidden', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('to_hidden', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
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
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['note_id'], ['note.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('note_subscription',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('note_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['note_id'], ['note.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('note_id', 'user_id')
    )
    op.create_table('oauth2_application',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.Unicode(length=50), nullable=False),
    sa.Column('client_id', sa.Unicode(length=50), nullable=False),
    sa.Column('client_secret_encrypted', sa.LargeBinary(), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', 'read_email', 'skip_authorization', 'web_user', 'role_moderator', 'role_administrator', name='scope'), as_tuple=True, dimensions=1), nullable=False),
    sa.Column('is_confidential', sa.Boolean(), nullable=False),
    sa.Column('redirect_uris', sa.ARRAY(sa.Unicode(length=1000), dimensions=1), nullable=False),
    sa.Column('avatar_id', sa.Unicode(length=64), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('oauth2_application_client_id_idx', 'oauth2_application', ['client_id'], unique=True)
    op.create_table('trace',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Unicode(length=255), nullable=False),
    sa.Column('description', sa.Unicode(length=255), nullable=False),
    sa.Column('visibility', sa.Enum('identifiable', 'public', 'trackable', 'private', name='trace_visibility'), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Unicode(length=64), nullable=False),
    sa.Column('tags', sa.ARRAY(sa.Unicode(length=40), dimensions=1), server_default='{}', nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_block',
    sa.Column('from_user_id', sa.BigInteger(), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=True),
    sa.Column('acknowledged', sa.Boolean(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('revoked_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=True),
    sa.Column('revoked_user_id', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
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
    sa.Column('user_email_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_token_email_change',
    sa.Column('new_email', sa.Unicode(length=254), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('user_email_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_token_email_reply',
    sa.Column('mail_source', sa.Enum('system', 'message', 'diary_comment', name='mailsource'), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('user_email_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['to_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_token_reset_password',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('user_email_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('changeset_bounds',
    sa.Column('changeset_id', sa.BigInteger(), nullable=False),
    sa.Column('bounds', app.models.geometry.PolygonType(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['changeset_id'], ['changeset.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('changeset_bounds_bounds_idx', 'changeset_bounds', ['bounds'], unique=False, postgresql_using='gist')
    op.create_index('changeset_bounds_id_idx', 'changeset_bounds', ['changeset_id'], unique=False)
    op.create_table('changeset_comment',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('changeset_id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['changeset_id'], ['changeset.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('changeset_comment_idx', 'changeset_comment', ['changeset_id', 'created_at'], unique=False)
    op.create_table('changeset_subscription',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('changeset_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['changeset_id'], ['changeset.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('changeset_id', 'user_id')
    )
    op.create_table('diary_comment',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('diary_id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
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
    sa.Column('sequence_id', sa.BigInteger(), nullable=False),
    sa.Column('changeset_id', sa.BigInteger(), nullable=False),
    sa.Column('type', sa.Enum('node', 'way', 'relation', name='element_type'), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('version', sa.BigInteger(), nullable=False),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('point', app.models.geometry.PointType(), nullable=True),
    sa.Column('next_sequence_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['changeset_id'], ['changeset.id'], ),
    sa.PrimaryKeyConstraint('sequence_id', name='element_pkey')
    )
    op.create_index('element_changeset_idx', 'element', ['changeset_id'], unique=False)
    op.create_index('element_current_idx', 'element', ['type', 'id', 'next_sequence_id', 'sequence_id'], unique=False)
    op.create_index('element_node_point_idx', 'element', ['point'], unique=False, postgresql_where=sa.text("type = 'node' AND visible = true AND next_sequence_id IS NULL"), postgresql_using='gist')
    op.create_index('element_version_idx', 'element', ['type', 'id', 'version'], unique=False)
    op.create_table('issue_comment',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('issue_id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False, minvalue=1), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth2_token',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('application_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', 'read_email', 'skip_authorization', 'web_user', 'role_moderator', 'role_administrator', name='scope'), as_tuple=True, dimensions=1), nullable=False),
    sa.Column('redirect_uri', sa.Unicode(length=1000), nullable=True),
    sa.Column('code_challenge_method', sa.Enum('plain', 'S256', name='oauth2codechallengemethod'), nullable=True),
    sa.Column('code_challenge', sa.Unicode(length=255), nullable=True),
    sa.Column('authorized_at', postgresql.TIMESTAMP(timezone=timezone=True), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['oauth2_application.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('oauth2_token_hashed_idx', 'oauth2_token', ['token_hashed'], unique=False)
    op.create_index('oauth2_token_user_app_idx', 'oauth2_token', ['user_id', 'application_id'], unique=False)
    op.create_table('report',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('issue_id', sa.BigInteger(), nullable=False),
    sa.Column('category', sa.Enum('spam', 'offensive', 'threat', 'vandal', 'personal', 'abusive', 'other', name='reportcategory'), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=timezone=True), server_default=sa.text('statement_timestamp()'), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trace_segment',
    sa.Column('trace_id', sa.BigInteger(), nullable=False),
    sa.Column('track_num', sa.SmallInteger(), nullable=False),
    sa.Column('segment_num', sa.SmallInteger(), nullable=False),
    sa.Column('points', app.models.geometry.MultiPointType(), nullable=False),
    sa.Column('capture_times', sa.ARRAY(postgresql.TIMESTAMP(timezone=timezone=True), dimensions=1), nullable=True),
    sa.Column('elevations', sa.ARRAY(sa.REAL()), nullable=True),
    sa.ForeignKeyConstraint(['trace_id'], ['trace.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('trace_id', 'track_num', 'segment_num')
    )
    op.create_index('trace_segment_points_idx', 'trace_segment', ['points'], unique=False, postgresql_using='gist')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('trace_segment_points_idx', table_name='trace_segment', postgresql_using='gist')
    op.drop_table('trace_segment')
    op.drop_table('report')
    op.drop_index('oauth2_token_user_app_idx', table_name='oauth2_token')
    op.drop_index('oauth2_token_hashed_idx', table_name='oauth2_token')
    op.drop_table('oauth2_token')
    op.drop_table('issue_comment')
    op.drop_index('element_version_idx', table_name='element')
    op.drop_index('element_node_point_idx', table_name='element', postgresql_where=sa.text("type = 'node' AND visible = true AND next_sequence_id IS NULL"), postgresql_using='gist')
    op.drop_index('element_current_idx', table_name='element')
    op.drop_index('element_changeset_idx', table_name='element')
    op.drop_table('element')
    op.drop_table('diary_subscription')
    op.drop_table('diary_comment')
    op.drop_table('changeset_subscription')
    op.drop_index('changeset_comment_idx', table_name='changeset_comment')
    op.drop_table('changeset_comment')
    op.drop_index('changeset_bounds_id_idx', table_name='changeset_bounds')
    op.drop_index('changeset_bounds_bounds_idx', table_name='changeset_bounds', postgresql_using='gist')
    op.drop_table('changeset_bounds')
    op.drop_table('user_token_reset_password')
    op.drop_table('user_token_email_reply')
    op.drop_table('user_token_email_change')
    op.drop_table('user_token_account_confirm')
    op.drop_table('user_pref')
    op.drop_table('user_block')
    op.drop_table('trace')
    op.drop_index('oauth2_application_client_id_idx', table_name='oauth2_application')
    op.drop_table('oauth2_application')
    op.drop_table('note_subscription')
    op.drop_table('note_comment')
    op.drop_table('message')
    op.drop_index('mail_processing_at_idx', table_name='mail')
    op.drop_table('mail')
    op.drop_table('issue')
    op.drop_table('friendship')
    op.drop_table('diary')
    op.drop_index('changeset_user_idx', table_name='changeset', postgresql_where=sa.text('user_id IS NOT NULL'))
    op.drop_index('changeset_union_bounds_idx', table_name='changeset', postgresql_where=sa.text('union_bounds IS NOT NULL'), postgresql_using='gist')
    op.drop_index('changeset_open_idx', table_name='changeset', postgresql_where=sa.text('closed_at IS NULL'))
    op.drop_index('changeset_empty_idx', table_name='changeset', postgresql_where=sa.text('closed_at IS NOT NULL AND size = 0'))
    op.drop_index('changeset_created_at_idx', table_name='changeset')
    op.drop_index('changeset_closed_at_idx', table_name='changeset', postgresql_where=sa.text('closed_at IS NOT NULL'))
    op.drop_table('changeset')
    op.drop_index('user_pending_idx', table_name='user', postgresql_where=sa.text("status = 'pending_activation' OR status = 'pending_terms'"))
    op.drop_index('user_email_idx', table_name='user')
    op.drop_index('user_display_name_idx', table_name='user')
    op.drop_table('user')
    op.drop_table('note')
    op.drop_index('element_member_idx', table_name='element_member')
    op.drop_table('element_member')
    op.drop_table('acl_mx')
    op.drop_table('acl_inet')
    op.drop_table('acl_domain')
    # ### end Alembic commands ###
