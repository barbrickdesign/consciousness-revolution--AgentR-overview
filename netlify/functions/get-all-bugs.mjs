// Get All Bugs - Netlify Function
// Fetches bug reports from GitHub Issues

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const REPO_OWNER = 'overkillkulture';
const REPO_NAME = 'consciousness-bugs';

export async function handler(event, context) {
    // Handle CORS preflight
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            body: ''
        };
    }

    try {
        const headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Consciousness-Revolution-Bug-Tracker'
        };

        // Add auth if token exists (higher rate limit)
        if (GITHUB_TOKEN) {
            headers['Authorization'] = `token ${GITHUB_TOKEN}`;
        }

        const response = await fetch(
            `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/issues?state=all&per_page=100`,
            { headers }
        );

        if (!response.ok) {
            // If repo doesn't exist or is private, return empty array
            if (response.status === 404) {
                return {
                    statusCode: 200,
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ bugs: [], message: 'Bug repo not found' })
                };
            }
            throw new Error(`GitHub API error: ${response.status}`);
        }

        const issues = await response.json();

        // Transform to bug format
        const bugs = issues.map(issue => ({
            id: issue.number,
            title: issue.title,
            description: issue.body || '',
            status: issue.state,
            priority: issue.labels.find(l => l.name.includes('priority'))?.name || 'normal',
            labels: issue.labels.map(l => l.name),
            created: issue.created_at,
            updated: issue.updated_at,
            url: issue.html_url
        }));

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'Cache-Control': 'public, max-age=60'  // Cache for 1 minute
            },
            body: JSON.stringify({
                bugs,
                total: bugs.length,
                open: bugs.filter(b => b.status === 'open').length,
                closed: bugs.filter(b => b.status === 'closed').length,
                timestamp: new Date().toISOString()
            })
        };

    } catch (error) {
        console.error('Get bugs error:', error);
        return {
            statusCode: 500,
            headers: { 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({ error: 'Failed to fetch bugs', bugs: [] })
        };
    }
}
