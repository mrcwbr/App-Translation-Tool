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
    p = Project.query.first()
    name = request.form.get('name')
    component_id = request.form.get('componentID')
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

    # Format name
    name = name.upper()
    name = name.replace(' ', '_')

    i = Identifier(name=name, description=description, component_id=component_id, project_id=p.id)

    db.session.add(i)
    db.session.commit()

    return jsonify({'success': True, 'newIdent': i.to_json_dict()})


@ident.route('/identifier', methods=['PUT'])
def update_component():
    p = Project.query.first()
    identifier_id = request.form.get('id')
    name = request.form.get('name')
    component_id = request.form.get('componentID')
    description = request.form.get('description')

    if not name or len(name) < 3:
        return jsonify({'success': False, 'msg': "Identifiers's name is shorter than 3 characters"})

    if component_id == "":
        component_id = None
    else:
        # Check if Component exists
        c = Component.query.filter_by(id=component_id).first()
        if c is None:
            return jsonify({'success': False, 'msg': 'Unknown component in project.'})

    if description == "":
        description = None

    i = Identifier.query.filter(Identifier.id == identifier_id).first()
    i.name = name
    i.component_id = component_id
    i.description = description

    db.session.commit()

    return jsonify({'success': True, 'updatedIdentifier': i.to_json_dict()})


@ident.route('/identifier', methods=['DELETE'])
def delete_component():
    ident_id = request.form.get('id')

    if not ident_id:
        return jsonify({'success': False})

    i = Identifier.query.filter_by(id=ident_id).first()
    db.session.delete(i)
    db.session.commit()
    return jsonify({'success': True})
