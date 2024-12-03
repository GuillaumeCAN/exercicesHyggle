from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from .models import EnergyData
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')


def show_data(request):
    # importation CSV
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        try:
            # clear all
            EnergyData.objects.all().delete()

            df = pd.read_csv(csv_file, delimiter=';')
            df.columns = df.columns.str.strip()

            if 'Date' not in df.columns or 'Region' not in df.columns or 'Valeur (TWh)' not in df.columns:
                messages.error(request, "Erreur : Les colonnes attendues sont manquantes.")
                return render(request, 'show_data.html')

            # Conversion dates
            df['Date'] = pd.to_datetime(df['Date'], format='%Y', errors='coerce')
            if df['Date'].isnull().any():
                messages.error(request, "Erreur : Certaines dates sont invalides.")
                return render(request, 'show_data.html')

            # Conversion de 'Valeur (TWh)'
            df['Valeur (TWh)'] = df['Valeur (TWh)'].apply(lambda x: float(str(x).replace(',', '.')))

            # Importation donnée
            for _, row in df.iterrows():
                EnergyData.objects.create(
                    date=row['Date'],
                    region=row['Region'],
                    consumption_twh=row['Valeur (TWh)']
                )
            messages.success(request, "Fichier importé avec succès.")

        except Exception as e:
            messages.error(request, f"Erreur lors de l'importation : {e}")


    data = EnergyData.objects.all()
    data_list = [(item.region, item.consumption_twh, item.date.isoformat() if item.date else '') for item in data]
    unique_regions = list(set([item.region for item in EnergyData.objects.all()]))
    paginator = Paginator(data_list, 12)  # 12 éléments par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data_list_json = json.dumps(data_list)

    return render(request, 'show_data.html', {
        'page_obj': page_obj,
        'data_list': page_obj.object_list,
        'data_list_json': data_list_json,
        'unique_regions': unique_regions
    })




######### API #########

# API - GET
def energy_data_list(request):
    data = EnergyData.objects.all()
    data_list = [
        {
            'id': item.id,
            'date': item.date.isoformat() if item.date else '',
            'region': item.region,
            'consumption_twh': item.consumption_twh
        }
        for item in data
    ]
    return JsonResponse(data_list, safe=False)


# API - ADD
@csrf_exempt
def add_energy_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date = data.get('date')
            region = data.get('region')
            consumption_twh = data.get('consumption_twh')

            if not date or not region or not consumption_twh:
                return JsonResponse({'error': 'Date, region, and consumption_twh are required fields'}, status=400)

            energy_data = EnergyData.objects.create(
                date=date,
                region=region,
                consumption_twh=consumption_twh
            )

            return JsonResponse({
                'id': energy_data.id,
                'date': energy_data.date,
                'region': energy_data.region,
                'consumption_twh': energy_data.consumption_twh
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



# API - DELETE
@csrf_exempt
def delete_energy_data(request, id):
    if request.method == 'DELETE':
        try:
            energy_data = EnergyData.objects.get(id=id)
            energy_data.delete()

            return JsonResponse({'message': 'Data deleted successfully'}, status=200)

        except EnergyData.DoesNotExist:
            return JsonResponse({'error': 'Data not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



# API - GET BY ID
def get_energy_data(request, id):
    if request.method == 'GET':
        try:
            energy_data = EnergyData.objects.get(id=id)

            data = {
                'id': energy_data.id,
                'region': energy_data.region,
                'consumption_twh': energy_data.consumption_twh,
                'date': energy_data.date.isoformat() if energy_data.date else None
            }

            return JsonResponse(data, status=200)

        except EnergyData.DoesNotExist:
            return JsonResponse({'error': 'Data not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



# API - UPDATE
@csrf_exempt
def update_energy_data(request, id):
    if request.method == 'PUT':
        try:
            energy_data = EnergyData.objects.get(id=id)
            body = json.loads(request.body)

            if 'region' in body:
                energy_data.region = body['region']
            if 'consumption_twh' in body:
                energy_data.consumption_twh = body['consumption_twh']
            if 'date' in body:
                energy_data.date = body['date']

            energy_data.save()

            return JsonResponse({
                'message': 'Data updated successfully',
                'data': {
                    'id': energy_data.id,
                    'region': energy_data.region,
                    'consumption_twh': energy_data.consumption_twh,
                    'date': energy_data.date if energy_data.date else None
                }
            }, status=200)

        except EnergyData.DoesNotExist:
            return JsonResponse({'error': 'Data not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)