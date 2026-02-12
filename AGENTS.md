# Repository Guidelines

## Project Structure & Module Organization
- `backend/`: Flask API and business logic (`controllers/`, `services/`, `models/`, `utils/`).
- `backend/migrations/`: Alembic schema migrations.
- `frontend/`: React + TypeScript app (`src/components`, `src/pages`, `src/hooks`, `src/store`, `src/tests`).
- `frontend/e2e/`: Playwright end-to-end specs.
- `scripts/`: local CI, health-check, hook, and environment helper scripts.
- `assets/`, `docs/`, and root markdown files: static resources and project documentation.

## Build, Test, and Development Commands
- `uv sync --extra test`: install Python dependencies (including test tools).
- `cd frontend && npm install`: install frontend dependencies.
- `npm run dev`: start full stack with Docker Compose.
- `npm run dev:backend`: run backend locally (`backend/app.py`).
- `npm run dev:frontend`: run frontend Vite dev server.
- `npm run lint`: run backend `flake8` + frontend `eslint`.
- `npm run test`: run backend `pytest` + frontend `vitest`.
- `npm run test:e2e`: run Playwright E2E tests.
- `npm run quick-check`: fast pre-push validation (lint + frontend tests + backend tests).

## Coding Style & Naming Conventions
- Python: 4-space indentation, `snake_case` for functions/modules, `PascalCase` for classes.
- TypeScript/React: component files in `PascalCase.tsx`, hooks as `useX.ts`, utility functions in `camelCase`.
- Keep API interaction in `frontend/src/api/`; avoid scattering request logic across components.
- Prefer small, focused functions and place tests close to the changed domain.

## Testing Guidelines
- Backend uses `pytest` under `backend/tests` with `test_*.py` naming.
- Frontend unit tests use Vitest and Testing Library under `frontend/src/tests` with `*.test.ts(x)`.
- E2E tests use Playwright in `frontend/e2e`; real full-flow tests require a valid `GOOGLE_API_KEY`.
- For each fix/feature, add or update tests and run the smallest relevant suite before full checks.

## Commit & Pull Request Guidelines
- Follow repository history style: `fix: ...`, `feat: ...`, `docs: ...`, `merge: ...`.
- Use concise, imperative commit subjects; keep one logical change per commit.
- PRs should include: change summary, linked issue(s), test evidence, and UI screenshots when applicable.
- Add the CLA statement from `CLA.md` in the PR description or comments.

## Security & Configuration Tips
- Copy `.env.example` to `.env`; never commit secrets or API keys.
- After `.env` changes, restart containers/services to apply new values.
- If runtime behavior differs from `.env`, verify settings configured in the web UI (can override defaults).

## Maintainer Authority
- The user is the primary maintainer of this project.
- Review authority policy: only the user reviews other contributors' changes.
