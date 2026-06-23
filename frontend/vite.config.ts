import { defineConfig, type PluginOption } from 'vite'
import vue from '@vitejs/plugin-vue'

// Default to the compose service name so the dockerised dev server can reach the
// backend container. Override with VITE_API_PROXY_TARGET for other setups
// (e.g. http://localhost:8000 when running the API on the host).
const proxyTarget = process.env.VITE_API_PROXY_TARGET ?? 'http://backend-dev:8000'

export default defineConfig(async ({ command }) => {
  const plugins: PluginOption[] = [vue()]

  // Vue DevTools — adds the on-screen floating DevTools panel during development.
  // Only loaded for the dev server (not production builds), and imported lazily so
  // the dev server still starts if the dependency has not been installed yet.
  if (command === 'serve') {
    try {
      const { default: vueDevTools } = await import('vite-plugin-vue-devtools')
      plugins.push(vueDevTools())
    } catch {
      console.warn(
        '[vite] vite-plugin-vue-devtools not installed — run `npm install` to enable on-screen Vue DevTools.',
      )
    }
  }

  return {
    plugins,
    server: {
      host: true,
      // Poll the filesystem so file changes are detected across Docker bind
      // mounts (inotify events are not always propagated into the container),
      // which keeps HMR / auto-reload working reliably in the dev container.
      watch: {
        usePolling: true,
        interval: 300,
      },
      proxy: {
        '/api': {
          target: proxyTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  }
})
