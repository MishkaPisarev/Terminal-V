# Terminal Web

React/Vite frontend for Terminal-V financial platform.

## Features

- **Real-time Dashboard** - Displays 5 data sources with live updates (10 updates/sec)
- **Optimized Performance** - Uses React.memo and efficient state management for high-frequency updates
- **Valkyrris Design System** - Exact clone of Valkyrris color scheme and typography
- **Responsive Layout** - Header, Sidebar, and Dashboard Grid

## Structure

```
src/
├── components/
│   ├── Header.tsx              # Fixed header matching Valkyrris style
│   ├── Sidebar.tsx             # Navigation sidebar
│   ├── DashboardLayout.tsx     # Main layout wrapper
│   └── widgets/               # 5 data source widgets
│       ├── MarketStreamWidget.tsx
│       ├── MacroEconWidget.tsx
│       ├── NewsSentimentWidget.tsx
│       ├── BlockchainWidget.tsx
│       └── UserActivityWidget.tsx
├── hooks/
│   └── useNexusStream.ts      # Custom hook for Redis stream connection
├── pages/
│   └── Dashboard.tsx         # Main dashboard page
└── types/
    └── nexus.ts               # TypeScript types matching Nexus Engine models
```

## Development

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Build for production
pnpm build
```

## Architecture

### Data Flow

```
Nexus Engine (Redis) → Core API (WebSocket/SSE) → useNexusStream → Dashboard Widgets
```

### Performance Optimizations

1. **React.memo** - All widgets are memoized to prevent unnecessary re-renders
2. **Optimized State Updates** - `useNexusStream` only updates state when data actually changes
3. **Functional Updates** - Uses functional setState to avoid stale closures
4. **Selective Re-renders** - Each widget only re-renders when its specific data changes

### Widget Layout

The dashboard uses a responsive grid:
- **Market Stream** - Price, volume, 24h change
- **Macro Econ** - GDP, inflation, unemployment, interest rates
- **News Sentiment** - Sentiment score, label, keywords, article count
- **Blockchain** - Block height, transactions, gas price, hash rate
- **User Activity** - Active users, transactions, volume, top symbols

## Configuration

The `useNexusStream` hook connects to Core API WebSocket endpoint:

```typescript
const { data, isConnected, error } = useNexusStream({
  apiUrl: 'http://localhost:8000',  // Core API URL
  reconnectInterval: 3000,
  maxReconnectAttempts: 10,
})
```

## Design System

Uses `@terminal-v/ui-kit` package with Valkyrris design language:
- **Colors**: Dark theme (#0B0C0D primary, #A30000 accent)
- **Typography**: JetBrains Mono for headings, Inter for body
- **Components**: Button, Card, Input, Section

## Next Steps

1. **Widget Positions** - Wait for user instructions on specific widget positions
2. **Text Labels** - Wait for user instructions on specific text labels
3. **Core API Integration** - Implement WebSocket endpoint in Core API to proxy Redis stream
