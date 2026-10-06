import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { Sparkles, CheckCircle, Lightbulb } from 'lucide-react-native';
import { MathRenderer } from './MathRenderer';
import { FailureType, FAILURE_TYPE_MAP } from '../types/math';

interface PrescriptionChatViewProps {
  prescriptionText: string;
  failureType: FailureType;
  missedKeyword: string;
}

export const PrescriptionChatView: React.FC<PrescriptionChatViewProps> = ({
  prescriptionText,
  failureType,
  missedKeyword,
}) => {
  const failureInfo = FAILURE_TYPE_MAP[failureType] || FAILURE_TYPE_MAP.concept;

  // Split prescription text into lines or paragraphs to render latex formulas gracefully
  const renderFormattedPrescription = (text: string) => {
    const parts = text.split(/(?=\n###|\n\d+\.)/);
    return parts.map((part, idx) => {
      const trimmed = part.trim();
      if (!trimmed) return null;

      const hasMath = trimmed.includes('$') || trimmed.includes('\\');

      return (
        <View key={`presc_${idx}`} style={styles.paragraphBox}>
          {hasMath ? (
            <MathRenderer
              latex={trimmed.replace(/\$/g, '')}
              fontSize={14}
              color="#E2E8F0"
              backgroundColor="transparent"
            />
          ) : (
            <Text style={styles.prescriptionBodyText}>{trimmed}</Text>
          )}
        </View>
      );
    });
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.badgeRow}>
          <View style={[styles.typeBadge, { backgroundColor: `${failureInfo.color}22` }]}>
            <Sparkles size={14} color={failureInfo.color} />
            <Text style={[styles.typeBadgeText, { color: failureInfo.color }]}>
              {failureInfo.label} 처방 완료
            </Text>
          </View>
          <View style={styles.resolvedBadge}>
            <CheckCircle size={12} color="#34D399" />
            <Text style={styles.resolvedText}>RCA 저장됨</Text>
          </View>
        </View>
      </View>

      <View style={styles.keywordHighlight}>
        <Lightbulb size={16} color="#FBBF24" />
        <Text style={styles.keywordText}>
          교정 대상 키워드: <Text style={styles.boldKeyword}>{missedKeyword}</Text>
        </Text>
      </View>

      {/* Body Content */}
      <View style={styles.content}>
        {renderFormattedPrescription(prescriptionText)}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#0F172A',
    borderRadius: 16,
    borderWidth: 1.5,
    borderColor: '#4338CA',
    padding: 16,
    marginVertical: 12,
    shadowColor: '#4338CA',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  header: {
    marginBottom: 10,
  },
  badgeRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  typeBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  typeBadgeText: {
    fontSize: 12,
    fontWeight: '700',
  },
  resolvedBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(52, 211, 153, 0.15)',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  resolvedText: {
    fontSize: 11,
    color: '#34D399',
    fontWeight: '600',
  },
  keywordHighlight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#1E293B',
    padding: 10,
    borderRadius: 8,
    marginBottom: 12,
  },
  keywordText: {
    fontSize: 12,
    color: '#CBD5E1',
  },
  boldKeyword: {
    color: '#FDE047',
    fontWeight: '700',
  },
  content: {
    gap: 8,
  },
  paragraphBox: {
    marginVertical: 4,
  },
  prescriptionBodyText: {
    fontSize: 13,
    lineHeight: 20,
    color: '#E2E8F0',
    fontWeight: '400',
  },
});
