# Databricks Environment Setup

## Goal

Install the MockERP Python project and its dependencies once in the Databricks
environment instead of running `%pip install` every time a notebook executes.

## Serverless notebook setup

For a standard Serverless notebook:

1. Open the notebook's **Environment** side panel.
2. Add this project directory as a dependency:

   ```text
   /Workspace/Users/<your-databricks-user>/MockERP
   ```

3. Apply the environment and restart Python when Databricks requests it.
4. Run the notebook normally:

   ```python
   from mockerp.generators import generate_entity
   ```

Databricks reads the root `pyproject.toml`, installs `mockerp`, and resolves
`Faker` from the declared dependencies. The notebook should not contain a
repeated `%pip install` command or a `sys.path` modification.

On Serverless, `%pip install` is notebook-scoped and does not create a shared
cluster-level installation. Free Edition does not provide the classic
cluster-library or init-script workflow, so use the Environment panel instead.

## Git Folder Serverless

When the repository is opened as a Databricks Git Folder and Git Folder
Serverless is available, use that mode. The environment is managed from the
`pyproject.toml` at the Git Folder root, so notebooks and Python files in the
same folder share the project environment.

## Jobs

For a Job, configure the project directory or the built wheel as a task
dependency. The Job environment must resolve the same `pyproject.toml`
dependencies before executing the notebook or Python entry point.

## Local development versus Databricks execution

```text
Local development       → pip install -e .
Serverless notebook     → Environment side panel → project directory
Git Folder Serverless   → pyproject.toml at Git Folder root
Production Job          → project wheel or project dependency
```

The generator code remains independent of this installation mechanism. Only
the environment setup changes between local development and Databricks.
