"""add task priority column

Revision ID: 5528976b7e84
Revises: 82e5b20e89e6
Create Date: 2025-01-31 18:46:07.766541

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5528976b7e84'
down_revision: Union[str, None] = '82e5b20e89e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('priority', sa.Integer(), nullable=True))
    op.create_check_constraint(
        'check_priority_range',  # Constraint name
        'tasks',  # Table name
        sa.text('priority >= 1 AND priority <= 10')  # Constraint condition
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('check_priority_range', 'tasks', type_='check')
    op.drop_column('tasks', 'priority')
    # ### end Alembic commands ###

