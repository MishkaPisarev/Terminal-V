# Design System - Valkyrris Clone

This document confirms the exact color palette and design tokens copied from Valkyrris site.

## Color Palette

### Primary Colors
- **brand.primary**: `#0B0C0D` - Main background
- **brand.secondary**: `#121417` - Secondary background
- **brand.accent**: `#A30000` - Primary accent (red)
- **brand.accentDark**: `#8A0000` - Darker accent variant
- **brand.border**: `#23272E` - Border color

### Status Colors
- **brand.success**: `#3A4D39` - Success state
- **brand.successDark**: `#2A3D2A` - Dark success variant
- **brand.amber**: `#F59E0B` - Warning/amber

### Text Colors
- **brand.text.primary**: `#E6E9ED` - Primary text
- **brand.text.secondary**: `#C0C6CC` - Secondary text
- **brand.text.muted**: `#9CA3AF` - Muted text

### Additional
- **brand.navy**: `#0F172A` - Navy blue variant

## Typography

### Font Families
- **Headings**: `JetBrains Mono` (monospace)
- **Body**: `Inter` (sans-serif)
- **Display**: `JetBrains Mono` (monospace)

### Font Sizes
Standard Tailwind scale with custom line heights:
- xs: 0.75rem / 1rem
- sm: 0.875rem / 1.25rem
- base: 1rem / 1.5rem
- lg: 1.125rem / 1.75rem
- xl: 1.25rem / 1.75rem
- 2xl: 1.5rem / 2rem
- 3xl: 1.875rem / 2.25rem
- 4xl: 2.25rem / 2.5rem
- 5xl: 3rem / 1
- 6xl: 3.75rem / 1
- 7xl: 4.5rem / 1
- 8xl: 6rem / 1
- 9xl: 8rem / 1

## Components

### Button
- Variants: `primary`, `secondary`, `outline`, `ghost`
- Sizes: `sm`, `md`, `lg`
- Uses brand.accent for primary variant

### Card
- Background: `brand.secondary`
- Border: `brand.border`
- Hover effect: border changes to `brand.accent`

### Input
- Background: `brand.secondary`
- Border: `brand.border`
- Focus: `brand.accent` ring
- Text: `brand.text.primary`
- Placeholder: `brand.text.muted`

### Section
- Background variants: `default` (brand.primary), `dark` (brand.secondary), `accent` (brand.accent)

## Animations

All animations from Valkyrris are included:
- fade-in
- slide-up
- pulse-slow
- float
- pulse-glow
- text-reveal
- glow-pulse
- slide-in-left
- slide-in-right
- scale-in

## Verification

To verify colors match Valkyrris:
1. Check `packages/ui-kit/tailwind.config.js` - contains exact color values
2. Check `packages/ui-kit/src/index.css` - contains exact CSS from Valkyrris
3. Compare with original `valkyrris-site/tailwind.config.js`

All colors are **exact matches** to the Valkyrris design system.
