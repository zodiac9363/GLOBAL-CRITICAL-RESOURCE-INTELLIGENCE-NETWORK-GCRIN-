import React from 'react';

export default function LiveAlertFeed({ alerts }: { alerts: any[] }) {
  if (!alerts) return <div className="minimal-card p-8 animate-pulse h-96"></div>;

  return (
    <div className="minimal-card p-8 h-full flex flex-col">
      <div className="mb-8">
        <p className="font-mono text-xs uppercase tracking-widest text-[#888888] mb-2">[02] LIVE INTELLIGENCE</p>
        <h2 className="text-3xl font-serif">Alert Feed.</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto pr-4 space-y-0 divide-y divide-white/10">
        {alerts.length === 0 ? (
          <div className="text-[#888888] font-mono text-xs py-8">No active alerts detected.</div>
        ) : (
          alerts.map((alert: any, idx: number) => (
            <div key={idx} className="py-5 group">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-serif text-lg text-white">
                  {alert.title}
                </h3>
              </div>
              <p className="text-xs font-mono text-[#888888] mb-3">{alert.message}</p>
              <div className="text-[10px] font-mono text-[#444444] uppercase tracking-wider">
                {new Date(alert.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} — LOGGED
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
