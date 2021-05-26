import enum
from datetime import datetime

from app.extensions import db, ma
from marshmallow_enum import EnumField


class priorityEnum(enum.Enum):
    low, medium, high = "low", "medium", "high"

    def __str__(self):
        return self.name


task_empl = db.Table(
    "task_empl",
    db.Column("task_id", db.Integer, db.ForeignKey("task.id")),
    db.Column("empl_id", db.Integer, db.ForeignKey("employee.id")),
)


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.String(), default=datetime.utcnow())
    deadline = db.Column(db.String())
    priority = db.Column(db.Enum(priorityEnum), default="high")
    is_done = db.Column(db.Boolean(), default=False)
    category_id = db.Column(db.Integer(), db.ForeignKey("category.id"))

    def __repr__(self):
        return f"<Task-{self.id}\n \
        Title {self.title}\n \
        Description {self.description}\n \
        Created at {self.created_at}\n \
        Priority {self.priority}\n \
        Category {self.category_id}\n \
        Is done {self.is_done}>"


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="category", lazy=True)


class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    completed_task = db.Column(db.Integer(), default=0, nullable=False)

    tasks = db.relationship("Task", secondary=task_empl, backref=db.backref("empls"), lazy="dynamic")


class TaskSchema(ma.SQLAlchemyAutoSchema):
    priority = EnumField(priorityEnum, by_value=True)

    class Meta:
        model = Task


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
