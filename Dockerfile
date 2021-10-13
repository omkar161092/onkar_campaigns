# Create the base image
FROM python:3.7-slim

# Change the working directory
WORKDIR /home/ec2-user/Capstone/

# Install Dependency
RUN pip install pandas scikit-learn flask gunicorn numpy
RUN pip install xgboost==1.4.2
RUN pip install mlxtend==0.19

# Copy local folder into the container
COPY app.py app.py
COPY finalized_model_age.pkl finalized_model_age.pkl
COPY finalized_model_gender.pkl finalized_model_gender.pkl
COPY Test_data.csv Test_data.csv
COPY templates/table.html /templates/table.html


# Set "python" as the entry point
ENTRYPOINT ["python"]

# Set the command as the script name
CMD ["app.py"]

#Expose the post 5000.
EXPOSE 5000