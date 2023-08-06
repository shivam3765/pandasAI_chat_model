FROM python:3.11.4
ARG APP_HOME=/opt/deployment
ARG PROJECT_NAME="cg-principal-assitant"
ENV APP_HOME=${APP_HOME} \
    PROJECT_NAME=${PROJECT_NAME} \
    PROJECT_HOME=${APP_HOME}/${PROJECT_NAME}
COPY src/ ${PROJECT_HOME}/src
ADD ./requirements.txt /
RUN pip install --no-cache-dir --upgrade -r requirements.txt
WORKDIR ${PROJECT_HOME}/src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]