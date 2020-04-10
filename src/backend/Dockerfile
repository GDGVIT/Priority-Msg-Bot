FROM rasa/rasa:latest-full

# Check Python Environment
RUN python --version
RUN pip --version

# Set working directory
WORKDIR /app

ADD . .

ENTRYPOINT []

EXPOSE 5005

CMD $(echo "rasa run -p $PORT --debug --enable-api" | sed 's/=//')