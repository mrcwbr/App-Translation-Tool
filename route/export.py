from flask import Blueprint, render_template, request, jsonify
from helpers.database import db
from model.models import Project, Identifier, Language, Translation

exp = Blueprint('export', __name__)


@exp.route('/export', methods=['GET'])
def translation():
    p = Project.query.first()

    language_code = request.args.get('lang')
    platform = request.args.get('platform')

    language = Language.query.filter_by(code=language_code).first()

    if not language:
        return "Unknown language-code!"

    if not platform or (platform != 'iOS' and platform != 'Android'):
        return "Unknown platform!"

    translations = Translation.query.filter(Translation.language_code == language.code,
                                            Translation.identifier.has(project_id=p.id)).all()

    last_update = max(t.timestamp for t in translations)

    result = add_comment(platform, "Updated: " + last_update.strftime('%Y-%m-%d %H:%M:%S'))

    if platform == 'Android':
        result += '<resources>\n'

    for t in translations:
        # TODO: Add comment for new component --> order by component and identfier
        result += build_translation_row(platform, t.identifier.name, t.text)

    if platform == 'Android':
        result += '</resources>\n'

    return result


def build_translation_row(platform, identifier, translation):
    if platform == 'iOS':
        # "Speed" = "Geschwindigkeit";
        return '"%s" = "%s";\n' % (identifier, translation)

    elif platform == 'Android':
        #
        return '<string name="%s">%s</string>\n' % (identifier, translation)


def add_comment(platform, text):
    if platform == 'iOS':
        # // Stand 10.10.2010
        return '// %s\n' % text

    elif platform == 'Android':
        # <!-- Strings related to Facebook-Login -->
        return '<!-- %s -->\n' % text
