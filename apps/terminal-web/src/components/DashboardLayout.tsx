import { ReactNode } from 'react'
import { Header } from './Header'
import { Sidebar } from './Sidebar'
import { cn } from '@terminal-v/ui-kit'

interface DashboardLayoutProps {
  children: ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-brand-primary">
      <Header />
      <Sidebar />
      <main 
        className={cn(
          "pt-16 pl-64 min-h-screen",
          "transition-all duration-300"
        )}
      >
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  )
}
