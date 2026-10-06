import React, { useState, useRef, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from 'react-native';
import {
  ArrowLeft,
  Send,
  Sparkles,
  Bot,
  Lightbulb,
} from 'lucide-react-native';
import { useMathStore } from '../store/useMathStore';
import { useAuthStore } from '../store/useAuthStore';
import { VisualMathChatBubble } from '../components/VisualMathChatBubble';

interface ChatTutorScreenProps {
  navigation: any;
}

export const ChatTutorScreen: React.FC<ChatTutorScreenProps> = ({ navigation }) => {
  const { grade } = useAuthStore();
  const { currentProblem, chatMessages, isChatLoading, sendChatMessage } = useMathStore();
  const [inputText, setInputText] = useState('');
  const scrollViewRef = useRef<ScrollView>(null);

  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [chatMessages, isChatLoading]);

  const handleSend = async (textToSend?: string) => {
    const text = textToSend || inputText;
    if (!text.trim() || isChatLoading) return;

    setInputText('');
    await sendChatMessage(text.trim(), grade);
  };

  const handleQuickQuestion = (q: string) => {
    handleSend(q);
  };

  if (!currentProblem) {
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>대화할 문제 데이터가 없습니다.</Text>
        <TouchableOpacity
          style={styles.backBtn}
          onPress={() => navigation.navigate('Camera')}
        >
          <Text style={styles.backBtnText}>문제 촬영하러 가기</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
    >
      {/* Top Header */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.headerBackBtn}
          onPress={() => navigation.goBack()}
        >
          <ArrowLeft size={20} color="#CBD5E1" />
        </TouchableOpacity>

        <View style={styles.headerTitleRow}>
          <View style={styles.botIconCircle}>
            <Bot size={18} color="#FFFFFF" />
          </View>
          <View>
            <Text style={styles.headerTitle}>루트 쌤 (AI 시각화 수학 멘토)</Text>
            <Text style={styles.headerSubtitle}>
              {grade} 맞춤형 · 도식화 & Socratic 문답
            </Text>
          </View>
        </View>

        <View style={styles.gradeBadge}>
          <Text style={styles.gradeBadgeText}>{grade}</Text>
        </View>
      </View>

      {/* Problem Reference Banner */}
      <View style={styles.problemBanner}>
        <Sparkles size={14} color="#818CF8" />
        <Text style={styles.problemBannerText} numberOfLines={1}>
          문제: {currentProblem.ocr_text.replace(/\$/g, '')}
        </Text>
      </View>

      {/* Chat Messages List */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.chatScroll}
        contentContainerStyle={styles.chatContent}
        showsVerticalScrollIndicator={false}
      >
        {chatMessages.map((msg) => (
          <VisualMathChatBubble
            key={msg.id}
            message={msg}
            onSelectFollowup={handleQuickQuestion}
          />
        ))}

        {isChatLoading ? (
          <View style={styles.loadingBubble}>
            <ActivityIndicator size="small" color="#818CF8" />
            <Text style={styles.loadingText}>루트 쌤이 도식화 그래프를 그리며 생각 중...</Text>
          </View>
        ) : null}
      </ScrollView>

      {/* Quick Prompts Bar */}
      <View style={styles.quickBar}>
        <View style={styles.quickBarHeader}>
          <Lightbulb size={12} color="#FBBF24" />
          <Text style={styles.quickBarTitle}>자주 묻는 질문:</Text>
        </View>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.quickScroll}>
          <TouchableOpacity
            style={styles.quickPromptBtn}
            onPress={() => handleQuickQuestion('대칭축이 음수일 땐 그림이 어떻게 바뀌나요?')}
          >
            <Text style={styles.quickPromptText}>대칭축이 음수일 땐?</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.quickPromptBtn}
            onPress={() => handleQuickQuestion('초등학생도 이해할 수 있게 더 쉽게 설명해줘.')}
          >
            <Text style={styles.quickPromptText}>더 쉽게 설명해줘</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.quickPromptBtn}
            onPress={() => handleQuickQuestion('왜 여기서 부호가 바뀌나요?')}
          >
            <Text style={styles.quickPromptText}>왜 부호가 바뀌어?</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      {/* Message Input Bar */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="이해 안 되는 점을 루트 쌤에게 물어보세요..."
          placeholderTextColor="#64748B"
          value={inputText}
          onChangeText={setInputText}
          onSubmitEditing={() => handleSend()}
          returnKeyType="send"
          multiline={false}
        />
        <TouchableOpacity
          style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
          onPress={() => handleSend()}
          disabled={!inputText.trim() || isChatLoading}
        >
          <Send size={18} color="#FFFFFF" />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F19',
  },
  emptyContainer: {
    flex: 1,
    backgroundColor: '#0B0F19',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  emptyText: {
    fontSize: 16,
    color: '#94A3B8',
    marginBottom: 16,
  },
  backBtn: {
    backgroundColor: '#4F46E5',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 12,
  },
  backBtnText: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingTop: 50,
    paddingBottom: 12,
    backgroundColor: '#0F172A',
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
  },
  headerBackBtn: {
    padding: 6,
  },
  headerTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    flex: 1,
    marginLeft: 8,
  },
  botIconCircle: {
    width: 34,
    height: 34,
    borderRadius: 12,
    backgroundColor: '#4F46E5',
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerTitle: {
    fontSize: 14,
    fontWeight: '800',
    color: '#F8FAFC',
  },
  headerSubtitle: {
    fontSize: 11,
    color: '#94A3B8',
  },
  gradeBadge: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  gradeBadgeText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#818CF8',
  },
  problemBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#111827',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
  },
  problemBannerText: {
    fontSize: 11,
    color: '#CBD5E1',
    flex: 1,
  },
  chatScroll: {
    flex: 1,
  },
  chatContent: {
    padding: 16,
    paddingBottom: 20,
  },
  loadingBubble: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#111827',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 14,
    alignSelf: 'flex-start',
    marginVertical: 6,
    borderWidth: 1,
    borderColor: '#1F2937',
  },
  loadingText: {
    fontSize: 12,
    color: '#94A3B8',
  },
  quickBar: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: '#0F172A',
    borderTopWidth: 1,
    borderTopColor: '#1E293B',
  },
  quickBarHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    marginBottom: 6,
  },
  quickBarTitle: {
    fontSize: 10,
    fontWeight: '700',
    color: '#94A3B8',
  },
  quickScroll: {
    flexDirection: 'row',
  },
  quickPromptBtn: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  quickPromptText: {
    fontSize: 11,
    color: '#E2E8F0',
    fontWeight: '600',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 10,
    backgroundColor: '#0F172A',
    borderTopWidth: 1,
    borderTopColor: '#1E293B',
    paddingBottom: Platform.OS === 'ios' ? 24 : 10,
  },
  input: {
    flex: 1,
    backgroundColor: '#1E293B',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    color: '#F8FAFC',
    fontSize: 13,
    borderWidth: 1,
    borderColor: '#334155',
  },
  sendButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#4F46E5',
    alignItems: 'center',
    justifyContent: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#334155',
  },
});
