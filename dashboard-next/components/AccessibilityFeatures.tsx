import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Settings, Type, Contrast, Volume2, Keyboard } from 'lucide-react';

export const AccessibilityPanel = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [fontSize, setFontSize] = useState(16);
  const [highContrast, setHighContrast] = useState(false);
  const [screenReader, setScreenReader] = useState(false);

  useEffect(() => {
    document.documentElement.style.fontSize = `${fontSize}px`;
    document.documentElement.classList.toggle('high-contrast', highContrast);
  }, [fontSize, highContrast]);

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="fixed left-4 top-4 z-50 p-3 bg-slate-800/80 backdrop-blur-sm border border-slate-700/50 rounded-full text-slate-300 hover:text-white transition-all"
        aria-label="Accessibility Settings"
      >
        <Settings className="w-5 h-5" />
      </button>

      {isOpen && (
        <motion.div
          initial={{ opacity: 0, x: -300 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -300 }}
          className="fixed left-4 top-16 z-50 w-80 bg-slate-900/95 backdrop-blur-sm border border-slate-700 rounded-2xl p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white">Accessibility</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-slate-400 hover:text-white"
            >
              ×
            </button>
          </div>

          <div className="space-y-6">
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-3">
                <Type className="w-4 h-4" />
                Font Size
              </label>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setFontSize(Math.max(12, fontSize - 2))}
                  className="px-3 py-1 bg-slate-700 text-white rounded"
                >
                  A-
                </button>
                <span className="text-white font-mono">{fontSize}px</span>
                <button
                  onClick={() => setFontSize(Math.min(24, fontSize + 2))}
                  className="px-3 py-1 bg-slate-700 text-white rounded"
                >
                  A+
                </button>
              </div>
            </div>

            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-3">
                <Contrast className="w-4 h-4" />
                High Contrast
              </label>
              <button
                onClick={() => setHighContrast(!highContrast)}
                className={`w-full p-3 rounded-lg border transition-colors ${
                  highContrast
                    ? 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400'
                    : 'bg-slate-800/50 border-slate-700/50 text-slate-300'
                }`}
              >
                {highContrast ? 'Enabled' : 'Disabled'}
              </button>
            </div>

            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-3">
                <Volume2 className="w-4 h-4" />
                Screen Reader Support
              </label>
              <button
                onClick={() => setScreenReader(!screenReader)}
                className={`w-full p-3 rounded-lg border transition-colors ${
                  screenReader
                    ? 'bg-green-500/20 border-green-500/50 text-green-400'
                    : 'bg-slate-800/50 border-slate-700/50 text-slate-300'
                }`}
              >
                {screenReader ? 'Enabled' : 'Disabled'}
              </button>
            </div>

            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-3">
                <Keyboard className="w-4 h-4" />
                Keyboard Navigation
              </label>
              <div className="text-xs text-slate-400 space-y-1">
                <p>• Tab: Navigate elements</p>
                <p>• Enter/Space: Activate</p>
                <p>• Esc: Close modals</p>
                <p>• Arrow keys: Navigate charts</p>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </>
  );
};

export const KeyboardNavigation = () => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Skip navigation
      if (e.key === 'Tab' && e.shiftKey) {
        const skipLink = document.getElementById('skip-to-content');
        if (skipLink) skipLink.focus();
      }

      // Quick navigation
      if (e.altKey) {
        switch (e.key) {
          case '1':
            e.preventDefault();
            document.querySelector('.dashboard-header')?.scrollIntoView();
            break;
          case '2':
            e.preventDefault();
            document.querySelector('.stat-cards')?.scrollIntoView();
            break;
          case '3':
            e.preventDefault();
            document.querySelector('.chart-container')?.scrollIntoView();
            break;
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <a
      id="skip-to-content"
      href="#main-content"
      className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-500 text-white px-4 py-2 rounded-lg z-50"
    >
      Skip to main content
    </a>
  );
};

export const ScreenReaderAnnouncements = ({ message }: { message: string }) => (
  <div
    role="status"
    aria-live="polite"
    aria-atomic="true"
    className="sr-only"
  >
    {message}
  </div>
);
