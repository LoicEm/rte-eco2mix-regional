FROM prefecthq/prefect:0.14.0-python3.6

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python setup.py install