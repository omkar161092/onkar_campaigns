# Create the base image
FROM python:3.7-slim

# Change the working directory
WORKDIR /home/ec2-user/Capstone/

# Copy local folder into the container
COPY app.py app.py
COPY finalized_model_age.pkl finalized_model_age.pkl
COPY finalized_model_gender.pkl finalized_model_gender.pkl
COPY Test_data.csv Test_data.csv
COPY templates/table.html /templates/table.html
COPY requirements.txt requirements.txt

# Install Dependency
RUN pip install -r requirements.txt

# Set "python" as the entry point
ENTRYPOINT ["python"]

# Set the command as the script name
CMD ["app.py"]

#Expose the post 5000.
EXPOSE 5000