# region IMPORTS
import json

from app.todo import todo_bp
from flask import (flash, jsonify, redirect, render_template, request, session,
                   url_for)

from .forms import *
from .models import *

# endregion

# region VARIABLES
menu = [
    ("User", "/register", "user"),
    ("Home", "/", "home"),
    ("About", "/about", "info-circle"),
    ("Portfolio", "/portfolio", "book-content"),
    ("Contact", "/contact", "envelope"),
    ("ToDo List", "/todo", "list-check"),
]
# endregion


# region TASK_LIST_FUNC
def getTaskList():
    if len(Task.query.all()) != 0:
        if len(Category.query.all()) != 0:
            countCategories = max(db.session.query(Category.id).all())[0]
            categories = [''.join(category[0])
                          for category in db.session.query(Category.name).all()]
        else:
            return ''
        todos = Task.query.all()
        resList = {}
        for i in range(countCategories):
            for item in todos:
                if item.category_id == i+1:
                    catName = Category.query.get_or_404(item.category_id).name
                    lowList, mediumList, highList, doneList = [], [], [], []
                    if item.is_done == 1:
                        if catName in resList:
                            resList[catName].append(
                                item)
                        else:
                            resList[catName] = [item]
                    elif item.priority.value == 'low':
                        if catName in resList:
                            resList[catName].append(
                                item)
                        else:
                            resList[catName] = [item]
                    elif item.priority.value == 'medium':
                        if catName in resList:
                            resList[catName].append(
                                item)
                        else:
                            resList[catName] = [
                                item]
                    else:
                        if catName in resList:
                            resList[catName].append(
                                item)
                        else:
                            resList[catName] = [item]

        if "Others" in resList:
            tmp = resList['Others']
            del resList['Others']
            resList['Others'] = tmp
        return resList
    else:
        return ''
# endregion


# region TASK_ROUTES
@todo_bp.route("/todo/create", methods=["GET", "POST"], endpoint='create')
@todo_bp.route("/todo", methods=["GET", "POST"])
@todo_bp.route("/todo/<int:todo_id>", methods=["GET", "POST"], endpoint='view')
@todo_bp.route("/todo/<int:todo_id>/update", methods=["GET", "POST"], endpoint='update')
@todo_bp.route("/todo/<int:todo_id>/delete", methods=["GET", "POST"], endpoint='delete')
@todo_bp.route("/todo/<int:todo_id>/get_by_id", methods=["GET", "POST"], endpoint='get_by_id')
@todo_bp.route("/todo/<int:todo_id>/mark_todo", methods=["GET", "POST"], endpoint='mark_todo')
def todo(todo_id=None):
    # Index page allows to add new tasks, see these tasks, edit and deleted them.
    form = TaskForm()
    formCat = CategoryForm()
    formEmpl = EmployeeForm()
    todos = getTaskList()
    # Get data from db by Id
    if request.endpoint == 'todo_bp.get_by_id':
        task = Task.query.get_or_404(todo_id)
        print("<<<==== GET TASK BY ID ====>>>")
        print(f"<<<==== {todo_id} ====>>>")
        return json.dumps({
            'title': task.title,
            'description': task.description,
            'priority': task.priority.value,
            'timeline': task.created_at+" - "+task.deadline,
            'is_done': task.is_done,
            'category': task.category_id,
            'employee': [empl.id for empl in task.empls],
        })
    if request.endpoint == 'todo_bp.view':
        task = Task.query.get_or_404(todo_id)
        print("<<<==== VIEW TASK BY ID ====>>>")
        print(f"<<<==== {todo_id} ====>>>")
        return json.dumps({
            'Id': task.id,
            'Title': task.title,
            'Description': task.description,
            'Priority': task.priority.value,
            'Created': task.created_at,
            'Deadline': task.deadline,
            'Status': "Done" if task.is_done else "Ongoing",
            'Category': f"<a href='#' onclick=view_todo('{Category.query.get_or_404(task.category_id).name}',2)>"+Category.query.get_or_404(task.category_id).name+"</a>",
            'Employee': [f"<a href='#' onclick=view_todo('{empl.name}',3)>"+empl.name+"</a>" for empl in task.empls]
        })

    # Add new task
    if request.endpoint == 'todo_bp.create':
        if request.method == "POST":
            print(f"<<<==== ADDING NEW TASK ====>>>")
            if form.validate_on_submit():
                print(f"<<<==== VALIDATION COMPLETE ====>>>")
                task = Task(title=request.form['title'],
                            description=request.form['description'],
                            priority=request.form['priority'],
                            created_at=request.form['timeline'].split(
                    " - ")[0],
                    deadline=request.form['timeline'].split(" - ")[1],
                    category_id=db.session.query(Category.id).filter(Category.id == request.form['category']))
                try:
                    db.session.add(task)
                    for item in request.form.getlist('employee'):
                        empl = Employee.query.get_or_404(int(item))
                        task.empls.append(empl)
                    db.session.commit()
                    print(f"<<<==== TASK ADDED ====>>>")
                    return json.dumps(
                        {'success': 'true', 'msg': 'Task has been added successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
                except Exception as err:
                    db.session.rollback()
                    # flash("There are some issues adding the task!!", "error")
                    print(f"<<<==== ERROR ADDED TASK ====>>>")
                    print(err)
                    return json.dumps(
                        {'success': 'false', 'msg': 'There are some issues adding the task!!', 'data': form.data, 'errors': form.errors})
            else:
                print(f"<<<==== VALIDATION FAILED ====>>>")
                return json.dumps(
                    {'success': 'false', 'msg': 'Validation failed.', 'data': form.data, 'errors': form.errors})
    # Edit task by ID
    if request.endpoint == 'todo_bp.update':
        print(f"<<<==== UPDATING TASK WAS STARTED ====>>>")
        print(f"<<<==== {todo_id} ====>>>")
        task = Task.query.get_or_404(todo_id)
        if form.validate_on_submit():
            task.title = request.form['title']
            task.description = request.form['description']
            task.priority = request.form['priority']
            task.created_at = request.form['timeline'].split(" - ")[0]
            task.deadline = request.form['timeline'].split(" - ")[1]
            task.is_done = 1 if 'is_done' in request.form else 0
            task.category_id = request.form['category']
            try:
                task.empls = []
                for item in request.form.getlist('employee'):
                    empl = Employee.query.get_or_404(int(item))
                    task.empls.append(empl)
                db.session.commit()
                empls = Employee.query.all()
                for empl in empls:
                    compl_tasks = 0
                    for task in db.session.query(Task).filter(Task.empls.contains(empl)).all():
                        if task.is_done:
                            compl_tasks = compl_tasks + 1
                    empl.completed_task = compl_tasks
                db.session.commit()
                print(f"<<<==== TASK UPDATED SUCCESSFULY ====>>>")
                return json.dumps(
                    {'success': 'true', 'msg': 'Task has been updated successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
            except Exception as err:
                print(f"<<<==== TASK UPDATE FAILED ====>>>")
                print(f"<<<==== {err} ====>>>")
                return json.dumps(
                    {'success': 'false', 'msg': 'There are some issues updating the task!!', 'data': form.data, 'errors': form.errors})
        else:
            print(f"<<<==== VALIDATION FAILED ====>>>")
            return json.dumps(
                {'success': 'false', 'msg': 'Validation failed.', 'data': form.data, 'errors': form.errors})

    # Mark TODO task by ID
    if request.endpoint == 'todo_bp.mark_todo':
        print(f"<<<==== MARKING TASK WAS STARTED ====>>>")
        print(f"<<<==== {todo_id} ====>>>")
        task = Task.query.get_or_404(todo_id)
        empls = Employee.query.all()
        checked = request.get_json()
        task.is_done = 1 if checked['check'] else 0

        try:
            db.session.commit()
            for empl in empls:
                compl_tasks = 0
                for task in db.session.query(Task).filter(Task.empls.contains(empl)).all():
                    if task.is_done:
                        compl_tasks = compl_tasks + 1
                empl.completed_task = compl_tasks
            db.session.commit()
            print(f"<<<==== TASK MARKED SUCCESSFULY ====>>>")
            return json.dumps(
                {'success': 'true', 'msg': 'Task has been updated successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
        except Exception as err:
            print(f"<<<==== MARKING TASK FAILED ====>>>")
            print(f"<<<==== {err} ====>>>")
            return json.dumps(
                {'success': 'false', 'msg': 'There are some issues adding the task!!', 'data': form.data, 'errors': form.errors})

    # Deleting task by ID
    if request.endpoint == 'todo_bp.delete':
        print(f"<<<==== DELETING TASK WAS STARTED ====>>>")
        print(f"<<<==== {todo_id} ====>>>")
        task = Task.query.get_or_404(todo_id)
        try:
            task.empls = []
            db.session.delete(task)
            db.session.commit()
            print(f"<<<==== TASK DELETED ====>>>")
            return json.dumps(
                {'success': 'true', 'data': render_template('tasklist.html', todos=getTaskList())})
        except Exception as err:
            print(f"<<<==== DELETING TASK FAILED ====>>>")
            print(f"<<<==== {err} ====>>>")
            return "There are some issues deleting the task!"
    return render_template(
        "todo.html",
        todos=todos,
        menu=menu,
        form=form,
        formCat=formCat,
        formEmpl=formEmpl,
        reqMethod=request.method
    )
# endregion


# region CAT_ROUTES
@ todo_bp.route("/todo/category/create", methods=["GET", "POST"], endpoint='cat_create')
@ todo_bp.route("/todo/category/<string:cat_name>/update", methods=["GET", "POST"], endpoint='cat_update')
@ todo_bp.route("/todo/category/<string:cat_name>/delete", methods=["GET", "POST"], endpoint='cat_delete')
@ todo_bp.route("/todo/category/<string:cat_name>", methods=["GET", "POST"], endpoint='cat_view')
@ todo_bp.route("/todo/category/<string:cat_name>/permission", methods=["GET", "POST"], endpoint='cat_permission')
@ todo_bp.route("/todo/category/view", methods=["GET", "POST"], endpoint='cat_list')
def category(cat_name=None):
    form = CategoryForm()
    todos = getTaskList()

    if request.endpoint == 'todo_bp.cat_list':
        catgs = Category.query.all()

        print(f"<<<==== GETTING CATEGORY LIST ====>>>")
        res = []
        for cat in catgs:
            todos = Task.query.filter_by(
                category_id=Category.query.filter_by(name=cat.name).first().id).all()
            res.append({
                'Id': cat.id,
                'Name': f"<a href='#' onclick=view_todo('{cat.name}',2)>"+cat.name+"</a>",
                'Tasks': [task.id for task in todos]
            })
        return json.dumps(res)

    if request.endpoint == 'todo_bp.cat_update':
        print(f"<<<==== UPDATING CATEGORY WAS STARTED ====>>>")
        print(f"<<<==== {cat_name} ====>>>")
        cat = Category.query.get_or_404(
            Category.query.filter_by(name=cat_name).first().id)
        if form.validate_on_submit():
            cat.name = request.form['cat_name']
            id_tasks = request.form.getlist('cat_tasks')
            tasks = []
            for id_task in id_tasks:
                tasks.append(Task.query.get_or_404(int(id_task)))
            if tasks:
                for task in tasks:
                    task.category_id = cat.id
            try:
                db.session.commit()
                print(f"<<<==== CATEGORY WAS UPDATED ====>>>")
                return json.dumps(
                    {'success': 'true', 'msg': 'Category has been updated successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
            except Exception as err:
                print(f"<<<==== UPDATING CATEGORY FAILED ====>>>")
                print(f"<<<==== {err} ====>>>")
                return json.dumps(
                    {'success': 'false', 'msg': 'There are some issues updating the category!!', 'data': form.data, 'errors': form.errors})
        else:
            print(f"<<<==== VALIDATION FAILED ====>>>")
            return json.dumps(
                {'success': 'false', 'msg': 'Validation failed.', 'data': form.data, 'errors': form.errors})

    if request.endpoint == 'todo_bp.cat_view':
        print(f"<<<==== VIEW CATEGORY BY ID ====>>>")
        print(f"<<<==== {cat_name} ====>>>")
        tasks = Task.query.filter_by(
            category_id=Category.query.filter_by(name=cat_name).first().id).all()
        res = []
        for item in tasks:
            res.append({
                'Id': item.id,
                'Title': f"<a href='#' onclick=view_todo('{item.id}',1)>"+item.title+"</a>",
                'Description': item.description,
                'Priority': item.priority.value,
                'Created': item.created_at,
                'Deadline': item.deadline,
                'Status': "Done" if item.is_done else "Ongoing",
                'Employee': [f"<a href='#' onclick=view_todo('{empl.name}',3)>"+empl.name+"</a>" for empl in item.empls]
            })
        return json.dumps(res)

    if request.endpoint == 'todo_bp.cat_create':
        if request.method == "POST":
            print(f"<<<==== ADDING CATEGORY WAS STARTED ====>>>")
            if form.validate_on_submit():
                cat = Category(name=request.form['cat_name'])
                try:
                    db.session.add(cat)
                    db.session.commit()
                    print(f"<<<==== ADDING CATEGORY COMPLETE ====>>>")
                    return json.dumps(
                        {'success': 'true', 'msg': 'Category has been added successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
                except Exception as err:
                    db.session.rollback()
                    print(f"<<<==== ERROR ADDED CATEGORY ====>>>")
                    print(f"<<<==== {err} ====>>>")
                    return json.dumps(
                        {'success': 'false', 'msg': "There are some issues adding the category!!<br>Maybe it's already exists.", 'data': form.data, 'errors': form.errors})
            else:
                print(f"<<<==== VALIDATION FAILED ====>>>")
                return json.dumps(
                    {'success': 'false', 'msg': 'Validation failed.', 'data': form.data, 'errors': form.errors})

    if request.endpoint == 'todo_bp.cat_delete':
        if cat_name == "Others":
            return json.dumps({
                'success': 'false',
                'msg': 'You CANNOT DELETE default Category!'
            })
        print(f"<<<==== DELETING CATEGORY WAS STARTED ====>>>")
        print(f"<<<==== {cat_name} ====>>>")
        cat = Category.query.get_or_404(
            Category.query.filter_by(name=cat_name).first().id)
        tasksCat = Task.query.filter_by(
            category_id=Category.query.filter_by(name=cat_name).first().id).all()
        if tasksCat:
            for item in tasksCat:
                item.category_id = Category.query.filter_by(
                    name='Others').first().id
        try:
            db.session.commit()
            db.session.delete(cat)
            db.session.commit()
            print(f"<<<==== DELETING CATEGORY COMPLETE ====>>>")
            return json.dumps(
                {'success': 'true', 'data': render_template('tasklist.html', todos=getTaskList())})
        except Exception as err:
            print(f"<<<==== DELETING CATEGORY FAILED ====>>>")
            print(f"<<<==== {err} ====>>>")
            return "There are some issues deleting the task!"
# endregion


# region EMPL_ROUTES
@todo_bp.route("/todo/employee/create", methods=["GET", "POST"], endpoint='empl_create')
@todo_bp.route("/todo/employee/<string:empl_name>/update", methods=["GET", "POST"], endpoint='empl_update')
@todo_bp.route("/todo/employee/<string:empl_name>/delete", methods=["GET", "POST"], endpoint='empl_delete')
@todo_bp.route("/todo/employee/<string:empl_name>", methods=["GET", "POST"], endpoint='empl_view')
@todo_bp.route("/todo/employee/<string:empl_name>/permission", methods=["GET", "POST"], endpoint='empl_permission')
@todo_bp.route("/todo/employee/view", methods=["GET", "POST"], endpoint='empl_list')
def employee(empl_name=None):
    form = EmployeeForm()
    todos = getTaskList()

    if request.endpoint == 'todo_bp.empl_permission':
        if empl_name == "Maksym":
            return json.dumps({
                'success': 'false',
                'msg': 'You CANNOT EDIT default Employee!'
            })
        else:
            return json.dumps({
                'success': 'true'
            })

    if request.endpoint == 'todo_bp.empl_list':
        tasks = Task.query.all()
        empls = Employee.query.all()
        print(f"<<<==== GETTING EMPLOYEE LIST ====>>>")

        res = []
        for empl in empls:
            compl_tasks = 0
            for task in db.session.query(Task).filter(Task.empls.contains(empl)).all():
                if task.is_done:
                    compl_tasks = compl_tasks + 1
            empl.completed_task = compl_tasks
            res.append({
                'Id': empl.id,
                'Name': f"<a href='#' onclick=view_todo('{empl.name}',3)>"+empl.name+"</a>",
                'compl_tasks': compl_tasks,
                'todo_tasks': len(db.session.query(Task).filter(Task.empls.contains(empl)).all())-compl_tasks
            })
        db.session.commit()

        return json.dumps(res)

    if request.endpoint == 'todo_bp.empl_update':
        print(f"<<<==== UPDATING EMPLOYEE WAS STARTED ====>>>")
        print(f"<<<==== {empl_name} ====>>>")
        empl = Employee.query.get_or_404(
            Employee.query.filter_by(name=empl_name).first().id)
        if form.validate_on_submit():
            empl.name = request.form['empl_name']
            id_tasks = request.form.getlist('empl_tasks')
            tasks = []
            for id_task in id_tasks:
                tasks.append(Task.query.get_or_404(int(id_task)))
            if tasks:
                for task in tasks:
                    task.empls = []
                    task.empls.append(empl)
            try:
                db.session.commit()
                print(f"<<<==== EMPLOYEE WAS UPDATED ====>>>")
                return json.dumps(
                    {'success': 'true', 'msg': 'Category has been updated successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
            except Exception as err:
                print(f"<<<==== UPDATING EMPLOYEE FAILED ====>>>")
                print(f"<<<==== {err} ====>>>")
                return json.dumps(
                    {'success': 'false', 'msg': 'There are some issues updating the employee!!', 'data': form.data, 'errors': form.errors})
        else:
            print(f"<<<==== VALIDATION FAILED ====>>>")
            return json.dumps(
                {'success': 'false', 'msg': 'Validation failed.', 'data': form.data, 'errors': form.errors})

    if request.endpoint == 'todo_bp.empl_view':
        print(f"<<<==== VIEW EMPLOYEE BY ID ====>>>")
        print(f"<<<==== {empl_name} ====>>>")
        tasks = []
        compl_tasks = 0
        for task in db.session.query(Task).filter(Task.empls.contains(Employee.query.filter_by(name=empl_name).first())).all():
            if task.is_done:
                compl_tasks = compl_tasks + 1
            tasks.append(task)
        res = []
        for item in tasks:
            res.append({
                'Id': item.id,
                'Title': f"<a href='#' onclick=view_todo('{item.id}',1)>"+item.title+"</a>",
                'Priority': item.priority.value,
                'Category': f"<a href='#' onclick=view_todo('{Category.query.get_or_404(item.category_id).name}',2)>"+Category.query.get_or_404(item.category_id).name+"</a>",
                'Deadline': item.deadline,
                'Status': "Done" if item.is_done else "Ongoing",
                'compl_tasks': compl_tasks,
                'todo_tasks': len(db.session.query(Task).filter(Task.empls.contains(Employee.query.filter_by(name=empl_name).first())).all())-compl_tasks
            })
        return json.dumps(res)

    if request.endpoint == 'todo_bp.empl_create':
        if request.method == "POST":
            print(f"<<<==== ADDING EMPLOYEE WAS STARTED ====>>>")
            if form.validate_on_submit():
                empl = Employee(name=request.form['empl_name'])
                tasks = request.form.getlist('empl_tasks')
                for item in tasks:
                    task = Task.query.get_or_404(item)
                    task.empls.append(empl)
                try:
                    db.session.commit()
                    db.session.add(empl)
                    db.session.commit()
                    print(f"<<<==== ADDING EMPLOYEE COMPLETE ====>>>")
                    return json.dumps(
                        {'success': 'true', 'msg': 'Employee has been added successfully.', 'data': render_template('tasklist.html', todos=getTaskList())})
                except Exception as err:
                    db.session.rollback()
                    print(f"<<<==== ERROR ADDED EMPLOYEE ====>>>")
                    print(f"<<<==== {err} ====>>>")
                    return json.dumps(
                        {'success': 'false', 'msg': "There are some issues adding the employee!!<br>Maybe it's already exists.", 'data': form.data, 'errors': form.errors})
            else:
                print(f"<<<==== VALIDATION FAILED ====>>>")
                return json.dumps(
                    {'success': 'false', 'msg': 'Validation failed.', 'data': form.data, 'errors': form.errors})

    if request.endpoint == 'todo_bp.empl_delete':
        if empl_name == "Maksym":
            return json.dumps({
                'success': 'false',
                'msg': 'You CANNOT DELETE default Employee!'
            })
        print(f"<<<==== DELETING EMPLOYEE WAS STARTED ====>>>")
        print(f"<<<==== {empl_name} ====>>>")
        empl = Employee.query.get_or_404(
            Employee.query.filter_by(name=empl_name).first().id)
        emplDefault = Employee.query.get_or_404(
            Employee.query.filter_by(name="Maksym").first().id)
        for task in db.session.query(Task).filter(Task.empls.contains(empl)).all():
            task.empls.pop(task.empls.index(empl))
            if emplDefault not in task.empls:
                task.empls.append(emplDefault)
        try:
            db.session.commit()
            db.session.delete(empl)
            db.session.commit()
            print(f"<<<==== DELETING CATEGORY COMPLETE ====>>>")
            return json.dumps(
                {'success': 'true', 'data': render_template('tasklist.html', todos=getTaskList())})
        except Exception as err:
            print(f"<<<==== DELETING CATEGORY FAILED ====>>>")
            print(f"<<<==== {err} ====>>>")
            return "There are some issues deleting the task!"
# endregion
