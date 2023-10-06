import sqlalchemy
from sqlalchemy.orm import relationship

from project.config import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self.tagname


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    body = db.Column(db.Text, unique=False, nullable=False)

    tags = relationship("Tag",
                    secondary='tagnote',
                    uselist=True,
                    backref='notes',
                    lazy='select')

class tagnote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

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


def remove_tag(param, session):
    tag = session.query(Tag).filter_by(tagname=param).one()
    session.delete(tag)
    session.commit()


def create_note(title, body, session):

    try:
        note = Note(title=title, body=body)
        session.add(note)
        session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        session.rollback()
        return False
    else:
        return True


def get_notes(session):
    return session.query(Note).all()

def apply_tag(session, note_id, tag_id):
    note = session.query(Note).filter_by(id=note_id).one()
    tag = session.query(Tag).filter_by(id=tag_id).one()
    note.tags.append(tag)
    session.commit()
