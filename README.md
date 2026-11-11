# OpenShift CI/CD Final Project

A sample Python Flask application demonstrating continuous integration with GitHub Actions and a complete Tekton/OpenShift Pipelines flow.

## Project structure

- `app.py` — Flask application with home and health endpoints.
- `tests/test_app.py` — unit tests using nose.
- `.github/workflows/workflow.yml` — flake8 linting and nose tests in GitHub Actions.
- `.tekton/tasks.yml` — cleanup, git-clone, flake8, nose, buildah, and openshift-client Tasks.
- `.tekton/pipeline.yml` — Pipeline named `oc-pipelines-oc-final`.
- `.tekton/pvc.yml` — 1Gi workspace PVC using storage class `skills-network-learner`.
- `.tekton/pipelinerun.yml` — PipelineRun named `oc-pipelines-oc-green`.
- `k8s/` — OpenShift Deployment, Service, and Route manifests.
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

Pushes and pull requests to `main` run two jobs: flake8 linting and nose unit tests. The latest validated successful run is in the repository's Actions tab.

## Apply the OpenShift Pipeline

Log in to your OpenShift course cluster, select your course project, and run these commands from the repository root:

```bash
oc apply -f .tekton/tasks.yml
oc apply -f .tekton/pvc.yml
oc apply -f .tekton/pipeline.yml
```

The Pipeline uses these ordered tasks:

1. `cleanup`
2. `git-clone`
3. `flake8`
4. `nose`
5. `buildah`
6. `deploy` (uses the `openshift-client` Task)

## Configure permissions and run

The Pipeline's `buildah` Task pushes to the OpenShift internal image registry, and the `openshift-client` Task creates a Deployment, Service, and Route. Give the Pipeline service account the required permissions in the selected project:

```bash
oc policy add-role-to-user system:image-builder -z pipeline
oc policy add-role-to-user edit -z pipeline
```

Set the image URL to the current project's internal registry path, then create the PipelineRun:

```bash
PROJECT=$(oc project -q)
IMAGE_URL=image-registry.openshift-image-registry.svc:5000/$PROJECT/openshift-cicd-app:latest
sed -i "s|YOUR_PROJECT|$PROJECT|g" .tekton/pipelinerun.yml
sed -i "s|image-registry.openshift-image-registry.svc:5000/$PROJECT/openshift-cicd-app:latest|$IMAGE_URL|g" .tekton/pipelinerun.yml
oc apply -f .tekton/pipelinerun.yml
oc get pipelinerun oc-pipelines-oc-green
oc get tasks
oc get pods
oc get route openshift-cicd-app
```

If your course namespace does not allow the Pipeline service account to push images or deploy workloads, ask the course administrator to grant the appropriate permissions. Some clusters may also restrict Buildah execution; use the cluster's approved Buildah Task/SCC configuration if required.

## Application logs

After the PipelineRun succeeds:

```bash
oc logs deployment/openshift-cicd-app --all-containers=true
```

Use the Route shown by `oc get route openshift-cicd-app` to test the app and its `/health` endpoint.

## Evidence checklist

- [ ] README URL
- [ ] `.github/workflows/workflow.yml` URL
- [ ] `.tekton/tasks.yml` URL
- [ ] Screenshot of PVC details (save as `oc-pipelines-console-pvc-details.png`)
- [ ] Successful GitHub Actions terminal output
- [ ] Screenshot of Pipeline `oc-pipelines-oc-final` details, showing cleanup, git-clone, flake8, nose, buildah, and deploy
- [ ] Screenshot of successful PipelineRun `oc-pipelines-oc-green`
- [ ] OpenShift application logs

OpenShift screenshots and application logs must be captured from your real course cluster; they are not fabricated by this repository.
