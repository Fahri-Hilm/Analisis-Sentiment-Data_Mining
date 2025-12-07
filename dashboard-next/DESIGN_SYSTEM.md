# 🎨 Garuda Elegant Design System

Design system yang **elegan, berkelas, dan ringan** untuk dashboard Garuda.

## 🎯 Design Principles

1. **Elegance First** - Subtle details, refined typography, premium feel
2. **Performance** - CSS-only animations, minimal JS overhead
3. **Consistency** - Unified spacing, colors, and interactions
4. **Accessibility** - WCAG 2.1 AA compliant

---

## 🎨 Color Palette

### Primary Colors
```css
Blue Primary:   #3b82f6  /* Main brand color */
Blue Light:     #60a5fa  /* Hover states */
Blue Dark:      #2563eb  /* Active states */
Cyan Accent:    #06b6d4  /* Secondary accent */
```

### Sentiment Colors
```css
Positive:       #10b981  /* Emerald-500 */
Negative:       #ef4444  /* Red-500 */
Neutral:        #6b7280  /* Gray-500 */
```

### Neutral Palette
```css
Background:     #0f172a  /* Slate-900 */
Card:           rgba(15, 23, 42, 0.6)  /* Glass effect */
Border:         #334155  /* Slate-700 */
Text Primary:   #f1f5f9  /* Slate-100 */
Text Muted:     #94a3b8  /* Slate-400 */
```

---

## 📝 Typography

### Font Stack
```css
Sans-serif: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
Monospace:  'JetBrains Mono', monospace
```

### Type Scale
```tsx
// Headings
<h1 className="heading-xl">   {/* 48px, bold, -0.025em */}
<h2 className="heading-lg">   {/* 30px, semibold, -0.02em */}
<h3 className="heading-md">   {/* 20px, semibold, -0.015em */}

// Body
<p className="text-base">     {/* 16px, normal */}
<p className="text-muted">    {/* 14px, slate-400 */}

// Stats
<div className="stat-number"> {/* 36px, bold, tabular-nums */}
```

---

## 🎴 Components

### Glass Card
```tsx
<div className="glass-card">
  {/* Premium glass effect with backdrop blur */}
</div>
```

**Features:**
- Backdrop blur: 2xl (40px)
- Border: slate-800/50
- Hover: Lift effect (-2px translateY)
- Shadow: Subtle depth

### Elegant Card
```tsx
<div className="elegant-card">
  {/* Glass card + padding + subtle inset shadow */}
</div>
```

**Use for:** Stat cards, info panels, content blocks

### Premium Button
```tsx
<button className="btn-premium">
  Click Me
</button>
```

**Features:**
- Gradient: Blue-600 → Blue-700
- Shadow: Blue-900/30
- Hover: Scale 1.02 + shadow lift
- Active: Scale 0.98

### Badge Elegant
```tsx
<span className="badge-elegant">
  Label
</span>
```

**Use for:** Tags, categories, status indicators

---

## 🎭 Animations

### CSS-Only (Lightweight)

```tsx
// Fade in
<div className="animate-fade-in">

// Slide up
<div className="animate-slide-up">

// Scale in
<div className="animate-scale-in">

// Float (continuous)
<div className="animate-float">

// Shimmer (loading)
<div className="animate-shimmer">
```

### Transitions
```tsx
// Smooth transition (300ms cubic-bezier)
<div className="transition-smooth">
```

---

## 🎨 Utilities

### Gradient Text
```tsx
<h1 className="text-gradient">
  Elegant Gradient
</h1>

<h1 className="text-gradient-primary">
  Blue Gradient
</h1>
```

### Scrollbar
```tsx
// Elegant scrollbar
<div className="scrollbar-elegant overflow-auto">

// Hide scrollbar
<div className="no-scrollbar overflow-auto">
```

### Divider
```tsx
<div className="divider-elegant" />
```

### Focus Ring
```tsx
<button className="focus-ring-elegant">
  Accessible Button
</button>
```

---

## 📐 Spacing System

```css
/* Tailwind default + custom */
4px   → space-1
8px   → space-2
12px  → space-3
16px  → space-4
20px  → space-5
24px  → space-6
32px  → space-8
72px  → space-18  /* Custom */
352px → space-88  /* Custom */
```

---

## 🎯 Usage Examples

### Stat Card
```tsx
<div className="elegant-card group">
  <div className="flex items-start justify-between mb-5">
    <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500/10 to-cyan-500/10 
                  border border-blue-500/20 group-hover:border-blue-400/40 
                  transition-smooth">
      <Icon className="w-5 h-5 text-blue-400" />
    </div>
    <span className="badge-elegant">+12%</span>
  </div>
  
  <div className="stat-number text-slate-50 mb-2">
    19,228
  </div>
  
  <p className="text-muted">
    Total Comments
  </p>
</div>
```

### Hero Section
```tsx
<section className="py-20">
  <h1 className="heading-xl text-gradient mb-4">
    Garuda: Mimpi Dunia
  </h1>
  <p className="text-lg text-slate-300 max-w-2xl">
    Analisis sentimen komprehensif untuk Timnas Indonesia
  </p>
</section>
```

### Chart Container
```tsx
<div className="elegant-card">
  <h3 className="heading-md mb-6">Sentiment Distribution</h3>
  <div className="divider-elegant mb-6" />
  {/* Chart component */}
</div>
```

---

## ⚡ Performance Tips

1. **Use CSS animations** instead of JS libraries
2. **Leverage `transition-smooth`** for consistent timing
3. **Avoid heavy backdrop-blur** on mobile (use media queries)
4. **Use `will-change` sparingly** (only on hover/active)
5. **Prefer `transform` over `top/left`** for animations

---

## 🎨 Color Usage Guidelines

### Do's ✅
- Use blue for primary actions and highlights
- Use emerald for positive sentiment/success
- Use red for negative sentiment/errors
- Use slate for neutral content
- Maintain 4.5:1 contrast ratio for text

### Don'ts ❌
- Don't use pure black (#000000)
- Don't use pure white (#FFFFFF) for text
- Don't mix warm and cool grays
- Don't use more than 3 accent colors per view

---

## 📱 Responsive Design

```tsx
// Mobile-first approach
<div className="p-4 md:p-6 lg:p-8">
  <h1 className="text-3xl md:text-4xl lg:text-5xl">
    Responsive Heading
  </h1>
</div>
```

### Breakpoints
```css
sm:  640px   /* Mobile landscape */
md:  768px   /* Tablet */
lg:  1024px  /* Desktop */
xl:  1280px  /* Large desktop */
2xl: 1536px  /* Extra large */
```

---

## 🔍 Accessibility

### Focus States
Always include visible focus indicators:
```tsx
<button className="focus-ring-elegant">
  Accessible Button
</button>
```

### Color Contrast
- Text on background: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- Interactive elements: 3:1 minimum

### Semantic HTML
```tsx
<main>
  <section aria-label="Statistics">
    <h2>Key Metrics</h2>
    {/* Content */}
  </section>
</main>
```

---

## 🎯 Implementation Checklist

- [x] Color palette defined
- [x] Typography scale established
- [x] Component library created
- [x] Animation system implemented
- [x] Responsive utilities added
- [x] Accessibility guidelines documented
- [x] Performance optimized (CSS-only)

---

**Version:** 1.0  
**Last Updated:** December 2025  
**Maintained by:** Garuda Team
