# Terminal-V

High-complexity financial platform demonstrating advanced architecture skills.

## Project Structure

```
Terminal-V/
├── apps/
│   ├── terminal-web/     # React/Vite frontend
│   ├── core-api/         # FastAPI backend
│   └── nexus-engine/     # Python data processing
├── packages/
│   └── ui-kit/           # Shared design system (Valkyrris clone)
└── ARCHITECTURE.md       # System architecture documentation
```

## Quick Start

### Prerequisites

- Node.js 18+
- pnpm 8+
- Python 3.11+
- Poetry (for Python packages)

### Installation

```bash
# Install all dependencies
pnpm install

# Install Python dependencies
cd apps/core-api && poetry install
cd ../nexus-engine && poetry install
```

### Development

```bash
# Start frontend
pnpm --filter terminal-web dev

# Start backend (in separate terminal)
cd apps/core-api
poetry run uvicorn core_api.main:app --reload
```

## Design System

This project uses an exact clone of the Valkyrris design language:

- **Colors**: Dark theme (#0B0C0D primary, #A30000 accent)
- **Typography**: JetBrains Mono for headings, Inter for body
- **Components**: Button, Card, Input, Section from `@terminal-v/ui-kit`

See `ARCHITECTURE.md` for detailed system architecture.
