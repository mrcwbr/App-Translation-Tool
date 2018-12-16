import datetime
from helpers.database import db


class LanguageProjectRelation(db.Model):  # https://gist.github.com/kirang89/10030736
    lang_code = db.Column(db.String(5), db.ForeignKey('language.code'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    is_default = db.Column(db.Boolean, default=False, nullable=False)

    language = db.relationship('Language', backref=db.backref('language_project_relation'))
    project = db.relationship('Project', backref=db.backref('language_project_relation'))

    def __repr__(self):
        return '<LP-Rel %s %s %s>' % (self.lang_code, self.project_id, self.is_default)


class Language(db.Model):
    code = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    flag_image_link = db.Column(db.String(100), nullable=True)

    projects = db.relationship("LanguageProjectRelation",
                               backref="languages",
                               primaryjoin=code == LanguageProjectRelation.lang_code)

    def __repr__(self):
        return '<Language %s code=%s>' % (self.name, self.code)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=True)

    languages = db.relationship("LanguageProjectRelation",
                                backref="projects",
                                primaryjoin=id == LanguageProjectRelation.project_id)

    def __repr__(self):
        return '<Project %s id=%s>' % (self.name, self.id)


class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('usage_classes', lazy=True))

    def __repr__(self):
        return '<Component %s id=%s>' % (self.name, self.id)

    def to_json_dict(self):
        return {'id': self.id, 'name': self.name}


class Identifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(100), nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('identifiers', lazy=True))

    component_id = db.Column(db.Integer, db.ForeignKey('component.id'), nullable=True)
    component = db.relationship('Component', backref=db.backref('identifiers'))

    def __repr__(self):
        return '<Identifier %s>' % self.id

    def to_json_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'componentID': self.component_id,
            'componentName': self.component.name if self.component else None,
            'description': self.description
        }


class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DATETIME, default=datetime.datetime.utcnow())

    identifier_id = db.Column(db.Integer, db.ForeignKey('identifier.id'), nullable=False)
    identifier = db.relationship('Identifier', backref=db.backref('translations'))

    language_code = db.Column(db.String(5), db.ForeignKey('language.code'), nullable=False)
    language = db.relationship('Language', backref=db.backref('translations', lazy=True))

    def __repr__(self):
        return '<Translation id=%s lang=%s>' % (self.id, self.language_code)

    def to_json_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'identifier': self.identifier.name
        }
