"use client";

import { useState } from 'react';
import { Search, Calendar, Settings, Play, Square } from 'lucide-react';

export function DailyAutoSearch() {
  const [isActive, setIsActive] = useState(false);
  const [settings, setSettings] = useState({
    keywords: [
      // Core Timnas
      'timnas sepakbola indonesia', 'garuda sepakbola', 'timnas senior indonesia', 'skuad garuda',
      // Pelatih & Staff
      'shin tae yong', 'pelatih timnas indonesia', 'asisten pelatih garuda',
      // Organisasi
      'pssi', 'federasi sepakbola indonesia', 'ketua pssi', 'exco pssi',
      // Pemain
      'pemain timnas indonesia', 'kapten timnas', 'striker timnas', 'kiper timnas', 'bek timnas',
      // Liga Domestik
      'liga 1 indonesia', 'bri liga 1', 'pemain naturalisasi', 'pemain keturunan',
      // Kompetisi
      'kualifikasi piala dunia 2026', 'aff cup 2024', 'asian cup 2027', 'sea games sepakbola',
      // Ranking & Prestasi
      'fifa ranking indonesia', 'peringkat timnas asia', 'prestasi sepakbola indonesia',
      // Isu Terkini
      'gagal lolos piala dunia', 'evaluasi timnas', 'target timnas 2025', 'program pembinaan',
      // Fasilitas & TC
      'training camp timnas', 'stadion timnas', 'markas latihan garuda',
      // Media & Fans
      'suporter timnas', 'the jakmania', 'aremania timnas', 'bonek timnas'
    ],
    trustedChannels: [
      // Media Resmi
      'PSSI TV', 'Garuda Select', 'Liga 1 Match',
      // Media Nasional
      'Kompas TV', 'Metro TV', 'tvOne', 'CNN Indonesia', 'CNBC Indonesia',
      'detikcom', 'Liputan6', 'Tribunnews', 'Okezone',
      // Media Olahraga
      'Bola.com', 'Goal Indonesia', 'Bolasport', 'Indosport',
      'ESPN Indonesia', 'Supersoccer', 'Football Tribe Indonesia',
      // YouTuber Kredibel
      'Pandit Football', 'Akmal Marhali', 'Rizky Ridho', 'Persija TV'
    ],
    maxVideos: 8,
    maxCommentsPerVideo: 150,
    updateInterval: 30,
    onlyTrustedSources: true,
    dateRange: 3 // days
  });
  const [foundVideos, setFoundVideos] = useState([]);

  const handleStart = () => {
    setIsActive(true);
    // Simulate finding videos
    setTimeout(() => {
      setFoundVideos([
        { id: '1', title: 'PSSI Umumkan Evaluasi Menyeluruh Timnas Sepakbola', comments: 312, date: 'Today' },
        { id: '2', title: 'Pemain Naturalisasi Baru Masuk Skuad Garuda 2025', comments: 267, date: 'Yesterday' },
        { id: '3', title: 'Training Camp Timnas di Eropa Januari 2025', comments: 198, date: '2 days ago' },
        { id: '4', title: 'Suporter Jakmania Dukung Program Pembinaan Timnas', comments: 156, date: 'Today' },
        { id: '5', title: 'Target Timnas Lolos Asian Cup 2027 Setelah Gagal Piala Dunia', comments: 134, date: '3 days ago' }
      ]);
    }, 2000);
  };

  return (
    <div className="glass-card rounded-2xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-white flex items-center gap-2">
          <Calendar className="w-5 h-5 text-cyan-400" />
          Daily Auto Search
        </h3>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${isActive ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
          <span className="text-sm font-mono">{isActive ? 'ACTIVE' : 'INACTIVE'}</span>
        </div>
      </div>

      {/* Settings */}
      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm text-slate-300 mb-2">Keywords</label>
          <input
            type="text"
            value={settings.keywords.join(', ')}
            onChange={(e) => setSettings(prev => ({
              ...prev,
              keywords: e.target.value.split(', ')
            }))}
            className="w-full px-3 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white text-sm"
            placeholder="timnas sepakbola indonesia, shin tae yong, pssi, liga 1"
          />
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm text-slate-300 mb-2">Max Videos</label>
            <select
              value={settings.maxVideos}
              onChange={(e) => setSettings(prev => ({ ...prev, maxVideos: Number(e.target.value) }))}
              className="w-full px-3 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white text-sm"
            >
              {settings.dateRange === 1 && (
                <>
                  <option value={3}>3 videos</option>
                  <option value={5}>5 videos</option>
                </>
              )}
              {settings.dateRange === 3 && (
                <>
                  <option value={5}>5 videos</option>
                  <option value={8}>8 videos (Recommended)</option>
                  <option value={12}>12 videos</option>
                </>
              )}
              {settings.dateRange === 7 && (
                <>
                  <option value={10}>10 videos</option>
                  <option value={15}>15 videos (Recommended)</option>
                  <option value={20}>20 videos</option>
                </>
              )}
              {settings.dateRange === 30 && (
                <>
                  <option value={20}>20 videos</option>
                  <option value={30}>30 videos (Recommended)</option>
                  <option value={50}>50 videos</option>
                </>
              )}
            </select>
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-2">Comments/Video</label>
            <select
              value={settings.maxCommentsPerVideo}
              onChange={(e) => setSettings(prev => ({ ...prev, maxCommentsPerVideo: Number(e.target.value) }))}
              className="w-full px-3 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white text-sm"
            >
              <option value={100}>100 comments</option>
              <option value={150}>150 comments (Recommended)</option>
              <option value={250}>250 comments</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-2">Date Range</label>
            <select
              value={settings.dateRange}
              onChange={(e) => setSettings(prev => ({ ...prev, dateRange: Number(e.target.value) }))}
              className="w-full px-3 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-white text-sm"
            >
              <option value={1}>Per Hari (Today)</option>
              <option value={3}>3 Hari (Recommended)</option>
              <option value={7}>Per Minggu (7 days)</option>
              <option value={30}>Per Bulan (30 days)</option>
            </select>
          </div>
        </div>

        <div className="flex items-center justify-between p-3 bg-slate-800/30 rounded-lg">
          <div>
            <div className="text-sm font-medium text-slate-300">Trusted Sources Only</div>
            <div className="text-xs text-slate-500">Filter hanya channel media terpercaya</div>
          </div>
          <button
            onClick={() => setSettings(prev => ({ ...prev, onlyTrustedSources: !prev.onlyTrustedSources }))}
            className={`relative w-12 h-6 rounded-full transition-colors ${
              settings.onlyTrustedSources ? 'bg-green-600' : 'bg-slate-600'
            }`}
          >
            <div className={`absolute w-5 h-5 bg-white rounded-full top-0.5 transition-transform ${
              settings.onlyTrustedSources ? 'translate-x-6' : 'translate-x-0.5'
            }`} />
          </button>
        </div>
      </div>

      {/* Control Button */}
      <button
        onClick={isActive ? () => setIsActive(false) : handleStart}
        className={`w-full px-4 py-3 rounded-xl font-medium transition-all flex items-center justify-center gap-2 ${
          isActive 
            ? 'bg-red-600 hover:bg-red-700 text-white' 
            : 'bg-green-600 hover:bg-green-700 text-white'
        }`}
      >
        {isActive ? <Square className="w-5 h-5" /> : <Play className="w-5 h-5" />}
        {isActive ? 'Stop Auto Search' : 'Start Daily Search'}
      </button>

      {/* Found Videos */}
      {foundVideos.length > 0 && (
        <div className="mt-6 pt-6 border-t border-slate-700/50">
          <h4 className="text-sm font-medium text-slate-300 mb-3">Today's Videos Found</h4>
          <div className="space-y-2">
            {foundVideos.map((video) => (
              <div key={video.id} className="p-3 bg-slate-800/30 rounded-lg">
                <div className="text-sm text-white mb-1">{video.title}</div>
                <div className="flex justify-between text-xs text-slate-400">
                  <span>{video.comments} comments found</span>
                  <span>{video.date}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
