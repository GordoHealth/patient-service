"""initial_database_migration.py
Revision ID: db601437d90f
Revises:
Create Date: 2023-08-06 05:12:47.078508
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'db601437d90f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()

    if 'api_keys' not in tables:
        op.create_table('api_keys',
                        sa.Column('access_token', sa.String(), nullable=True),
                        sa.Column('name', sa.String(), nullable=False),
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                        sa.PrimaryKeyConstraint('id')
                        )
    if 'products' not in tables:
        op.create_table('products',
                        sa.Column('name', sa.String(), nullable=False),
                        sa.Column('level', sa.String(), nullable=False),
                        sa.Column('key', sa.String(), nullable=False),
                        sa.Column('isbn', sa.String(length=255), nullable=True),
                        sa.Column('active', sa.Boolean(), server_default=sa.text('true'), nullable=True),
                        sa.Column('official_name', sa.String(), nullable=False),
                        sa.Column('short_name', sa.String(), nullable=False),
                        sa.Column('evolve_isbn', sa.String(length=255), nullable=False),
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                        sa.PrimaryKeyConstraint('id')
                        )

    indexes = [index["name"] for index in inspector.get_indexes('products')]
    if 'index_products_on_active_and_name_and_level' not in indexes:
        op.create_index('index_products_on_active_and_name_and_level',
                        'products', ['active', 'name', 'level'], unique=False)

    if 'index_products_on_evolve_isbn' not in indexes:
        op.create_index('index_products_on_evolve_isbn', 'products', ['evolve_isbn'], unique=True)

    if 'index_products_on_isbn' not in indexes:
        op.create_index('index_products_on_isbn', 'products', ['isbn'], unique=False)

    if 'index_products_on_key' not in indexes:
        op.create_index('index_products_on_key', 'products', ['key'], unique=True)

    if 'index_products_on_name_and_level' not in indexes:
        op.create_index('index_products_on_name_and_level', 'products', ['name', 'level'], unique=True)

    if 'index_products_on_official_name' not in indexes:
        op.create_index('index_products_on_official_name', 'products', ['official_name'], unique=True)

    if 'index_products_on_short_name' not in indexes:
        op.create_index('index_products_on_short_name', 'products', ['short_name'], unique=True)

    # Delete this table eventually, for now ingest all the data as is
    if 'users' not in tables:
        op.create_table('users',
                        sa.Column('email', sa.String(), server_default='', nullable=False),
                        sa.Column('encrypted_password', sa.String(), server_default='', nullable=False),
                        sa.Column('reset_password_token', sa.String(), nullable=True),
                        sa.Column('reset_password_sent_at', sa.DateTime(), nullable=True),
                        sa.Column('remember_created_at', sa.DateTime(), nullable=True),
                        sa.Column('sign_in_count', sa.Integer(), server_default='0', nullable=False),
                        sa.Column('current_sign_in_at', sa.DateTime(), nullable=True),
                        sa.Column('last_sign_in_at', sa.DateTime(), nullable=True),
                        sa.Column('current_sign_in_ip', sa.String(), nullable=True),
                        sa.Column('last_sign_in_ip', sa.String(), nullable=True),
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                        sa.PrimaryKeyConstraint('id')
                        )

    indexes = [index["name"] for index in inspector.get_indexes('users')]
    if 'index_users_on_email' not in indexes:
        op.create_index('index_users_on_email', 'users', ['email'], unique=True)

    if 'index_users_on_reset_password_token' not in indexes:
        op.create_index('index_users_on_reset_password_token', 'users', ['reset_password_token'], unique=True)

    if 'licenses' not in tables:
        op.create_table('licenses',
                        sa.Column('user_email', sa.String(), nullable=False),
                        sa.Column('active', sa.Boolean(), server_default=sa.text('false'), nullable=True),
                        sa.Column('key', sa.String(), nullable=False),
                        sa.Column('product_key', sa.String(), nullable=False),
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                        sa.ForeignKeyConstraint(['product_key'], ['products.key'], ),
                        sa.PrimaryKeyConstraint('id')
                        )

    indexes = [index["name"] for index in inspector.get_indexes('licenses')]
    if 'index_licenses_on_key' not in indexes:
        op.create_index('index_licenses_on_key', 'licenses', ['key'], unique=True)

    if 'index_licenses_on_product_key_and_user_email' not in indexes:
        op.create_index('index_licenses_on_product_key_and_user_email',
                        'licenses', ['product_key', 'user_email'], unique=True)
    if 'index_licenses_on_user_email' not in indexes:
        op.create_index('index_licenses_on_user_email', 'licenses', ['user_email'], unique=False)


def downgrade() -> None:
    # Intentionally commented out all the drop table, as this is not a new database
    # op.drop_index('index_licenses_on_user_email', table_name='licenses')
    # op.drop_index('index_licenses_on_product_key_and_user_email', table_name='licenses')
    # op.drop_index('index_licenses_on_key', table_name='licenses')
    # op.drop_table('licenses')
    # op.drop_index('index_users_on_reset_password_token', table_name='users')
    # op.drop_index('index_users_on_email', table_name='users')
    # op.drop_table('users')
    # op.drop_index('index_products_on_short_name', table_name='products')
    # op.drop_index('index_products_on_official_name', table_name='products')
    # op.drop_index('index_products_on_name_and_level', table_name='products')
    # op.drop_index('index_products_on_key', table_name='products')
    # op.drop_index('index_products_on_isbn', table_name='products')
    # op.drop_index('index_products_on_evolve_isbn', table_name='products')
    # op.drop_index('index_products_on_active_and_name_and_level', table_name='products')
    # op.drop_table('products')
    # op.drop_table('api_keys')
    pass
