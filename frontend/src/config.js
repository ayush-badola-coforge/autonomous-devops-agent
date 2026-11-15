const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '')
const CHAT_ENDPOINT = import.meta.env.VITE_CHAT_ENDPOINT || '/api/chat'
const CONVERSATIONS_ENDPOINT = import.meta.env.VITE_CONVERSATIONS_ENDPOINT || '/api/conversations'

export const getChatUrl = () => `${API_BASE}${CHAT_ENDPOINT.startsWith('/') ? '' : '/'}${CHAT_ENDPOINT}`
export const getConversationsUrl = () => `${API_BASE}${CONVERSATIONS_ENDPOINT.startsWith('/') ? '' : '/'}${CONVERSATIONS_ENDPOINT}`
export const getDeleteConversationUrl = (id) => `${getConversationsUrl()}/${encodeURIComponent(id)}`

