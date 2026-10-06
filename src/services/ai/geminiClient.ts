import { GoogleGenerativeAI } from '@google/generative-ai';
import { ENV } from '../../config/env';

// Initialize Gemini Client
let genAI: GoogleGenerativeAI | null = null;

export function getGeminiClient(): GoogleGenerativeAI | null {
  if (!genAI && ENV.GEMINI_API_KEY) {
    genAI = new GoogleGenerativeAI(ENV.GEMINI_API_KEY);
  }
  return genAI;
}

export function setGeminiApiKey(apiKey: string) {
  ENV.GEMINI_API_KEY = apiKey;
  genAI = new GoogleGenerativeAI(apiKey);
}
