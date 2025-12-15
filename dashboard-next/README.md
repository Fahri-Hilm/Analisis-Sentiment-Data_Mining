# 🚀 Modern Sentiment Dashboard v5.0

Advanced Next.js dashboard dengan AI sentiment analysis dan smart comment filtering untuk analisis real-time komentar YouTube.

## 🔄 Model Architecture

Dashboard ini menggunakan **dual model system**:

### 📊 **Static Pages (SVM Model)**
- **Main Dashboard** (`/`) - Uses pre-trained SVM on labeled data
- **Analytics** (`/analytics`) - Historical analysis with SVM
- **Dataset** (`/dataset`) - Processed data visualization
- **Model Performance** (`/model`) - SVM training metrics

### 🔴 **Live Pages (Gemini AI)**
- **Live Comments** (`/live-comments`) - Real-time AI analysis
- **Live Analysis** (`/realtime`) - Stream monitoring with AI
- **Real-time APIs** - Gemini AI integration

### 🎯 **Why Dual Models?**
- **SVM**: Perfect for historical, cleaned data analysis
- **Gemini AI**: Ideal for real-time, contextual understanding
- **Complementary**: Each model serves different use cases optimally

- **🤖 Aggressive AI Analysis** - 96% reduction in neutral results
- **🔍 Smart Comment Filter** - AI selects relevant comments only
- **⚡ Real-time Processing** - Live YouTube comment analysis
- **🎯 Indonesian Optimized** - Advanced language processing
- **📊 Interactive Visualizations** - Modern charts and animations

## 🛠 Tech Stack

- **Next.js 14** (App Router) - React framework
- **TypeScript** - Type safety and better DX
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Recharts** - Interactive data visualizations
- **Lucide React** - Modern icon library

## 📦 Installation

```bash
cd dashboard-next

# Install dependencies
npm install

# Run development server
npm run dev
```

Dashboard akan berjalan di: **http://localhost:3000**

## 🎯 Key Pages

### 1. **Main Dashboard** (`/`)
- Overview sentiment statistics
- Real-time data visualization
- Quick access to all features
- Performance metrics display

### 2. **Live Comments** (`/live-comments`)
```typescript
// Features:
✅ Real-time YouTube comment fetching
✅ Smart AI filter toggle
✅ Aggressive sentiment analysis toggle
✅ Individual comment reasoning display
✅ Spam and irrelevant content filtering
```

### 3. **Live Analysis** (`/realtime`)
```typescript
// Features:
✅ Auto-search latest timnas videos
✅ Batch comment processing with AI
✅ Real-time sentiment monitoring
✅ Interactive charts and visualizations
✅ Stream control with start/stop functionality
```

### 4. **Analytics** (`/analytics`)
- Advanced sentiment analytics
- Trend analysis over time
- Performance comparisons
- Export functionality

## 🔧 Components

### **Enhanced StatCard**
```typescript
interface StatCardProps {
  title: string;
  value: number;
  icon: LucideIcon;
  color: string;
  trend?: number;
  confidence?: number;
}
```

### **Smart SentimentChart**
- Real-time data updates
- Interactive tooltips
- Responsive design
- Color-coded sentiment display

### **Advanced FilterPanel**
```typescript
interface FilterPanelProps {
  aiEnabled: boolean;
  filterEnabled: boolean;
  onAiToggle: (enabled: boolean) => void;
  onFilterToggle: (enabled: boolean) => void;
}
```

### **Live Comment Display**
```typescript
interface CommentProps {
  text: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  confidence: number;
  reasoning: string;
  model: string;
  filterReason?: string;
}
```

## 🚀 API Integration

### **Smart Comment Filtering**
```typescript
// Fetch with smart filter
const response = await fetch(
  `/api/live-comments?videoId=${videoId}&sentiment=true&filter=true`
);

// Response structure
interface ApiResponse {
  comments: Comment[];
  total: number;
  filtered: boolean;
  sentimentAnalysis: {
    enabled: boolean;
    model: string;
    summary: Record<string, number>;
    avgConfidence: number;
  };
}
```

### **Real-time Updates**
```typescript
// Auto-refresh with smart filtering
useEffect(() => {
  const interval = setInterval(async () => {
    if (isStreaming) {
      await fetchCommentsWithFilter();
    }
  }, 30000); // 30 seconds
  
  return () => clearInterval(interval);
}, [isStreaming, filterEnabled]);
```

## 🎨 UI/UX Features

### **Modern Design System**
- Glass morphism effects
- Gradient backgrounds
- Smooth animations with Framer Motion
- Responsive grid layouts
- Dark theme optimized

### **Interactive Elements**
```css
/* Glass card effect */
.glass-card {
  @apply bg-slate-900/20 backdrop-blur-xl border border-slate-800/50;
}

/* Gradient text */
.gradient-text {
  @apply bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent;
}
```

### **Smart Toggles**
- AI Analysis toggle with brain icon
- Smart Filter toggle with search icon
- Real-time status indicators
- Loading states with animations

## 📊 Data Visualization

### **Sentiment Distribution**
```typescript
const sentimentData = [
  { name: 'Positive', value: positive, color: '#10b981' },
  { name: 'Negative', value: negative, color: '#ef4444' },
  { name: 'Neutral', value: neutral, color: '#6b7280' }
];
```

### **Real-time Charts**
- Pie charts for sentiment distribution
- Bar charts for emotion analysis
- Line charts for trend analysis
- Heatmaps for activity patterns

## 🔍 Smart Filtering UI

### **Filter Controls**
```typescript
<div className="flex items-center gap-4">
  <div className="flex items-center gap-2">
    <input
      type="checkbox"
      checked={aiEnabled}
      onChange={(e) => setAiEnabled(e.target.checked)}
    />
    <label>🤖 AI Analysis</label>
  </div>
  
  <div className="flex items-center gap-2">
    <input
      type="checkbox"
      checked={filterEnabled}
      onChange={(e) => setFilterEnabled(e.target.checked)}
    />
    <label>🔍 Smart Filter</label>
  </div>
</div>
```

### **Filter Status Display**
```typescript
{filterEnabled && (
  <span className="flex items-center gap-1 text-green-400">
    🔍 Smart Filter Active
  </span>
)}
```

## 🚀 Performance Optimizations

### **Smart Loading**
- Skeleton loading states
- Progressive data loading
- Optimistic UI updates
- Error boundaries

### **Efficient Rendering**
```typescript
// Memoized components
const MemoizedCommentCard = memo(CommentCard);

// Virtualized lists for large datasets
const VirtualizedCommentList = ({ comments }) => {
  return (
    <FixedSizeList
      height={600}
      itemCount={comments.length}
      itemSize={120}
    >
      {({ index, style }) => (
        <div style={style}>
          <MemoizedCommentCard comment={comments[index]} />
        </div>
      )}
    </FixedSizeList>
  );
};
```

## 🔧 Configuration

### **Environment Variables**
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
YOUTUBE_API_KEY=your_youtube_api_key
```

### **TypeScript Configuration**
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

## 📱 Responsive Design

### **Breakpoints**
```css
/* Mobile First */
.container {
  @apply px-4 sm:px-6 lg:px-8;
}

/* Grid Layouts */
.stats-grid {
  @apply grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4;
}

.chart-grid {
  @apply grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6;
}
```

## 🚨 Error Handling

### **Error Boundaries**
```typescript
class SentimentErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### **API Error Handling**
```typescript
const fetchWithRetry = async (url: string, retries = 3) => {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  } catch (error) {
    if (retries > 0) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      return fetchWithRetry(url, retries - 1);
    }
    throw error;
  }
};
```

## 📊 Production Build

```bash
# Build for production
npm run build

# Start production server
npm start

# Analyze bundle size
npm run analyze
```

## 🎯 Next Steps

1. ✅ **Completed**: Smart comment filtering with AI
2. ✅ **Completed**: Aggressive sentiment analysis
3. ✅ **Completed**: Real-time dashboard updates
4. 🔄 **In Progress**: WebSocket real-time updates
5. 📋 **Planned**: Advanced emotion detection
6. 📋 **Planned**: Export functionality
7. 📋 **Planned**: Mobile app companion

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Follow TypeScript and ESLint rules
4. Add tests for new features
5. Update documentation
6. Submit pull request

## 📄 License

This project is licensed under the MIT License.

---

**Dashboard v5.0 - Powered by AI for Indonesian Football Analytics** 🚀⚽
