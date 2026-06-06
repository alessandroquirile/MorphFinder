import {useState} from 'react';
import type {Structure, Homomorphism} from '../../domain/models/types';
import {MorphismApiClient} from '../api/morphismApiClient';

export const useFindMorphisms = () => {
    const [homomorphisms, setHomomorphisms] = useState<Homomorphism[]>([]);
    const [strategy, setStrategy] = useState<string>('');
    const [timeElapsed, setTimeElapsed] = useState<number>(0);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const findMorphisms = async (source: Structure | null, target: Structure | null) => {
        if (!source || !target) return;
        
        setLoading(true);
        setError(null);
        
        try {
            const data = await MorphismApiClient.findMorphisms(source, target);
            setHomomorphisms(data.homomorphisms);
            setStrategy(data.strategy);
            setTimeElapsed(data.time_elapsed);
            return data.homomorphisms;
        } catch (err) {
            const message = err instanceof Error ? err.message : 'An unknown error occurred.';
            setError(message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return {
        homomorphisms,
        strategy,
        timeElapsed,
        loading,
        error,
        findMorphisms,
        setHomomorphisms
    };
};
