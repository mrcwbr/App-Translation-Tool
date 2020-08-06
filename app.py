from os import getenv
from flask import Flask, render_template, request, jsonify
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

custom_db_uri = getenv('CUSTOM_DB_URI', None)
if custom_db_uri is None:
    raise Exception('CUSTOM_DB_URI not preset, set this value as a env var')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = custom_db_uri
db.init_app(app)


@app.route('/')
def root():
    p = Project.query.first()  # TODO check if Project is none
    number_of_identifiers = len(Identifier.query.filter_by(project_id=p.id).all())
    number_of_components = len(Component.query.filter_by(project_id=p.id).all())
    number_of_languages = len(LanguageProjectRelation.query.filter(LanguageProjectRelation.project_id == p.id).all())
    languages = p.languages

    for lang in languages:
        translations = Translation.query.filter(Translation.language_code == lang.lang_code,
                                                Translation.identifier.has(project_id=p.id)).all()

        lang.last_update = None if len(translations) == 0 else max(t.timestamp for t in translations)
        lang.translated_percentage = 0 if number_of_identifiers == 0 else round(len(translations) * 100
                                                                                / number_of_identifiers)

    return render_template('root.html',
                           project=p,
                           languages=languages,
                           number_of_identifiers=number_of_identifiers,
                           number_of_components=number_of_components,
                           number_of_languages=number_of_languages)


@app.route('/init', methods=['POST'])
def init_translation_tool():
    project_name = request.form.get('projectName')
    __abs_db_path = request.form.get('absDBPath')
    lang_code = request.form.get('langCode')
    lang_name = request.form.get('langName')
    lang_img = request.form.get('langImg')

    # write the yml
    # data = {'database': {'absolute-path': str(__abs_db_path)}}
    # with io.open('config.yml', 'w', encoding='utf8') as outfile:
    # yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    # Init DB
    # init_db()

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
    app.run(host='0.0.0.0')
