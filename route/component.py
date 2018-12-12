from flask import Blueprint, render_template, request, jsonify
from helpers.database import db
from model.models import Project, Component

comp = Blueprint('component', __name__)


@comp.route('/component', methods=['GET'])
def component():
    p = Project.query.first()
    c = Component.query.filter_by(project_id=p.id).order_by(Component.id.desc()).all()

    return render_template('components.html', project=p, components=c)


@comp.route('/component', methods=['POST'])
def add_component():
    name = request.form.get('name')

    if not name:
        return jsonify({'success': False})

    p = Project.query.first()

    if len(Component.query.filter(Component.project_id == p.id, Component.name == name).all()) != 0 \
            or len(name) < 3:
        return jsonify({'success': False})

    c = Component(name=name, project_id=p.id)
    db.session.add_all([c])
    db.session.commit()

    return jsonify({'success': True, 'newComp': c.to_json_dict()})


@comp.route('/component', methods=['PUT'])
def update_component():
    name = request.form.get('name')
    comp_id = request.form.get('id')

    if not name or not comp_id:
        return jsonify({'success': False})

    print('TODO')  # TODO add put


@comp.route('/component', methods=['DELETE'])
def delete_component():
    comp_id = request.form.get('id')

    if not comp_id:
        return jsonify({'success': False})

    c = Component.query.filter_by(id=comp_id).first()
    db.session.delete(c)
    db.session.commit()
    return jsonify({'success': True})

