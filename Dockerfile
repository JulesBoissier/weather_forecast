FROM python:3.9-slim

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# # Expose port 80to allow communication to/from server
EXPOSE 80

# 
COPY ./app /code/app

# 
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "80"]