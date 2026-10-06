import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import {
  Sparkles,
  Layers,
  CheckCircle2,
  Scissors,
  ArrowLeft,
  BookOpen,
  Bot,
  MessageSquare,
} from 'lucide-react-native';
import { useMathStore } from '../store/useMathStore';
import { useWeaknessStore } from '../store/useWeaknessStore';
import { useAuthStore } from '../store/useAuthStore';
import { MathRenderer } from '../components/MathRenderer';
import { GraphRenderer } from '../components/GraphRenderer';
import { AdaptiveWarningBanner } from '../components/AdaptiveWarningBanner';
import { DiagnosticModal } from '../components/DiagnosticModal';
import { PrescriptionChatView } from '../components/PrescriptionChatView';

interface SolutionScreenProps {
  navigation: any;
}

export const SolutionScreen: React.FC<SolutionScreenProps> = ({ navigation }) => {
  const { userId } = useAuthStore();
  const {
    currentProblem,
    selectedClause,
    selectedKeyword,
    selectedFailureType,
    isDiagnosticModalOpen,
    prescriptionResponse,
    isGeneratingPrescription,
    setSelectedFailureType,
    setDiagnosticModalOpen,
    submitDiagnosisAndGetPrescription,
  } = useMathStore();

  const { adaptiveAlert, dismissAdaptiveAlert } = useWeaknessStore();

  if (!currentProblem) {
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>풀이 데이터가 없습니다.</Text>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.navigate('Camera')}
        >
          <Text style={styles.backButtonText}>문제 촬영하러 가기</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const handleStartRCA = () => {
    navigation.navigate('Diagnosis');
  };

  const handleStartChat = () => {
    navigation.navigate('ChatTutor');
  };

  return (
    <View style={styles.wrapper}>
      <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
        {/* Top Nav Header */}
        <View style={styles.topHeader}>
          <TouchableOpacity
            style={styles.headerBackBtn}
            onPress={() => navigation.goBack()}
          >
            <ArrowLeft size={20} color="#CBD5E1" />
            <Text style={styles.headerBackText}>문제 다시 찍기</Text>
          </TouchableOpacity>
          <View style={styles.headerBadge}>
            <Sparkles size={14} color="#818CF8" />
            <Text style={styles.headerBadgeText}>AI 분석 완료</Text>
          </View>
        </View>

        {/* 1. Proactive Adaptive Weakness Alert Banner */}
        <AdaptiveWarningBanner
          alert={adaptiveAlert}
          onDismiss={dismissAdaptiveAlert}
        />

        {/* 2. Problem Statement Box */}
        <View style={styles.sectionCard}>
          <View style={styles.cardHeader}>
            <BookOpen size={16} color="#818CF8" />
            <Text style={styles.cardTitle}>인식된 문제 원문</Text>
          </View>
          <View style={styles.ocrMathContainer}>
            <MathRenderer
              latex={currentProblem.ocr_text}
              fontSize={15}
              color="#F8FAFC"
            />
          </View>
        </View>

        {/* 3. Core Required Concepts Tags */}
        <View style={styles.conceptsSection}>
          <Text style={styles.conceptsLabel}>필요 핵심 수학 개념:</Text>
          <View style={styles.conceptsRow}>
            {currentProblem.concepts.map((concept, idx) => (
              <View key={`c_${idx}`} style={styles.conceptTag}>
                <Layers size={12} color="#A78BFA" />
                <Text style={styles.conceptTagText}>{concept}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* 4. AI Dynamic Graph / Geometry Visualization */}
        {currentProblem.visualization_svg ? (
          <GraphRenderer
            svgXml={currentProblem.visualization_svg}
            height={260}
            title="AI 도식화 (그래프 & 좌표평면)"
            caption="문제를 수식으로만 보지 말고, 대칭축과 구간의 위치 관계를 시각적으로 확인하세요."
          />
        ) : null}

        {/* 5. 1:1 Visual Math Chatbot Banner ('루트 쌤에게 물어보기') */}
        <TouchableOpacity
          style={styles.chatTutorBanner}
          onPress={handleStartChat}
          activeOpacity={0.85}
        >
          <View style={styles.chatTutorLeft}>
            <View style={styles.chatBotIconCircle}>
              <Bot size={22} color="#FFFFFF" />
            </View>
            <View style={styles.chatTutorTextContainer}>
              <Text style={styles.chatTutorTitle}>루트 쌤과 1:1 시각화 대화하기</Text>
              <Text style={styles.chatTutorSubtitle}>
                "이해가 안 가요", "그림 다시 그려줘" 무엇이든 질문하세요!
              </Text>
            </View>
          </View>
          <View style={styles.chatBadge}>
            <MessageSquare size={12} color="#818CF8" />
            <Text style={styles.chatBadgeText}>질문하기</Text>
          </View>
        </TouchableOpacity>

        {/* 6. Step-by-Step Rigorous Math Solution */}
        <View style={styles.sectionCard}>
          <View style={styles.cardHeader}>
            <CheckCircle2 size={16} color="#34D399" />
            <Text style={styles.cardTitle}>단계별 개념 조합 풀이</Text>
          </View>

          <View style={styles.stepsContainer}>
            {currentProblem.step_by_step_solution.map((step) => (
              <View key={`step_${step.step_number}`} style={styles.stepCard}>
                <View style={styles.stepHeader}>
                  <View style={styles.stepNumberBubble}>
                    <Text style={styles.stepNumberText}>{step.step_number}</Text>
                  </View>
                  <Text style={styles.stepTitleText}>{step.title}</Text>
                </View>

                <View style={styles.mathBlock}>
                  <MathRenderer
                    latex={step.latex_content}
                    fontSize={15}
                    displayMode={true}
                    color="#E0E7FF"
                  />
                </View>

                <Text style={styles.stepExplanation}>{step.explanation}</Text>

                {step.key_takeaway ? (
                  <View style={styles.takeawayBox}>
                    <Text style={styles.takeawayText}>
                      💡 <Text style={styles.takeawayBold}>핵심 포인트:</Text> {step.key_takeaway}
                    </Text>
                  </View>
                ) : null}
              </View>
            ))}
          </View>
        </View>

        {/* 7. Final Answer Box */}
        <View style={styles.answerCard}>
          <Text style={styles.answerLabel}>최종 정답</Text>
          <Text style={styles.answerValue}>{currentProblem.answer}</Text>
        </View>

        {/* 8. Existing Prescription Display */}
        {prescriptionResponse && selectedFailureType ? (
          <PrescriptionChatView
            prescriptionText={prescriptionResponse}
            failureType={selectedFailureType}
            missedKeyword={selectedKeyword || '핵심 조건'}
          />
        ) : null}

        {/* 9. RCA Root Cause Analysis Action Button */}
        <TouchableOpacity
          style={styles.rcaActionButton}
          onPress={handleStartRCA}
          activeOpacity={0.85}
        >
          <View style={styles.rcaButtonInner}>
            <View style={styles.rcaIconCircle}>
              <Scissors size={20} color="#FFFFFF" />
            </View>
            <View style={styles.rcaTextContainer}>
              <Text style={styles.rcaButtonTitle}>
                왜 이 문제를 못 풀었나요? (RCA 진단)
              </Text>
              <Text style={styles.rcaButtonSubtitle}>
                문제를 단어 단위로 쪼개어 막힌 근본 원인을 진단합니다.
              </Text>
            </View>
          </View>
        </TouchableOpacity>
      </ScrollView>

      {/* Diagnostic Modal */}
      <DiagnosticModal
        visible={isDiagnosticModalOpen}
        selectedClause={selectedClause}
        selectedKeyword={selectedKeyword}
        selectedFailureType={selectedFailureType}
        isLoadingPrescription={isGeneratingPrescription}
        onSelectFailureType={setSelectedFailureType}
        onSubmitDiagnosis={() => submitDiagnosisAndGetPrescription(userId)}
        onClose={() => setDiagnosticModalOpen(false)}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    backgroundColor: '#0B0F19',
  },
  container: {
    flex: 1,
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
  topHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  headerBackBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 6,
  },
  headerBackText: {
    fontSize: 13,
    color: '#94A3B8',
    fontWeight: '600',
  },
  headerBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(99, 102, 241, 0.15)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  headerBadgeText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#818CF8',
  },
  sectionCard: {
    backgroundColor: '#111827',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#1F2937',
    padding: 16,
    marginVertical: 8,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 10,
    paddingBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#1F2937',
  },
  cardTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#E0E7FF',
  },
  ocrMathContainer: {
    paddingVertical: 4,
  },
  conceptsSection: {
    marginVertical: 8,
  },
  conceptsLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: '#94A3B8',
    marginBottom: 6,
  },
  conceptsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  conceptTag: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#1E1B4B',
    borderWidth: 1,
    borderColor: '#4338CA',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 8,
  },
  conceptTagText: {
    fontSize: 12,
    color: '#C7D2FE',
    fontWeight: '600',
  },
  chatTutorBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#1E1B4B',
    borderRadius: 16,
    padding: 14,
    marginVertical: 8,
    borderWidth: 1.5,
    borderColor: '#6366F1',
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
  },
  chatTutorLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
  },
  chatBotIconCircle: {
    width: 40,
    height: 40,
    borderRadius: 14,
    backgroundColor: '#4F46E5',
    alignItems: 'center',
    justifyContent: 'center',
  },
  chatTutorTextContainer: {
    flex: 1,
  },
  chatTutorTitle: {
    fontSize: 14,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  chatTutorSubtitle: {
    fontSize: 11,
    color: '#C7D2FE',
    marginTop: 2,
  },
  chatBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(99, 102, 241, 0.2)',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#6366F1',
  },
  chatBadgeText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#A5B4FC',
  },
  stepsContainer: {
    gap: 12,
  },
  stepCard: {
    backgroundColor: '#1E293B',
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: '#334155',
  },
  stepHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 8,
  },
  stepNumberBubble: {
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: '#4F46E5',
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepNumberText: {
    fontSize: 11,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  stepTitleText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#F8FAFC',
    flex: 1,
  },
  mathBlock: {
    backgroundColor: '#0F172A',
    borderRadius: 8,
    padding: 10,
    marginVertical: 6,
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  stepExplanation: {
    fontSize: 13,
    lineHeight: 20,
    color: '#CBD5E1',
    marginVertical: 4,
  },
  takeawayBox: {
    marginTop: 8,
    backgroundColor: 'rgba(245, 158, 11, 0.1)',
    borderRadius: 8,
    padding: 8,
    borderLeftWidth: 3,
    borderLeftColor: '#F59E0B',
  },
  takeawayText: {
    fontSize: 12,
    lineHeight: 18,
    color: '#FDE68A',
  },
  takeawayBold: {
    fontWeight: '700',
  },
  answerCard: {
    backgroundColor: '#064E3B',
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    marginVertical: 8,
    borderWidth: 1,
    borderColor: '#059669',
  },
  answerLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: '#A7F3D0',
    textTransform: 'uppercase',
  },
  answerValue: {
    fontSize: 22,
    fontWeight: '900',
    color: '#FFFFFF',
    marginTop: 4,
  },
  rcaActionButton: {
    backgroundColor: '#4338CA',
    borderRadius: 16,
    padding: 16,
    marginVertical: 14,
    shadowColor: '#4338CA',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.35,
    shadowRadius: 10,
    elevation: 6,
    borderWidth: 1,
    borderColor: '#6366F1',
  },
  rcaButtonInner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
  },
  rcaIconCircle: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#312E81',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#818CF8',
  },
  rcaTextContainer: {
    flex: 1,
  },
  rcaButtonTitle: {
    fontSize: 15,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  rcaButtonSubtitle: {
    fontSize: 12,
    color: '#C7D2FE',
    marginTop: 3,
    lineHeight: 16,
  },
});
