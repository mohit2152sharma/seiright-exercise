# seiright-exercise

> [!NOTE]
> The work on prompt is not yet finished. I am still working on improving the prompt. I am planning to include the compliance policy within the system prompt of the llm. Apart from that, rest of the setup is done. The project is written in such a way that once the prompt is finalised, I just need to update the `seiright/core/prompts/system.txt` file and the service will start using the new system prompt.

## WebServer

For developing the api endpoint, I have selected the web framework **_FastAPI_**.

To run the web app:

- I have provided a dockerfile, using which you can create a docker image and run the web app in docker container
- To create the image run `docker build -f Dockerfile -t webapp .`
- To run the web server run `docker run -p 80:8000 -e SECRET_KEY=$SECRET_KEY -e ALGORITHM=$ALGORITHM --name containerName -it webapp`
- To run the server successfully, it requires two environment variable, `SECRET_KEY` and `ALGORITHM`.
- `SECRET_KEY` is your ssl key, which you can generate by running `openssl rand -hex 32`
- `ALGORITHM` you can choose something like `HS256`

In the webserver, I have implemented some basic security, a user needs to be authenticated before he/she can make a successful request. Only those users which are in database (`db.json`) can be authenticated. To authenticate:

- first get your token by running
  ```bash
  curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=monte&password=secret&scope=&client_id=&client_secret='
  ```
- The above endpoint will return a token, which you can copy and use in subsequent requests, as follows

  ```bash
  token=$(curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=monte&password=secret&scope=&client_id=&client_secret=' -s | jq .access_token --raw-output);

  curl -X 'GET' \
  'http://127.0.0.1:8000/check-compliance?url=https://mercury.com' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer ${token}"
  ```

- The endpoint `check-compliance` can be used to check whether a given web page is compliant or not.

  - This endpoint takes a `url` as a parameter.
  - It crawls the given webpage and extracts all the text of the webpage.
  - The text is then sent to LLM (like `openai`), and is checked against a compliance policy.
  - It returns the following response:

  ```python
  class CheckComplianceResponse(BaseModel):
    is_compliant: bool # whether given page is compliant or not
    llm_provider: str # which llm provider was used to check the compliance
    confidence_score: float # confidence score of the compliance
    reason: str # reason for compliance or non-compliance
    user: str # user name
    url: str # url passed by the user
  ```

  - The backend is written in a way such that it makes it easy to switch between LLM Providers.
    - The idea here was to make a LLM agnostic backend, which makes it easy to switch between LLM providers. As you would always want to use the latest state of the art model
    - Another idea that I was planning to explore was to compare LLMs against each other.
      - Let different LLMs generate the response and compare them against each other.

## Other Stuff

- I have also included `pytest` setup and included some basic tests of `utils`.
- I have implemented `ci/cd` for the project using `github actions`.
  - The `ci/cd` runs the `tests` whenever a PR is raised
  - It deploys the project whenever a new `push` is made to the main branch. It builds and pushes the new image to ECR
  - The github action uses cache to speed up the build pipeline.
- I have also included the `terraform` code, which was used to create resources for this project in `aws`. This includes
  - ECR Repository for this project with lifecycle policy attached to it.
  - AWS EKS Cluster for application deployment
