import os
import uuid
from dotenv import load_dotenv

# Load environment variables from .env before anything else
load_dotenv()

from cotizador import create_app
from cotizador.db import get_db

def clear_collection(db, collection_name):
    """Deletes all documents in a collection."""
    collection_ref = db.collection(collection_name)
    docs = collection_ref.limit(100).stream()
    deleted = 0
    for doc in docs:
        doc.reference.delete()
        deleted += 1
    # If there are more documents, recursively call to delete the next batch
    if deleted >= 100:
        clear_collection(db, collection_name)

def seed_tipos_cliente(db):
    """Seeds the 'tipos_cliente' collection."""
    collection_name = 'tipos_cliente'
    print(f"Seeding '{collection_name}' collection...")
    clear_collection(db, collection_name)
    collection_ref = db.collection(collection_name)

    tipos = [
        {"nombre": "Agencia de Medios", "descuento": 0.20},
        {"nombre": "Cliente Directo", "descuento": 0.05},
        {"nombre": "Agencia Creativa", "descuento": 0.15},
        {"nombre": "Partner Estratégico", "descuento": 0.25},
        {"nombre": "Gobierno", "descuento": 0.10},
        {"nombre": "Intercambio", "descuento": 1.0},
    ]

    for tipo_data in tipos:
        doc_id = str(uuid.uuid4())
        tipo_data['id'] = doc_id
        collection_ref.document(doc_id).set(tipo_data)
        print(f"  Added: {tipo_data['nombre']}")

    return [doc.to_dict() for doc in collection_ref.stream()]

def seed_soportes(db):
    """Seeds the 'soportes' collection."""
    collection_name = 'soportes'
    print(f"\nSeeding '{collection_name}' collection...")
    clear_collection(db, collection_name)
    collection_ref = db.collection(collection_name)

    soportes = [
        {"codigo": "G4C-CMX-001", "nombre": "Espectacular en Periférico Norte", "tipo_soporte": "Unipolar", "municipio": "Naucalpan de Juárez", "precio_minimo": 12000.0, "precio_mensual": 28000.0, "latitud": 19.4939, "longitud": -99.2312, "place_id": "ChIJ_w-L3Tr_0YURw2sY7oAG5z8"},
        {"codigo": "G4C-CMX-002", "nombre": "Muro en Viaducto Tlalpan", "tipo_soporte": "Muro", "municipio": "Tlalpan", "precio_minimo": 9000.0, "precio_mensual": 22000.0, "latitud": 19.2883, "longitud": -99.1485, "place_id": "ChIJ-U0TH6r_0YURbL2BwM0E1xQ"},
        {"codigo": "G4C-JAL-001", "nombre": "Pantalla Digital en Av. Américas", "tipo_soporte": "Pantalla Digital", "municipio": "Guadalajara", "precio_minimo": 18000.0, "precio_mensual": 45000.0, "latitud": 20.6932, "longitud": -103.3828, "place_id": "ChIJ8f4o1b_zKIQRqPjI_k_88Hw"},
        {"codigo": "G4C-MTY-001", "nombre": "Valla Publicitaria en Av. Lázaro Cárdenas", "tipo_soporte": "Valla", "municipio": "San Pedro Garza García", "precio_minimo": 8500.0, "precio_mensual": 19500.0, "latitud": 25.6493, "longitud": -100.3554, "place_id": "ChIJcTj5kaxfYYYRl_B97zaM9Yk"},
        {"codigo": "G4C-PUE-001", "nombre": "Puente Peatonal en Atlixcáyotl", "tipo_soporte": "Puente", "municipio": "Puebla", "precio_minimo": 6000.0, "precio_mensual": 15000.0, "latitud": 19.0153, "longitud": -98.2431, "place_id": "ChIJgXq0r7-uz4URk_0_8bCg1fQ"}
    ]

    for soporte_data in soportes:
        doc_id = str(uuid.uuid4())
        soporte_data['id'] = doc_id
        collection_ref.document(doc_id).set(soporte_data)
        print(f"  Added: {soporte_data['codigo']}")

    return [doc.to_dict() for doc in collection_ref.stream()]

def seed_cotizaciones(db, tipos_cliente, soportes):
    """Seeds the 'cotizaciones' collection."""
    collection_name = 'cotizaciones'
    print(f"\nSeeding '{collection_name}' collection...")
    clear_collection(db, collection_name)

    if not tipos_cliente or not soportes:
        print("  Skipping cotizaciones seeding: missing prerequisite data.")
        return

    collection_ref = db.collection(collection_name)
    cotizaciones = [
        {"titulo": "Campaña de Lanzamiento - Nuevo Refresco", "tipo_cliente": tipos_cliente[0]['id'], "anunciante": "Refrescos Mundiales S.A.", "agencia": "Medios Globales", "probabilidad_cierre": 0.8, "presupuesto_estimado": 75000.0, "ejecutivo": "Ana Rodríguez", "periodo_inicio": "2024-09-01", "periodo_fin": "2024-09-30", "soportes_seleccionados": [soportes[0]['id'], soportes[2]['id']], "logo_cliente_ref": "logos/refrescos_mundiales_logo.png", "logo_agencia_ref": "logos/medios_globales_logo.png"},
        {"titulo": "Campaña Institucional - Gobierno del Estado", "tipo_cliente": tipos_cliente[4]['id'], "anunciante": "Gobierno del Estado", "agencia": "", "probabilidad_cierre": 0.95, "presupuesto_estimado": 120000.0, "ejecutivo": "Carlos Sánchez", "periodo_inicio": "2024-10-01", "periodo_fin": "2024-12-31", "soportes_seleccionados": [soportes[1]['id'], soportes[3]['id'], soportes[4]['id']], "logo_cliente_ref": "logos/gobierno_logo.png", "logo_agencia_ref": ""}
    ]

    for cotizacion_data in cotizaciones:
        doc_id = str(uuid.uuid4())
        cotizacion_data['id'] = doc_id
        collection_ref.document(doc_id).set(cotizacion_data)
        print(f"  Added: {cotizacion_data['titulo']}")

def run_seeding():
    """The main seeding function."""
    db = get_db()
    if not db:
        print("Database not initialized. Aborting seeding.")
        return

    print("=======================================")
    print("  STARTING DATABASE SEEDING PROCESS  ")
    print("=======================================")

    tipos_cliente_data = seed_tipos_cliente(db)
    soportes_data = seed_soportes(db)
    seed_cotizaciones(db, tipos_cliente_data, soportes_data)

    print("\n=======================================")
    print("   DATABASE SEEDING FINISHED   ")
    print("=======================================")

if __name__ == '__main__':
    # Create a Flask app context to use the 'g' object and get_db()
    app = create_app()
    with app.app_context():
        run_seeding()
