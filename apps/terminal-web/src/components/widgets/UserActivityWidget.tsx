import { memo } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@terminal-v/ui-kit'
import type { UserActivityData } from '../../types/nexus'

interface UserActivityWidgetProps {
  data: UserActivityData | null
}

export const UserActivityWidget = memo(function UserActivityWidget({
  data,
}: UserActivityWidgetProps) {
  if (!data) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle className="font-mono uppercase">USER_ACTIVITY</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-brand-text-muted">Loading...</div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="h-full hover:border-brand-accent transition-colors">
      <CardHeader>
        <CardTitle className="font-mono uppercase text-sm">
          USER_ACTIVITY
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-xs text-brand-text-muted uppercase font-mono mb-1">
              ACTIVE USERS
            </div>
            <div className="text-2xl font-bold font-mono text-brand-text-primary">
              {data.active_users.toLocaleString('en-US')}
            </div>
          </div>
          
          <div>
            <div className="text-xs text-brand-text-muted uppercase font-mono mb-1">
              TX 24H
            </div>
            <div className="text-2xl font-bold font-mono text-brand-text-primary">
              {data.transactions_24h.toLocaleString('en-US')}
            </div>
          </div>
        </div>

        <div>
          <div className="text-xs text-brand-text-muted uppercase font-mono mb-1">
            VOLUME 24H
          </div>
          <div className="text-xl font-bold font-mono text-brand-text-primary">
            ${data.total_volume_24h.toLocaleString('en-US', { 
              minimumFractionDigits: 0, 
              maximumFractionDigits: 0 
            })}
          </div>
        </div>

        {data.top_symbols.length > 0 && (
          <div>
            <div className="text-xs text-brand-text-muted uppercase font-mono mb-2">
              TOP SYMBOLS
            </div>
            <div className="flex flex-wrap gap-2">
              {data.top_symbols.map((symbol, idx) => (
                <span
                  key={idx}
                  className="px-2 py-1 bg-brand-border rounded text-xs font-mono text-brand-text-secondary"
                >
                  {symbol}
                </span>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
})
