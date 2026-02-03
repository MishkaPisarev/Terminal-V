import { memo } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@terminal-v/ui-kit'
import type { BlockchainData } from '../../types/nexus'

interface BlockchainWidgetProps {
  data: BlockchainData | null
}

export const BlockchainWidget = memo(function BlockchainWidget({
  data,
}: BlockchainWidgetProps) {
  if (!data) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle className="font-mono uppercase">BLOCKCHAIN</CardTitle>
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
          BLOCKCHAIN | {data.network.toUpperCase()}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="text-xs text-brand-text-muted uppercase font-mono mb-1">
            BLOCK HEIGHT
          </div>
          <div className="text-3xl font-bold font-mono text-brand-text-primary">
            {data.block_height.toLocaleString('en-US')}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-xs text-brand-text-muted uppercase font-mono mb-1">
              TX COUNT
            </div>
            <div className="text-xl font-bold font-mono text-brand-text-primary">
              {data.transaction_count}
            </div>
          </div>
          
          {data.gas_price !== null && (
            <div>
              <div className="text-xs text-brand-text-muted uppercase font-mono mb-1">
                GAS PRICE
              </div>
              <div className="text-xl font-bold font-mono text-brand-text-primary">
                {data.gas_price.toFixed(1)} Gwei
              </div>
            </div>
          )}
        </div>

        {data.hash_rate !== null && (
          <div>
            <div className="text-xs text-brand-text-muted uppercase font-mono mb-1">
              HASH RATE
            </div>
            <div className="text-lg font-mono text-brand-text-primary">
              {data.hash_rate.toFixed(2)} TH/s
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
})
