import { memo } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@terminal-v/ui-kit'
import type { MacroEconData } from '../../types/nexus'

interface MacroEconWidgetProps {
  data: MacroEconData | null
}

export const MacroEconWidget = memo(function MacroEconWidget({
  data,
}: MacroEconWidgetProps) {
  if (!data) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle className="font-mono uppercase">MACRO_ECON</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-brand-text-muted">Loading...</div>
        </CardContent>
      </Card>
    )
  }

  const indicators = [
    { label: 'GDP GROWTH', value: data.gdp_growth, suffix: '%', color: 'text-brand-text-primary' },
    { label: 'INFLATION', value: data.inflation_rate, suffix: '%', color: 'text-yellow-500' },
    { label: 'UNEMPLOYMENT', value: data.unemployment_rate, suffix: '%', color: 'text-red-500' },
    { label: 'INTEREST RATE', value: data.interest_rate, suffix: '%', color: 'text-blue-500' },
  ]

  return (
    <Card className="h-full hover:border-brand-accent transition-colors">
      <CardHeader>
        <CardTitle className="font-mono uppercase text-sm">
          MACRO_ECON | {data.region}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          {indicators.map((indicator) => (
            <div key={indicator.label} className="space-y-1">
              <div className="text-xs text-brand-text-muted uppercase font-mono">
                {indicator.label}
              </div>
              <div className={`text-xl font-bold font-mono ${indicator.color}`}>
                {indicator.value !== null 
                  ? `${indicator.value.toFixed(2)}${indicator.suffix}`
                  : 'N/A'
                }
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
})
