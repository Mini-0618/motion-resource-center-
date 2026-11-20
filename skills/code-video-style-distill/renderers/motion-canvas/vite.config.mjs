// plain Vite build of the Motion Canvas scene (no editor UI); JSX goes through Motion Canvas' own runtime.
export default {
  base: './',
  esbuild: {jsx: 'automatic', jsxImportSource: '@motion-canvas/2d/lib'},
  build: {outDir: 'dist', target: 'esnext', emptyOutDir: true, chunkSizeWarningLimit: 4000},
  logLevel: 'warn',
};
