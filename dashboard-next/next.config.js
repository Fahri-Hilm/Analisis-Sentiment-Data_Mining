/** @type {import('next').NextConfig} */
const nextConfig = {
    swcMinify: true, // Enable SWC minification for faster builds and optimization
    compiler: {
        removeConsole: process.env.NODE_ENV === "production", // Remove console.log in prod
    },
};


module.exports = nextConfig;
