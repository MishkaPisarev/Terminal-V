import { InputHTMLAttributes, forwardRef } from 'react'
import { cn } from '../lib/utils'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  className?: string
  error?: boolean
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          'flex w-full rounded-lg border bg-brand-secondary px-4 py-2 text-sm',
          'text-brand-text-primary placeholder:text-brand-text-muted',
          'border-brand-border focus:border-brand-accent focus:outline-none',
          'focus:ring-2 focus:ring-brand-accent focus:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'transition-colors',
          error && 'border-red-500 focus:border-red-500 focus:ring-red-500',
          className
        )}
        {...props}
      />
    )
  }
)

Input.displayName = 'Input'
