import React, {useState} from 'react';
import type {Homomorphism} from '../domain/models/types';
import {CheckCircle2, ChevronRight, HelpCircle, Layers, X} from 'lucide-react';

const LEGEND = {
    Trivial: 'f maps all elements of S to the identity or zero of T.',
    Monomorphism: 'f is injective: no two elements in S map to the same element in T.',
    Epimorphism: 'f is surjective: every element in T is covered by S.',
    Isomorphism: 'f is bijective: both injective and surjective.',
    Endomorphism: 'f is a homomorphism from S to itself.',
    Automorphism: 'f is an isomorphism from S to itself.'
};

interface SidebarProps {
    homomorphisms: Homomorphism[];
    strategy: string;
    timeElapsed: number;
    selected: Homomorphism | null;
    onSelect: (h: Homomorphism) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({homomorphisms, strategy, timeElapsed, selected, onSelect}) => {
    const [showLegend, setShowLegend] = useState(false);

    return (
        <aside className="w-80 h-full border-r border-slate-200 bg-white flex flex-col shrink-0">
            <div className="p-6 border-b border-slate-100">
                <div className="flex items-center justify-between mb-1">
                    <h2 className="text-sm font-bold uppercase tracking-wider text-slate-500">Results</h2>
                    <button onClick={() => setShowLegend(true)}
                            className="text-slate-400 hover:text-indigo-600 transition-colors">
                        <HelpCircle size={18}/>
                    </button>
                </div>
                <div className="flex items-center justify-between">
                    <span className="text-2xl font-black text-slate-800">Found Morphisms</span>
                    <span className="bg-indigo-100 text-indigo-700 text-xs font-bold px-2 py-0.5 rounded-full">
            {homomorphisms.length}
          </span>
                </div>
            </div>

            {showLegend && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm p-4">
                    <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-bold text-lg">Property Legend</h3>
                            <button onClick={() => setShowLegend(false)}
                                    className="text-slate-400 hover:text-slate-600"><X size={20}/></button>
                        </div>
                        <div className="space-y-3">
                            {Object.entries(LEGEND).map(([term, def]) => (
                                <div key={term}>
                                    <span className="font-bold text-indigo-700 text-sm">{term}:</span>
                                    <p className="text-xs text-slate-600">{def}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            <div className="flex-1 overflow-y-auto py-4">
                {homomorphisms.length === 0 ? (
                    <div className="px-6 py-12 text-center text-slate-400">
                        <Layers size={40} className="mx-auto mb-3 opacity-20"/>
                        <p className="text-sm">No results yet. Define structures and run discovery.</p>
                    </div>
                ) : (
                    <div className="space-y-1 px-3">
                        {homomorphisms.map((h, i) => {
                            const isSelected = selected === h;
                            const primaryLabel = h.properties[0] || 'Homomorphism';

                            return (
                                <button
                                    key={i}
                                    onClick={() => onSelect(h)}
                                    className={`w-full text-left p-4 rounded-xl transition-all group relative ${
                                        isSelected
                                            ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-100'
                                            : 'hover:bg-slate-50 text-slate-700'
                                    }`}
                                >
                                    <div className="flex items-start justify-between">
                                        <div>
                      <span
                          className={`text-[10px] font-black uppercase tracking-widest mb-1 block ${isSelected ? 'text-indigo-200' : 'text-slate-400'}`}>
                        Morphism #{i + 1}
                      </span>
                                            <h3 className="font-bold text-lg leading-tight">{primaryLabel}</h3>
                                        </div>
                                        {isSelected && <CheckCircle2 size={18} className="text-indigo-200"/>}
                                    </div>

                                    <div className={`mt-3 flex flex-wrap gap-1 ${isSelected ? 'opacity-80' : ''}`}>
                                        {h.properties.slice(1).map((prop, pi) => (
                                            <span key={pi}
                                                  className={`text-[10px] px-1.5 py-0.5 rounded font-medium border ${
                                                      isSelected ? 'border-white/20 bg-white/10' : 'border-slate-200 bg-slate-100'
                                                  }`}>
                        {prop}
                      </span>
                                        ))}
                                    </div>

                                    {!isSelected && (
                                        <ChevronRight size={16}
                                                      className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-300 opacity-0 group-hover:opacity-100 transition-all"/>
                                    )}
                                </button>
                            );
                        })}
                    </div>
                )}
            </div>

            <div className="p-6 bg-slate-50 border-t border-slate-200">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4 text-center">Engine
                    Statistics
                </div>
                <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="bg-white p-3 rounded-lg border border-slate-200 text-center">
                        <div className="text-sm font-bold text-slate-700">{(timeElapsed * 1000).toFixed(2)} ms</div>
                        <div className="text-[9px] text-slate-400 font-bold uppercase">Time Elapsed</div>
                    </div>
                    <div className="bg-white p-3 rounded-lg border border-slate-200 text-center">
                        <div className="text-sm font-bold text-slate-700">CSP+Pruning</div>
                        <div className="text-[9px] text-slate-400 font-bold uppercase">Algorithm</div>
                    </div>
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg border border-indigo-100 text-center">
                    <div className="text-sm font-bold text-indigo-700 capitalize">{strategy || 'Unknown'}</div>
                    <div className="text-[9px] text-indigo-400 font-bold uppercase">Generating Set Strategy</div>
                </div>
            </div>
        </aside>
    );
};
