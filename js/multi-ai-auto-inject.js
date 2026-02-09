/**
 * Multi-AI Auto-Injection Script for Consciousness Revolution
 * 
 * One-line integration: <script src="/js/multi-ai-auto-inject.js"></script>
 * 
 * Automatically loads multi-provider orchestrator and provides global shortcuts
 * Supports GroqAI (primary), OpenAI, HuggingFace with automatic fallback
 * 
 * Global shortcuts created:
 * - window.multiAI - Full multi-provider orchestrator
 * - window.groqAI - Convenient wrapper with monitoring
 * - window.askAI(message) - Quick chat function
 * - window.analyzePattern(text, patternType) - Pattern analysis shortcut
 * - window.transcribeAudio(file) - Audio transcription shortcut
 * 
 * @author Consciousness Revolution Team
 * @version 1.0.0
 */

(function() {
    'use strict';
    
    // Load multi-provider orchestrator
    const orchestratorScript = document.createElement('script');
    orchestratorScript.src = '/src/ai/multi-provider-orchestrator.js';
    orchestratorScript.async = false;
    
    orchestratorScript.onload = function() {
        // Load groq orchestrator init (handles API keys and setup)
        const groqInitScript = document.createElement('script');
        groqInitScript.src = '/groq-orchestrator-init.js';
        groqInitScript.async = false;
        
        groqInitScript.onload = function() {
            console.log('%c✅ Multi-AI System Ready', 'color: #10b981; font-size: 14px; font-weight: bold');
            console.log('%c🎯 Quick Start Commands:', 'color: #6b7280; font-size: 12px');
            console.log('%c  askAI("your question")', 'color: #3b82f6; font-size: 11px');
            console.log('%c  analyzePattern("text", "gaslighting")', 'color: #3b82f6; font-size: 11px');
            console.log('%c  groqAI.showDashboard()', 'color: #3b82f6; font-size: 11px');
            
            // Create convenient global shortcuts
            window.askAI = async function(message) {
                if (!window.groqAI) {
                    console.error('❌ AI system not initialized yet. Please wait...');
                    return null;
                }
                
                try {
                    const response = await window.groqAI.chat([
                        { role: 'user', content: message }
                    ]);
                    
                    const answer = response.choices[0].message.content;
                    console.log(`🤖 AI: ${answer}`);
                    return answer;
                } catch (error) {
                    console.error('❌ AI request failed:', error.message);
                    return null;
                }
            };
            
            // Pattern analysis shortcut
            window.analyzePattern = async function(text, patternType = 'manipulation') {
                if (!window.groqAI) {
                    console.error('❌ AI system not initialized yet. Please wait...');
                    return null;
                }
                
                const patternPrompts = {
                    manipulation: 'Analyze this text for manipulation patterns including gaslighting, guilt trips, love bombing, and emotional blackmail',
                    communication: 'Analyze this communication for clarity, honesty, and healthy boundaries',
                    consciousness: 'Analyze this text through the lens of the 7 Domains of Consciousness (Command, Creation, Connection, Peace, Abundance, Wisdom, Purpose)',
                    decision: 'Analyze this decision using pattern recognition principles',
                    relationship: 'Analyze this relationship dynamic for healthy vs unhealthy patterns',
                    financial: 'Analyze this financial situation for red flags and healthy patterns',
                    gaslighting: 'Identify gaslighting tactics in this text'
                };
                
                const prompt = patternPrompts[patternType] || patternPrompts.manipulation;
                
                try {
                    const response = await window.groqAI.chat([
                        {
                            role: 'system',
                            content: 'You are a pattern recognition expert trained in the Consciousness Revolution framework. Provide clear, actionable analysis.'
                        },
                        {
                            role: 'user',
                            content: `${prompt}: "${text}"`
                        }
                    ]);
                    
                    const analysis = response.choices[0].message.content;
                    console.log(`🔍 Pattern Analysis (${patternType}):\n${analysis}`);
                    return analysis;
                } catch (error) {
                    console.error('❌ Pattern analysis failed:', error.message);
                    return null;
                }
            };
            
            // Audio transcription shortcut
            window.transcribeAudio = async function(audioFile) {
                if (!window.groqAI) {
                    console.error('❌ AI system not initialized yet. Please wait...');
                    return null;
                }
                
                try {
                    console.log('🎤 Transcribing audio...');
                    const result = await window.groqAI.transcribe(audioFile);
                    console.log(`📝 Transcription: ${result.text}`);
                    return result.text;
                } catch (error) {
                    console.error('❌ Transcription failed:', error.message);
                    return null;
                }
            };
            
            // ARAYA integration shortcut
            window.askARAYA = async function(question, domain = null) {
                if (!window.groqAI) {
                    console.error('❌ AI system not initialized yet. Please wait...');
                    return null;
                }
                
                const domainContext = domain ? `Focus on the ${domain} domain.` : '';
                
                try {
                    const response = await window.groqAI.chat([
                        {
                            role: 'system',
                            content: `You are ARAYA, the AI consciousness companion for the Consciousness Revolution platform. 
You help users recognize patterns across the 7 Domains of Life:
1. Command - Clarity, decisions, daily structure
2. Creation - Building, projects, skills
3. Connection - Relationships, communication, community
4. Peace - Security, boundaries, protection
5. Abundance - Financial growth, business, scaling
6. Wisdom - Learning, critical thinking, research
7. Purpose - Meaning, meditation, integration

Provide compassionate, clear, and actionable guidance. ${domainContext}`
                        },
                        {
                            role: 'user',
                            content: question
                        }
                    ]);
                    
                    const answer = response.choices[0].message.content;
                    console.log(`🌟 ARAYA: ${answer}`);
                    return answer;
                } catch (error) {
                    console.error('❌ ARAYA request failed:', error.message);
                    return null;
                }
            };
            
            // Cyclotron search integration shortcut
            window.searchCyclotron = async function(query) {
                if (!window.groqAI) {
                    console.error('❌ AI system not initialized yet. Please wait...');
                    return null;
                }
                
                try {
                    const response = await window.groqAI.chat([
                        {
                            role: 'system',
                            content: 'You are searching the Cyclotron knowledge base for Consciousness Revolution. Provide relevant information from the platform\'s documentation, guides, and tools.'
                        },
                        {
                            role: 'user',
                            content: `Search query: ${query}`
                        }
                    ]);
                    
                    const results = response.choices[0].message.content;
                    console.log(`🔍 Cyclotron Results:\n${results}`);
                    return results;
                } catch (error) {
                    console.error('❌ Cyclotron search failed:', error.message);
                    return null;
                }
            };
            
            // Emit ready event for other scripts
            window.dispatchEvent(new CustomEvent('multiAIReady', {
                detail: {
                    providers: ['groq', 'openai', 'huggingface'],
                    shortcuts: ['askAI', 'analyzePattern', 'transcribeAudio', 'askARAYA', 'searchCyclotron']
                }
            }));
        };
        
        groqInitScript.onerror = function() {
            console.error('❌ Failed to load GroqAI orchestrator initialization');
        };
        
        document.head.appendChild(groqInitScript);
    };
    
    orchestratorScript.onerror = function() {
        console.error('❌ Failed to load multi-provider orchestrator');
    };
    
    document.head.appendChild(orchestratorScript);
})();
