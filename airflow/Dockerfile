FROM puckel/docker-airflow:1.10.4

USER root
RUN addgroup --gid 999 docker && usermod -aG docker airflow
USER airflow