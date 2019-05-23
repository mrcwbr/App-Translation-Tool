from flask import Flask, render_template, request, jsonify
import yaml
import io
import validators
from helpers.database import db
from model.models import Project, Identifier, Component, LanguageProjectRelation, Translation, Language

from route.component import comp  # Imported object import must be a other name than file
from route.identifier import ident
from route.translation import trans
from route.export import exp

app = Flask(__name__)

app.register_blueprint(comp)
app.register_blueprint(ident)
app.register_blueprint(trans)
app.register_blueprint(exp)


def get_db_path():
    try:
        with open("config.yml", 'r') as stream:
            yaml_content = yaml.safe_load(stream)
            db_path = yaml_content['database']['absolute-path']
            return db_path
    except:
        return None


__abs_db_path = get_db_path()


def init_db():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + __abs_db_path + 'translation.db?check_same_thread=False'
    db.init_app(app)


def init_required():
    return render_template('init.html')


if __abs_db_path is not None:
    init_db()


@app.route('/')
def root():
    if get_db_path() is None:
        return init_required()

    p = Project.query.first()
    number_of_identifiers = len(Identifier.query.filter_by(project_id=p.id).all())
    number_of_components = len(Component.query.filter_by(project_id=p.id).all())
    number_of_languages = len(LanguageProjectRelation.query.filter(LanguageProjectRelation.project_id == p.id).all())
    languages = p.languages

    for l in languages:
        translations = Translation.query.filter(Translation.language_code == l.lang_code,
                                                Translation.identifier.has(project_id=p.id)).all()

        l.last_update = None if len(translations) == 0 else max(t.timestamp for t in translations)
        l.translated_percentage = 0 if number_of_identifiers == 0 else round(len(translations) * 100 / number_of_identifiers)

    return render_template('root.html',
                           project=p,
                           languages=languages,
                           number_of_identifiers=number_of_identifiers,
                           number_of_components=number_of_components,
                           number_of_languages=number_of_languages)


@app.route('/init', methods=['POST'])
def init_translation_tool():
    project_name = request.form.get('projectName')
    global __abs_db_path
    __abs_db_path = request.form.get('absDBPath')
    lang_code = request.form.get('langCode')
    lang_name = request.form.get('langName')
    lang_img = request.form.get('langImg')

    # write the yml
    data = {'database': {'absolute-path': str(__abs_db_path)}}
    with io.open('config.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    # Init DB
    init_db()

    # Create DB and Project
    db.create_all()
    p = Project(name=project_name)
    db.session.add(p)
    db.session.commit()

    __add_language(lang_code, lang_name, lang_img, p, True)

    return '', 204


@app.route('/language', methods=['POST'])
def language_route():
    lang_code = request.form.get('langCode')
    lang_name = request.form.get('langName')
    lang_img = request.form.get('langImg')

    res = __add_language(lang_code, lang_name, lang_img, Project.query.first(), False)
    if res is None:
        return '', 204
    else:
        return jsonify({'msg': res}), 400


def __add_language(lang_code, lang_name, lang_img, project, is_default):
    if len(lang_code) != 5:
        return 'Invalid Language Code'

    if len(lang_name) < 2:
        return 'Invalid Language Name'

    if not validators.url(lang_img):
        return 'Invalid image URL'

    lang = Language(code=lang_code,
                    name=lang_name,
                    flag_image_link=lang_img)

    lp_rel = LanguageProjectRelation(project_id=project.id, lang_code=lang.code, is_default=is_default)

    lang.projects.append(lp_rel)
    project.languages.append(lp_rel)

    db.session.add(lang)
    db.session.commit()

    return None


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    p = Project.query.first()
    return render_template('404.html', project=p), 404


if __name__ == '__main__':
    app.run()



