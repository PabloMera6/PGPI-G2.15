
FROM python:3.10.11


WORKDIR /app


RUN git clone https://github.com/PabloMera6/PGPI-G2.15.git

WORKDIR /app/PGPI-G2.15/src

# Agrega un comando para imprimir el contenido del directorio actual
RUN echo "Contenido del directorio:" && ls



# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn


RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py loaddata populate.json

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "motos_para_todos.wsgi:application", "--bind", "0.0.0.0:8000"]