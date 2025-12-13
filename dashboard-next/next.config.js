/** @type {import('next').NextConfig} */
const nextConfig = {
    swcMinify: true,
    compiler: {
        removeConsole: process.env.NODE_ENV === "production",
    },
    compress: true,
    poweredByHeader: false,
    reactStrictMode: true,
    generateEtags: false,
    typescript: {
        // Skip type checking during build for faster deployment
        ignoreBuildErrors: true,
    },
    eslint: {
        // Skip ESLint during build for faster deployment
        ignoreDuringBuilds: true,
    },
    experimental: {
        optimizePackageImports: ['recharts', 'framer-motion', 'lucide-react'],
        optimizeCss: true,
        turbo: {
            rules: {
                '*.svg': {
                    loaders: ['@svgr/webpack'],
                    as: '*.js',
                },
            },
        },
    },
    images: {
        formats: ['image/webp', 'image/avif'],
        minimumCacheTTL: 31536000,
    },
};

module.exports = nextConfig;
