export interface Structure {
    name: string;
    elements: any[];
    table?: Record<string, any>;
    formula?: string;
    constants: Record<string, any>;
}

export interface Homomorphism {
    mapping: Record<string, any>;
    properties: string[];
    image: any[];
    kernel: any[];
}

export interface MorphismResponse {
    homomorphisms: Homomorphism[];
    strategy: string;
    time_elapsed: number;
}
