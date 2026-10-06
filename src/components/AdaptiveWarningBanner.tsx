import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { Flame, X, ShieldAlert, ArrowRight } from 'lucide-react-native';
import { AdaptiveDiagnosticAlert } from '../types/math';

interface AdaptiveWarningBannerProps {
  alert: AdaptiveDiagnosticAlert | null;
  onDismiss: () => void;
}

export const AdaptiveWarningBanner: React.FC<AdaptiveWarningBannerProps> = ({
  alert,
  onDismiss,
}) => {
  if (!alert || !alert.has_critical_warning) return null;

  return (
    <View style={styles.container}>
      {/* Top Warning Badge */}
      <View style={styles.header}>
        <View style={styles.badge}>
          <Flame size={14} color="#EF4444" />
          <Text style={styles.badgeText}>
            누적 취약점 선제 지적 ({alert.repetition_count}회 반복 감지)
          </Text>
        </View>
        <TouchableOpacity onPress={onDismiss} style={styles.closeBtn}>
          <X size={16} color="#9CA3AF" />
        </TouchableOpacity>
      </View>

      {/* Main Blunt Warning Message */}
      <View style={styles.body}>
        <View style={styles.iconBox}>
          <ShieldAlert size={24} color="#F59E0B" />
        </View>
        <View style={styles.messageBox}>
          <Text style={styles.recurringTitle}>
            반복 취약 개념: <Text style={styles.conceptHighlight}>{alert.recurring_concept}</Text>
          </Text>
          <Text style={styles.bluntMessage}>
            {alert.blunt_feedback_message}
          </Text>
        </View>
      </View>

      {/* Action Plan */}
      {alert.remedy_action_plan ? (
        <View style={styles.actionPlanBox}>
          <Text style={styles.actionPlanTitle}>🎯 RootMath 근본 교정 처방:</Text>
          <Text style={styles.actionPlanText}>
            {alert.remedy_action_plan}
          </Text>
        </View>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#1E1B4B',
    borderRadius: 16,
    borderWidth: 1.5,
    borderColor: '#EF4444',
    padding: 14,
    marginVertical: 10,
    shadowColor: '#EF4444',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 4,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: 'rgba(239, 68, 68, 0.2)',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 8,
  },
  badgeText: {
    fontSize: 11,
    fontWeight: '800',
    color: '#F87171',
  },
  closeBtn: {
    padding: 4,
  },
  body: {
    flexDirection: 'row',
    gap: 12,
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  iconBox: {
    backgroundColor: 'rgba(245, 158, 11, 0.15)',
    padding: 8,
    borderRadius: 10,
    marginTop: 2,
  },
  messageBox: {
    flex: 1,
  },
  recurringTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: '#E0E7FF',
    marginBottom: 4,
  },
  conceptHighlight: {
    color: '#FBBF24',
    fontWeight: '800',
  },
  bluntMessage: {
    fontSize: 13,
    lineHeight: 19,
    color: '#CBD5E1',
    fontWeight: '500',
  },
  actionPlanBox: {
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    borderRadius: 10,
    padding: 10,
    borderLeftWidth: 3,
    borderLeftColor: '#10B981',
  },
  actionPlanTitle: {
    fontSize: 11,
    fontWeight: '800',
    color: '#34D399',
    marginBottom: 4,
  },
  actionPlanText: {
    fontSize: 12,
    lineHeight: 18,
    color: '#E2E8F0',
  },
});
