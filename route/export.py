from flask import Blueprint, render_template, request, jsonify
from model.models import Project, Language, Translation, Identifier, Component

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

    translations = Translation.query\
        .filter(Translation.language_code == language.code, Translation.identifier.has(project_id=p.id))\
        .join(Identifier)\
        .outerjoin(Component)\
        .order_by(Component.name, Identifier.name)\
        .all()

    last_update = max(t.timestamp for t in translations)

    result = add_comment(platform, "Updated: " + last_update.strftime('%Y-%m-%d %H:%M:%S'))

    if platform == 'Android':
        result += '<resources>\n'

    last_component_name = None
    for t in translations:
        # Create block for every component
        if t.identifier.component is None:
            result += '\n' + add_comment(platform, 'Identifiers without component')
            last_component_name = None
        elif t.identifier.component.name != last_component_name:
            result += '\n' + add_comment(platform, 'Component: ' + t.identifier.component.name)
            last_component_name = t.identifier.component.name

        result += build_translation_row(platform, t.identifier.name, t.text, t.identifier.description)

    if platform == 'Android':
        result += '</resources>\n'

    return result


def build_translation_row(platform, identifier, translation_text, description):
    if platform == 'iOS':
        # Format: "NEGATIVE_ALERT" = "Achtung"; // Comment
        result = '"%s" = "%s";' % (identifier, escape_ios(translation_text))
        return result + '\n' if description is None else result + ' // ' + description + '\n'

    elif platform == 'Android':
        # Format: <string name="NEGATIVE_ALERT">Achtung</string> <!-- Comment -->
        result = '<string name="%s">%s</string>' % (identifier, escape_android(translation_text))
        return result + '\n' if description is None else result + ' <!-- ' + description + '-->\n'


def escape_ios(text):
    text = text.replace("%s", "%@")  # type: str
    text = text.replace('"', '\\"')
    return text


def escape_android(text):
    # https://developer.android.com/guide/topics/resources/string-resource#FormattingAndStyling
    text = text.replace('@', '\\@')
    text = text.replace('?', '\\?')
    text = text.replace('<', '&lt;')
    text = text.replace('&', '&amp;')
    text = text.replace("'", "\\'")  # Single quote
    text = text.replace('"', '\\"')  # Double quote
    return text


def add_comment(platform, text):
    if platform == 'iOS':
        # // Stand 10.10.2010
        return '// %s\n' % text

    elif platform == 'Android':
        # <!-- Strings related to Facebook-Login -->
        return '<!-- %s -->\n' % text
