---
name: Streamlit Python App Setup
description: How to set up a Python/Streamlit app in this pnpm monorepo — artifact registration, packages, and workflow.
---

## Rule

`createArtifact()` does NOT support Python/Streamlit — only expo, react-vite, data-visualization, mockup-sandbox, slides, video-js. For Streamlit, skip createArtifact and go directly to:

1. Write all Python files under `artifacts/<slug>/`
2. Install packages via `installLanguagePackages({ language: "python", packages: [...] })`
3. Register the workflow via `configureWorkflow({ name: "...", command: "cd artifacts/<slug> && streamlit run app.py --server.port=5000 --server.address=0.0.0.0 --server.headless=true", waitForPort: 5000, outputType: "webview" })`

**Why:** The artifact system only bootstraps JS/TS project types. Python apps are standalone directories managed via the workflow system.

**How to apply:** Any time a user asks for a Python/Streamlit app, skip createArtifact entirely.

## Port

Port 5000 is a valid supported port for Streamlit in this environment.

## Package install note

`pip` is not available directly in the NixOS shell. Always use `installLanguagePackages({ language: "python", ... })` from the code_execution sandbox.

## sys.path pattern

Pages in `pages/` subdirectory need `sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))` at the top of each file to import from `utils/` and `data/` relative to the app root.
