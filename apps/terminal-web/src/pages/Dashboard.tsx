import { memo } from 'react'
import { DashboardLayout } from '../components/DashboardLayout'
import { useNexusStream } from '../hooks/useNexusStream'
import { MarketStreamWidget } from '../components/widgets/MarketStreamWidget'
import { MacroEconWidget } from '../components/widgets/MacroEconWidget'
import { NewsSentimentWidget } from '../components/widgets/NewsSentimentWidget'
import { BlockchainWidget } from '../components/widgets/BlockchainWidget'
import { UserActivityWidget } from '../components/widgets/UserActivityWidget'

export const Dashboard = memo(function Dashboard() {
  const { data, isConnected, error } = useNexusStream()

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Connection Status */}
        <div className="flex items-center justify-between">
          <h1 
            className="text-3xl font-bold text-brand-text-primary uppercase"
            style={{ fontFamily: 'JetBrains Mono', letterSpacing: '-0.05em' }}
          >
            DASHBOARD
          </h1>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
            <span className="text-sm text-brand-text-secondary font-mono uppercase">
              {isConnected ? 'CONNECTED' : 'DISCONNECTED'}
            </span>
          </div>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500 rounded-lg p-4 space-y-2">
            <div className="text-red-500 font-mono text-sm font-bold">
              ERROR: {error.message}
            </div>
            {(error.message.includes('CORS') || error.message.includes('Backend API')) && (
              <div className="text-yellow-400 font-mono text-xs mt-2 space-y-1">
                <div>💡 To fix this:</div>
                <div>1. Start Core API server: <code className="bg-black/30 px-1 rounded">cd apps/core-api && poetry run uvicorn core_api.main:app --reload</code></div>
                <div>2. Or deploy Core API to production and set VITE_API_URL in GitHub Secrets</div>
                <div>3. Check that API is accessible at: <code className="bg-black/30 px-1 rounded">{import.meta.env.VITE_API_URL || 'http://localhost:8000'}</code></div>
              </div>
            )}
          </div>
        )}

        {/* Widget Grid - 5 widgets */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Market Stream Widget */}
          <div className="lg:col-span-1">
            <MarketStreamWidget data={data?.market_stream ?? null} />
          </div>

          {/* Macro Econ Widget */}
          <div className="lg:col-span-1">
            <MacroEconWidget data={data?.macro_econ ?? null} />
          </div>

          {/* News Sentiment Widget */}
          <div className="lg:col-span-1">
            <NewsSentimentWidget data={data?.news_sentiment ?? null} />
          </div>

          {/* Blockchain Widget */}
          <div className="lg:col-span-1">
            <BlockchainWidget data={data?.blockchain ?? null} />
          </div>

          {/* User Activity Widget */}
          <div className="lg:col-span-2">
            <UserActivityWidget data={data?.user_activity ?? null} />
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
})
