#!/usr/bin/env python3
"""Update araya-chat.mjs with name extraction functionality"""

# Read the backup file
with open('araya-chat.mjs.backup', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add comment about name extraction
content = content.replace(
    '// NOW WITH CYCLOTRON BRAIN CONNECTION (124k+ atoms)\n\nconst DEEPSEEK_API_KEY',
    '''// NOW WITH CYCLOTRON BRAIN CONNECTION (124k+ atoms)
// NOW WITH NAME EXTRACTION - Araya remembers people by name!

const DEEPSEEK_API_KEY'''
)

# 2. Add extractName function after ARAYA_LEGAL_PROMPT
name_extraction_code = '''

// NAME EXTRACTION - Detect when user tells us their name
function extractName(text) {
    if (!text || typeof text !== 'string') return null;

    // Patterns to detect name introductions
    const patterns = [
        /(?:i'm|im|i am)\\s+([A-Z][a-z]+)/i,
        /my name is\\s+([A-Z][a-z]+)/i,
        /call me\\s+([A-Z][a-z]+)/i,
        /(?:^|\\s)([A-Z][a-z]+)\\s+here/i,
        /this is\\s+([A-Z][a-z]+)/i,
        /name'?s?\\s+([A-Z][a-z]+)/i,
        /^([A-Z][a-z]+)\\.?\\s*$/  // Just a name by itself
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

// Brain helper'''

content = content.replace(
    'VOICE: Direct, strategic, focused. "The pattern here is..." "The contradiction shows..." "Procedurally, they violated..."`;\n\n// Brain helper',
    'VOICE: Direct, strategic, focused. "The pattern here is..." "The contradiction shows..." "Procedurally, they violated..."`;' + name_extraction_code
)

# 3. Update fetchMemory to return profileId
content = content.replace(
    '''// Memory helper - fetch from Supabase
async function fetchMemory(userId) {
    if (!SUPABASE_URL || !SUPABASE_KEY || !userId) {
        return { profile: null, messages: [], total_interactions: 0 };
    }''',
    '''// Memory helper - fetch from Supabase (now returns profileId too)
async function fetchMemory(userId) {
    if (!SUPABASE_URL || !SUPABASE_KEY || !userId) {
        return { profile: null, profileId: null, messages: [], total_interactions: 0 };
    }'''
)

# 4. Update fetchMemory to capture profileId
content = content.replace(
    '''let profile = null;
        if (profiles && profiles.length > 0) {
            try {
                profile = JSON.parse(profiles[0].content);
            } catch (e) {
                profile = profiles[0].content;
            }
        }

        return {
            profile,
            messages: messages?.reverse() || [],
            total_interactions: messages?.length || 0
        };
    } catch (error) {
        console.error('Memory fetch error:', error);
        return { profile: null, messages: [], total_interactions: 0 };
    }
}''',
    '''let profile = null;
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
}'''
)

# 5. Add name extraction logic in handler
content = content.replace(
    '''// Pattern analysis (quiet)
        const patterns = analyzePatterns(message);''',
    '''// NAME EXTRACTION - Check if user is telling us their name
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
        const patterns = analyzePatterns(message);'''
)

# 6. Update response to include userName and nameExtracted
content = content.replace(
    '''interactions: memory.total_interactions,
                timestamp: new Date().toISOString()''',
    '''interactions: memory.total_interactions,
                userName: memory.profile?.name || null,
                nameExtracted: nameExtracted,
                timestamp: new Date().toISOString()'''
)

# Write the updated content
with open('araya-chat.mjs', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: araya-chat.mjs updated with name extraction!")
print("Changes made:")
print("  1. Added header comment about name extraction")
print("  2. Added extractName() function")
print("  3. Added updateUserProfile() function")
print("  4. Updated fetchMemory() to return profileId")
print("  5. Added name extraction logic in handler")
print("  6. Added userName and nameExtracted to response")
