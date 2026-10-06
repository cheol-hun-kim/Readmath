import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import {
  ArrowLeft,
  Scissors,
  Sparkles,
  BookOpen,
  Sigma,
  LineChart,
  SearchCode,
  CheckCircle2,
} from 'lucide-react-native';
import { useMathStore } from '../store/useMathStore';
import { useAuthStore } from '../store/useAuthStore';
import { ProblemDecompositionView } from '../components/ProblemDecompositionView';
import { PrescriptionChatView } from '../components/PrescriptionChatView';
import { FailureType, FAILURE_TYPE_MAP } from '../types/math';

interface DiagnosisScreenProps {
  navigation: any;
}

export const DiagnosisScreen: React.FC<DiagnosisScreenProps> = ({ navigation }) => {
  const { userId } = useAuthStore();
  const {
    currentProblem,
    selectedClause,
    selectedKeyword,
    selectedFailureType,
    prescriptionResponse,
    isGeneratingPrescription,
    setSelectedClause,
    setSelectedKeyword,
    setSelectedFailureType,
    submitDiagnosisAndGetPrescription,
  } = useMathStore();

  if (!currentProblem) {
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>진단할 문제 데이터가 없습니다.</Text>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.navigate('Camera')}
        >
          <Text style={styles.backButtonText}>카메라로 돌아가기</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const handleSelectClause = (clause: string, keyword: string) => {
    setSelectedClause(clause);
    setSelectedKeyword(keyword);
  };

  const handleSubmit = () => {
    submitDiagnosisAndGetPrescription(userId);
  };

  const getIcon = (type: FailureType) => {
    switch (type) {
      case 'concept':
        return <BookOpen size={20} color={FAILURE_TYPE_MAP.concept.color} />;
      case 'modeling':
        return <Sigma size={20} color={FAILURE_TYPE_MAP.modeling.color} />;
      case 'visual':
        return <LineChart size={20} color={FAILURE_TYPE_MAP.visual.color} />;
      case 'interpretation':
        return <SearchCode size={20} color={FAILURE_TYPE_MAP.interpretation.color} />;
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backBtn}
          onPress={() => navigation.goBack()}
        >
          <ArrowLeft size={20} color="#CBD5E1" />
          <Text style={styles.backText}>풀이로 돌아가기</Text>
        </TouchableOpacity>

        <View style={styles.rcaBadge}>
          <Scissors size={14} color="#A78BFA" />
          <Text style={styles.rcaBadgeText}>RCA 자가진단</Text>
        </View>
      </View>

      {/* Intro Banner */}
      <View style={styles.introCard}>
        <Text style={styles.introTitle}>🔍 왜 풀지 못했는지 원인을 분해합니다</Text>
        <Text style={styles.introDesc}>
          문제를 문장과 단어 단위로 쪼갰습니다. 막힌 단어를 누르고 실패 원인을 진단하세요.
        </Text>
      </View>

      {/* 1. Problem Decomposition View (Interactive Chips) */}
      <ProblemDecompositionView
        ocrText={currentProblem.ocr_text}
        decomposedClauses={currentProblem.decomposed_clauses}
        selectedClause={selectedClause}
        selectedKeyword={selectedKeyword}
        onSelectClause={handleSelectClause}
      />

      {/* 2. Failure Category Selection */}
      <View style={styles.categorySection}>
        <Text style={styles.sectionHeaderTitle}>진단 카테고리 선택</Text>
        <Text style={styles.sectionHeaderSubtitle}>
          선택한 부분에서 어떤 문제로 풀이가 막혔나요?
        </Text>

        <View style={styles.categoryGrid}>
          {(Object.keys(FAILURE_TYPE_MAP) as FailureType[]).map((typeKey) => {
            const info = FAILURE_TYPE_MAP[typeKey];
            const isSelected = selectedFailureType === typeKey;

            return (
              <TouchableOpacity
                key={typeKey}
                style={[
                  styles.categoryCard,
                  isSelected && {
                    borderColor: info.color,
                    backgroundColor: 'rgba(30, 27, 75, 0.9)',
                  },
                ]}
                onPress={() => setSelectedFailureType(typeKey)}
                activeOpacity={0.8}
              >
                <View style={styles.cardTop}>
                  <View
                    style={[
                      styles.iconCircle,
                      { backgroundColor: `${info.color}22` },
                    ]}
                  >
                    {getIcon(typeKey)}
                  </View>
                  {isSelected ? (
                    <CheckCircle2 size={18} color={info.color} />
                  ) : null}
                </View>

                <Text style={styles.categoryLabel}>{info.label}</Text>
                <Text style={styles.categoryDesc}>{info.description}</Text>
              </TouchableOpacity>
            );
          })}
        </View>
      </View>

      {/* 3. Action Button: Request Tailored Prescription */}
      <TouchableOpacity
        style={[
          styles.prescribeButton,
          (!selectedFailureType || isGeneratingPrescription) && styles.btnDisabled,
        ]}
        onPress={handleSubmit}
        disabled={!selectedFailureType || isGeneratingPrescription}
        activeOpacity={0.85}
      >
        {isGeneratingPrescription ? (
          <View style={styles.btnRow}>
            <ActivityIndicator size="small" color="#FFFFFF" />
            <Text style={styles.prescribeBtnText}>AI 맞춤형 처방 생성 중...</Text>
          </View>
        ) : (
          <View style={styles.btnRow}>
            <Sparkles size={18} color="#FFFFFF" />
            <Text style={styles.prescribeBtnText}>막힌 지점 1:1 맞춤 처방 받기</Text>
          </View>
        )}
      </TouchableOpacity>

      {/* 4. Display AI Prescription Result */}
      {prescriptionResponse && selectedFailureType ? (
        <PrescriptionChatView
          prescriptionText={prescriptionResponse}
          failureType={selectedFailureType}
          missedKeyword={selectedKeyword || '선택 조건'}
        />
      ) : null}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F19',
  },
  contentContainer: {
    padding: 16,
    paddingTop: 44,
    paddingBottom: 40,
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
  backButton: {
    backgroundColor: '#4F46E5',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 12,
  },
  backButtonText: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 14,
  },
  backBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  backText: {
    fontSize: 13,
    color: '#94A3B8',
    fontWeight: '600',
  },
  rcaBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(167, 139, 250, 0.15)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  rcaBadgeText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#A78BFA',
  },
  introCard: {
    backgroundColor: 'rgba(79, 70, 229, 0.1)',
    borderRadius: 14,
    padding: 14,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: 'rgba(79, 70, 229, 0.25)',
  },
  introTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#C7D2FE',
    marginBottom: 4,
  },
  introDesc: {
    fontSize: 12,
    color: '#94A3B8',
    lineHeight: 18,
  },
  categorySection: {
    marginVertical: 12,
  },
  sectionHeaderTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#F1F5F9',
  },
  sectionHeaderSubtitle: {
    fontSize: 12,
    color: '#94A3B8',
    marginTop: 2,
    marginBottom: 12,
  },
  categoryGrid: {
    gap: 10,
  },
  categoryCard: {
    backgroundColor: '#1E293B',
    borderRadius: 14,
    padding: 14,
    borderWidth: 1.5,
    borderColor: '#334155',
  },
  cardTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  iconCircle: {
    width: 36,
    height: 36,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  categoryLabel: {
    fontSize: 14,
    fontWeight: '700',
    color: '#F8FAFC',
    marginBottom: 4,
  },
  categoryDesc: {
    fontSize: 12,
    color: '#94A3B8',
    lineHeight: 16,
  },
  prescribeButton: {
    backgroundColor: '#4F46E5',
    paddingVertical: 16,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.35,
    shadowRadius: 8,
    elevation: 4,
    marginVertical: 14,
  },
  btnDisabled: {
    backgroundColor: '#334155',
    shadowOpacity: 0,
    elevation: 0,
  },
  btnRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  prescribeBtnText: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: '700',
  },
});
