from flask import Flask, request, jsonify
import datetime
import pandas as pd
import numpy as np
app = Flask(__name__)


diasAdicionales = [0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]


data = {
    'Años': list(range(1, 21)),
    'Días Trabajados': [360*i for i in range(1, 21)],
    'Días Vacaciones': [15]*20,
    'Días Adicionales':diasAdicionales,
    'Total Vacaciones':[15+ diasAdicionales[i] for i in range(len(diasAdicionales)) ],
    'Acumulado': []
}
acumulado = 0
for valor in data['Total Vacaciones']:
    acumulado += valor
    data['Acumulado'].append(acumulado)



df = pd.DataFrame(data)


def calculate_days(start_date, end_date, method=False):
    print("Fechas%%%%%%%%%%%%%%%%")
    print(start_date)
    print(end_date)
    if not method:
        method = False
    else:
        method = True

    if method:
        start_date = start_date.replace(day=30)
        end_date = end_date.replace(day=30)

        if start_date.day == 31 or datetime.date(start_date.year, start_date.month, 1) + datetime.timedelta(days=31) <= end_date:
            start_date = start_date.replace(day=1, month=start_date.month+1)

        if start_date > end_date.replace(day=1):
            end_date = end_date.replace(day=1, month=end_date.month-1)

    return 360 * (end_date.year - start_date.year) + 30 * (end_date.month - start_date.month) + (end_date.day - start_date.day)



def calculatedVacionesGenereada(dayLaborado,anioLaborado):
    if(anioLaborado < 1):
        vacionGenerado = anioLaborado *15
    else:
        # Calcular la diferencia absoluta entre el valor buscado y los valores en la columna 'Años'
        diferencias = np.abs(df['Años'] - int(anioLaborado))

        # Encontrar el índice del valor más cercano
        indice_cercano = np.argmin(diferencias)

        # Obtener el valor de la columna 'Acumulado' correspondiente al índice encontrado
        valor_acumuladoA = df['Acumulado'].iloc[indice_cercano]
        valor_acumuladoB = df['Días Trabajados'].iloc[indice_cercano]
        vacionGenerado = (dayLaborado * valor_acumuladoA)/valor_acumuladoB
    
    return vacionGenerado
        



@app.route('/days360', methods=['POST'])
def calculate_days360():
    data = request.get_json()
    start_date_str = data['start_date']
    end_date_str = data['end_date']
    method = data.get('method', False)
    anioLaborado =  data['anioLaborado']
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    result = calculate_days(start_date, end_date, method)

    vacacionGenerado = calculatedVacionesGenereada(result,anioLaborado)

    response = {
        'diaLaborado': result,
        'vacacionGenerado': vacacionGenerado
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()
