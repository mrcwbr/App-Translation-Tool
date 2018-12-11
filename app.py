import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from helpers import local_database_path

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + local_database_path.absolute_db_path + 'translation.db?check_same_thread=False'
db = SQLAlchemy(app)


# TODO: Project sturucture
# TODO: Stand als datum in oberste zeile als kommentar exportieren
# TODO: Default Language angeben -> if not translated completely no export or error message

@app.route('/')
def root():
    p = Project.query.first()
    number_of_identifiers = len(Identifier.query.filter_by(project_id=p.id).all())
    number_of_components = len(Component.query.filter_by(project_id=p.id).all())
    number_of_languages = len(LanguageProjectRelation.query.filter(LanguageProjectRelation.project_id == p.id).all())

    return render_template('root.html',
                           project=p,
                           number_of_identifiers=number_of_identifiers,
                           number_of_components=number_of_components,
                           number_of_languages=number_of_languages)


@app.route('/identifier')
def identifier():
    p = Project.query.first()
    i = Identifier.query.filter_by(project_id=p.id).all()

    return render_template('identifiers.html', project=p, identifiers=i)


@app.route('/component', methods=['GET'])
def component():
    p = Project.query.first()
    c = Component.query.filter_by(project_id=p.id).order_by(Component.id.desc()).all()

    return render_template('components.html', project=p, components=c)


@app.route('/component', methods=['POST', 'PUT', 'DELETE'])
def modify_component():
    name = request.form.get('name')
    id = request.form.get('id')

    if request.method == 'POST':
        if not name:
            return jsonify({'success': False})

        p = Project.query.first()

        if len(Component.query.filter(Component.project_id == p.id, Component.name == name).all()) != 0 or len(name) < 3:
            return jsonify({'success': False})

        c = Component(name=name, project_id=p.id)
        db.session.add_all([c])
        db.session.commit()

        return jsonify({'success': True, 'id': c.id})

    elif request.method == 'PUT':
        print('TODO')  # TODO add todo

    elif request.method == 'DELETE':
        if not id:
            return jsonify({'success': False})

        c = Component.query.filter_by(id=id).first()
        db.session.delete(c)
        db.session.commit()
        return jsonify({'success': True})

    return jsonify({'success': False})



@app.route('/translation/<language_code>')
def translation(language_code):
    language = Language.query.filter_by(code=language_code).first()

    p = Project.query.first()
    t = Identifier.query.filter_by(project_id=p.id).all()

    return render_template('translation.html', project=p, translations=t, language=language)


if __name__ == '__main__':
    app.run()


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


class Identifier(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    description = db.Column(db.String(100), nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('identifiers', lazy=True))

    component_id = db.Column(db.Integer, db.ForeignKey('component.id'), nullable=True)
    component = db.relationship('Component', backref=db.backref('identifiers', lazy=True))

    def __repr__(self):
        return '<Identifier %s>' % self.id


class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DATETIME, default=datetime.datetime.utcnow())

    identifier_id = db.Column(db.String(255), db.ForeignKey('identifier.id'), nullable=False)
    identifier = db.relationship('Identifier', backref=db.backref('translations', lazy=True))

    language_code = db.Column(db.String(5), db.ForeignKey('language.code'), nullable=False)
    language = db.relationship('Language', backref=db.backref('translations', lazy=True))

    def __repr__(self):
        return '<Translation id=%s lang=%s>' % (self.id, self.language_code)
