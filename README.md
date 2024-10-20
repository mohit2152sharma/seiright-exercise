# seiright-exercise

## API Server

### Starting the webserver

- To start the webserver, you will two environment variables. `SECRET_KEY` and `ALGORITHM`. Use the following snippet of code before starting the server:

  ```bash
  export SECRET_KEY=$(openssl rand -hex 32)
  export ALGORITHM=HS256
  ```

- [ ] Web app
- [ ] Include terraform code to create kube cluster
- [ ] Deployment to kubernetes cluster
- [ ] Test cases for webapp

## LLM

- [ ] LLM server, llm agnostic
- [ ] evaluate LLM response by comparing with other LLMs
