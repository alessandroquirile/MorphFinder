import React, {useState} from 'react';
import {Sidebar} from './components/Sidebar';
import {MorphismCanvas} from './components/MorphismCanvas';
import {StructureBuilder} from './components/StructureBuilder';
import {useFindMorphisms} from './application/hooks/useFindMorphisms';
import type {Homomorphism, Structure} from './domain/models/types';
import {Plus, Search, Loader2} from 'lucide-react';

const App: React.FC = () => {
    const [source, setSource] = useState<Structure | null>(null);
    const [target, setTarget] = useState<Structure | null>(null);
    const [selectedHom, setSelectedHom] = useState<Homomorphism | null>(null);
    const [showBuilder, setShowBuilder] = useState<'source' | 'target' | null>(null);

    const {
        homomorphisms,
        strategy,
        timeElapsed,
        loading,
        findMorphisms,
    } = useFindMorphisms();

    const handleFindMorphisms = async () => {
        try {
            const results = await findMorphisms(source, target);
            if (results && results.length > 0) {
                setSelectedHom(results[0]);
            } else if (results) {
                alert('No homomorphisms found.');
            }
        } catch (error) {
            console.error('Error finding morphisms:', error);
            alert(`Error: ${error instanceof Error ? error.message : 'An unknown error occurred.'}`);
        }
    };

    return (
        <div className="flex h-screen w-full bg-slate-50 overflow-hidden text-slate-900">
            {/* Sidebar */}
            <Sidebar
                homomorphisms={homomorphisms}
                strategy={strategy}
                timeElapsed={timeElapsed}
                selected={selectedHom}
                onSelect={setSelectedHom}
            />

            {/* Main Content */}
            <main className="flex-1 flex flex-col relative">
                {/* Header */}
                <header
                    className="h-16 border-b border-slate-200 bg-white flex items-center justify-between px-6 shrink-0">
                    <div className="flex items-center space-x-4">
                        <h1 className="text-xl font-bold text-indigo-600">MorphFinder</h1>
                        <div className="h-6 w-px bg-slate-200"/>
                        <div className="flex space-x-2">
                            <button
                                onClick={() => setShowBuilder('source')}
                                className={`px-3 py-1 rounded-md text-sm font-medium transition-colors border ${
                                    source ? 'bg-indigo-50 text-indigo-700 border-indigo-100 hover:bg-indigo-100' : 'bg-slate-100 text-slate-600 border-transparent hover:bg-slate-200'
                                }`}
                            >
                                {source ? `Edit Source: ${source.name}` : '+ Add Source'}
                            </button>
                            <button
                                onClick={() => setShowBuilder('target')}
                                className={`px-3 py-1 rounded-md text-sm font-medium transition-colors border ${
                                    target ? 'bg-indigo-50 text-indigo-700 border-indigo-100 hover:bg-indigo-100' : 'bg-slate-100 text-slate-600 border-transparent hover:bg-slate-200'
                                }`}
                            >
                                {target ? `Edit Target: ${target.name}` : '+ Add Target'}
                            </button>
                        </div>
                    </div>

                    <button
                        onClick={handleFindMorphisms}
                        disabled={!source || !target || loading}
                        className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 text-white px-4 py-2 rounded-lg font-semibold transition-all shadow-sm"
                    >
                        {loading ? <Loader2 className="animate-spin" size={18}/> : <Search size={18}/>}
                        <span>{loading ? 'Discovering...' : 'Discover Morphisms'}</span>
                    </button>
                </header>

                {/* Canvas Area */}
                <div
                    className="flex-1 relative bg-[radial-gradient(#e2e8f0_1px,transparent_1px)] [background-size:24px_24px]">
                    {source && target ? (
                        <MorphismCanvas
                            source={source}
                            target={target}
                            homomorphism={selectedHom}
                        />
                    ) : (
                        <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-400">
                            <Plus size={48} className="mb-4 opacity-20"/>
                            <p className="text-lg">Please define both Source and Target structures to begin.</p>
                        </div>
                    )}
                </div>

                {/* Builder Modal */}
                {showBuilder && (
                    <StructureBuilder
                        type={showBuilder}
                        initialData={showBuilder === 'source' ? source : target}
                        onSave={(structure) => {
                            if (showBuilder === 'source') setSource(structure);
                            else setTarget(structure);
                            setShowBuilder(null);
                        }}
                        onClose={() => setShowBuilder(null)}
                    />
                )}
            </main>
        </div>
    );
};

export default App;
