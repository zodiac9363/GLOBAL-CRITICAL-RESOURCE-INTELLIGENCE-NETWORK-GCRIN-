"use client";

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import GlobalRiskOverview from './modules/GlobalRiskOverview';
import LiveAlertFeed from './modules/LiveAlertFeed';
import TopRisksTable from './modules/TopRisksTable';
import { Target, RefreshCw } from 'lucide-react';

import { motion } from 'framer-motion';

const revealVariants = {
  hidden: { opacity: 0, y: 120 },
  visible: { 
    opacity: 1, 
    y: 0, 
    transition: { 
      duration: 1.4, 
      ease: [0.16, 1, 0.3, 1] // Elegant slow ease-out (Intergest style)
    } 
  }
};

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      const summaryRes = await axios.get(`${baseURL}/dashboard-summary`);
      setSummary(summaryRes.data);
      const alertsRes = await axios.get(`${baseURL}/alerts?limit=10`);
      setAlerts(alertsRes.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full relative z-10 pointer-events-none text-[#FAFAFA]">
      <div className="max-w-7xl mx-auto pointer-events-auto px-6 md:px-12">
        
        {/* Section 1: Header & Global Overview (100vh) */}
        <section className="min-h-screen flex flex-col justify-center py-20">
          <header className="flex justify-between items-end mb-16 border-b border-white/10 pb-6">
            <div className="group cursor-default">
              <h1 className="text-5xl md:text-7xl font-serif tracking-tight mb-2 flex items-center gap-4">
                <span className="text-roll">
                  <span className="text-roll-row">Global Intelligence.</span>
                  <span className="text-roll-row text-roll-clone" aria-hidden="true">Global Intelligence.</span>
                </span>
              </h1>
              <p className="font-mono text-sm tracking-widest text-[#888888] uppercase">
                Critical Resource Network [GCRIN]
              </p>
            </div>
            
            <button 
              onClick={fetchData} 
              className={`p-3 rounded-none border border-white/10 subtle-bg transition-colors ${loading ? 'animate-spin opacity-50' : ''}`}
              aria-label="Refresh Data"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </header>

          <motion.div
            initial="hidden"
            animate="visible"
            variants={revealVariants}
          >
            <GlobalRiskOverview data={summary} />
          </motion.div>
        </section>

        {/* Section 2: Highest Priority Threats (100vh) */}
        <section className="min-h-screen flex flex-col justify-center py-20">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "0px 0px -100px 0px" }}
            variants={revealVariants}
          >
            <TopRisksTable risks={summary?.top_risks || []} />
          </motion.div>
        </section>

        {/* Section 3: Live Alert Feed (100vh) */}
        <section className="min-h-screen flex flex-col justify-center py-20 mb-20">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "0px 0px -100px 0px" }}
            variants={revealVariants}
          >
            <LiveAlertFeed alerts={alerts} />
          </motion.div>
        </section>

      </div>
    </div>
  );
}
