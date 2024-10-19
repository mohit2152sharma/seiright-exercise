
FROM python:3.11


COPY ./pyproject.toml /pyproject.toml 
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install

COPY ./ /

CMD ["uvicorn", "prediction_service.main:app", "--host", "0.0.0.0", "--port", "80"]
