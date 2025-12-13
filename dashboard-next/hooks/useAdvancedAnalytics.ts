import { useState, useEffect } from 'react';

interface TrendData {
  date: string;
  positive: number;
  negative: number;
  neutral: number;
  total: number;
}

interface TargetData {
  name: string;
  value: number;
  positive: number;
  negative: number;
  neutral: number;
  sentiment: number;
  sampleComments: string[];
}

export function useTrendAnalysis(period: string = 'monthly') {
  const [data, setData] = useState<TrendData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTrendData() {
      try {
        setLoading(true);
        const response = await fetch(`/api/analytics/trend?period=${period}`);
        const result = await response.json();
        
        if (result.success) {
          setData(result.data);
        } else {
          setError(result.error);
        }
      } catch (err) {
        setError('Failed to fetch trend data');
        console.error('Trend analysis error:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchTrendData();
  }, [period]);

  return { data, loading, error };
}

export function useTargetAnalysis(target?: string) {
  const [data, setData] = useState<TargetData[]>([]);
  const [targetDetail, setTargetDetail] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTargetData() {
      try {
        setLoading(true);
        const url = target ? `/api/analytics/targets?target=${target}` : '/api/analytics/targets';
        const response = await fetch(url);
        const result = await response.json();
        
        if (result.success) {
          if (target) {
            setTargetDetail(result.target);
          } else {
            setData(result.data);
          }
        } else {
          setError(result.error);
        }
      } catch (err) {
        setError('Failed to fetch target data');
        console.error('Target analysis error:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchTargetData();
  }, [target]);

  return { data, targetDetail, loading, error };
}
