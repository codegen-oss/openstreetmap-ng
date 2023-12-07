"""Initial migration

Revision ID: 1edfe6805def
Revises:
Create Date: 2023-12-07 12:01:27.308307+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Text
import models.element_member_type
import models.geometry_type
from geoalchemy2 import Geometry
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1edfe6805def'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('acl_domain',
    sa.Column('domain', sa.Unicode(), nullable=False),
    sa.Column('restrictions', sa.ARRAY(sa.Unicode()), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('acl_inet',
    sa.Column('inet', postgresql.CIDR(), nullable=False),
    sa.Column('restrictions', sa.ARRAY(sa.Unicode()), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('acl_mx',
    sa.Column('mx', sa.Unicode(), nullable=False),
    sa.Column('restrictions', sa.ARRAY(sa.Unicode()), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cache',
    sa.Column('id', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('value', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_geospatial_table('note',
    sa.Column('point', models.geometry_type.PointType(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.Column('hidden_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth1_nonce',
    sa.Column('nonce', sa.Unicode(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('nonce', 'created_at')
    )
    op.create_geospatial_table('user',
    sa.Column('email', sa.Unicode(length=254), nullable=False),
    sa.Column('display_name', sa.Unicode(), nullable=False),
    sa.Column('password_hashed', sa.Unicode(), nullable=False),
    sa.Column('created_ip', postgresql.INET(), nullable=False),
    sa.Column('status', sa.Enum('pending', 'active', name='userstatus'), nullable=False),
    sa.Column('auth_provider', sa.Enum('openid', 'google', 'facebook', 'microsoft', 'github', 'wikipedia', name='authprovider'), nullable=True),
    sa.Column('auth_uid', sa.Unicode(), nullable=True),
    sa.Column('languages', sa.ARRAY(sa.Unicode(length=10)), nullable=False),
    sa.Column('password_changed_at', sa.DateTime(), nullable=True),
    sa.Column('password_salt', sa.Unicode(), nullable=True),
    sa.Column('consider_public_domain', sa.Boolean(), nullable=False),
    sa.Column('roles', sa.ARRAY(sa.Enum('moderator', 'administrator', name='userrole')), nullable=False),
    sa.Column('description', sa.UnicodeText(), nullable=False),
    sa.Column('description_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('editor', sa.Enum('id', 'remote', name='editor'), nullable=True),
    sa.Column('avatar_type', sa.Enum('default', 'gravatar', 'custom', name='avatartype'), nullable=False),
    sa.Column('avatar_id', sa.Unicode(length=64), nullable=True),
    sa.Column('home_point', models.geometry_type.PointType(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('home_zoom', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('display_name'),
    sa.UniqueConstraint('email')
    )
    op.create_geospatial_table('changeset',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('boundary', models.geometry_type.PolygonType(geometry_type='POLYGON', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_geospatial_table('diary',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.Unicode(length=255), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('language_code', sa.Unicode(length=10), nullable=False),
    sa.Column('point', models.geometry_type.PointType(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
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
    sa.Column('status', sa.Enum('open', 'resolved', 'ignored', name='issuestatus'), nullable=False),
    sa.Column('updated_user_id', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['updated_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mail',
    sa.Column('from_user_id', sa.BigInteger(), nullable=True),
    sa.Column('from_type', sa.Enum('system', 'message', 'diary_comment', name='mailfromtype'), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('subject', sa.UnicodeText(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('ref', sa.UnicodeText(), nullable=True),
    sa.Column('priority', sa.SmallInteger(), nullable=False),
    sa.Column('processing_counter', sa.SmallInteger(), nullable=False),
    sa.Column('processing_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
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
    sa.Column('is_read', sa.Boolean(), nullable=False),
    sa.Column('from_hidden', sa.Boolean(), nullable=False),
    sa.Column('to_hidden', sa.Boolean(), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
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
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['note_id'], ['note.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth1_application',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.Column('consumer_key', sa.Unicode(length=40), nullable=False),
    sa.Column('consumer_secret_encrypted', sa.LargeBinary(), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', name='scope')), nullable=False),
    sa.Column('application_url', sa.Unicode(), nullable=False),
    sa.Column('callback_url', sa.Unicode(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth2_application',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.Column('client_id', sa.Unicode(length=50), nullable=False),
    sa.Column('client_secret_encrypted', sa.LargeBinary(), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', name='scope')), nullable=False),
    sa.Column('type', sa.Enum('public', 'confidential', name='oauth2applicationtype'), nullable=False),
    sa.Column('redirect_uris', sa.ARRAY(sa.Unicode()), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_geospatial_table('trace',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.Column('description', sa.Unicode(), nullable=False),
    sa.Column('visibility', sa.Enum('identifiable', 'public', 'trackable', 'private', name='tracevisibility'), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('start_point', models.geometry_type.PointType(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('file_id', sa.Unicode(length=64), nullable=False),
    sa.Column('image_id', sa.Unicode(length=64), nullable=False),
    sa.Column('icon_id', sa.Unicode(length=64), nullable=False),
    sa.Column('tags', sa.ARRAY(sa.Unicode()), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_block',
    sa.Column('from_user_id', sa.BigInteger(), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.Column('acknowledged', sa.Boolean(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('revoked_at', sa.DateTime(), nullable=True),
    sa.Column('revoked_user_id', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
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
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_token_email_change',
    sa.Column('from_email', sa.Unicode(), nullable=False),
    sa.Column('to_email', sa.Unicode(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_token_email_reply',
    sa.Column('source_type', sa.Enum('system', 'message', 'diary_comment', name='mailfromtype'), nullable=False),
    sa.Column('to_user_id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['to_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_token_session',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('changeset_comment',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('changeset_id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
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
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
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
    op.create_geospatial_table('element',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('changeset_id', sa.BigInteger(), nullable=False),
    sa.Column('type', sa.Enum('node', 'way', 'relation', name='elementtype'), nullable=False),
    sa.Column('typed_id', sa.BigInteger(), nullable=False),
    sa.Column('version', sa.BigInteger(), nullable=False),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('point', models.geometry_type.PointType(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('members', models.element_member_type.ElementMemberRefType(astext_type=Text()), nullable=False),
    sa.Column('superseded_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['changeset_id'], ['changeset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type', 'typed_id', 'version')
    )
    op.create_table('issue_comment',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('issue_id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth1_token',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('application_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('token_secret', sa.LargeBinary(length=40), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', name='scope')), nullable=False),
    sa.Column('callback_url', sa.Unicode(), nullable=True),
    sa.Column('verifier', sa.Unicode(), nullable=True),
    sa.Column('authorized_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['oauth1_application.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth2_token',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('application_id', sa.BigInteger(), nullable=False),
    sa.Column('token_hashed', sa.LargeBinary(length=32), nullable=False),
    sa.Column('scopes', sa.ARRAY(sa.Enum('read_prefs', 'write_prefs', 'write_diary', 'write_api', 'read_gpx', 'write_gpx', 'write_notes', name='scope')), nullable=False),
    sa.Column('redirect_uri', sa.Unicode(), nullable=False),
    sa.Column('code_challenge_method', sa.Enum('plain', 'S256', name='oauth2codechallengemethod'), nullable=True),
    sa.Column('code_challenge', sa.Unicode(), nullable=True),
    sa.Column('authorized_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['oauth2_application.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('report',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('issue_id', sa.BigInteger(), nullable=False),
    sa.Column('category', sa.Enum('spam', 'offensive', 'threat', 'vandal', 'personal', 'abusive', 'other', name='reportcategory'), nullable=False),
    sa.Column('body', sa.UnicodeText(), nullable=False),
    sa.Column('body_rich_hash', sa.LargeBinary(length=32), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_geospatial_table('trace_point',
    sa.Column('trace_id', sa.BigInteger(), nullable=False),
    sa.Column('track_idx', sa.SmallInteger(), nullable=False),
    sa.Column('captured_at', sa.DateTime(), nullable=False),
    sa.Column('point', models.geometry_type.PointType(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('elevation', sa.Float(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['trace_id'], ['trace.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_geospatial_table('trace_point')
    op.drop_table('report')
    op.drop_table('oauth2_token')
    op.drop_table('oauth1_token')
    op.drop_table('issue_comment')
    op.drop_geospatial_table('element')
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
    op.drop_geospatial_table('trace')
    op.drop_table('oauth2_application')
    op.drop_table('oauth1_application')
    op.drop_table('note_comment')
    op.drop_table('message')
    op.drop_table('mail')
    op.drop_table('issue')
    op.drop_table('friendship')
    op.drop_geospatial_table('diary')
    op.drop_geospatial_table('changeset')
    op.drop_geospatial_table('user')
    op.drop_table('oauth1_nonce')
    op.drop_geospatial_table('note')
    op.drop_table('cache')
    op.drop_table('acl_mx')
    op.drop_table('acl_inet')
    op.drop_table('acl_domain')
    # ### end Alembic commands ###
