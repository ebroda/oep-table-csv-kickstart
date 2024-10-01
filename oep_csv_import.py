from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from oep_client import OepClient, OepTableAlreadyExistsException, OepClientSideException
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import FileField, StringField

from settings import SETTINGS

app = Flask(__name__, template_folder='frontend/views', static_folder='frontend/app')
app.secret_key = 'oep-csv-import'


class CSVForm(FlaskForm):
    file = FileField(validators=[FileAllowed(['csv'])], render_kw={'accept': 'text/csv'})
    seperator = StringField(default=',', render_kw={'maxlength': 1})
    encoding = SelectField(choices=[('utf-8', 'UTF-8'), ('latin1', 'ISO-8859-1 / latin-1'), ('ascii', 'ASCII')])


@app.route('/')
def main_get():
    return render_template('upload.html', form=CSVForm())


@app.route('/upload', methods=['POST'])
def main_post():
    table_name = request.form.get('table_name')

    total_rows = int(request.form.get('total_rows'))

    primary_row = -1
    if 'primary' in request.form:
        primary_row = int(request.form.get('primary'))

    columns = []
    for i in range(total_rows):
        field_name = request.form.get('field_name%d' % i).strip()

        if len(field_name) == 0:
            continue

        field_type = request.form.get('type%d' % i)
        nullable = ('nullable%d' % i) in request.form

        row_dict = {'name': field_name, 'data_type': field_type, 'is_nullable': nullable}

        if primary_row == i:
            row_dict['primary_key'] = True

        columns.append(row_dict)

    schema = {"columns": columns}
    rtn_dict = {'table': table_name, 'columns': columns, 'success': True, 'oep_url': '%s://%s/dataedit/wizard/model_draft/%s#wizard-container-upload' % (SETTINGS['OEP_PROTOCOL'], SETTINGS['OEP_HOST'], table_name)}

    topic = 'model_draft'
    cli = OepClient(token=SETTINGS['OEP_API_TOKEN'], host=SETTINGS['OEP_HOST'], protocol=SETTINGS['OEP_PROTOCOL'], default_schema=topic)
    try:
        cli.create_table(table_name, schema)
    except OepTableAlreadyExistsException as exp:
        rtn_dict['success'] = False
        rtn_dict['exception'] = {'name': 'OepTableAlreadyExistsException', 'msg': str(exp)}
    except OepClientSideException as exp:
        rtn_dict['success'] = False
        msg = str(exp)

        if msg.startswith("{'reason': "):
            msg = msg[12:-2].replace('\n', '<br />')
        rtn_dict['exception'] = {'name': 'OepClientSideException', 'msg': msg}

    return jsonify(rtn_dict)


if __name__ == '__main__':
    app.run(debug=True)
