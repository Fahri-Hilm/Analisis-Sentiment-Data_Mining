import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export function useDashboardStats() {
    const { data, error, isLoading } = useSWR("/api/stats", fetcher, {
        refreshInterval: 0,
        revalidateOnFocus: false,
        revalidateOnReconnect: false,
        dedupingInterval: 300000, // 5 minutes
        keepPreviousData: true,
    });

    return {
        stats: data,
        isLoading,
        isError: error,
    };
}
