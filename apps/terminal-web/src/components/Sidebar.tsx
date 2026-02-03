import { memo } from 'react'
import { cn } from '@terminal-v/ui-kit'

interface SidebarProps {
  className?: string
}

const navItems = [
  { id: 'market', label: 'MARKET_STREAM', icon: '📈' },
  { id: 'macro', label: 'MACRO_ECON', icon: '🌍' },
  { id: 'sentiment', label: 'NEWS_SENTIMENT', icon: '📰' },
  { id: 'blockchain', label: 'BLOCKCHAIN', icon: '⛓️' },
  { id: 'activity', label: 'USER_ACTIVITY', icon: '👥' },
]

export const Sidebar = memo(function Sidebar({ className }: SidebarProps) {
  return (
    <aside
      className={cn(
        "fixed left-0 top-16 bottom-0 w-64 bg-brand-secondary border-r border-brand-border overflow-y-auto",
        className
      )}
    >
      <nav className="p-4 space-y-2">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={cn(
              "w-full text-left px-4 py-3 rounded-lg transition-all",
              "text-brand-text-secondary hover:text-brand-text-primary",
              "hover:bg-brand-border border border-transparent hover:border-brand-accent/50",
              "font-mono text-sm uppercase tracking-wider"
            )}
            style={{ fontFamily: 'JetBrains Mono' }}
          >
            <span className="mr-3">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  )
})
