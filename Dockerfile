FROM python

WORKDIR /app

COPY requirements.txt .

#устанавливаем зависимости (хз зачем это)
RUN pip install --no-cache-dir -r requirements.txt 

#копируем исходный код приложения 
COPY . . 


CMD ["python", "app.py"]