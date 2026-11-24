# Build the final prompt with chunks and original error

from typing import List
import re

class PromptBuilderService:
    @staticmethod
    def build(error: str, chunks: List) -> str:
        context = "\n\n".join(
            re.sub(r'\\+','',chunk["text"])[:300] for chunk in chunks)
        prompt = f"""
You are a Senior DevOps Engineer.

Question:
{error}

Context:
{context}

Answer using ONLY the provided context.

Requirements:
- Explain the issue.
- List likely causes.
- Provide troubleshooting steps.
- Explain how to verify the fix.
- If the answer is not in the context, respond exactly:

"I could not find sufficient information in the knowledge base to troubleshoot this issue."

- If the question is outside the knowledge base, respond exactly:

"The question lies outside my scope. Please ask another question."
"""
        return prompt