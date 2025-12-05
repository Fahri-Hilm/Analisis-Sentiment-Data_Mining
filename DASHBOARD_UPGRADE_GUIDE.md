# Dashboard Upgrade Guide

## 📊 Dashboard Baru - Fitur Lengkap

File: `dashboard_upgraded.py`

### ✨ Fitur Baru

#### 1. Advanced Filtering (Sidebar)
- **Date Range Filter** - Filter by custom date range
- **Sentiment Filter** - Multi-select sentiments
- **Keyword Search** - Search specific keywords
- **Live Filter Info** - Show filtered vs total comments

#### 2. Tab 1: Overview
- **Key Metrics** - Total, Positive, Negative, Neutral counts
- **Sentiment Distribution** - Pie chart
- **Broad Sentiment** - Bar chart (Positive/Negative/Neutral)

#### 3. Tab 2: Trends
- **Time-Series Chart** - Sentiment trends over time
- **Period Comparison** - Compare two time periods
- **Trend Metrics** - Positive/Negative percentage changes

#### 4. Tab 3: Details
- **Top Keywords** - Per sentiment category
- **Sentiment Labels** - Top 10 labels distribution

#### 5. Tab 4: Samples
- **Sample Comments** - View actual comments
- **Filter by Sentiment** - Select specific sentiment
- **Adjustable Count** - Show 1-20 samples

#### 6. Tab 5: Export & Settings
- **Export CSV** - Download filtered data
- **Export Summary** - Download statistics
- **Statistics** - Display data info

### 🚀 How to Use

#### Step 1: Run Dashboard
```bash
streamlit run dashboard_upgraded.py
```

#### Step 2: Use Filters (Sidebar)
1. Select date range
2. Choose sentiments
3. Enter keyword (optional)
4. View filtered results

#### Step 3: Explore Tabs
- **Overview**: Quick metrics
- **Trends**: Time-series analysis
- **Details**: Keywords & labels
- **Samples**: View comments
- **Export**: Download data

### 📈 Key Improvements

| Feature | Old | New |
|---------|-----|-----|
| Filtering | ❌ | ✅ Advanced |
| Time-Series | ❌ | ✅ Full trends |
| Comparison | ❌ | ✅ Period compare |
| Export | ❌ | ✅ CSV/Summary |
| Samples | ❌ | ✅ Filterable |
| Keywords | ✅ | ✅ Enhanced |
| Statistics | ✅ | ✅ Enhanced |

### 💡 Usage Examples

#### Example 1: Analyze Positive Sentiment
1. Sidebar: Select only "positive_support"
2. Tab 3: View top keywords for positive
3. Tab 4: See sample positive comments

#### Example 2: Compare Two Periods
1. Tab 2: Set Period 1 (Jan 1-7)
2. Tab 2: Set Period 2 (Jan 8-14)
3. View metrics comparison

#### Example 3: Export Report
1. Tab 5: Click "Export as CSV"
2. Download filtered data
3. Use in Excel/analysis

### 🎯 Next Steps

1. **Backup Old Dashboard**
   ```bash
   cp dashboard.py dashboard_backup.py
   ```

2. **Replace with New Dashboard**
   ```bash
   cp dashboard_upgraded.py dashboard.py
   ```

3. **Run New Dashboard**
   ```bash
   streamlit run dashboard.py
   ```

4. **Test All Features**
   - Test filters
   - Check all tabs
   - Try export

### 📝 Notes

- All old dashboards in `archive/legacy_dashboards/` can be deleted
- New dashboard is backward compatible
- Uses same data format
- No additional dependencies needed

### ✅ Checklist

- [x] Advanced filtering
- [x] Time-series trends
- [x] Period comparison
- [x] Export functionality
- [x] Sample viewer
- [x] Keyword analysis
- [x] Statistics display
- [x] Responsive design

---

**Status**: ✅ Ready to use
**Recommendation**: Replace old dashboard with this version
