import React from 'react';

export default function GlobalRiskOverview({ data }: { data: any }) {
  if (!data) return <div className="minimal-card p-8 animate-pulse h-48"></div>;

  return (
    <div className="minimal-card p-8 flex flex-col justify-between">
      <div className="mb-10">
        <p className="font-mono text-xs uppercase tracking-widest text-[#888888] mb-2">[01] SYSTEM METRICS</p>
        <h2 className="text-3xl font-serif">Global Overview.</h2>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-white/10 border border-white/10">
        <div className="bg-[#0A0A0B] p-6 hover:bg-white/[0.02] transition-colors">
          <span className="font-mono text-[10px] text-[#888888] uppercase block mb-4 tracking-wider">Active Alerts</span>
          <div className="text-4xl font-serif text-[#D4AF37]">{data.active_alerts}</div>
        </div>
        
        <div className="bg-[#0A0A0B] p-6 hover:bg-white/[0.02] transition-colors">
          <span className="font-mono text-[10px] text-[#888888] uppercase block mb-4 tracking-wider">Critical Risks</span>
          <div className="text-4xl font-serif text-[#C41E3A]">{data.critical_risks}</div>
        </div>

        <div className="bg-[#0A0A0B] p-6 hover:bg-white/[0.02] transition-colors">
          <span className="font-mono text-[10px] text-[#888888] uppercase block mb-4 tracking-wider">Affected Regions</span>
          <div className="text-4xl font-serif text-white">{data.affected_countries}</div>
        </div>

        <div className="bg-[#0A0A0B] p-6 hover:bg-white/[0.02] transition-colors">
          <span className="font-mono text-[10px] text-[#888888] uppercase block mb-4 tracking-wider">Commodities</span>
          <div className="text-4xl font-serif text-[#888888]">8</div>
        </div>
      </div>
    </div>
  );
}
