# Przy pierwszym uruchomieniu:  flask --app app shell
# A następnie:
# >>> db.create_all()
# >>> exit()
#
# Dalej uruchamiamy: flask --app app app
from flask import render_template, request

from project.config import db, app
from project.crud import get_tags, create_tag, remove_tag, create_note, get_notes, apply_tag


@app.route('/')
def hello():
    return render_template('notes.html', notes=get_notes(db.session), tags=get_tags(db.session),
                           tytul="Tags", no_error=True)


@app.route('/addtag')
def route_addtag():
    args = request.args
    create_tag(args["name"], db.session)

    return render_template('notes.html', notes=get_notes(db.session), tags=get_tags(db.session),
                           tytul="Dodano tag")


@app.route('/removetag')
def route_removetag():
    args = request.args
    remove_tag(args["name"], db.session)

    return render_template('notes.html', notes=get_notes(db.session), tags=get_tags(db.session),
                           tytul="removed tag")


@app.route('/addnote')
def route_addnote():
    args = request.args
    create_note(args["title"], args["body"], db.session)

    return render_template('notes.html', notes=get_notes(db.session), tags=get_tags(db.session),
                           tytul="Dodano note")

@app.route('/applytag', methods=["POST"] )
def route_applytag():
    args = request.form
    print(args)
    apply_tag(session=db.session, note_id=args["note_id"], tag_id=args["tag_id"])

    return render_template('notes.html', notes=get_notes(db.session), tags=get_tags(db.session),
                           tytul="Dodano note")
