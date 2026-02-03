// Brain Query API - Search Cyclotron knowledge base
// Netlify Serverless Function

import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// Load brain export at cold start
let brainData = null;

function loadBrain() {
    if (brainData) return brainData;

    try {
        // In Netlify, we need to load from the deployed files
        const response = fetch('https://conciousnessrevolution.io/brain-export.json');
        return null; // Will be loaded async
    } catch (error) {
        console.error('Brain load error:', error);
        return null;
    }
}

// Search brain for relevant knowledge
function searchBrain(atoms, query, limit = 5) {
    if (!atoms || !query) return [];

    const queryLower = query.toLowerCase();
    const queryWords = queryLower.split(/\s+/).filter(w => w.length > 2);

    // Score each atom by relevance
    const scored = atoms.map(atom => {
        const content = (atom.content || '').toLowerCase();
        let score = 0;

        // Exact phrase match
        if (content.includes(queryLower)) score += 10;

        // Word matches
        for (const word of queryWords) {
            if (content.includes(word)) score += 2;
        }

        // Type weights
        const typeWeights = {
            'knowledge': 1.5,
            'pattern': 1.4,
            'insight': 1.3,
            'concept': 1.2,
            'fact': 1.1,
            'ability': 1.0
        };
        score *= typeWeights[atom.type] || 1;

        return { ...atom, score };
    });

    // Return top matches
    return scored
        .filter(a => a.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, limit)
        .map(({ score, ...atom }) => atom);
}

export async function handler(event, context) {
    // CORS preflight
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
            },
            body: ''
        };
    }

    try {
        let query = '';
        let limit = 5;

        if (event.httpMethod === 'POST') {
            const body = JSON.parse(event.body || '{}');
            query = body.query || '';
            limit = body.limit || 5;
        } else if (event.httpMethod === 'GET') {
            query = event.queryStringParameters?.query || '';
            limit = parseInt(event.queryStringParameters?.limit) || 5;
        }

        if (!query) {
            return {
                statusCode: 400,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ error: 'Missing query parameter' })
            };
        }

        // Fetch brain data
        const brainResponse = await fetch('https://conciousnessrevolution.io/brain-export.json');
        if (!brainResponse.ok) {
            throw new Error('Failed to load brain data');
        }
        const atoms = await brainResponse.json();

        // Search
        const results = searchBrain(atoms, query, limit);

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query,
                count: results.length,
                atoms: results,
                timestamp: new Date().toISOString()
            })
        };

    } catch (error) {
        console.error('Brain query error:', error);
        return {
            statusCode: 500,
            headers: { 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({ error: error.message })
        };
    }
}
