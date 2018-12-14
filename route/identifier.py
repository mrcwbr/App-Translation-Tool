from flask import Blueprint, render_template, request, jsonify
from helpers.database import db
from model.models import Project, Identifier, Component

ident = Blueprint('identifier', __name__)


@ident.route('/identifier', methods=['GET'])
def identifier():
    p = Project.query.first()
    i = Identifier.query.filter_by(project_id=p.id).order_by(Identifier.id.desc()).all()
    all_components = Component.query.filter_by(project_id=p.id).all()

    return render_template('identifiers.html', project=p, identifiers=i, all_components=all_components)


@ident.route('/identifier', methods=['POST'])
def add_identifier():
    name = request.form.get('name')
    component_id = request.form.get('component_id')
    description = request.form.get('description')

    if not name:
        return jsonify({'success': False})

    p = Project.query.first()

    if len(Identifier.query.filter(Identifier.project_id == p.id, Identifier.id == name).all()) != 0 \
            or len(name) < 3:
        return jsonify({'success': False})

    if component_id == "":
        component_id = None
    else:
        # Check if Component exists
        c = Component.query.filter_by(id=component_id).first()
        if c is None:
            return jsonify({'success': False})

    if description == "":
        description = None

    i = Identifier(name=name, description=description, component_id=component_id, project_id=p.id)

    db.session.add(i)
    db.session.commit()

    return jsonify({'success': True, 'newIdent': i.to_json_dict()})

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


@ident.route('/identifier', methods=['DELETE'])
def delete_component():
    ident_id = request.form.get('id')

    if not ident_id:
        return jsonify({'success': False})

    i = Identifier.query.filter_by(id=ident_id).first()
    db.session.delete(i)
    db.session.commit()
    return jsonify({'success': True})
