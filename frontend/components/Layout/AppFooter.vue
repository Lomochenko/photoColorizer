<template>
  <footer class="border-t border-dark-800 bg-dark-900/50 backdrop-blur-lg mt-20">
    <div class="container mx-auto px-4 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Brand -->
        <div class="md:col-span-1">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">PhotoColorizer</h3>
              <p class="text-xs text-dark-400">AI-Powered</p>
            </div>
          </div>
          <p class="text-dark-400 text-sm leading-relaxed">
            Transform your black and white photos into vibrant, colorized memories using advanced deep learning technology.
          </p>
        </div>

        <!-- Features -->
        <div>
          <h4 class="text-white font-semibold mb-4">Features</h4>
          <ul class="space-y-2">
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                AI Colorization
              </a>
            </li>
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                Batch Processing
              </a>
            </li>
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                High Resolution
              </a>
            </li>
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                Custom Parameters
              </a>
            </li>
          </ul>
        </div>

        <!-- Resources -->
        <div>
          <h4 class="text-white font-semibold mb-4">Resources</h4>
          <ul class="space-y-2">
            <li>
              <a href="https://github.com/Lomochenko/photoColorizer" target="_blank" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                Source Code
              </a>
            </li>
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                Documentation
              </a>
            </li>
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                API Reference
              </a>
            </li>
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                Examples
              </a>
            </li>
          </ul>
        </div>

        <!-- Connect -->
        <div>
          <h4 class="text-white font-semibold mb-4">Connect</h4>
          <ul class="space-y-2">
            <li>
              <a href="https://github.com/Lomochenko/photoColorizer" target="_blank" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm flex items-center space-x-2">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                <span>GitHub</span>
              </a>
            </li>
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                Support
              </a>
            </li>
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                Privacy Policy
              </a>
            </li>
            <li>
              <a href="#" class="text-dark-400 hover:text-white transition-colors duration-300 text-sm">
                Terms of Service
              </a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom -->
      <div class="border-t border-dark-800 mt-8 pt-8 flex flex-col md:flex-row items-center justify-between">
        <p class="text-dark-400 text-sm">
          © 2024 PhotoColorizer. Built with advanced AI technology.
        </p>
        <div class="flex items-center space-x-4 mt-4 md:mt-0">
          <span class="text-dark-400 text-sm">Powered by</span>
          <div class="flex items-center space-x-2">
            <div class="w-6 h-6 bg-gradient-to-r from-blue-500 to-purple-500 rounded"></div>
            <span class="text-white text-sm font-semibold">Deep Learning</span>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// No script needed for static footer
</script>