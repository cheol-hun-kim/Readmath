import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  Modal,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import {
  X,
  BookOpen,
  Sigma,
  LineChart,
  SearchCode,
  Sparkles,
  CheckCircle2,
} from 'lucide-react-native';
import { FailureType, FAILURE_TYPE_MAP } from '../types/math';

interface DiagnosticModalProps {
  visible: boolean;
  selectedClause: string | null;
  selectedKeyword: string | null;
  selectedFailureType: FailureType | null;
  isLoadingPrescription: boolean;
  onSelectFailureType: (type: FailureType) => void;
  onSubmitDiagnosis: () => void;
  onClose: () => void;
}

export const DiagnosticModal: React.FC<DiagnosticModalProps> = ({
  visible,
  selectedClause,
  selectedKeyword,
  selectedFailureType,
  isLoadingPrescription,
  onSelectFailureType,
  onSubmitDiagnosis,
  onClose,
}) => {
  const getIcon = (type: FailureType) => {
    switch (type) {
      case 'concept':
        return <BookOpen size={22} color={FAILURE_TYPE_MAP.concept.color} />;
      case 'modeling':
        return <Sigma size={22} color={FAILURE_TYPE_MAP.modeling.color} />;
      case 'visual':
        return <LineChart size={22} color={FAILURE_TYPE_MAP.visual.color} />;
      case 'interpretation':
        return <SearchCode size={22} color={FAILURE_TYPE_MAP.interpretation.color} />;
    }
  };

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="slide"
      onRequestClose={onClose}
    >
      <View style={styles.overlay}>
        <View style={styles.modalContent}>
          {/* Header */}
          <View style={styles.header}>
            <View>
              <Text style={styles.modalTitle}>근본 원인 분석 (RCA)</Text>
              <Text style={styles.modalSubtitle}>
                왜 이 문제를 스스로 풀지 못했나요?
              </Text>
            </View>
            <TouchableOpacity onPress={onClose} style={styles.closeButton}>
              <X size={20} color="#9CA3AF" />
            </TouchableOpacity>
          </View>

          {/* Selected Focus Condition */}
          <View style={styles.focusClauseCard}>
            <Text style={styles.focusLabel}>막혔던 지점:</Text>
            <Text style={styles.focusClauseText} numberOfLines={2}>
              "{selectedKeyword || selectedClause || '문제 전체'}"
            </Text>
          </View>

          {/* Failure Types Radio List */}
          <ScrollView style={styles.optionsList} showsVerticalScrollIndicator={false}>
            {(Object.keys(FAILURE_TYPE_MAP) as FailureType[]).map((typeKey) => {
              const info = FAILURE_TYPE_MAP[typeKey];
              const isSelected = selectedFailureType === typeKey;

              return (
                <TouchableOpacity
                  key={typeKey}
                  style={[
                    styles.optionCard,
                    isSelected && {
                      borderColor: info.color,
                      backgroundColor: 'rgba(30, 27, 75, 0.8)',
                    },
                  ]}
                  onPress={() => onSelectFailureType(typeKey)}
                  activeOpacity={0.75}
                >
                  <View style={styles.optionLeft}>
                    <View
                      style={[
                        styles.iconContainer,
                        { backgroundColor: `${info.color}1A` },
                      ]}
                    >
                      {getIcon(typeKey)}
                    </View>
                    <View style={styles.optionTextContainer}>
                      <View style={styles.badgeRow}>
                        <Text style={[styles.optionLabel, isSelected && { color: '#FFFFFF' }]}>
                          {info.label}
                        </Text>
                        <View style={[styles.badge, { backgroundColor: `${info.color}26` }]}>
                          <Text style={[styles.badgeText, { color: info.color }]}>
                            {info.badge}
                          </Text>
                        </View>
                      </View>
                      <Text style={styles.optionDescription}>
                        {info.description}
                      </Text>
                    </View>
                  </View>

                  <View style={styles.radioButton}>
                    {isSelected ? (
                      <CheckCircle2 size={20} color={info.color} />
                    ) : (
                      <View style={styles.radioCircle} />
                    )}
                  </View>
                </TouchableOpacity>
              );
            })}
          </ScrollView>

          {/* Action Footer */}
          <View style={styles.footer}>
            <TouchableOpacity
              style={[
                styles.submitButton,
                (!selectedFailureType || isLoadingPrescription) && styles.submitButtonDisabled,
              ]}
              onPress={onSubmitDiagnosis}
              disabled={!selectedFailureType || isLoadingPrescription}
              activeOpacity={0.8}
            >
              {isLoadingPrescription ? (
                <View style={styles.buttonLoadingRow}>
                  <ActivityIndicator size="small" color="#FFFFFF" />
                  <Text style={styles.submitButtonText}>AI 맞춤 처방 생성 중...</Text>
                </View>
              ) : (
                <View style={styles.buttonContentRow}>
                  <Sparkles size={18} color="#FFFFFF" />
                  <Text style={styles.submitButtonText}>맞춤형 RCA 처방 받기</Text>
                </View>
              )}
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.75)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#0F172A',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 34,
    maxHeight: '85%',
    borderWidth: 1,
    borderColor: '#334155',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 14,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '800',
    color: '#F8FAFC',
  },
  modalSubtitle: {
    fontSize: 13,
    color: '#94A3B8',
    marginTop: 2,
  },
  closeButton: {
    padding: 6,
    borderRadius: 20,
    backgroundColor: '#1E293B',
  },
  focusClauseCard: {
    backgroundColor: '#1E293B',
    padding: 12,
    borderRadius: 10,
    marginBottom: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#6366F1',
  },
  focusLabel: {
    fontSize: 11,
    color: '#818CF8',
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  focusClauseText: {
    fontSize: 13,
    color: '#E2E8F0',
    marginTop: 4,
    fontWeight: '600',
  },
  optionsList: {
    marginBottom: 16,
  },
  optionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#1E293B',
    borderRadius: 14,
    padding: 14,
    marginBottom: 10,
    borderWidth: 1.5,
    borderColor: '#334155',
  },
  optionLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    gap: 12,
  },
  iconContainer: {
    width: 44,
    height: 44,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  optionTextContainer: {
    flex: 1,
  },
  badgeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  optionLabel: {
    fontSize: 14,
    fontWeight: '700',
    color: '#F1F5F9',
  },
  badge: {
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6,
  },
  badgeText: {
    fontSize: 10,
    fontWeight: '700',
  },
  optionDescription: {
    fontSize: 12,
    color: '#94A3B8',
    lineHeight: 16,
  },
  radioButton: {
    marginLeft: 10,
  },
  radioCircle: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#475569',
  },
  footer: {
    paddingTop: 8,
  },
  submitButton: {
    backgroundColor: '#4F46E5',
    paddingVertical: 14,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  submitButtonDisabled: {
    backgroundColor: '#334155',
    shadowOpacity: 0,
    elevation: 0,
  },
  buttonContentRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  buttonLoadingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: '700',
  },
});
