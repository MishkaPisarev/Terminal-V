import { memo, useMemo } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@terminal-v/ui-kit'
import type { NewsSentimentData } from '../../types/nexus'

interface NewsSentimentWidgetProps {
  data: NewsSentimentData | null
}

export const NewsSentimentWidget = memo(function NewsSentimentWidget({
  data,
}: NewsSentimentWidgetProps) {
  const sentimentColor = useMemo(() => {
    if (!data) return 'text-brand-text-muted'
    if (data.sentiment_score > 0.3) return 'text-green-500'
    if (data.sentiment_score < -0.3) return 'text-red-500'
    return 'text-yellow-500'
  }, [data])

  const sentimentBarWidth = useMemo(() => {
    if (!data) return 50
    // Convert -1 to 1 range to 0-100%
    return ((data.sentiment_score + 1) / 2) * 100
  }, [data])

  if (!data) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle className="font-mono uppercase">NEWS_SENTIMENT</CardTitle>
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
          NEWS_SENTIMENT
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className={`text-2xl font-bold font-mono ${sentimentColor} uppercase`}>
              {data.sentiment_label}
            </div>
            <div className={`text-lg font-mono ${sentimentColor}`}>
              {data.sentiment_score > 0 ? '+' : ''}{data.sentiment_score.toFixed(2)}
            </div>
          </div>
          
          {/* Sentiment Bar */}
          <div className="w-full h-2 bg-brand-border rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-200 ${
                data.sentiment_score > 0.3 
                  ? 'bg-green-500' 
                  : data.sentiment_score < -0.3 
                  ? 'bg-red-500' 
                  : 'bg-yellow-500'
              }`}
              style={{ width: `${sentimentBarWidth}%` }}
            />
          </div>
        </div>

        <div>
          <div className="text-xs text-brand-text-muted uppercase font-mono mb-2">
            ARTICLES ANALYZED
          </div>
          <div className="text-xl font-bold font-mono text-brand-text-primary">
            {data.article_count}
          </div>
        </div>

        {data.keywords.length > 0 && (
          <div>
            <div className="text-xs text-brand-text-muted uppercase font-mono mb-2">
              KEYWORDS
            </div>
            <div className="flex flex-wrap gap-2">
              {data.keywords.slice(0, 5).map((keyword, idx) => (
                <span
                  key={idx}
                  className="px-2 py-1 bg-brand-border rounded text-xs font-mono text-brand-text-secondary"
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
})
