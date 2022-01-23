from __main__ import app
from flask import Flask, request, render_template, redirect, url_for
from forms import TodoForm
from models import todos

@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            vdata = list(form.data.values())
            vdata.pop(3)
            todos.create(vdata)
            print(vdata)

        return redirect(url_for("todos_list"))

    return render_template("todos.html", form=form, todos=todos.all(), error=error)



@app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    todo = todos.get(todo_id)
    form = TodoForm(data=todo)
    if request.method == "POST":
        if form.validate_on_submit():

            if request.form['submit']=='Go':
                vdata = (form.data)
                vdata.pop('csrf_token')
                todos.update(todo_id, vdata)
            if request.form['submit']=='Delete':
                vdata = (form.data)
                vdata.pop('csrf_token')
                todos.delete(todo_id)

        return redirect(url_for("todos_list"))

    return render_template("todo.html", form=form, todo_id=todo_id)

