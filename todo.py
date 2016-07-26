from flask import Flask, render_template, request, redirect, session
import pg
db = pg.DB(dbname='todo_db')
app = Flask('MyApp')
app.debug = True

@app.route('/')
def home():

    query = db.query('''
        select
            *
        from
            list
        order by
            completed, task
    ''')

    return render_template(
        'list.html',
        title='To Do List',
        list=query.namedresult())

@app.route('/addtask', methods=['POST'])
def addtask():
    task_name = request.form['task_name']
    db.insert('list', task=task_name)
    return redirect('/')

@app.route('/markcomplete', methods=['POST'])
def complete():
    dict = request.form

    query = db.query('''
        select
            *
        from
            list
    ''')
    print query

    if 'complete' in dict:
        for key in dict.keys():
            if key != 'complete':
                db.update('list', {'id': key}, completed='True')
            else:
                pass
    elif 'undo' in dict:
        for key in dict.keys():
            if key != 'undo':
                db.update('list', {'id': key}, completed='False')
            else:
                pass
    elif 'delete' in dict:
        for key in dict.keys():
            if key != 'delete':
                db.delete('list', {'id': key})
            else:
                pass
    else:
        pass

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
