/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**",
      },
    ],
  },
  async rewrites() {
    const rawTarget =
      process.env.BACKEND_URL ||
      process.env.NEXT_PUBLIC_BACKEND_URL ||
      process.env.NEXT_PUBLIC_API_URL ||
      process.env.NEXT_API_URL ||
      "https://pricewise-9cov.onrender.com";
    const backendTarget = rawTarget.replace(/\/api\/v1\/?$/, "").replace(/\/+$/, "");
    return [
      {
        source: "/api/v1/:path*",
        destination: `${backendTarget}/api/v1/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
