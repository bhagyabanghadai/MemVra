import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { IncomingMessage, ServerResponse } from 'http'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    {
      name: 'security-headers',
      configureServer(server) {
        server.middlewares.use((_req: IncomingMessage, res: ServerResponse, next: () => void) => {
          // Prevent clickjacking
          res.setHeader('X-Frame-Options', 'DENY');

          // Prevent MIME sniffing
          res.setHeader('X-Content-Type-Options', 'nosniff');

          // XSS Protection (legacy but still good)
          res.setHeader('X-XSS-Protection', '1; mode=block');

          // Referrer Policy
          res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

          // Content Security Policy
          res.setHeader('Content-Security-Policy',
            "default-src 'self'; " +
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; " + // Vite needs unsafe-eval in dev
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
            "img-src 'self' data: blob: https://grainy-gradients.vercel.app https://api.dicebear.com; " +
            "font-src 'self' https://fonts.gstatic.com; " +
            "connect-src 'self' http://localhost:8080 http://localhost:8000 https://raw.githack.com https://raw.githubusercontent.com; " +
            "frame-ancestors 'none';"
          );

          // Permissions Policy (formerly Feature-Policy)
          res.setHeader('Permissions-Policy',
            'geolocation=(), microphone=(), camera=()'
          );

          next();
        });
      }
    }
  ],
  server: {
    port: 5173,
    proxy: {
      '/v1/logical': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/v1/intuitive': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/v1/stats': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/v1/profile': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/v1': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      }
    }
  }
})
