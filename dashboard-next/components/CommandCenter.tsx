"use client";

import * as React from "react";
import { Command } from "cmdk";
import { useRouter } from "next/navigation";
import {
    LayoutDashboard,
    BarChart3,
    Database,
    Settings,
    FileText,
    Search,
    MessageSquare,
    Moon,
    Sun,
    Laptop,
    ArrowRight
} from "lucide-react";

export function CommandCenter() {
    const [open, setOpen] = React.useState(false);
    const router = useRouter();

    // Toggle with Ctrl+K or Cmd+K
    React.useEffect(() => {
        const down = (e: KeyboardEvent) => {
            if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                setOpen((open) => !open);
            }
        };

        document.addEventListener("keydown", down);
        return () => document.removeEventListener("keydown", down);
    }, []);

    const runCommand = React.useCallback((command: () => unknown) => {
        setOpen(false);
        command();
    }, []);

    return (
        <>
            <div
                className="fixed bottom-4 right-4 z-40 px-3 py-1.5 bg-slate-800/50 backdrop-blur-md border border-slate-700/50 rounded-lg text-xs text-slate-400 font-mono hidden md:flex items-center gap-2 cursor-pointer hover:bg-slate-800/80 transition-colors"
                onClick={() => setOpen(true)}
            >
                <span>Command Menu</span>
                <kbd className="bg-slate-900/50 px-1.5 py-0.5 rounded border border-slate-700 text-slate-300 font-sans">⌘K</kbd>
            </div>

            <Command.Dialog
                open={open}
                onOpenChange={setOpen}
                label="Global Command Menu"
                className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] px-4"
            >
                <div className="fixed inset-0 bg-[#020617]/60 backdrop-blur-sm transition-opacity" onClick={() => setOpen(false)} />

                <div className="relative w-full max-w-xl bg-[#0f172a]/90 border border-slate-700/50 rounded-xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200 ring-1 ring-white/10">
                    <div className="flex items-center border-b border-slate-700/50 px-4">
                        <Search className="w-5 h-5 text-slate-400 mr-3" />
                        <Command.Input
                            placeholder="Type a command or search..."
                            className="w-full h-14 bg-transparent outline-none text-base text-white placeholder:text-slate-500 font-light"
                        />
                    </div>

                    <Command.List className="max-h-[300px] overflow-y-auto p-2 custom-scrollbar">
                        <Command.Empty className="py-6 text-center text-slate-500 text-sm">No results found.</Command.Empty>

                        <Command.Group heading="Navigation" className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-2 px-2 mt-2">
                            <Command.Item
                                onSelect={() => runCommand(() => router.push("/"))}
                                className="flex items-center gap-3 px-3 py-3 rounded-lg text-slate-300 hover:bg-cyan-500/10 hover:text-cyan-400 cursor-pointer transition-colors group aria-selected:bg-cyan-500/10 aria-selected:text-cyan-400"
                            >
                                <LayoutDashboard className="w-4 h-4" />
                                <span className="flex-1 font-medium text-sm">Dashboard Overview</span>
                                <span className="text-xs text-slate-600 group-hover:text-cyan-500/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">Jump to <ArrowRight className="w-3 h-3" /></span>
                            </Command.Item>

                            <Command.Item
                                onSelect={() => runCommand(() => router.push("/analytics"))}
                                className="flex items-center gap-3 px-3 py-3 rounded-lg text-slate-300 hover:bg-cyan-500/10 hover:text-cyan-400 cursor-pointer transition-colors group aria-selected:bg-cyan-500/10 aria-selected:text-cyan-400"
                            >
                                <BarChart3 className="w-4 h-4" />
                                <span className="flex-1 font-medium text-sm">Analytics</span>
                            </Command.Item>

                            <Command.Item
                                onSelect={() => runCommand(() => router.push("/dataset"))}
                                className="flex items-center gap-3 px-3 py-3 rounded-lg text-slate-300 hover:bg-cyan-500/10 hover:text-cyan-400 cursor-pointer transition-colors group aria-selected:bg-cyan-500/10 aria-selected:text-cyan-400"
                            >
                                <Database className="w-4 h-4" />
                                <span className="flex-1 font-medium text-sm">Dataset Manager</span>
                            </Command.Item>

                            <Command.Item
                                onSelect={() => runCommand(() => router.push("/comments"))}
                                className="flex items-center gap-3 px-3 py-3 rounded-lg text-slate-300 hover:bg-cyan-500/10 hover:text-cyan-400 cursor-pointer transition-colors group aria-selected:bg-cyan-500/10 aria-selected:text-cyan-400"
                            >
                                <MessageSquare className="w-4 h-4" />
                                <span className="flex-1 font-medium text-sm">Comments Analyzer</span>
                            </Command.Item>
                        </Command.Group>

                        <Command.Separator className="h-px bg-slate-700/50 my-2" />

                        <Command.Group heading="System" className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-2 px-2">
                            <Command.Item
                                onSelect={() => runCommand(() => router.push("/settings"))}
                                className="flex items-center gap-3 px-3 py-3 rounded-lg text-slate-300 hover:bg-purple-500/10 hover:text-purple-400 cursor-pointer transition-colors group aria-selected:bg-purple-500/10 aria-selected:text-purple-400"
                            >
                                <Settings className="w-4 h-4" />
                                <span className="flex-1 font-medium text-sm">Model Settings</span>
                            </Command.Item>

                            <Command.Item
                                onSelect={() => runCommand(() => router.push("/docs"))}
                                className="flex items-center gap-3 px-3 py-3 rounded-lg text-slate-300 hover:bg-purple-500/10 hover:text-purple-400 cursor-pointer transition-colors group aria-selected:bg-purple-500/10 aria-selected:text-purple-400"
                            >
                                <FileText className="w-4 h-4" />
                                <span className="flex-1 font-medium text-sm">Documentation</span>
                            </Command.Item>
                        </Command.Group>

                        <Command.Separator className="h-px bg-slate-700/50 my-2" />

                        <Command.Group heading="Appearance" className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-2 px-2">
                            <Command.Item className="flex items-center gap-3 px-3 py-3 rounded-lg text-slate-400 hover:bg-slate-800 cursor-pointer transition-colors aria-selected:bg-slate-800 aria-selected:text-slate-200">
                                <Moon className="w-4 h-4" />
                                <span>Dark Mode</span>
                            </Command.Item>
                            <Command.Item className="flex items-center gap-3 px-3 py-3 rounded-lg text-slate-400 hover:bg-slate-800 cursor-pointer transition-colors aria-selected:bg-slate-800 aria-selected:text-slate-200">
                                <Sun className="w-4 h-4" />
                                <span>Light Mode</span>
                            </Command.Item>
                            <Command.Item className="flex items-center gap-3 px-3 py-3 rounded-lg text-slate-400 hover:bg-slate-800 cursor-pointer transition-colors aria-selected:bg-slate-800 aria-selected:text-slate-200">
                                <Laptop className="w-4 h-4" />
                                <span>System</span>
                            </Command.Item>
                        </Command.Group>

                    </Command.List>

                    <div className="border-t border-slate-700/50 px-4 py-2 flex items-center justify-between text-[10px] text-slate-500 font-mono">
                        <div className="flex gap-2">
                            <span>Navigate <kbd className="bg-slate-800 px-1 rounded">↓</kbd> <kbd className="bg-slate-800 px-1 rounded">↑</kbd></span>
                            <span>Select <kbd className="bg-slate-800 px-1 rounded">↵</kbd></span>
                        </div>
                        <span>Sentiment Dashboard v2.0</span>
                    </div>
                </div>
            </Command.Dialog>
        </>
    );
}
