import { defineConfig } from 'tsup'
import { copyFileSync } from 'fs'
import { join } from 'path'

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  splitting: false,
  sourcemap: true,
  clean: true,
  external: ['react', 'react-dom'],
  onSuccess: () => {
    // Copy CSS file to dist after build
    try {
      copyFileSync(
        join(process.cwd(), 'src', 'index.css'),
        join(process.cwd(), 'dist', 'styles.css')
      )
    } catch (err) {
      console.error('Failed to copy CSS file:', err)
    }
  },
})
