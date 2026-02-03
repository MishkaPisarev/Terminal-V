import { ReactNode } from 'react'
import { cn } from '../lib/utils'

interface SectionProps {
  children: ReactNode
  className?: string
  id?: string
  background?: 'default' | 'dark' | 'accent'
}

export function Section({ 
  children, 
  className, 
  id, 
  background = 'default' 
}: SectionProps) {
  const backgroundClasses = {
    default: 'bg-brand-primary',
    dark: 'bg-brand-secondary',
    accent: 'bg-brand-accent'
  }

  return (
    <section 
      id={id}
      className={cn(
        'py-20 lg:py-32',
        backgroundClasses[background],
        className
      )}
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {children}
      </div>
    </section>
  )
}
