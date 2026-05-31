import React from 'react';
import { motion } from 'framer-motion';

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15
    }
  }
};

const item = {
  hidden: { opacity: 0, x: -20 },
  show: { opacity: 1, x: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } }
};

export default function TopRisksTable({ risks }: { risks: any[] }) {
  if (!risks) return <div className="minimal-card p-8 animate-pulse h-64"></div>;

  return (
    <div className="minimal-card p-8">
      <div className="mb-8">
        <p className="font-mono text-xs uppercase tracking-widest text-[#888888] mb-2">[03] CRITICAL THREATS</p>
        <h2 className="text-3xl font-serif">Highest Priority.</h2>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-white/10">
              <th className="px-4 py-4 font-mono text-[10px] uppercase tracking-widest text-[#888888] font-normal">Resource</th>
              <th className="px-4 py-4 font-mono text-[10px] uppercase tracking-widest text-[#888888] font-normal">Region</th>
              <th className="px-4 py-4 font-mono text-[10px] uppercase tracking-widest text-[#888888] font-normal">Risk Type</th>
              <th className="px-4 py-4 font-mono text-[10px] uppercase tracking-widest text-[#888888] font-normal text-right">Severity</th>
            </tr>
          </thead>
          <motion.tbody 
            variants={container}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
            className="divide-y divide-white/5"
          >
            {risks.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-[#888888] font-mono text-xs">
                  No high priority threats.
                </td>
              </tr>
            ) : (
              risks.map((risk: any, idx: number) => (
                <motion.tr variants={item} key={idx} className="hover:bg-white/[0.02] transition-colors group cursor-default">
                  <td className="px-4 py-5 font-serif text-lg text-white">
                    {risk.commodity || "Multiple"}
                  </td>
                  <td className="px-4 py-5 font-mono text-xs text-[#FAFAFA]">{risk.country || "Global"}</td>
                  <td className="px-4 py-5 font-mono text-xs text-[#888888]">{risk.type}</td>
                  <td className="px-4 py-5 text-right">
                    <span className={`inline-block border px-3 py-1 text-[10px] font-mono uppercase tracking-widest ${
                      risk.severity === 'Critical' ? 'border-[#C41E3A] text-[#C41E3A] bg-[#C41E3A]/5' : 
                      risk.severity === 'High' ? 'border-[#D4AF37] text-[#D4AF37] bg-[#D4AF37]/5' : 
                      'border-[#4A5D23] text-[#4A5D23] bg-[#4A5D23]/5'
                    }`}>
                      {risk.severity}
                    </span>
                  </td>
                </motion.tr>
              ))
            )}
          </motion.tbody>
        </table>
      </div>
    </div>
  );
}
