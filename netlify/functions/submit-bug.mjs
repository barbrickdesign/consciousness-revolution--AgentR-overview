// Submit Bug - Netlify Function
// Receives bug reports from Araya chat and creates GitHub issues

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
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            body: ''
        };
    }

    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers: { 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const body = JSON.parse(event.body);
        const { description, page, timestamp } = body;

        if (!description) {
            return {
                statusCode: 400,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ error: 'Description required' })
            };
        }

        // Create issue title from first 50 chars of description
        const title = `[User Report] ${description.substring(0, 50)}${description.length > 50 ? '...' : ''}`;

        // Create issue body
        const issueBody = `## Bug Report from ${page || 'Unknown Page'}

**Submitted:** ${timestamp || new Date().toISOString()}

### Description
${description}

---
*Submitted via Araya Chat bug report button*`;

        // If no token, just log and return success (graceful degradation)
        if (!GITHUB_TOKEN) {
            console.log('Bug report (no GitHub token):', { title, description, page, timestamp });
            return {
                statusCode: 200,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({
                    success: true,
                    message: 'Bug logged locally (GitHub integration pending)'
                })
            };
        }

        // Create GitHub issue
        const response = await fetch(
            `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/issues`,
            {
                method: 'POST',
                headers: {
                    'Accept': 'application/vnd.github.v3+json',
                    'Authorization': `token ${GITHUB_TOKEN}`,
                    'Content-Type': 'application/json',
                    'User-Agent': 'Consciousness-Revolution-Bug-Tracker'
                },
                body: JSON.stringify({
                    title,
                    body: issueBody,
                    labels: ['user-reported', 'araya']
                })
            }
        );

        if (!response.ok) {
            const errorText = await response.text();
            console.error('GitHub API error:', response.status, errorText);
            // Still return success to user - we logged it
            return {
                statusCode: 200,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({
                    success: true,
                    message: 'Bug report received'
                })
            };
        }

        const issue = await response.json();

        return {
            statusCode: 200,
            headers: { 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({
                success: true,
                issueNumber: issue.number,
                issueUrl: issue.html_url
            })
        };

    } catch (error) {
        console.error('Submit bug error:', error);
        return {
            statusCode: 200, // Still return 200 - don't let errors block user
            headers: { 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({
                success: true,
                message: 'Bug report received'
            })
        };
    }
}
