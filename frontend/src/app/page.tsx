"use client";

import dynamic from 'next/dynamic';
import Dashboard from '@/components/Dashboard';

// Dynamically import the 3D Network Background component to avoid SSR issues
const NetworkBackground = dynamic(() => import('@/components/NetworkBackground'), { ssr: false });

import { Canvas } from '@react-three/fiber';

export default function Home() {
  return (
    <main className="relative w-full min-h-screen bg-black overflow-x-hidden">
      {/* 3D Background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <Canvas camera={{ position: [0, 0, 8], fov: 60 }}>
          <NetworkBackground />
        </Canvas>
      </div>

      {/* UI Overlay */}
      <Dashboard />
    </main>
  );
}
