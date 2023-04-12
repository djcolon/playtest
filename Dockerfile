FROM mcr.microsoft.com/playwright/python:v1.32.1-jammy

# set the working directory
WORKDIR /app/

# install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the files to the folder
COPY . /app/

# run the program
CMD [ "python", "main.py" ]