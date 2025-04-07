FROM apache/airflow:2.10.5


COPY requirements.txt /

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r /requirements.txt

USER root
RUN groupadd --gid 999 docker \
    && usermod -aG docker airflow

USER airflow
