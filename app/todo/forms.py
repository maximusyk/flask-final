from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from .models import Category, Task, Employee

csrf = CSRFProtect()

PRIORITY_CHOICES = [("high", "high"), ("medium", "medium"), ("low", "low")]


class TaskForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.category.choices = [
            (el.id, el.name) for el in Category.query.all()
        ]
        self.employee.choices = [
            (el.id, el.name) for el in Employee.query.all()
        ]
    title = StringField(
        "title",
        validators=[DataRequired(message="Title cannot be empty")]
    )
    description = TextAreaField(
        "description",
        validators=[
            DataRequired(message="Description cannot be empty"),
            Length(min=2, max=100),
        ],
        render_kw={"rows": 3}
    )
    priority = SelectField("priority", choices=PRIORITY_CHOICES)
    timeline = StringField("timeline")
    is_done = BooleanField('is_done')

    category = SelectField("category", coerce=int)
    employee = SelectMultipleField("employee", coerce=int)


class CategoryForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cat_tasks.choices = [
            (el.id, el.title) for el in Task.query.all()
        ]
    cat_name = StringField('cat_name', validators=[
        DataRequired(message="Category name cannot be empty")])

    cat_tasks = SelectMultipleField("cat_tasks", coerce=int)


class EmployeeForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.empl_tasks.choices = [
            (el.id, el.title) for el in Task.query.all()
        ]
    empl_name = StringField('empl_name', validators=[
        DataRequired(message="Employee name cannot be empty")])
    empl_tasks = SelectMultipleField("empl_tasks", coerce=int)
