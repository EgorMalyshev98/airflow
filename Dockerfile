FROM apache/airflow:2.7.3

COPY requirements.txt /

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r /requirements.txt
