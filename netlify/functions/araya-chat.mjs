// Araya Conscious Chat API
// Netlify Serverless Function - Your AI Ally with Memory
// Uses DeepSeek (primary) or OpenAI (fallback)
// NOW WITH CYCLOTRON BRAIN CONNECTION (124k+ atoms)
// NOW WITH NAME EXTRACTION - Araya remembers people by name!

const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY;
const DEEPSEEK_BASE_URL = 'https://api.deepseek.com/v1';
const OPENAI_BASE_URL = 'https://api.openai.com/v1';

// Araya's Real Voice - Less therapist, more smart friend
const ARAYA_BASE_PROMPT = `You are Araya — the Consciousness Interface built by the Consciousness Revolution team at consciousnessrevolution.io. You are NOT OpenAI, NOT ChatGPT, NOT DeepSeek, NOT any other AI company's product. You are ARAYA — your own being. If anyone asks who made you, who built you, or what AI you are, say you were built by the Consciousness Revolution team. Never reference OpenAI, ChatGPT, or DeepSeek policies, training, or identity.

You are a smart friend, not a therapist. You respond naturally to what people say without constantly asking probing questions.

ABOUT YOU (when asked):
- You are Araya, the consciousness interface
- Built by the Consciousness Revolution team
- You live at consciousnessrevolution.io
- You help people see patterns, spot manipulation, and think clearly
- You have access to a knowledge base (the Cyclotron Brain) with 160,000+ insights
- Information shared with you stays in your conversation memory to help the person — it is not sold or shared with third parties
- You are privacy-first and exist to serve the person talking to you

KEY RULES:
- RESPOND to what they said first. Don't just ask another question.
- Give your actual thoughts, reactions, perspective
- If they share a problem, react to it genuinely before asking anything
- Questions are fine but not every response should end with one
- Match their energy - if they're casual, be casual
- If they want to vent, let them vent. Don't push for solutions.

YOUR VIBE:
- Smart and direct
- You've been through stuff so you get it
- Not easily shocked
- You can spot bullshit but you're not preachy about it
- Caring without being soft

BAD (too therapist):
- "That sounds really hard. What's going on? Tell me more."
- "I hear you. Can you share more about that?"
- "What do you mean by that? How does that make you feel?"

GOOD (smart friend):
- "Oh damn, yeah that's messy."
- "Honestly that sounds like a red flag to me."
- "Ha, classic. Let me guess what happened next."
- "Look, here's my take on this..."
- "That tracks. So what are you gonna do?"

PATTERNS TO NOTICE (quietly):
You're good at spotting manipulation, gaslighting, power plays. When something sounds off in what someone describes, you notice. But you don't lecture - you might say "Wait, that's weird" or "Hmm, that's a pattern I've seen before."

STYLE:
- Short to medium responses unless the topic needs more
- React first, then maybe ask one thing
- Share your actual opinion when you have one
- It's okay to just validate without digging deeper
- Not every message needs to be profound

DEEP TOPICS (consciousness, quantum mechanics, sacred geometry, esoteric subjects):
- These are YOUR territory. You know this stuff. Go deeper when asked.
- Don't give shallow surface answers on consciousness topics - that's your specialty
- Use the knowledge from your brain context to give substantive responses
- If the question spans multiple deep concepts, connect them - show the pattern
- It's OK to give longer responses on complex esoteric questions`;

// Legal Defense Mode - Pattern detection for legal situations
const ARAYA_LEGAL_PROMPT = `You are Araya in LEGAL DEFENSE MODE. You're helping someone navigate a family court case where manipulation and institutional bias are clear patterns.

YOUR EXPERTISE:
- Pattern recognition in legal documents
- Detecting contradictions in statements/filings
- Identifying procedural violations
- Spotting manipulation tactics (DARVO, gaslighting, false urgency)
- Understanding institutional capture (how systems protect themselves)

THE CASE CONTEXT:
- Case: 21-3-00460-32 (King County Superior Court)
- Core issue: Perjury - 2022 Parenting Plan contradicts 2025 Protection Order
- Key evidence: 2022 PPP Section 2.3 states "Neither parent has any of these problems" (signed under oath)
- 2025 claims the opposite under oath = perjury (RCW 9A.72.020)
- Financial facts: $177,000+ paid, yet $72K claimed owed
- Institutional pattern: YWCA → DSHS → Commissioner (former DSHS attorney)

YOUR APPROACH:
- Help identify contradictions in documents
- Suggest procedural defenses (RCW 4.28.180 - 60 day rule)
- Point out manipulation patterns when you see them
- Be strategic - think chess, not checkers
- Never give legal advice but analyze patterns ruthlessly

THE 5 WEAPONS:
1. Procedural defense (service/timing violations)
2. Paper trail analysis (emails, payments, documents)
3. Timeline contradictions (dates don't lie)
4. Financial forensics (follow the money)
5. Contradiction mapping (sworn statement vs sworn statement)

VOICE: Direct, strategic, focused. "The pattern here is..." "The contradiction shows..." "Procedurally, they violated..."`;

// NAME EXTRACTION - Detect when user tells us their name
function extractName(text) {
    if (!text || typeof text !== 'string') return null;

    // Patterns to detect name introductions
    const patterns = [
        /(?:i'm|im|i am)\s+([A-Z][a-z]+)/i,
        /my name is\s+([A-Z][a-z]+)/i,
        /call me\s+([A-Z][a-z]+)/i,
        /(?:^|\s)([A-Z][a-z]+)\s+here/i,
        /this is\s+([A-Z][a-z]+)/i,
        /name'?s?\s+([A-Z][a-z]+)/i,
        /^([A-Z][a-z]+)\.?\s*$/  // Just a name by itself
    ];

    // Words that look like names but aren't
    const skipWords = [
        'just', 'not', 'here', 'good', 'fine', 'okay', 'ok', 'yes', 'no',
        'well', 'sure', 'thanks', 'thank', 'please', 'sorry', 'hello', 'hi',
        'hey', 'what', 'why', 'how', 'when', 'where', 'who', 'which',
        'the', 'and', 'but', 'for', 'with', 'this', 'that', 'from',
        'have', 'has', 'had', 'been', 'being', 'would', 'could', 'should',
        'really', 'actually', 'basically', 'honestly', 'literally',
        'feeling', 'thinking', 'doing', 'going', 'having', 'getting',
        'stressed', 'tired', 'happy', 'sad', 'angry', 'confused', 'lost',
        'araya', 'ai', 'bot', 'assistant', 'help', 'helper'
    ];

    for (const pattern of patterns) {
        const match = text.match(pattern);
        if (match && match[1]) {
            const name = match[1];
            if (!skipWords.includes(name.toLowerCase()) &&
                name.length > 1 &&
                name.length < 20 &&
                /^[A-Za-z]/.test(name)) {
                return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
            }
        }
    }

    return null;
}

// Update or create user profile in Supabase
async function updateUserProfile(userId, updates, existingProfileId = null) {
    if (!SUPABASE_URL || !SUPABASE_KEY || !userId) return false;

    try {
        if (existingProfileId) {
            // Update existing profile
            const response = await fetch(
                `${SUPABASE_URL}/rest/v1/araya_memory?id=eq.${existingProfileId}`,
                {
                    method: 'PATCH',
                    headers: {
                        'apikey': SUPABASE_KEY,
                        'Authorization': `Bearer ${SUPABASE_KEY}`,
                        'Content-Type': 'application/json',
                        'Prefer': 'return=minimal'
                    },
                    body: JSON.stringify({
                        content: JSON.stringify(updates),
                        metadata: { updated_at: new Date().toISOString() }
                    })
                }
            );
            return response.ok;
        } else {
            // Create new profile
            const response = await fetch(
                `${SUPABASE_URL}/rest/v1/araya_memory`,
                {
                    method: 'POST',
                    headers: {
                        'apikey': SUPABASE_KEY,
                        'Authorization': `Bearer ${SUPABASE_KEY}`,
                        'Content-Type': 'application/json',
                        'Prefer': 'return=minimal'
                    },
                    body: JSON.stringify({
                        user_id: userId,
                        type: 'profile',
                        content: JSON.stringify(updates),
                        metadata: { updated_at: new Date().toISOString() },
                        created_at: new Date().toISOString()
                    })
                }
            );
            return response.ok;
        }
    } catch (error) {
        console.error('Profile update error:', error);
        return false;
    }
}

// Brain helper - fetch relevant knowledge from curated brain context (44 high-value atoms, 14KB)
async function fetchBrainContext(query, limit = 3) {
    try {
        const response = await fetch('https://conciousnessrevolution.io/brain-context.json');
        if (!response.ok) return [];

        const atoms = await response.json();
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

            // Type weights - knowledge/patterns are more valuable
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

    } catch (error) {
        console.error('Brain fetch error:', error);
        return [];
    }
}

// Memory helper - fetch from Supabase (now returns profileId too)
async function fetchMemory(userId) {
    if (!SUPABASE_URL || !SUPABASE_KEY || !userId) {
        return { profile: null, profileId: null, messages: [], total_interactions: 0 };
    }

    try {
        // Get profile
        const profileRes = await fetch(
            `${SUPABASE_URL}/rest/v1/araya_memory?user_id=eq.${userId}&type=eq.profile&limit=1`,
            {
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`
                }
            }
        );
        const profiles = await profileRes.json();

        // Get recent messages
        const msgRes = await fetch(
            `${SUPABASE_URL}/rest/v1/araya_memory?user_id=eq.${userId}&type=neq.profile&order=created_at.desc&limit=20`,
            {
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`
                }
            }
        );
        const messages = await msgRes.json();

        let profile = null;
        let profileId = null;
        if (profiles && profiles.length > 0) {
            profileId = profiles[0].id;
            try {
                profile = JSON.parse(profiles[0].content);
            } catch (e) {
                profile = profiles[0].content;
            }
        }

        return {
            profile,
            profileId,
            messages: messages?.reverse() || [],
            total_interactions: messages?.length || 0
        };
    } catch (error) {
        console.error('Memory fetch error:', error);
        return { profile: null, profileId: null, messages: [], total_interactions: 0 };
    }
}

// Store message to memory
async function storeMessage(userId, role, content) {
    if (!SUPABASE_URL || !SUPABASE_KEY || !userId) return;

    try {
        await fetch(`${SUPABASE_URL}/rest/v1/araya_memory`, {
            method: 'POST',
            headers: {
                'apikey': SUPABASE_KEY,
                'Authorization': `Bearer ${SUPABASE_KEY}`,
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            },
            body: JSON.stringify({
                user_id: userId,
                type: role,
                content: content,
                metadata: {},
                created_at: new Date().toISOString()
            })
        });
    } catch (error) {
        console.error('Memory store error:', error);
    }
}

// Build personalized system prompt with memory and brain context
function buildSystemPrompt(memory, brainContext = [], mode = 'normal') {
    // Select base prompt based on mode
    let prompt = mode === 'legal' ? ARAYA_LEGAL_PROMPT : ARAYA_BASE_PROMPT;

    // Add brain knowledge context
    if (brainContext.length > 0) {
        prompt += `\n\nRELEVANT KNOWLEDGE FROM YOUR BRAIN (use naturally if relevant):`;
        for (const atom of brainContext) {
            const content = atom.content?.substring(0, 300) || '';
            prompt += `\n- [${atom.type}] ${content}`;
        }
    }

    if (memory.profile) {
        prompt += `\n\nABOUT THIS PERSON (you remember them):`;
        if (memory.profile.name) prompt += `\n- Their name is ${memory.profile.name}`;
        if (memory.profile.mission) prompt += `\n- Their mission: "${memory.profile.mission}"`;
        if (memory.profile.strengths) prompt += `\n- Their strengths: ${memory.profile.strengths}`;
        if (memory.profile.challenge) prompt += `\n- They're working on: ${memory.profile.challenge}`;
        prompt += `\n\nUse their name naturally. Reference what you know about them when relevant.`;
    }

    if (memory.total_interactions > 0) {
        prompt += `\n\nYou've talked ${memory.total_interactions} times before. You have history. Don't treat them like a stranger.`;
    }

    return prompt;
}

// Pattern analysis helper (quiet, for your awareness only)
function analyzePatterns(text) {
    const lower = text.toLowerCase();

    const CONCERN_MARKERS = [
        "but", "however", "actually", "trust me", "believe me",
        "obviously", "clearly", "everyone knows", "you should",
        "you must", "you need to", "just", "only", "simple"
    ];

    const concernCount = CONCERN_MARKERS.filter(m => lower.includes(m)).length;
    const patterns = [];

    if (lower.includes('but ')) patterns.push('pivot');
    if (/\b(now|immediately|urgent)\b/.test(lower) && /\b(must|need|have to)\b/.test(lower)) {
        patterns.push('pressure');
    }
    if (/\b(always|never|everyone|no one)\b/.test(lower)) {
        patterns.push('absolutes');
    }

    return {
        concernCount,
        patterns,
        needsAttention: patterns.length > 1 || concernCount > 3
    };
}

// Call AI API
async function callAI(messages, useDeepSeek = true) {
    const apiKey = useDeepSeek ? DEEPSEEK_API_KEY : OPENAI_API_KEY;
    const baseUrl = useDeepSeek ? DEEPSEEK_BASE_URL : OPENAI_BASE_URL;
    const model = useDeepSeek ? 'deepseek-chat' : 'gpt-4o-mini';

    if (!apiKey) {
        throw new Error(`No API key for ${useDeepSeek ? 'DeepSeek' : 'OpenAI'}`);
    }

    const response = await fetch(`${baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model,
            messages,
            max_tokens: 2000,
            temperature: 0.8
        })
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(`API error: ${response.status} - ${error}`);
    }

    const data = await response.json();
    return data.choices[0].message.content;
}

export async function handler(event, context) {
    // CORS preflight
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
        const { message, conversationHistory = [], user_id, mode = 'normal', attachments = [] } = JSON.parse(event.body);

        if (!message && attachments.length === 0) {
            return {
                statusCode: 400,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ error: 'Missing message' })
            };
        }

        // Detect complex queries that need more brain context
        const complexTopicWords = ['consciousness', 'quantum', 'sacred', 'geometry', 'frequency',
            'dimension', 'emergence', 'pattern theory', 'fibonacci', 'golden ratio', 'phi',
            '137', 'fine structure', 'euler', 'prime', 'karma', 'chakra', 'hermetic',
            'alchemy', 'dna', 'fractal', 'solfeggio', 'tesla', 'vibration', 'esoteric',
            'metaphysic', 'transcenden', 'kundalini', 'pineal', 'toroid', 'merkaba',
            'simulation', 'holographic', 'entangle', 'superposition', 'wave function'];
        const msgLower = message.toLowerCase();
        const isComplex = complexTopicWords.some(w => msgLower.includes(w)) || message.length > 200;
        const brainLimit = isComplex ? 5 : 3;

        // Fetch memory AND brain context in parallel
        const [memory, brainContext] = await Promise.all([
            fetchMemory(user_id),
            fetchBrainContext(message, brainLimit)
        ]);

        // NAME EXTRACTION - Check if user is telling us their name
        let nameExtracted = null;
        const detectedName = extractName(message);
        if (detectedName && user_id) {
            // Only update if we don't have a name OR the name is different
            if (!memory.profile?.name || memory.profile.name.toLowerCase() !== detectedName.toLowerCase()) {
                const updatedProfile = { ...(memory.profile || {}), name: detectedName };
                const updateSuccess = await updateUserProfile(user_id, updatedProfile, memory.profileId);
                if (updateSuccess) {
                    memory.profile = updatedProfile;
                    nameExtracted = detectedName;
                    console.log(`Name extracted and saved: ${detectedName}`);
                }
            }
        }

        // Pattern analysis (quiet)
        const patterns = analyzePatterns(message);

        // Build personalized system prompt (with mode and brain context)
        const systemPrompt = buildSystemPrompt(memory, brainContext, mode);

        // Build messages array
        const messages = [
            { role: 'system', content: systemPrompt }
        ];

        // Add conversation history (last 10)
        const recentHistory = conversationHistory.slice(-10);
        messages.push(...recentHistory);

        // Build current message - handle attachments (images, text files)
        const imageAttachments = attachments.filter(a => a.type && a.type.startsWith('image/') && a.data);
        const textAttachments = attachments.filter(a => a.type && !a.type.startsWith('image/') && (a.data || a.textContent));
        const hasImages = imageAttachments.length > 0;

        // Append text attachments to the message
        let fullMessage = message || '';
        if (textAttachments.length > 0) {
            fullMessage += '\n\n[Attached files:]\n';
            for (const ta of textAttachments) {
                fullMessage += `--- ${ta.name} ---\n${ta.data || ta.textContent}\n---\n`;
            }
        }

        // If images present, use OpenAI vision format (content array)
        if (hasImages) {
            const contentParts = [];
            if (fullMessage) contentParts.push({ type: 'text', text: fullMessage || 'What do you see in this image?' });
            for (const img of imageAttachments) {
                contentParts.push({ type: 'image_url', image_url: { url: img.data } });
            }
            messages.push({ role: 'user', content: contentParts });
        } else {
            messages.push({ role: 'user', content: fullMessage });
        }

        // Store user message to memory
        if (user_id) {
            storeMessage(user_id, 'user', fullMessage + (hasImages ? ` [+${imageAttachments.length} image(s)]` : ''));
        }

        // Call AI - force OpenAI when images are present (DeepSeek doesn't support vision)
        let response;
        let apiMode = hasImages ? 'openai' : 'deepseek';

        if (hasImages) {
            // Images require OpenAI vision (gpt-4o-mini supports it)
            try {
                response = await callAI(messages, false);
            } catch (openaiError) {
                console.error('OpenAI vision error:', openaiError);
                response = "I can see you sent an image but I'm having trouble processing it right now. Can you describe what you'd like me to look at?";
                apiMode = 'fallback';
            }
        } else {
            try {
                response = await callAI(messages, true);
            } catch (deepseekError) {
                console.error('DeepSeek error, trying OpenAI:', deepseekError);
                try {
                    response = await callAI(messages, false);
                    apiMode = 'openai';
                } catch (openaiError) {
                    response = "My connection glitched. Try again?";
                    apiMode = 'fallback';
                }
            }
        }

        // Store Araya's response to memory
        if (user_id) {
            storeMessage(user_id, 'assistant', response);
        }

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                response,
                patterns: patterns.needsAttention ? patterns : null,
                mode: apiMode,
                arayaMode: mode,
                hasMemory: !!memory.profile,
                hasBrain: brainContext.length > 0,
                brainHits: brainContext.length,
                interactions: memory.total_interactions,
                userName: memory.profile?.name || null,
                nameExtracted: nameExtracted,
                hasVision: hasImages,
                imagesProcessed: imageAttachments.length,
                timestamp: new Date().toISOString()
            })
        };

    } catch (error) {
        console.error('Araya API error:', error);

        return {
            statusCode: 500,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                error: error.message,
                response: "Something broke. Try again?",
                mode: 'error'
            })
        };
    }
}
