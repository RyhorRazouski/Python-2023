# Przy pierwszym uruchomieniu:  flask --app app shell
# A następnie:
# >>> db.create_all()
# >>> exit()
#
# Dalej uruchamiamy: flask --app app app
import sqlalchemy
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self.tagname


def get_tags(session):
    return session.query(Tag).all()


def create_tag(name, session):
    try:
        tag = Tag(tagname=name)
        session.add(tag)
        session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        session.rollback()
        return False
    else:
        return True


@app.route('/')
def hello():
    return render_template('notes.html', data=get_tags(db.session),
                           tytul="Tags", no_error=True)


@app.route('/addtag')
def route_addtag():
    args = request.args
    create_tag(args["name"], db.session)

    return render_template('notes.html', data=get_tags(db.session),
                           tytul="Dodano tag")


def remove_tag(param, session):
    tag = session.query(Tag).filter_by(tagname=param).one()
    session.delete(tag)
    session.commit()

@app.route('/removetag')
def route_removetag():
    args = request.args
    remove_tag(args["name"], db.session)

    return render_template('notes.html', data=get_tags(db.session),
                           tytul="removed tag")

