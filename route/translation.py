from flask import Blueprint, render_template, request, jsonify
from helpers.database import db
from model.models import Project, Identifier, Language

trans = Blueprint('translation', __name__)


@trans.route('/translation/<language_code>', methods=['GET'])
def translation(language_code):
    language = Language.query.filter_by(code=language_code).first()

    p = Project.query.first()
    t = Identifier.query.filter_by(project_id=p.id).all()

    return render_template('translation.html', project=p, translations=t, language=language)


@trans.route('/translation', methods=['POST'])
def add_translation():
    '''
    p = Project.query.first()
    name = request.form.get('name')
    component_id = request.form.get('component_id')
    description = request.form.get('description')

    if not name:
        return jsonify({'success': False, 'msg': 'No identifier-name presented.'})

    if len(Identifier.query.filter(Identifier.project_id == p.id, Identifier.name == name).all()) != 0 \
            or len(name) < 3:
        return jsonify({'success': False,
                        'msg': "Identifiers's name is shorter than 3 characters or already in usage."})

    if component_id == "":
        component_id = None
    else:
        # Check if Component exists
        c = Component.query.filter_by(id=component_id).first()
        if c is None:
            return jsonify({'success': False, 'msg': 'Unknown component in project.'})

    if description == "":
        description = None

    i = Identifier(name=name, description=description, component_id=component_id, project_id=p.id)

    db.session.add(i)
    db.session.commit()

    return jsonify({'success': True, 'newIdent': i.to_json_dict()})'''
    return ''

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




@trans.route('/translation', methods=['DELETE'])
def delete_component():
    ident_id = request.form.get('id')

    if not ident_id:
        return jsonify({'success': False})

    i = Identifier.query.filter_by(id=ident_id).first()
    db.session.delete(i)
    db.session.commit()
    return jsonify({'success': True})
'''
