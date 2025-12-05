# 🚀 Modern Sentiment Dashboard

Dashboard modern dengan Next.js 14, TypeScript, Tailwind CSS, dan Framer Motion.

## 🛠 Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS** (Styling modern)
- **Framer Motion** (Animasi smooth)
- **Recharts** (Visualisasi interaktif)
- **Lucide React** (Icons)

## 📦 Installation

```bash
cd dashboard-next

# Install dependencies
npm install

# Run development server
npm run dev
```

Dashboard akan berjalan di: **http://localhost:3000**

## ✨ Features

- ✅ Modern UI dengan gradient & shadows
- ✅ Smooth animations (Framer Motion)
- ✅ Interactive charts (Recharts)
- ✅ Responsive design
- ✅ Dark mode ready
- ✅ Real-time data updates
- ✅ TypeScript untuk type safety

## 🎨 Components

- **StatCard**: Kartu statistik dengan icon & trend
- **SentimentChart**: Bar chart kategori sentimen
- **TrendChart**: Pie chart distribusi sentimen
- **HeatmapChart**: Heatmap aktivitas per hari/jam
- **FilterPanel**: Panel filter interaktif

## 🔗 Integration dengan Python Backend

Untuk koneksi dengan model ML Python:

1. Jalankan FastAPI backend (port 8000)
2. Update API endpoint di `app/api/sentiment-data/route.ts`
3. Fetch data dari Python model

## 📊 Production Build

```bash
npm run build
npm start
```

## 🎯 Next Steps

1. Integrasikan dengan FastAPI backend
2. Tambahkan real-time WebSocket
3. Implementasi filter advanced
4. Deploy ke Vercel/AWS
