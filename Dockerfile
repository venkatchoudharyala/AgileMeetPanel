FROM python:3.7

WORKDIR /AgileMeetPanel

COPY . /AgileMeetPanel

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "App.py"]
