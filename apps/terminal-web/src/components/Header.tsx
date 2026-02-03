import { memo } from 'react'
import { cn } from '@terminal-v/ui-kit'

interface HeaderProps {
  className?: string
}

export const Header = memo(function Header({ className }: HeaderProps) {
  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 bg-brand-secondary/95 backdrop-blur-sm border-b border-brand-border transition-transform duration-300",
        className
      )}
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <span 
              className="text-xl font-bold text-brand-text-primary tracking-wider uppercase"
              style={{ fontFamily: 'JetBrains Mono', letterSpacing: '-0.05em' }}
            >
              TERMINAL-V
            </span>
          </div>

          {/* Status Indicator */}
          <div className="hidden md:flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-brand-accent animate-pulse"></div>
              <span className="text-sm text-brand-text-secondary font-mono">LIVE</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
})
