"""Alembic environment configuration for M2R2 Supabase migrations.

Handles both online (live database) and offline (SQL script generation) modes.
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from pathlib import Path

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get database URL from environment (for Supabase)
# Expected format: postgresql://[user[:password]@][host][:port][/database]
DB_URL = os.environ.get(
    "DATABASE_URL",
    os.environ.get(
        "SUPABASE_DB_URL",
        "postgresql://postgres:password@localhost:5432/humanaios"
    )
)

# Override config with actual database URL
config.set_main_option("sqlalchemy.url", DB_URL)

# Add project root to path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in os.sys.path:
    os.sys.path.insert(0, str(project_root))

from src.models.orm_supabase import Base

# Set target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (generate SQL script).

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (connect to live database).

    In this scenario we need to create an Engine and associate a
    connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DB_URL

    # Filter to only SQLAlchemy-valid options (exclude Alembic-specific keys)
    filtered_config = {k: v for k, v in configuration.items()
                      if k.startswith("sqlalchemy.") and not k.endswith("_scheme")}
    filtered_config["sqlalchemy.url"] = DB_URL

    connectable = engine_from_config(
        filtered_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
