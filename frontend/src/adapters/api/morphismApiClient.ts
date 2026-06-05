import type {Structure, MorphismResponse} from '../../domain/models/types';

export class MorphismApiClient {
    private static BASE_URL = 'http://localhost:8000/v1';

    static async findMorphisms(source: Structure, target: Structure): Promise<MorphismResponse> {
        const response = await fetch(`${this.BASE_URL}/morphisms/find`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({source, target}),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to find morphisms');
        }

        return data;
    }
}
