"use client";

import React, { useState, useEffect, useRef, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import {
  Sparkles,
  Send,
  Bot,
  User,
  ShieldCheck,
  CheckCircle2,
  Scale,
  ExternalLink,
  Cpu,
} from "lucide-react";
import { chatAssistant } from "@/lib/api";
import { ChatResponse, ProductSummary } from "@/types";
import { formatINR } from "@/lib/utils";
import { useCompareStore } from "@/store/compareStore";

interface MessageItem {
  id: string;
  sender: "user" | "assistant";
  text: string;
  recommendedProducts?: ProductSummary[];
  requirements?: any;
  modelUsed?: string;
}

function AssistantContent() {
  const searchParams = useSearchParams();
  const initialPrompt = searchParams.get("prompt") || "";

  const [inputMessage, setInputMessage] = useState(initialPrompt);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [messages, setMessages] = useState<MessageItem[]>([
    {
      id: "welcome",
      sender: "assistant",
      text: "Hello! I am PriceWise AI, your grounded electronics shopping advisor in India. What device are you looking for today? Tell me your budget, primary use case (such as software development, gaming, photography, or office productivity), and any preferred brands.",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { addVariant, hasVariant } = useCompareStore();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputMessage;
    if (!text.trim() || loading) return;

    const userMsg: MessageItem = {
      id: Date.now().toString(),
      sender: "user",
      text: text.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage("");
    setLoading(true);

    try {
      const resp = await chatAssistant({
        message: text.trim(),
        conversation_id: conversationId,
      });

      setConversationId(resp.conversation_id);

      const aiMsg: MessageItem = {
        id: (Date.now() + 1).toString(),
        sender: "assistant",
        text: resp.message,
        recommendedProducts: resp.recommended_products,
        requirements: resp.extracted_requirements,
        modelUsed: resp.model_used,
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: "assistant",
          text: "I encountered an error connecting to the intelligence engine. Please try again or rephrase your requirements.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handlePromptClick = (p: string) => {
    setInputMessage(p);
    handleSendMessage(p);
  };

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 flex flex-col h-[calc(100vh-8rem)]">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800 shrink-0">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white flex items-center gap-2">
              <span>PriceWise AI Assistant</span>
              <span className="rounded-full bg-cyan-500/10 px-2 py-0.5 text-[10px] font-semibold text-cyan-400 border border-cyan-500/20">
                Grounded Model
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              Grounded in verified electronics data • INR pricing • Zero hallucinations
            </p>
          </div>
        </div>

        <div className="hidden sm:flex items-center gap-1.5 text-xs text-emerald-400 font-medium">
          <ShieldCheck className="h-4 w-4" />
          <span>Active Guardrails</span>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto py-6 space-y-6 pr-2">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3.5 ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            {msg.sender === "assistant" && (
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                <Bot className="h-4 w-4" />
              </div>
            )}

            <div
              className={`max-w-2xl rounded-2xl p-4 space-y-3 ${
                msg.sender === "user"
                  ? "bg-blue-600 text-white rounded-tr-none text-sm leading-relaxed"
                  : "bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-none text-sm leading-relaxed"
              }`}
            >
              {/* Extracted requirement chips if present */}
              {msg.requirements && (msg.requirements.budget || msg.requirements.category_slug) && (
                <div className="flex flex-wrap gap-1.5 pb-2 border-b border-slate-800 text-[11px]">
                  {msg.requirements.category_slug && (
                    <span className="rounded-md bg-blue-500/10 px-2 py-0.5 text-blue-400 border border-blue-500/20 capitalize">
                      Category: {msg.requirements.category_slug}
                    </span>
                  )}
                  {msg.requirements.budget && (
                    <span className="rounded-md bg-emerald-500/10 px-2 py-0.5 text-emerald-400 border border-emerald-500/20">
                      Budget: {formatINR(msg.requirements.budget)}
                    </span>
                  )}
                  {msg.requirements.key_priorities?.map((pr: string) => (
                    <span key={pr} className="rounded-md bg-cyan-500/10 px-2 py-0.5 text-cyan-400 border border-cyan-500/20">
                      {pr}
                    </span>
                  ))}
                </div>
              )}

              <p className="whitespace-pre-line">{msg.text}</p>

              {/* Recommended Product Cards */}
              {msg.recommendedProducts && msg.recommendedProducts.length > 0 && (
                <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                    Recommended Electronics
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {msg.recommendedProducts.map((p) => {
                      const inCompare = hasVariant(p.primary_variant_id);
                      return (
                        <div
                          key={p.id}
                          className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-950/60 p-3 hover:border-slate-700 transition-colors"
                        >
                          <div className="h-14 w-14 shrink-0 rounded-lg bg-slate-900 flex items-center justify-center p-1">
                            {p.image_url ? (
                              <img src={p.image_url} alt={p.name} className="h-full object-contain" />
                            ) : (
                              <Cpu className="h-5 w-5 text-slate-600" />
                            )}
                          </div>
                          <div className="flex-1 min-w-0">
                            <h4 className="text-xs font-bold text-white truncate">{p.name}</h4>
                            <span className="text-xs font-extrabold text-cyan-400">
                              {formatINR(p.best_price)}
                            </span>
                            <div className="mt-1 flex items-center gap-2">
                              <a
                                href={`/products/${p.slug}`}
                                className="text-[10px] font-semibold text-blue-400 hover:text-blue-300"
                              >
                                Details →
                              </a>
                              <button
                                onClick={() => addVariant(p.primary_variant_id)}
                                className="text-[10px] font-medium text-slate-400 hover:text-white"
                              >
                                {inCompare ? "✓ Added" : "+ Compare"}
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {msg.modelUsed && (
                <div className="text-[10px] text-slate-500 pt-1 text-right">
                  Engine: {msg.modelUsed}
                </div>
              )}
            </div>

            {msg.sender === "user" && (
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-600 text-white">
                <User className="h-4 w-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3.5 justify-start items-center">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Bot className="h-4 w-4 animate-spin" />
            </div>
            <div className="rounded-2xl bg-slate-900 border border-slate-800 p-4 text-xs text-slate-400 flex items-center gap-2">
              <span className="inline-block h-2 w-2 rounded-full bg-cyan-400 animate-ping" />
              Analyzing electronics catalog & formulating recommendation...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Starters */}
      <div className="pt-2 pb-3 shrink-0 flex flex-wrap gap-2 text-xs">
        <button
          onClick={() => handlePromptClick("I have ₹50,000. Recommend a smartphone with the best battery and camera.")}
          className="rounded-full border border-slate-800 bg-slate-900/40 px-3 py-1 text-slate-400 hover:border-slate-700 hover:text-white transition-colors"
        >
          &ldquo;Phone under ₹50,000 with best camera&rdquo;
        </button>
        <button
          onClick={() => handlePromptClick("Recommend a laptop for computer science, coding, and lightweight gaming under ₹1,00,000.")}
          className="rounded-full border border-slate-800 bg-slate-900/40 px-3 py-1 text-slate-400 hover:border-slate-700 hover:text-white transition-colors"
        >
          &ldquo;Laptop for coding under ₹1 Lakh&rdquo;
        </button>
        <button
          onClick={() => handlePromptClick("Compare AirPods Pro 2 vs Sony WH-1000XM5 for sound quality and ANC.")}
          className="rounded-full border border-slate-800 bg-slate-900/40 px-3 py-1 text-slate-400 hover:border-slate-700 hover:text-white transition-colors"
        >
          &ldquo;Compare AirPods Pro vs Sony XM5&rdquo;
        </button>
      </div>

      {/* Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="relative shrink-0"
      >
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Ask anything about electronics, specs, or marketplace deals..."
          disabled={loading}
          className="w-full rounded-2xl border border-slate-700 bg-slate-900 py-3.5 pl-4 pr-12 text-sm text-white placeholder-slate-500 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 disabled:opacity-50 transition-all"
        />
        <button
          type="submit"
          disabled={loading || !inputMessage.trim()}
          className="absolute right-2.5 top-1/2 -translate-y-1/2 flex h-8 w-8 items-center justify-center rounded-xl bg-cyan-600 text-white hover:bg-cyan-500 disabled:opacity-50 transition-colors"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
}

export default function AssistantPage() {
  return (
    <Suspense fallback={<div className="p-12 text-center text-sm text-slate-400">Loading AI Assistant...</div>}>
      <AssistantContent />
    </Suspense>
  );
}
