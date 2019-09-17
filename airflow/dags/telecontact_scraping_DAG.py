from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime,timedelta
import docker
import logging
import itertools

CITIES = ["Rabat","Casablanca","Marrakech"]
ACTIVITIES = ["Tech","Bank"]

#Dag's default args
default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': datetime(2019, 8, 19,18),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(hours=2), 
}

#instantiate the DAG
dag = DAG(
    'telecontact_scraping',
    default_args=default_args,
    schedule_interval='@once'
)

def do_test_docker():
    client = docker.APIClient()
    for image in client.images():
        logging.info(str(image))

def get_task(activity,city):
    return DockerOperator(
        task_id= f'mine_{activity}_{city}',
        image='tahasadiki/telecontact-scraper:latest',
        api_version='auto',
        auto_remove=True,
        command=f"{activity} {city}",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )

with dag :
    t1 = PythonOperator(
    task_id="test_docker",
    python_callable=do_test_docker
    )

    t3 = BashOperator(
        task_id='scraping_done',
        bash_command='echo "Scraping Done!"'
    )

    
    for activity,city in itertools.product(ACTIVITIES,CITIES):
        t1 >> get_task(activity,city) >> t3