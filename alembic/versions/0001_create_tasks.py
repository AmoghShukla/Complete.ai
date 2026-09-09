"""create task tables

Revision ID: 0001
Revises:
Create Date: 2026-09-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    reminder_type_enum = postgresql.ENUM(
        "EMAIL", "PUSH", "IN_APP", name="reminder_type_enum"
    )
    task_status_enum = postgresql.ENUM(
        "PENDING", "IN_PROGRESS", "COMPLETED", "ARCHIVED",
        name="task_status_enum",
    )
    task_priority_enum = postgresql.ENUM(
        "LOW", "MEDIUM", "HIGH", name="task_priority_enum"
    )
    reminder_type_enum.create(op.get_bind(), checkfirst=True)
    task_status_enum.create(op.get_bind(), checkfirst=True)
    task_priority_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_email", sa.String(length=255), nullable=False),
        sa.Column("user_name", sa.String(length=50), nullable=False),
        sa.Column("user_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("user_email"),
        sa.UniqueConstraint("user_name"),
    )
    op.create_index("ix_users_user_email", "users", ["user_email"])
    op.create_index("ix_users_user_name", "users", ["user_name"])

    op.create_table(
        "categories",
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_name", sa.String(length=50), nullable=False),
        sa.Column("category_color", sa.String(length=7), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("category_id"),
    )
    op.create_index("ix_categories_user_id", "categories", ["user_id"])

    op.create_table(
        "tags",
        sa.Column("tag_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tag_name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("tag_id"),
    )
    op.create_index("ix_tags_user_id", "tags", ["user_id"])
    op.create_index("ix_tags_tag_name", "tags", ["tag_name"])

    op.create_table(
        "tasks",
        sa.Column("task_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", task_status_enum, nullable=False),
        sa.Column("priority", task_priority_enum, nullable=False),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.category_id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("task_id"),
    )
    op.create_index("ix_tasks_user_id", "tasks", ["user_id"])
    op.create_index("ix_tasks_category_id", "tasks", ["category_id"])
    op.create_index("ix_tasks_status", "tasks", ["status"])
    op.create_index("ix_tasks_priority", "tasks", ["priority"])
    op.create_index("ix_tasks_due_date", "tasks", ["due_date"])

    op.create_table(
        "task_tags",
        sa.Column("task_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tag_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.tag_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.task_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("task_id", "tag_id"),
    )

    op.create_table(
        "reminders",
        sa.Column("reminder_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("remind_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reminder_type", reminder_type_enum, nullable=False),
        sa.Column("is_sent", sa.Boolean(), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.task_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("reminder_id"),
    )
    op.create_index("ix_reminders_task_id", "reminders", ["task_id"])
    op.create_index("ix_reminders_remind_at", "reminders", ["remind_at"])


def downgrade() -> None:
    op.drop_index("ix_reminders_remind_at", table_name="reminders")
    op.drop_index("ix_reminders_task_id", table_name="reminders")
    op.drop_table("reminders")
    op.drop_table("task_tags")
    op.drop_index("ix_tasks_due_date", table_name="tasks")
    op.drop_index("ix_tasks_priority", table_name="tasks")
    op.drop_index("ix_tasks_status", table_name="tasks")
    op.drop_index("ix_tasks_category_id", table_name="tasks")
    op.drop_index("ix_tasks_user_id", table_name="tasks")
    op.drop_table("tasks")
    postgresql.ENUM(name="task_priority_enum").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="task_status_enum").drop(op.get_bind(), checkfirst=True)
    op.drop_index("ix_tags_tag_name", table_name="tags")
    op.drop_index("ix_tags_user_id", table_name="tags")
    op.drop_table("tags")
    op.drop_index("ix_categories_user_id", table_name="categories")
    op.drop_table("categories")
    op.drop_index("ix_users_user_name", table_name="users")
    op.drop_index("ix_users_user_email", table_name="users")
    op.drop_table("users")
    postgresql.ENUM(name="reminder_type_enum").drop(op.get_bind(), checkfirst=True)