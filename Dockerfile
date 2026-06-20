FROM apache/airflow:3.2.2

USER root
COPY pyproject.toml /opt/airflow/pyproject.toml
COPY src/ /opt/airflow/src/
RUN touch /opt/airflow/README.md && \
    chown -R airflow:root /opt/airflow/src /opt/airflow/pyproject.toml /opt/airflow/README.md

USER airflow
RUN pip install /opt/airflow