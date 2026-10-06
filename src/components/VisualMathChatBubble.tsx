import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { Bot, User, Sparkles, HelpCircle } from 'lucide-react-native';
import { SvgXml } from 'react-native-svg';
import { ChatMessage } from '../types/math';
import { MathRenderer } from './MathRenderer';

interface VisualMathChatBubbleProps {
  message: ChatMessage;
  onSelectFollowup?: (question: string) => void;
  onApplyDiagnosis?: (diagnosis: any) => void;
}

export const VisualMathChatBubble: React.FC<VisualMathChatBubbleProps> = ({
  message,
  onSelectFollowup,
  onApplyDiagnosis,
}) => {
  const isUser = message.sender === 'user';

  return (
    <View style={[styles.container, isUser ? styles.userAlign : styles.aiAlign]}>
      {/* Sender Avatar */}
      <View style={[styles.avatar, isUser ? styles.userAvatar : styles.aiAvatar]}>
        {isUser ? (
          <User size={16} color="#FFFFFF" />
        ) : (
          <Bot size={18} color="#818CF8" />
        )}
      </View>

      <View style={[styles.bubbleContent, isUser ? styles.userBubble : styles.aiBubble]}>
        {/* Header tag for AI */}
        {!isUser ? (
          <View style={styles.aiHeader}>
            <Text style={styles.aiName}>루트 쌤 (AI 수학 멘토)</Text>
            {message.key_concept ? (
              <View style={styles.conceptTag}>
                <Sparkles size={10} color="#A78BFA" />
                <Text style={styles.conceptTagText}>{message.key_concept}</Text>
              </View>
            ) : null}
          </View>
        ) : null}

        {/* Text Message */}
        <Text style={[styles.messageText, isUser && styles.userMessageText]}>
          {message.text}
        </Text>

        {/* Dynamic SVG Visual Diagram / Geometry Chart */}
        {message.visualization_svg ? (
          <View style={styles.svgContainer}>
            <View style={styles.svgHeader}>
              <Text style={styles.svgTitle}>💡 실시간 도식화 설명</Text>
            </View>
            <View style={styles.svgCanvasWrapper}>
              <SvgXml xml={message.visualization_svg.trim()} width="100%" height={180} />
            </View>
          </View>
        ) : null}

        {/* Core LaTeX Formula Highlight */}
        {message.latex_formula ? (
          <View style={styles.latexCard}>
            <MathRenderer
              latex={message.latex_formula}
              fontSize={14}
              color="#FDE047"
              displayMode={true}
            />
          </View>
        ) : null}

        {/* 🎯 AI Pinpoint Diagnostic Card (Conversational RCA) */}
        {message.rca_diagnosis ? (
          <View style={styles.diagnosisCard}>
            <View style={styles.diagnosisCardHeader}>
              <View style={styles.diagnosisTitleRow}>
                <Sparkles size={14} color="#FBBF24" />
                <Text style={styles.diagnosisCardTitle}>AI 핀포인트 역진단 확정</Text>
              </View>
              <Text style={styles.diagnosisTypeBadge}>
                {message.rca_diagnosis.failure_type === 'visual' ? '도식화 실패' :
                 message.rca_diagnosis.failure_type === 'modeling' ? '수식 모델링 실패' :
                 message.rca_diagnosis.failure_type === 'interpretation' ? '조건 해석 실패' : '개념 미학습'}
              </Text>
            </View>
            <Text style={styles.diagnosisClauseText}>
              📍 <Text style={styles.boldText}>결손 조건:</Text> {message.rca_diagnosis.clause}
            </Text>
            <Text style={styles.diagnosisReasonText}>
              🎯 <Text style={styles.boldText}>원인 분석:</Text> {message.rca_diagnosis.reason}
            </Text>
            <TouchableOpacity
              style={styles.applyDiagnosisBtn}
              onPress={() => onApplyDiagnosis && onApplyDiagnosis(message.rca_diagnosis)}
              activeOpacity={0.8}
            >
              <Text style={styles.applyDiagnosisBtnText}>
                ✓ 이 진단으로 내 취약점 리포트에 자동 저장
              </Text>
            </TouchableOpacity>
          </View>
        ) : null}

        {/* Timestamp */}
        <Text style={[styles.timestamp, isUser && styles.userTimestamp]}>
          {message.timestamp}
        </Text>

        {/* Suggested Followup Questions (AI only) */}
        {!isUser && message.suggested_followups && message.suggested_followups.length > 0 ? (
          <View style={styles.followupContainer}>
            <View style={styles.followupHeader}>
              <HelpCircle size={12} color="#94A3B8" />
              <Text style={styles.followupTitle}>이어서 물어보기:</Text>
            </View>
            <View style={styles.chipsRow}>
              {message.suggested_followups.map((q, idx) => (
                <TouchableOpacity
                  key={`fu_${idx}`}
                  style={styles.chip}
                  onPress={() => onSelectFollowup && onSelectFollowup(q)}
                  activeOpacity={0.7}
                >
                  <Text style={styles.chipText}>{q}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        ) : null}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    marginVertical: 8,
    maxWidth: '92%',
  },
  userAlign: {
    alignSelf: 'flex-end',
    flexDirection: 'row-reverse',
  },
  aiAlign: {
    alignSelf: 'flex-start',
  },
  avatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 8,
    marginTop: 4,
  },
  userAvatar: {
    backgroundColor: '#4F46E5',
  },
  aiAvatar: {
    backgroundColor: '#1E1B4B',
    borderWidth: 1,
    borderColor: '#4338CA',
  },
  bubbleContent: {
    borderRadius: 18,
    padding: 14,
    flex: 1,
  },
  userBubble: {
    backgroundColor: '#4F46E5',
    borderBottomRightRadius: 4,
  },
  aiBubble: {
    backgroundColor: '#111827',
    borderWidth: 1,
    borderColor: '#1F2937',
    borderBottomLeftRadius: 4,
  },
  aiHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 6,
  },
  aiName: {
    fontSize: 12,
    fontWeight: '800',
    color: '#818CF8',
  },
  conceptTag: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(167, 139, 250, 0.15)',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6,
  },
  conceptTagText: {
    fontSize: 10,
    fontWeight: '700',
    color: '#C7D2FE',
  },
  messageText: {
    fontSize: 13,
    lineHeight: 20,
    color: '#E2E8F0',
    fontWeight: '400',
  },
  userMessageText: {
    color: '#FFFFFF',
    fontWeight: '500',
  },
  svgContainer: {
    marginTop: 10,
    backgroundColor: '#090D16',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#1E293B',
    overflow: 'hidden',
  },
  svgHeader: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    backgroundColor: '#0F172A',
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
  },
  svgTitle: {
    fontSize: 11,
    fontWeight: '700',
    color: '#60A5FA',
  },
  svgCanvasWrapper: {
    padding: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  latexCard: {
    backgroundColor: '#090D16',
    borderRadius: 8,
    padding: 8,
    marginVertical: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  diagnosisCard: {
    marginTop: 10,
    backgroundColor: '#0E1322',
    borderRadius: 12,
    borderWidth: 1.5,
    borderColor: '#6366F1',
    padding: 12,
  },
  diagnosisCardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  diagnosisTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  diagnosisCardTitle: {
    fontSize: 12,
    fontWeight: '800',
    color: '#FBBF24',
  },
  diagnosisTypeBadge: {
    fontSize: 10,
    fontWeight: '700',
    color: '#A5B4FC',
    backgroundColor: '#1E1B4B',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#4338CA',
  },
  diagnosisClauseText: {
    fontSize: 11,
    color: '#E2E8F0',
    marginBottom: 4,
  },
  diagnosisReasonText: {
    fontSize: 11,
    color: '#CBD5E1',
    marginBottom: 10,
  },
  boldText: {
    fontWeight: '700',
    color: '#FFFFFF',
  },
  applyDiagnosisBtn: {
    backgroundColor: '#4F46E5',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  applyDiagnosisBtnText: {
    color: '#FFFFFF',
    fontSize: 11,
    fontWeight: '700',
  },
  timestamp: {
    fontSize: 10,
    color: '#64748B',
    marginTop: 6,
    alignSelf: 'flex-end',
  },
  userTimestamp: {
    color: '#C7D2FE',
  },
  followupContainer: {
    marginTop: 10,
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#1E293B',
  },
  followupHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    marginBottom: 6,
  },
  followupTitle: {
    fontSize: 11,
    fontWeight: '700',
    color: '#94A3B8',
  },
  chipsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  chip: {
    backgroundColor: '#1E293B',
    borderWidth: 1,
    borderColor: '#334155',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  chipText: {
    fontSize: 11,
    color: '#CBD5E1',
    fontWeight: '500',
  },
});
