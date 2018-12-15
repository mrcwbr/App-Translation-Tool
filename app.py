from flask import Flask, render_template, request, jsonify
from helpers import local_database_path
from helpers.database import db
from model.models import Project, Identifier, Component, LanguageProjectRelation, Language

from route.component import comp  # Imported object import must be a other name than file
from route.identifier import ident
from route.translation import trans

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + local_database_path.absolute_db_path + 'translation.db?check_same_thread=False'

db.init_app(app)
app.register_blueprint(comp)
app.register_blueprint(ident)
app.register_blueprint(trans)


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


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    p = Project.query.first()
    return render_template('404.html', project=p), 404


if __name__ == '__main__':
    app.run()
