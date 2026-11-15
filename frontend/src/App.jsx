import { useState, useRef, useEffect } from 'react'
import {
  ArrowUp,
  Sun,
  Moon,
  Copy,
  Check
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { getChatUrl } from './config'
import './App.css'

function CodeBlock({ children, className }) {
  const [copied, setCopied] = useState(false)
  const language = className ? className.replace('language-', '') : ''
  const codeText = String(children).replace(/\n$/, '')

  const handleCopy = () => {
    navigator.clipboard.writeText(codeText)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  return (
    <div className="code-container">
      <div className="code-header">
        <span className="code-lang">{language || 'code'}</span>
        <button className="copy-btn" onClick={handleCopy} aria-label="Copy code">
          {copied ? <Check size={13} /> : <Copy size={13} />}
          <span>{copied ? 'Copied!' : 'Copy code'}</span>
        </button>
      </div>
      <pre className="code-pre">
        <code>{codeText}</code>
      </pre>
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([])
  const [prompt, setPrompt] = useState('')
  const [theme, setTheme] = useState('light')
  const [isLoading, setIsLoading] = useState(false)
  const [errorMsg, setErrorMsg] = useState(null)
  const textareaRef = useRef(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  const hasMessages = messages.length > 0

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleInputChange = (e) => {
    setPrompt(e.target.value)
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'))
  }

  const handleSendPrompt = async () => {
    const textToSend = prompt.trim()
    if (!textToSend || isLoading) return

    setErrorMsg(null)
    const userMessage = {
      id: `u-${Date.now()}`,
      sender: 'user',
      text: textToSend
    }

    setMessages((prev) => [...prev, userMessage])
    setPrompt('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }

    setIsLoading(true)

    try {
      const response = await fetch(getChatUrl(), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          error_message: textToSend,
          query: textToSend,
          prompt: textToSend
        })
      })

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`)
      }

      const data = await response.json()

      const assistantText =
        data.answer ||
        data.response ||
        data.result ||
        (typeof data === 'string' ? data : 'No response text received from backend.')

      const assistantMessage = {
        id: `a-${Date.now()}`,
        sender: 'assistant',
        text: assistantText
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      console.error('API Error:', err)
      setErrorMsg(`Failed to connect to backend: ${err.message}`)

      const errorBubble = {
        id: `err-${Date.now()}`,
        sender: 'assistant',
        text: `Error connecting to backend (${getChatUrl()}). Please ensure backend is running.`
      }

      setMessages((prev) => [...prev, errorBubble])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendPrompt()
    }
  }

  const renderPromptBox = (isCentered = false) => (
    <div className={`input-section ${isCentered ? 'centered' : ''}`}>
      <div className="input-container">
        <textarea
          ref={textareaRef}
          className="prompt-textarea"
          rows={1}
          placeholder="Ask a question or describe an issue..."
          value={prompt}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
        />
        <button
          type="button"
          className="send-btn"
          disabled={!prompt.trim() || isLoading}
          onClick={handleSendPrompt}
          aria-label="Send message"
        >
          <ArrowUp size={18} strokeWidth={2.4} />
        </button>
      </div>
      {errorMsg && <div className="error-note">{errorMsg}</div>}
      <div className="input-footer-note">
        RAG Assistant provides context-grounded responses from your knowledge base.
      </div>
    </div>
  )

  return (
    <div className="app-container">
      <main className="main-wrapper">
        <header className="top-bar">
          <div className="model-title">RAG Assistant</div>
          <button className="theme-toggle-header" onClick={toggleTheme} aria-label="Toggle theme">
            {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
            <span>{theme === 'dark' ? 'Light' : 'Dark'}</span>
          </button>
        </header>

        {!hasMessages ? (
          <div className="center-front-screen">
            <h1 className="front-headline">What can I help with?</h1>
            {renderPromptBox(true)}
          </div>
        ) : (
          <>
            <div className="chat-container">
              <div className="chat-messages">
                {messages.map((msg) => (
                  <div key={msg.id} className={`message-row ${msg.sender}`}>
                    <div className="message-bubble">
                      {msg.sender === 'assistant' ? (
                        <div className="markdown-body">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                              code({ inline, className, children, ...props }) {
                                if (!inline && className) {
                                  return (
                                    <CodeBlock className={className}>
                                      {children}
                                    </CodeBlock>
                                  )
                                }
                                return (
                                  <code className="inline-code" {...props}>
                                    {children}
                                  </code>
                                )
                              }
                            }}
                          >
                            {msg.text}
                          </ReactMarkdown>
                        </div>
                      ) : (
                        <div className="user-text">{msg.text}</div>
                      )}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="message-row assistant">
                    <div className="message-bubble">
                      <div className="typing-dots">
                        <span className="typing-dot" />
                        <span className="typing-dot" />
                        <span className="typing-dot" />
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>
            {renderPromptBox(false)}
          </>
        )}
      </main>
    </div>
  )
}
