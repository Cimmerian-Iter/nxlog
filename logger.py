import psutil
import time
import logging
from graypy import GELFUDPHandler
import geoip2.database

# Chemin vers la base de données GeoLite2
GEO_DATABASE_PATH = 'C:/Users/test/Downloads/database.mmdb'

# Configuration de l'adresse IP et du port de Graylog
GRAYLOG_SERVER = '172.30.33.3'
GRAYLOG_PORT = 12202

# Configuration du logger
logger = logging.getLogger('IPLogger')
logger.setLevel(logging.INFO)
handler = GELFUDPHandler(GRAYLOG_SERVER, GRAYLOG_PORT)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Chargement de la base de données géographique locale
geo_reader = geoip2.database.Reader(GEO_DATABASE_PATH)

# Fonction pour obtenir la localisation géographique d'une adresse IP à partir de la base de données locale
def get_ip_location(ip_address):
    if ip_address.startswith(('172.', '192.', '127.')):
        return 0 # Ignore les adresses IP qui commencent par "172" ou "192"
    try:
        response = geo_reader.city(ip_address)
        country_name = response.country.name
        logger.info({'IP_Address': ip_address, 'Country': country_name})
    except geoip2.errors.AddressNotFoundError:
        logger.info({'IP_Address': ip_address, 'Country': 'Unknown'})

# Fonction principale pour surveiller les connexions réseau
def monitor_network_connections():
    while True:
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if conn.status == 'ESTABLISHED':
                remote_ip = conn.raddr.ip
                get_ip_location(remote_ip)
        time.sleep(60)  # Attendre 60 secondes avant de vérifier à nouveau les connexions

if __name__ == "__main__":
    monitor_network_connections()
