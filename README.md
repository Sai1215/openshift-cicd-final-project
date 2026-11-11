# OpenShift CI/CD Final Project

A sample Python application demonstrating continuous integration with GitHub Actions and a Tekton pipeline for OpenShift Pipelines.

## Project structure

- `app.py` — Flask application with home and health endpoints.
- `tests/test_app.py` — unit tests using nose.
- `.github/workflows/workflow.yml` — flake8 linting and nose tests.
- `.tekton/tasks.yml` — cleanup, Git clone, and nose tasks.
- `.tekton/pipeline.yml` — Pipeline named `oc-pipelines-oc-final`.
- `.tekton/pvc.yml` — 1 GiB workspace PVC.
- `.tekton/pipelinerun.yml` — PipelineRun named `oc-pipelines-oc-green`.
- `Dockerfile` — container image for the Flask application.

## Run locally

```bash
python -m pip install -r requirements.txt
flake8 app.py tests
PYTHONPATH=. nosetests -v
python app.py
```

The application listens on port 8080. Visit `/health` for its health response.

## GitHub Actions

Pushes and pull requests to `main` run two jobs: flake8 linting and nose unit tests. The latest successful run is available from the repository's Actions tab.

## Deploy the Tekton pipeline to OpenShift

Run these commands from the repository root after logging in to your course OpenShift cluster and selecting the correct project:

```bash
oc apply -f .tekton/tasks.yml
oc apply -f .tekton/pvc.yml
oc apply -f .tekton/pipeline.yml
oc apply -f .tekton/pipelinerun.yml
oc get pvc
oc get pipelines
oc get pipelineruns
```

The PipelineRun uses the PVC `oc-pipelines-source-pvc`. If your cluster requires a specific storage class or a different access mode, edit `.tekton/pvc.yml` to match the course cluster before applying it.

## Deploy the sample application and view logs

The Dockerfile can be used with an OpenShift binary build:

```bash
oc new-build --name=openshift-cicd-app --strategy=docker --binary
oc start-build openshift-cicd-app --from-dir=. --follow
oc new-app openshift-cicd-app
oc expose service/openshift-cicd-app
oc get routes
oc logs deployment/openshift-cicd-app --follow
```

Use the route returned by `oc get routes` to check the application. The health endpoint is `/health`.

## Evidence checklist

- [ ] README URL
- [ ] `.github/workflows/workflow.yml` URL
- [ ] `.tekton/tasks.yml` URL
- [ ] Screenshot of PVC details (save as `oc-pipelines-console-pvc-details`)
- [ ] Text terminal output for successful GitHub Actions run
- [ ] Screenshot of Pipeline `oc-pipelines-oc-final` details
- [ ] Screenshot of successful PipelineRun `oc-pipelines-oc-green`
- [ ] OpenShift application logs

OpenShift screenshots and application logs must be collected from the real course cluster; they are not fabricated by this repository.
