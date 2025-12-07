import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export function useDashboardStats() {
    const { data, error, isLoading } = useSWR("/api/stats", fetcher, {
        refreshInterval: 0, // Disable auto-refresh for now to keep it static/fast
        revalidateOnFocus: false, // Don't revalidate when focusing window
        dedupingInterval: 60000, // Cache for 1 minute
    });

    return {
        stats: data,
        isLoading,
        isError: error,
    };
}
