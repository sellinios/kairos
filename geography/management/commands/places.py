from django.core.management.base import BaseCommand
import os
import json
from shapely.geometry import Point as ShapelyPoint
from django.contrib.gis.geos import Point as DjangoPoint
from django.db import connection
from geography.models import GeographicPlace, GeographicCategory, GeographicDivision, GeographicCountry, GeographicLevel
from concurrent.futures import ThreadPoolExecutor, as_completed
import geopandas as gpd

GREECE_BOUNDARIES = {
    'min_latitude': 34.8,
    'max_latitude': 41.8,
    'min_longitude': 19.6,
    'max_longitude': 28.2,
}

METER_TO_DEGREE = 100 / 111000.0
BATCH_SIZE = 20000
NUM_THREADS = 8
PROGRESS_FILE = 'progress.json'
PROJECT_DATA_DIR = '/home/lefteris.broker/aethra/data/natural-earth-vector-5.1.0'
GREECE_SHAPEFILE = os.path.join(PROJECT_DATA_DIR, '10m_cultural/ne_10m_admin_0_countries.shp')
ELEVATION_FILE = os.path.join(PROJECT_DATA_DIR, '10m_physical/ne_10m_geography_regions_elevation_points.shp')
MUNICIPALITIES_FILE = os.path.join(PROJECT_DATA_DIR, '10m_cultural/ne_10m_admin_0_countries_grc.shp')

greece_gdf = gpd.read_file(GREECE_SHAPEFILE)
greece_gdf = greece_gdf[greece_gdf['NAME'] == 'Greece']
municipalities_gdf = gpd.read_file(MUNICIPALITIES_FILE)
elevation_gdf = gpd.read_file(ELEVATION_FILE)

def save_progress(lat, lon):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({'last_latitude': lat, 'last_longitude': lon}, f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {'last_latitude': GREECE_BOUNDARIES['min_latitude'],
                'last_longitude': GREECE_BOUNDARIES['min_longitude']}

def is_land(lat, lon):
    point = ShapelyPoint(lon, lat)
    is_within_greece = greece_gdf.contains(point).any()
    if not is_within_greece:
        return False, None

    point_gdf = gpd.GeoDataFrame(geometry=[point], crs=greece_gdf.crs)
    elevation_point = gpd.sjoin(point_gdf, elevation_gdf, how="inner", predicate="within")

    if not elevation_point.empty and elevation_point.iloc[0]['elevation'] > 0:
        for _, municipality in municipalities_gdf.iterrows():
            if municipality['geometry'].contains(point):
                return True, municipality['NAME']
    return False, None

def truncate_geographic_place():
    with connection.cursor() as cursor:
        cursor.execute('TRUNCATE TABLE geography_geographicplace RESTART IDENTITY CASCADE;')

def create_places_batch(latitudes, longitudes, default_category, default_division):
    places_to_create = []
    for lat in latitudes:
        for lon in longitudes:
            is_land_point, municipality_name = is_land(lat, lon)
            if is_land_point:
                name = f"{lat}-{lon}"
                slug = f"{lat}-{lon}"

                municipality_division, _ = GeographicDivision.objects.get_or_create(
                    name=municipality_name,
                    slug=municipality_name.lower().replace(' ', '-'),
                    level=default_division.level,
                    country=default_division.country,
                    defaults={'parent': default_division}
                )

                place = GeographicPlace(
                    name=name,
                    slug=slug,
                    longitude=lon,
                    latitude=lat,
                    elevation=0,
                    category=default_category,
                    admin_division=municipality_division,
                    location=DjangoPoint(lon, lat, srid=4326)
                )
                places_to_create.append(place)

                if len(places_to_create) >= BATCH_SIZE:
                    GeographicPlace.objects.bulk_create(places_to_create)
                    places_to_create = []

    if places_to_create:
        GeographicPlace.objects.bulk_create(places_to_create)
    return len(places_to_create)

class Command(BaseCommand):
    help = 'Create geographic places for Greece'

    def handle(self, *args, **kwargs):
        greece = GeographicCountry.objects.get(slug="greece")
        default_category, _ = GeographicCategory.objects.get_or_create(name="Default Category")
        municipality_level, _ = GeographicLevel.objects.get_or_create(
            name="Municipality",
            level_order=1,
            country=greece
        )
        default_division, _ = GeographicDivision.objects.get_or_create(
            name="Default Municipality",
            slug="default-municipality",
            level=municipality_level,
            country=greece,
            defaults={'parent': None}
        )

        progress = load_progress()
        start_latitude = progress['last_latitude']
        start_longitude = progress['last_longitude']

        total_latitude_points = int(
            (GREECE_BOUNDARIES['max_latitude'] - GREECE_BOUNDARIES['min_latitude']) / METER_TO_DEGREE)
        total_longitude_points = int(
            (GREECE_BOUNDARIES['max_longitude'] - GREECE_BOUNDARIES['min_longitude']) / METER_TO_DEGREE)
        total_points = total_latitude_points * total_longitude_points

        latitude_range = [GREECE_BOUNDARIES['min_latitude'] + i * METER_TO_DEGREE for i in range(total_latitude_points)]
        longitude_range = [GREECE_BOUNDARIES['min_longitude'] + i * METER_TO_DEGREE for i in
                           range(total_longitude_points)]

        lat_chunks = [latitude_range[i:i + BATCH_SIZE] for i in range(0, len(latitude_range), BATCH_SIZE)]
        lon_chunks = [longitude_range[i:i + BATCH_SIZE] for i in range(0, len(longitude_range), BATCH_SIZE)]

        processed_points = 0

        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = []
            for lat_chunk in lat_chunks:
                for lon_chunk in lon_chunks:
                    if lat_chunk[0] >= start_latitude and lon_chunk[0] >= start_longitude:
                        futures.append(executor.submit(create_places_batch, lat_chunk, lon_chunk, default_category,
                                                       default_division))

            for future in as_completed(futures):
                processed_points += future.result()
                last_processed_lat = lat_chunk[0]
                last_processed_lon = lon_chunk[0]
                save_progress(last_processed_lat, last_processed_lon)
                progress_percentage = (processed_points / total_points) * 100
                print(f"Progress: {progress_percentage:.2f}%")

        print("Progress: 100%")
