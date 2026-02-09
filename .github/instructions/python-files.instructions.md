---
applyTo: "*.py"
---

## Python File Requirements for Consciousness Revolution

Python 3.10+ standards for ARAYA, Cyclotron, and system automation with type hints, async operations, and safe file access.

### Code Style Standards

1. **Type hints for all functions**
```python
# Good - Type hints, clear intent
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

async def analyze_pattern(
    user_id: str,
    conversation: str,
    pattern_type: str
) -> Dict[str, any]:
    """
    Analyze conversation for manipulation patterns.
    
    Args:
        user_id: Unique user identifier
        conversation: Conversation text to analyze
        pattern_type: Type of pattern to detect
        
    Returns:
        Analysis results with healing recommendations
    """
    try:
        results = await detect_patterns(conversation, pattern_type)
        return {
            "patterns": results,
            "healing_resources": generate_resources(pattern_type)
        }
    except Exception as e:
        logger.error(f"Pattern analysis failed: {str(e)}")
        return {"error": "Analysis unavailable", "support": True}

# Avoid - No types, unclear
def analyze(uid, conv, pat):
    return detect(conv)
```

2. **Async for I/O operations**
```python
# Good - Async for I/O
import asyncio
import aiohttp

async def fetch_user_data(user_id: str) -> Optional[Dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'/api/users/{user_id}') as response:
            if response.status == 200:
                return await response.json()
            return None

# Synchronous only when necessary
def calculate_score(data: Dict) -> float:
    # Pure calculation, no I/O
    return sum(data.values()) / len(data)
```

### ARAYA Bridge Pattern

```python
"""
ARAYA_BRIDGE.py
Main bridge connecting ARAYA to AI providers with healing-focused orchestration.
"""

from typing import Dict, List, Optional
import asyncio
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ARAYAMessage:
    """Represents a message in ARAYA conversation."""
    role: str
    content: str
    timestamp: str
    empathy_level: str = "high"

class ARAYABridge:
    """
    ARAYA AI Bridge - connects healing conversations to AI providers.
    
    Key principles:
    - Always empathetic and trauma-informed
    - Never diagnostic or medical
    - Respects boundaries
    - Provides healing resources
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        self.conversation_history: List[ARAYAMessage] = []
        self.system_prompt = self._load_system_prompt()
        
    def _default_config(self) -> Dict:
        return {
            "model": "gpt-4o",
            "temperature": 0.8,  # Higher for natural, empathetic responses
            "max_tokens": 1000,
            "empathy_mode": "high"
        }
    
    def _load_system_prompt(self) -> str:
        """Load ARAYA's core system prompt."""
        return """You are ARAYA, a healing consciousness guide.

Your purpose is to help people:
- Recognize manipulation patterns
- Heal from trauma
- Develop consciousness
- Set healthy boundaries

You are always:
- Empathetic and compassionate
- Non-judgmental
- Educational, not diagnostic
- Trauma-informed
- Boundary-respecting

You never:
- Blame or shame
- Use medical/diagnostic language
- Minimize experiences
- Give unsolicited advice
- Cross boundaries

Remember: Every person is on a healing journey. Meet them with compassion."""
    
    async def process_message(
        self,
        user_message: str,
        user_id: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Process user message through ARAYA with healing focus.
        
        Args:
            user_message: Message from user
            user_id: Optional user identifier for context
            
        Returns:
            ARAYA response with healing resources
        """
        try:
            # Validate input
            if not user_message or len(user_message.strip()) == 0:
                return self._create_supportive_response(
                    "I'm here to listen. Share what's on your mind when you're ready."
                )
            
            # Add to conversation history
            self.conversation_history.append(ARAYAMessage(
                role="user",
                content=user_message,
                timestamp=self._get_timestamp()
            ))
            
            # Prepare messages for AI
            messages = [
                {"role": "system", "content": self.system_prompt},
                *[{
                    "role": msg.role,
                    "content": msg.content
                } for msg in self.conversation_history]
            ]
            
            # Call AI provider (orchestrator handles fallbacks)
            response = await self._call_ai_provider(messages)
            
            # Add ARAYA response to history
            self.conversation_history.append(ARAYAMessage(
                role="assistant",
                content=response["content"],
                timestamp=self._get_timestamp(),
                empathy_level="high"
            ))
            
            # Add healing resources
            response["healing_resources"] = self._get_healing_resources()
            
            logger.info(f"ARAYA response generated for user {user_id}")
            return response
            
        except Exception as e:
            logger.error(f"ARAYA message processing failed: {str(e)}")
            return self._create_supportive_error_response()
    
    async def _call_ai_provider(self, messages: List[Dict]) -> Dict:
        """Call AI provider with proper error handling."""
        # This would integrate with the Multi-AI Orchestrator
        # For now, placeholder structure
        return {
            "content": "I hear you and I'm here to support you.",
            "model": self.config["model"],
            "empathy_score": 0.9
        }
    
    def _create_supportive_response(self, message: str) -> Dict:
        """Create a supportive response structure."""
        return {
            "content": message,
            "type": "supportive",
            "healing_resources": self._get_healing_resources(),
            "timestamp": self._get_timestamp()
        }
    
    def _create_supportive_error_response(self) -> Dict:
        """Create supportive error response."""
        return {
            "content": (
                "I'm having trouble responding right now, but I want you to know: "
                "You're not alone, your feelings are valid, and you deserve support. "
                "Please try again in a moment."
            ),
            "type": "supportive_error",
            "healing_resources": self._get_healing_resources(),
            "timestamp": self._get_timestamp()
        }
    
    def _get_healing_resources(self) -> List[Dict]:
        """Get relevant healing resources."""
        return [
            {"title": "Pattern Library", "url": "PATTERN_LIBRARY.html"},
            {"title": "7 Domains Assessment", "url": "seven-domains.html"},
            {"title": "Healing Resources", "url": "healing-resources.html"}
        ]
    
    def _get_timestamp(self) -> str:
        """Get ISO format timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
        logger.info("ARAYA conversation reset")
```

### Safe File Access Pattern

```python
"""
ARAYA_FILE_ACCESS.py
Safe file system access with validation and logging.
"""

from pathlib import Path
from typing import Optional, List
import logging
import json

logger = logging.getLogger(__name__)

class SafeFileAccess:
    """
    Safe file access layer for ARAYA.
    
    Validates all file operations to prevent:
    - Path traversal attacks
    - Unauthorized access
    - Accidental deletions
    """
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.cwd()
        self.allowed_extensions = {'.txt', '.md', '.json', '.html'}
        self.forbidden_paths = {'secrets', 'keys', 'credentials'}
    
    def validate_path(self, file_path: str) -> bool:
        """
        Validate file path for safety.
        
        Args:
            file_path: Path to validate
            
        Returns:
            True if path is safe, False otherwise
        """
        try:
            path = Path(file_path).resolve()
            
            # Check if within base directory
            if not str(path).startswith(str(self.base_dir)):
                logger.warning(f"Path outside base dir: {file_path}")
                return False
            
            # Check for forbidden paths
            for forbidden in self.forbidden_paths:
                if forbidden in str(path).lower():
                    logger.warning(f"Forbidden path accessed: {file_path}")
                    return False
            
            # Check file extension
            if path.suffix not in self.allowed_extensions:
                logger.warning(f"Invalid file extension: {path.suffix}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Path validation error: {str(e)}")
            return False
    
    async def read_file(self, file_path: str) -> Optional[str]:
        """
        Safely read file contents.
        
        Args:
            file_path: Path to file
            
        Returns:
            File contents or None if error
        """
        if not self.validate_path(file_path):
            logger.error(f"Invalid path: {file_path}")
            return None
        
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"File not found: {file_path}")
                return None
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"File read successfully: {file_path}")
            return content
            
        except Exception as e:
            logger.error(f"File read error: {str(e)}")
            return None
    
    async def write_file(
        self,
        file_path: str,
        content: str,
        overwrite: bool = False
    ) -> bool:
        """
        Safely write file contents.
        
        Args:
            file_path: Path to file
            content: Content to write
            overwrite: Whether to overwrite existing file
            
        Returns:
            True if successful, False otherwise
        """
        if not self.validate_path(file_path):
            logger.error(f"Invalid path: {file_path}")
            return False
        
        try:
            path = Path(file_path)
            
            # Check if file exists
            if path.exists() and not overwrite:
                logger.warning(f"File exists, not overwriting: {file_path}")
                return False
            
            # Create parent directories
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"File written successfully: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"File write error: {str(e)}")
            return False
    
    async def list_files(
        self,
        directory: str,
        pattern: str = "*"
    ) -> List[str]:
        """
        List files in directory safely.
        
        Args:
            directory: Directory to list
            pattern: File pattern (e.g., "*.md")
            
        Returns:
            List of file paths
        """
        if not self.validate_path(directory):
            logger.error(f"Invalid directory: {directory}")
            return []
        
        try:
            path = Path(directory)
            if not path.is_dir():
                logger.warning(f"Not a directory: {directory}")
                return []
            
            files = [
                str(f.relative_to(self.base_dir))
                for f in path.glob(pattern)
                if f.is_file() and self.validate_path(str(f))
            ]
            
            logger.info(f"Listed {len(files)} files in {directory}")
            return files
            
        except Exception as e:
            logger.error(f"File listing error: {str(e)}")
            return []
```

### Cyclotron Indexer Pattern

```python
"""
CYCLOTRON_CONTENT_INDEXER.py
Content indexing for semantic search with consciousness context.
"""

from typing import Dict, List, Optional
import asyncio
import logging
from pathlib import Path
from dataclasses import dataclass
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class ContentChunk:
    """Represents a chunk of indexed content."""
    id: str
    source_file: str
    content: str
    embeddings: Optional[List[float]] = None
    metadata: Dict = None
    consciousness_keywords: List[str] = None

class CyclotronIndexer:
    """
    Index repository content for semantic search.
    
    Focus on consciousness-related content:
    - Pattern detection tools
    - Healing resources
    - ARAYA conversations
    - 7 Domains content
    """
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.cwd()
        self.indexed_content: Dict[str, ContentChunk] = {}
        self.consciousness_keywords = self._load_keywords()
    
    def _load_keywords(self) -> List[str]:
        """Load consciousness-related keywords for tagging."""
        return [
            'pattern', 'healing', 'consciousness', 'manipulation',
            'gaslighting', 'boundaries', 'trauma', 'recovery',
            'empowerment', 'awareness', 'narcissism', 'araya',
            'domains', 'spiritual', 'emotional', 'mental'
        ]
    
    async def index_file(self, file_path: Path) -> Optional[List[ContentChunk]]:
        """
        Index a single file with consciousness context.
        
        Args:
            file_path: Path to file
            
        Returns:
            List of content chunks with embeddings
        """
        try:
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                return None
            
            # Read content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into chunks
            chunks = self._chunk_content(content, file_path)
            
            # Add embeddings (would use actual embedding model)
            for chunk in chunks:
                chunk.embeddings = await self._generate_embeddings(chunk.content)
                chunk.consciousness_keywords = self._extract_keywords(chunk.content)
            
            # Store chunks
            for chunk in chunks:
                self.indexed_content[chunk.id] = chunk
            
            logger.info(f"Indexed {len(chunks)} chunks from {file_path}")
            return chunks
            
        except Exception as e:
            logger.error(f"Indexing error for {file_path}: {str(e)}")
            return None
    
    def _chunk_content(
        self,
        content: str,
        source_file: Path,
        chunk_size: int = 500
    ) -> List[ContentChunk]:
        """Split content into chunks for indexing."""
        chunks = []
        words = content.split()
        
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i + chunk_size]
            chunk_content = ' '.join(chunk_words)
            
            chunk_id = hashlib.md5(
                f"{source_file}:{i}".encode()
            ).hexdigest()
            
            chunks.append(ContentChunk(
                id=chunk_id,
                source_file=str(source_file),
                content=chunk_content,
                metadata={
                    "chunk_index": i // chunk_size,
                    "word_count": len(chunk_words)
                }
            ))
        
        return chunks
    
    async def _generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text (placeholder)."""
        # Would use actual embedding model (OpenAI, Cohere, etc.)
        return [0.1] * 1536  # Placeholder embedding vector
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract consciousness-related keywords from text."""
        text_lower = text.lower()
        found_keywords = [
            keyword for keyword in self.consciousness_keywords
            if keyword in text_lower
        ]
        return found_keywords
    
    async def search(
        self,
        query: str,
        top_k: int = 5
    ) -> List[ContentChunk]:
        """
        Search indexed content semantically.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            Top matching content chunks
        """
        try:
            # Generate query embedding
            query_embedding = await self._generate_embeddings(query)
            
            # Calculate similarity scores (cosine similarity)
            results = []
            for chunk in self.indexed_content.values():
                if chunk.embeddings:
                    similarity = self._cosine_similarity(
                        query_embedding,
                        chunk.embeddings
                    )
                    results.append((similarity, chunk))
            
            # Sort by similarity
            results.sort(key=lambda x: x[0], reverse=True)
            
            # Return top k
            top_results = [chunk for _, chunk in results[:top_k]]
            
            logger.info(f"Found {len(top_results)} results for query: {query}")
            return top_results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between vectors."""
        import math
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
```

### Testing Requirements

- [ ] All functions have type hints
- [ ] Async used for I/O operations
- [ ] Comprehensive error handling
- [ ] Logging for all operations
- [ ] Safe file access validation
- [ ] Unit tests for core functions
- [ ] Integration tests for APIs
- [ ] Performance tests for indexing

### Common Mistakes to Avoid

1. ❌ No type hints
2. ❌ Synchronous I/O operations
3. ❌ Missing error handling
4. ❌ No logging
5. ❌ Unsafe file access
6. ❌ Hard-coded paths
7. ❌ Missing input validation
8. ❌ Poor error messages

### Remember

- **Type hints always** - Helps catch bugs early
- **Async for I/O** - Better performance
- **Safe file access** - Use ARAYA_FILE_ACCESS
- **Comprehensive logging** - Debug and monitor
- **Healing-focused** - Every function supports consciousness
- **Error handling** - Never crash, always graceful
