# Base da imagem (utilize uma imagem oficial do Python)
FROM python:3.12.7-alpine3.19

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o container
COPY requirements.txt ./

# Instala as dependências do projeto
RUN pip install -r requirements.txt
RUN pip install Django
RUN pip install django-debug-toolbar
RUN pip install pillow
RUN pip install django-crispy-forms
RUN pip install crispy-bootstrap5
RUN pip install django-filter
RUN pip install djangorestframework

# Copia todo o código do projeto para o container
COPY .. .

# Executa o servidor de desenvolvimento Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]