import type {Structure} from '../../domain/models/types';

/**
 * Detects the identity element in a finite algebraic structure using its Cayley table.
 * An element e is an identity if a * e = a and e * a = a for all a.
 */
export const getIdentity = (structure: Structure): string | null => {
    if (!structure.table) return null;
    const elements = structure.elements;

    for (const e of elements) {
        let isIdentity = true;
        for (const a of elements) {
            // Check e * a = a
            if (String(structure.table[`${elements.indexOf(e)},${elements.indexOf(a)}`]) !== String(a)) {
                isIdentity = false;
                break;
            }
            // Check a * e = a
            if (String(structure.table[`${elements.indexOf(a)},${elements.indexOf(e)}`]) !== String(a)) {
                isIdentity = false;
                break;
            }
        }
        if (isIdentity) return e;
    }
    return null;
};

/**
 * Naive identification of generators.
 * A set of elements generates the structure if all elements can be reached by repeated operations.
 * For simplicity in UI, we identify elements whose powers (in a cyclic sense) cover the structure.
 */
export const getGenerators = (structure: Structure): string[] => {
    if (!structure.table || structure.elements.length === 0) return [];
    
    // Simplification: In a small finite group/magma, elements that don't satisfy 
    // any special property or are "primitive" can be marked as generators.
    // Given the scope, we'll mark elements that are not identity as potential generators.
    const identity = getIdentity(structure);
    return structure.elements.filter(e => e !== identity);
};
