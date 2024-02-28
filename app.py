import re
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

excel_file = 'datospersonales.xlsx'
df = pd.read_excel(excel_file)

@app.route('/table', methods=['GET', 'POST'])
def table(): 
    if request.method == 'POST':
        filter_keyword = request.form['filter'].lower()
        
        df['Nombre Contacto'] = df['Nombre Contacto'].astype(str)
        
        # Filtrar los datos solo en la columna 'Nombre Contacto'
        filtered_data = df[df['Nombre Contacto'].str.contains(filter_keyword, case=False)]
        
        # Mostrar solo las columnas relevantes
        filtered_data = filtered_data[['Clave cliente','Nombre Contacto', 'Correo', 'Teléfono Contacto']]
    else:
        filtered_data = df[['Clave cliente','Nombre Contacto', 'Correo', 'Teléfono Contacto']]
    
    table_html = filtered_data.to_html(classes='table table-striped', index=False)
    return render_template('table.html', table_html=table_html)

@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if validar_contraseña(password):
            return redirect(url_for('table'))
        else:
            error_message = 'La contraseña no cumple con los requisitos.'
    
    return render_template('index.html', error_message=error_message)

def validar_contraseña(contraseña):
    regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-+=])[A-Za-z\d!@#$%^&*()-+=]{8,15}$"
    
    # Validar la contraseña usando la expresión regular
    if re.match(regex, contraseña):
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)


