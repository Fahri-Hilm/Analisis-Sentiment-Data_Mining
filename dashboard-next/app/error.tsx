"use client";

import { useEffect } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    useEffect(() => {
        console.error("Runtime Error:", error);
    }, [error]);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4 text-center bg-slate-950">
            <div className="p-6 bg-slate-900/50 border border-red-500/20 rounded-2xl backdrop-blur-xl">
                <div className="flex justify-center mb-4">
                    <div className="p-3 bg-red-500/10 rounded-full">
                        <AlertCircle className="w-8 h-8 text-red-500" />
                    </div>
                </div>
                <h2 className="text-2xl font-bold text-white mb-2">Something went wrong!</h2>
                <div className="mb-6 p-4 bg-black/30 rounded-lg font-mono text-xs text-red-300 max-w-lg overflow-auto text-left">
                    {error.message || "Unknown error occurred"}
                    {error.digest && <div className="mt-2 text-slate-500">Digest: {error.digest}</div>}
                </div>
                <button
                    onClick={reset}
                    className="flex items-center gap-2 px-6 py-3 mx-auto bg-blue-600 hover:bg-blue-500 text-white rounded-xl transition-all font-medium"
                >
                    <RefreshCw className="w-4 h-4" />
                    Try Again
                </button>
            </div>
        </div>
    );
}
