"use client";

import { useState } from 'react';
import { Settings, Save, RefreshCw, Key, Clock, Filter, Bell } from 'lucide-react';

export default function RealtimeSettings() {
  const [settings, setSettings] = useState({
    apiKey: '',
    refreshInterval: 30,
    maxComments: 1000,
    autoStop: true,
    notifications: true,
    filterSpam: true,
    minConfidence: 0.7
  });

  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // Simulate save
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const SettingCard = ({ title, description, children }: any) => (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        <p className="text-sm text-slate-400">{description}</p>
      </div>
      {children}
    </div>
  );

  return (
    <div className="min-h-screen p-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2 font-mono">⚙️ Stream Settings</h1>
          <p className="text-slate-400">Configure real-time analysis parameters</p>
        </div>
        <button
          onClick={handleSave}
          className={`px-6 py-3 rounded-xl font-medium transition-all flex items-center gap-2 ${
            saved 
              ? 'bg-green-600 text-white' 
              : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
        >
          <Save className="w-5 h-5" />
          {saved ? 'Saved!' : 'Save Settings'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* API Configuration */}
        <SettingCard
          title="API Configuration"
          description="Configure YouTube Data API settings"
        >
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
                <Key className="w-4 h-4" />
                YouTube API Key
              </label>
              <input
                type="password"
                value={settings.apiKey}
                onChange={(e) => setSettings({...settings, apiKey: e.target.value})}
                placeholder="Enter your YouTube Data API key"
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
                <RefreshCw className="w-4 h-4" />
                Refresh Interval (seconds)
              </label>
              <input
                type="number"
                value={settings.refreshInterval}
                onChange={(e) => setSettings({...settings, refreshInterval: parseInt(e.target.value)})}
                min="10"
                max="300"
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all"
              />
            </div>
          </div>
        </SettingCard>

        {/* Stream Limits */}
        <SettingCard
          title="Stream Limits"
          description="Set limits to manage resource usage"
        >
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Maximum Comments per Session
              </label>
              <input
                type="number"
                value={settings.maxComments}
                onChange={(e) => setSettings({...settings, maxComments: parseInt(e.target.value)})}
                min="100"
                max="10000"
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all"
              />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <label className="block text-sm font-medium text-slate-300">Auto-stop after 1 hour</label>
                <p className="text-xs text-slate-500">Automatically stop streaming after 1 hour</p>
              </div>
              <button
                onClick={() => setSettings({...settings, autoStop: !settings.autoStop})}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.autoStop ? 'bg-cyan-600' : 'bg-slate-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.autoStop ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        </SettingCard>

        {/* Analysis Settings */}
        <SettingCard
          title="Analysis Settings"
          description="Configure sentiment analysis parameters"
        >
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Minimum Confidence Threshold
              </label>
              <input
                type="range"
                min="0.5"
                max="1"
                step="0.1"
                value={settings.minConfidence}
                onChange={(e) => setSettings({...settings, minConfidence: parseFloat(e.target.value)})}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-xs text-slate-400 mt-1">
                <span>0.5</span>
                <span className="text-cyan-400">{settings.minConfidence}</span>
                <span>1.0</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <label className="block text-sm font-medium text-slate-300 flex items-center gap-2">
                  <Filter className="w-4 h-4" />
                  Filter Spam Comments
                </label>
                <p className="text-xs text-slate-500">Automatically filter out spam and low-quality comments</p>
              </div>
              <button
                onClick={() => setSettings({...settings, filterSpam: !settings.filterSpam})}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.filterSpam ? 'bg-cyan-600' : 'bg-slate-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.filterSpam ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        </SettingCard>

        {/* Notifications */}
        <SettingCard
          title="Notifications"
          description="Configure alerts and notifications"
        >
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="block text-sm font-medium text-slate-300 flex items-center gap-2">
                  <Bell className="w-4 h-4" />
                  Enable Notifications
                </label>
                <p className="text-xs text-slate-500">Get notified about important events</p>
              </div>
              <button
                onClick={() => setSettings({...settings, notifications: !settings.notifications})}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.notifications ? 'bg-cyan-600' : 'bg-slate-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.notifications ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
            
            {settings.notifications && (
              <div className="ml-6 space-y-3 border-l-2 border-slate-700 pl-4">
                <div className="flex items-center gap-3">
                  <input type="checkbox" defaultChecked className="rounded" />
                  <span className="text-sm text-slate-300">Sentiment spikes</span>
                </div>
                <div className="flex items-center gap-3">
                  <input type="checkbox" defaultChecked className="rounded" />
                  <span className="text-sm text-slate-300">Stream errors</span>
                </div>
                <div className="flex items-center gap-3">
                  <input type="checkbox" className="rounded" />
                  <span className="text-sm text-slate-300">Daily summaries</span>
                </div>
              </div>
            )}
          </div>
        </SettingCard>
      </div>

      {/* Current Status */}
      <div className="glass-card rounded-2xl p-6 border border-slate-800/50 bg-slate-900/20 backdrop-blur-xl">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Settings className="w-5 h-5 text-cyan-400" />
          Current Configuration
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <p className="text-2xl font-bold text-cyan-400">{settings.refreshInterval}s</p>
            <p className="text-sm text-slate-400">Refresh Interval</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-cyan-400">{settings.maxComments}</p>
            <p className="text-sm text-slate-400">Max Comments</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-cyan-400">{(settings.minConfidence * 100).toFixed(0)}%</p>
            <p className="text-sm text-slate-400">Min Confidence</p>
          </div>
        </div>
      </div>
    </div>
  );
}
