"use client";

export function TopCategories({ categories }: { categories: any[] }) {
  const getColor = (index: number) => {
    const colors = ["bg-blue-500", "bg-red-500", "bg-yellow-500", "bg-green-500", "bg-purple-500", "bg-pink-500", "bg-indigo-500", "bg-orange-500"];
    return colors[index % colors.length];
  };

  return (
    <div className="bg-gradient-to-br from-[#1a2942] to-[#0f1c2e] rounded-xl p-6 border border-blue-500/20">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h3 className="text-lg font-semibold">Top Sentiment Categories</h3>
          <div className="text-sm text-gray-400">Breakdown by topic from real data</div>
        </div>
      </div>
      <div className="space-y-4">
        <div className="grid grid-cols-4 text-xs text-gray-400 pb-2 border-b border-gray-700">
          <div className="col-span-2">CATEGORY</div>
          <div>COMMENTS</div>
          <div>PERCENTAGE</div>
        </div>
        {categories.map((category, i) => (
          <div key={i} className="grid grid-cols-4 items-center">
            <div className="col-span-2 flex items-center gap-3">
              <div className={`w-2 h-2 rounded-full ${getColor(i)}`}></div>
              <span className="text-sm">{category.name}</span>
            </div>
            <div className="text-sm text-gray-400">{category.count.toLocaleString()}</div>
            <div className="flex items-center gap-2">
              <div className="flex-1 bg-gray-700 rounded-full h-1.5">
                <div className={`${getColor(i)} h-1.5 rounded-full`} style={{ width: `${category.percentage}%` }}></div>
              </div>
              <span className="text-xs text-gray-400 w-12">{category.percentage}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
