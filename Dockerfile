# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the setup script and other necessary files
COPY . .

# Make sure the setup script is executable
RUN chmod +x setup.sh

# Run the setup script to install dependencies
RUN ./setup.sh

# Expose the port for the Gradio app
EXPOSE 7860 

# Define the command to run your application
CMD ["python", "-m", "src.chatbot"]