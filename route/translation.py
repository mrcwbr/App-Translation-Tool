from flask import Blueprint, render_template, request, jsonify
from helpers.database import db
from model.models import Project, Identifier, Language, Translation

trans = Blueprint('translation', __name__)


@trans.route('/translation/<language_code>', methods=['GET'])
def translation(language_code):
    p = Project.query.first()
    language = Language.query.filter_by(code=language_code).first()
    other_languages = Language.query.filter(Language.code != language_code).all()
    unused_identifier = Identifier.query.filter(Identifier.project_id == p.id,
                                                Identifier.id.notin_(db.session.query(Translation.identifier_id)
                                                                     .filter_by(language_code=language_code))).all()
    translations = Translation.query.filter(Translation.language_code == language.code,
                                            Translation.identifier.has(project_id=p.id)).order_by(
        Translation.id.desc()).all()

    return render_template('translation.html',
                           project=p,
                           translations=translations,
                           unused_identifier=unused_identifier,
                           language=language,
                           other_languages=other_languages)


@trans.route('/translation', methods=['POST'])
def add_translation():
    p = Project.query.first()
    translation_string = request.form.get('translationString')
    identifier_id = request.form.get('identifierID')
    language_code = request.form.get('langCode')

    if not translation_string or len(translation_string) < 2 or not identifier_id or not language_code:
        return jsonify({'success': False, 'msg': 'Parameter is missing.'})

    lang = Language.query.filter_by(code=language_code).first()
    if not lang:
        return jsonify({'success': False, 'msg': 'Invalid language-code.'})

    i = Identifier.query.filter(Identifier.project_id == p.id, Identifier.id == identifier_id).first()
    if not i:
        return jsonify({'success': False, 'msg': 'Invalid identifierID.'})

    if len(Translation.query.filter(Translation.identifier_id == i.id,
                                    Translation.language_code == lang.code).all()) != 0:
        return jsonify({'success': False, 'msg': 'Identifier already in usage.'})

    t = Translation(text=translation_string, identifier_id=i.id, language_code=lang.code)

    db.session.add(t)
    db.session.commit()

    return jsonify({'success': True, 'newTrans': t.to_json_dict()})

# TODO: Update


''' 
@ident.route('/identifier', methods=['PUT'])
def update_component():
    name = request.form.get('name')
    comp_id = request.form.get('id')

    if not name or len(name) < 3 or not comp_id:
        return jsonify({'success': False})

    c = Component.query.filter(Component.id == comp_id).first()
    check_already_used = Component.query.filter(Component.name == name).all()
    if not c or check_already_used:
        return jsonify({'success': False})

    c.name = name
    db.session.commit()

    return jsonify({'success': True, 'updateComp': c.to_json_dict()})

'''


@trans.route('/translation', methods=['DELETE'])
def delete_component():
    translation_id = request.form.get('id')

    if not translation_id:
        return jsonify({'success': False, 'msg': 'Parameter is missing.'})

    t = Translation.query.filter_by(id=translation_id).first()
    db.session.delete(t)
    db.session.commit()
    return jsonify({'success': True})

