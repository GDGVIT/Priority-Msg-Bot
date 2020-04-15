FROM rasa/rasa:latest-full

# Check Python Environment
RUN python --version
RUN pip --version

# Set working directory
WORKDIR /app

ADD . .

ENTRYPOINT []

EXPOSE 5005

CMD $(echo "rasa run -p $PORT --debug -m models --credentials credentials.yml --enable-api --log-file out.log --endpoints endpoints.yml" | sed 's/=//')