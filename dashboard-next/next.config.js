/** @type {import('next').NextConfig} */
const nextConfig = {
    swcMinify: true,
    compiler: {
        removeConsole: process.env.NODE_ENV === "production",
    },
    compress: true,
    poweredByHeader: false,
    reactStrictMode: true,
    experimental: {
        optimizePackageImports: ['recharts', 'lucide-react', 'framer-motion'],
    },
};

module.exports = nextConfig;
