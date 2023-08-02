FROM python:3.11 AS build

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
  pipenv install --system --deploy --ignore-pipfile

FROM python:3.11-slim AS runtime

WORKDIR /code

COPY --from=build /usr/local /usr/local
COPY . .

EXPOSE 3002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3002", "--proxy-headers"]
