import React, { useMemo } from 'react';
import ReactFlow, { 
  Background, 
  MarkerType,
  Position,
  type Node, 
  type Edge, 
} from 'reactflow';
import 'reactflow/dist/style.css';
import type { Structure, Homomorphism } from '../types';

interface MorphismCanvasProps {
  source: Structure;
  target: Structure;
  homomorphism: Homomorphism | null;
}

export const MorphismCanvas: React.FC<MorphismCanvasProps> = ({ source, target, homomorphism }) => {
  const { nodes, edges } = useMemo(() => {
    const flowNodes: Node[] = [];
    const flowEdges: Edge[] = [];

    // 1. Create Source Nodes (Left)
    source.elements.forEach((el, index) => {
      flowNodes.push({
        id: `s-${el}`,
        data: { label: String(el) },
        position: { x: 100, y: 100 + index * 80 },
        sourcePosition: Position.Right,
        targetPosition: Position.Left,
        style: { 
          background: '#eef2ff', 
          color: '#4338ca', 
          borderColor: '#4338ca',
          borderWidth: 2,
          fontWeight: 'bold',
          borderRadius: '12px',
          width: 60,
          height: 60,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '16px'
        },
      });
    });

    // 2. Create Target Nodes (Right)
    target.elements.forEach((el, index) => {
      flowNodes.push({
        id: `t-${el}`,
        data: { label: String(el) },
        position: { x: 600, y: 100 + index * 80 },
        sourcePosition: Position.Right,
        targetPosition: Position.Left,
        style: { 
          background: '#fff1f2', 
          color: '#be123c', 
          borderColor: '#be123c',
          borderWidth: 2,
          fontWeight: 'bold',
          borderRadius: '12px',
          width: 60,
          height: 60,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '16px'
        },
      });
    });

    // 3. Create Mapping Arcs (If homomorphism selected)
    if (homomorphism) {
      Object.entries(homomorphism.mapping).forEach(([srcKey, tgtVal]) => {
        flowEdges.push({
          id: `edge-${srcKey}-${tgtVal}`,
          source: `s-${srcKey}`,
          target: `t-${tgtVal}`,
          animated: true,
          style: { stroke: '#f43f5e', strokeWidth: 3 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color: '#f43f5e',
          },
        });
      });
    }

    return { nodes: flowNodes, edges: flowEdges };
  }, [source, target, homomorphism]);

  return (
    <div className="w-full h-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        nodesDraggable={true}
        nodesConnectable={false}
      >
        <Background color="#cbd5e1" gap={20} />
      </ReactFlow>

      {/* Info Overlay */}
      <div className="absolute bottom-6 right-6 flex flex-col space-y-2 pointer-events-none">
        <div className="bg-white/90 backdrop-blur p-4 rounded-xl border border-slate-200 shadow-xl max-w-xs">
          <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2">Structure Details</h4>
          <div className="space-y-3">
            <div>
              <div className="text-xs font-bold text-indigo-600 mb-1">Source: {source.name}</div>
              <div className="text-[10px] text-slate-500">Elements: {source.elements.length}</div>
            </div>
            <div className="h-px bg-slate-100" />
            <div>
              <div className="text-xs font-bold text-rose-600 mb-1">Target: {target.name}</div>
              <div className="text-[10px] text-slate-500">Elements: {target.elements.length}</div>
            </div>
          </div>
        </div>
        
        {homomorphism && (
          <div className="bg-white/90 backdrop-blur p-4 rounded-xl border border-indigo-100 shadow-xl max-w-xs space-y-4">
            <div>
              <h4 className="text-[10px] font-black uppercase tracking-widest text-indigo-400 mb-2">Ker(f)</h4>
              <div className="flex flex-wrap gap-1">
                {homomorphism.kernel.map((val, i) => (
                  <span key={i} className="bg-indigo-50 text-indigo-700 text-[10px] font-bold px-2 py-0.5 rounded border border-indigo-100">
                    {val}
                  </span>
                ))}
              </div>
            </div>
            
            <div className="h-px bg-slate-100" />

            <div>
              <h4 className="text-[10px] font-black uppercase tracking-widest text-rose-400 mb-2">Im(f)</h4>
              <div className="flex flex-wrap gap-1">
                {homomorphism.image.map((val, i) => (
                  <span key={i} className="bg-rose-50 text-rose-700 text-[10px] font-bold px-2 py-0.5 rounded border border-rose-100">
                    {val}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
