import React, {useState} from 'react';
import type {Structure} from '../types';
import {Code, Grid, Save, Upload, X} from 'lucide-react';

interface StructureBuilderProps {
    type: 'source' | 'target';
    initialData?: Structure | null;
    onSave: (s: Structure) => void;
    onClose: () => void;
}

export const StructureBuilder: React.FC<StructureBuilderProps> = ({type, initialData, onSave, onClose}) => {
    const [activeTab, setActiveTab] = useState<'table' | 'dsl' | 'json'>(initialData?.formula ? 'dsl' : 'table');
    const [name, setName] = useState(initialData?.name || (type === 'source' ? 'S' : 'T'));
    const [elementsInput, setElementsInput] = useState(initialData?.elements.join(', ') || '0, 1, 2, 3');
    const elements = elementsInput.split(',').map(e => e.trim()).filter(e => e !== '');
    const [table, setTable] = useState<Record<string, any>>(initialData?.table || {});
    const [formula, setFormula] = useState(initialData?.formula || '(a + b) % n');

    // Initialize table ONLY if we don't have initialData
    React.useEffect(() => {
        if (!initialData) {
            const newTable: Record<string, any> = {};
            for (let i = 0; i < elements.length; i++) {
                for (let j = 0; j < elements.length; j++) {
                    newTable[`${i},${j}`] = 0; // Default or calculate based on formula if possible
                }
            }
            setTable(newTable);
        }
    }, [elementsInput, initialData]);

    const handleCellChange = (i: number, j: number, value: string) => {
        setTable({...table, [`${i},${j}`]: value});
    };

    const handleSave = () => {
        onSave({
            name,
            elements,
            table: activeTab === 'table' ? table : undefined,
            formula: activeTab === 'dsl' ? formula : undefined,
            constants: elements.length > 0 ? {identity: elements[0]} : {},
        });
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm p-4">
            <div
                className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden border border-slate-200">
                {/* Header */}
                <div className="p-6 border-b border-slate-100 flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-black text-slate-800 tracking-tight">
                            Build {type === 'source' ? 'Source' : 'Target'} Structure
                        </h2>
                        <p className="text-slate-400 text-sm">Define elements and operations for your algebra.</p>
                    </div>
                    <button onClick={onClose} className="p-2 hover:bg-slate-100 rounded-full transition-colors">
                        <X size={24} className="text-slate-400"/>
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex px-6 border-b border-slate-100 bg-slate-50/50">
                    <TabButton
                        active={activeTab === 'table'}
                        onClick={() => setActiveTab('table')}
                        icon={<Grid size={16}/>}
                        label="Cayley Table"
                    />
                    <TabButton
                        active={activeTab === 'dsl'}
                        onClick={() => setActiveTab('dsl')}
                        icon={<Code size={16}/>}
                        label="DSL Editor"
                    />
                    <TabButton
                        active={activeTab === 'json'}
                        onClick={() => setActiveTab('json')}
                        icon={<Upload size={16}/>}
                        label="JSON Upload"
                    />
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-8">
                    <div className="max-w-2xl mx-auto space-y-8">
                        {/* Common Fields */}
                        <div className="grid grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Structure
                                    Name</label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all outline-none font-medium"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Elements
                                    (comma-separated)</label>
                                <input
                                    type="text"
                                    value={elementsInput}
                                    onChange={(e) => setElementsInput(e.target.value)}
                                    className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all outline-none font-medium"
                                />
                            </div>
                        </div>

                        {activeTab === 'table' && (
                            <div className="space-y-4">
                                <label className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Binary
                                    Operation Table (*)</label>
                                <div
                                    className="inline-block border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                                    <table className="border-collapse">
                                        <thead>
                                        <tr>
                                            <th className="bg-slate-50 border-b border-r border-slate-200 p-3 text-slate-400 text-xs font-bold w-12">*</th>
                                            {elements.map((el, i) => (
                                                <th key={i}
                                                    className="bg-slate-50 border-b border-r border-slate-200 p-3 text-indigo-600 text-xs font-bold w-12">{el}</th>
                                            ))}
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {elements.map((rowEl, i) => (
                                            <tr key={i}>
                                                <th className="bg-slate-50 border-r border-b border-slate-200 p-3 text-indigo-600 text-xs font-bold">{rowEl}</th>
                                                {elements.map((colEl, j) => (
                                                    <td key={j} className="border-r border-b border-slate-200 p-0">
                                                        <input
                                                            type="text"
                                                            value={table[`${i},${j}`] ?? ''}
                                                            onChange={(e) => handleCellChange(i, j, e.target.value)}
                                                            className="w-12 h-12 text-center text-sm font-bold focus:bg-indigo-50 focus:text-indigo-700 outline-none transition-colors border-none"
                                                        />
                                                    </td>
                                                ))}
                                            </tr>
                                        ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        )}

                        {activeTab === 'dsl' && (
                            <div className="space-y-4">
                                <div className="bg-indigo-50 border border-indigo-100 p-4 rounded-xl mb-6">
                                    <h4 className="text-xs font-bold text-indigo-700 uppercase mb-2">Expression
                                        Guide</h4>
                                    <p className="text-sm text-indigo-600 leading-relaxed">
                                        Write a Python-style expression using variables <b>a</b>, <b>b</b>,
                                        and <b>n</b> (set size).
                                        <br/>Example: <code
                                        className="bg-white px-1.5 py-0.5 rounded border border-indigo-200">(a + b) %
                                        n</code>
                                    </p>
                                </div>

                                <label className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Operation
                                    Formula</label>
                                <div className="relative group">
                  <textarea
                      value={formula}
                      onChange={(e) => setFormula(e.target.value)}
                      placeholder="(a + b) % n"
                      className="w-full h-32 px-6 py-4 rounded-2xl border-2 border-slate-100 bg-slate-50 font-mono text-lg focus:bg-white focus:border-indigo-500 transition-all outline-none resize-none shadow-inner"
                  />
                                    <Code
                                        className="absolute right-4 top-4 text-slate-200 group-focus-within:text-indigo-200 transition-colors"
                                        size={24}/>
                                </div>
                            </div>
                        )}

                        {activeTab === 'json' && (
                            <div
                                className="p-12 text-center border-2 border-dashed border-slate-200 rounded-3xl text-slate-400 bg-slate-50">
                                <Upload size={48} className="mx-auto mb-4 opacity-10"/>
                                <p className="font-medium">JSON Upload is coming soon.</p>
                                <p className="text-xs mt-1">Use the Cayley Table for now.</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Footer */}
                <div className="p-6 bg-slate-50 border-t border-slate-100 flex justify-end space-x-3">
                    <button
                        onClick={onClose}
                        className="px-6 py-2.5 rounded-xl font-bold text-slate-500 hover:bg-slate-200 transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={handleSave}
                        className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-2.5 rounded-xl font-bold transition-all shadow-lg shadow-indigo-200"
                    >
                        <Save size={18}/>
                        <span>Save Structure</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

const TabButton: React.FC<{ active: boolean; onClick: () => void; icon: React.ReactNode; label: string }> = ({
                                                                                                                 active,
                                                                                                                 onClick,
                                                                                                                 icon,
                                                                                                                 label
                                                                                                             }) => (
    <button
        onClick={onClick}
        className={`flex items-center space-x-2 px-6 py-4 text-sm font-bold transition-all border-b-2 ${
            active ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-400 hover:text-slate-600'
        }`}
    >
        {icon}
        <span>{label}</span>
    </button>
);
