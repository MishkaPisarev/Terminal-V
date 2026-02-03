import { memo, useMemo } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@terminal-v/ui-kit'
import type { MarketStreamData } from '../../types/nexus'

interface MarketStreamWidgetProps {
  data: MarketStreamData | null
}

export const MarketStreamWidget = memo(function MarketStreamWidget({
  data,
}: MarketStreamWidgetProps) {
  const changeColor = useMemo(() => {
    if (!data) return 'text-brand-text-muted'
    return data.change_24h >= 0 
      ? 'text-green-500' 
      : 'text-red-500'
  }, [data?.change_24h])

  const changeSymbol = useMemo(() => {
    if (!data) return ''
    return data.change_24h >= 0 ? '↑' : '↓'
  }, [data?.change_24h])

  if (!data) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle className="font-mono uppercase">MARKET_STREAM</CardTitle>
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
          MARKET_STREAM
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="text-2xl font-bold text-brand-text-primary font-mono mb-1">
            {data.symbol}
          </div>
          <div className="text-3xl font-bold text-brand-text-primary font-mono">
            ${data.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div>
            <div className="text-xs text-brand-text-muted uppercase font-mono mb-1">
              24H CHANGE
            </div>
            <div className={`text-lg font-bold font-mono ${changeColor}`}>
              {changeSymbol} {Math.abs(data.change_24h).toFixed(2)}%
            </div>
          </div>
          <div>
            <div className="text-xs text-brand-text-muted uppercase font-mono mb-1">
              VOLUME
            </div>
            <div className="text-lg font-mono text-brand-text-primary">
              {data.volume.toLocaleString('en-US', { maximumFractionDigits: 0 })}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
})
