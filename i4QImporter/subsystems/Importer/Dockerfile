FROM python:3.10
COPY ./requirements.txt .
# Install any needed packages specified in requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY ./data_importer.py .
# Run the application:
CMD [ "python", "./data_importer.py" ]