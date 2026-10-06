import React, { useState } from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
} from 'react-native';
import {
  Settings,
  Key,
  GraduationCap,
  Sparkles,
  Award,
  ShieldCheck,
  AlertTriangle,
} from 'lucide-react-native';
import { useAuthStore } from '../store/useAuthStore';
import { setGeminiApiKey } from '../services/ai/geminiClient';
import { CURRICULUM_MAP, GradeLevel } from '../types/math';

const ELEMENTARY_LOWER_GRADES: GradeLevel[] = ['초1', '초2'];
const ELEMENTARY_UPPER_GRADES: GradeLevel[] = ['초3', '초4', '초5', '초6'];
const MIDDLE_GRADES: GradeLevel[] = ['중1', '중2', '중3'];
const HIGH_GRADES: GradeLevel[] = ['고1', '고2', '고3/N수'];

export const SettingsScreen: React.FC = () => {
  const { grade, setGrade, geminiApiKey, setGeminiApiKey: storeSetApiKey } = useAuthStore();
  const [inputApiKey, setInputApiKey] = useState(geminiApiKey);

  const handleSaveApiKey = () => {
    storeSetApiKey(inputApiKey);
    setGeminiApiKey(inputApiKey);
    Alert.alert('저장 완료', 'Google Gemini API 키가 성공적으로 등록되었습니다.');
  };

  const currentCurriculum = CURRICULUM_MAP[grade as GradeLevel] || CURRICULUM_MAP['고1'];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.titleRow}>
          <Settings size={22} color="#818CF8" />
          <Text style={styles.headerTitle}>학년 및 교육과정 설정</Text>
        </View>
        <Text style={styles.headerSubtitle}>
          초1부터 고3/N수까지 대한민국 국가수학교육과정 엄격 격리
        </Text>
      </View>

      {/* 1. Grade Selection & Strict Curriculum Rule Display */}
      <View style={styles.sectionCard}>
        <View style={styles.cardHeader}>
          <GraduationCap size={18} color="#818CF8" />
          <Text style={styles.cardTitle}>학년 선택 (초1 ~ 고3/N수)</Text>
        </View>
        <Text style={styles.cardDesc}>
          설정한 학년 이상의 선행 공식(미분, 음수, 연립방정식 등)은 일체 배제되며 해당 학년의 정규 교과 도구로만 설명합니다.
        </Text>

        {/* Current Active Curriculum Scope Card */}
        <View style={styles.activeCurriculumCard}>
          <View style={styles.curriculumTopRow}>
            <View style={styles.badgeStage}>
              <Award size={14} color="#F59E0B" />
              <Text style={styles.badgeStageText}>{currentCurriculum.stageName}</Text>
            </View>
            <Text style={styles.curriculumGradeName}>{currentCurriculum.label}</Text>
          </View>

          <View style={styles.ruleItem}>
            <View style={styles.ruleHeader}>
              <ShieldCheck size={14} color="#10B981" />
              <Text style={styles.ruleTitleGreen}>허용 교육과정 범위:</Text>
            </View>
            <Text style={styles.ruleBody}>{currentCurriculum.allowedScope}</Text>
          </View>

          <View style={[styles.ruleItem, { borderLeftColor: '#EF4444' }]}>
            <View style={styles.ruleHeader}>
              <AlertTriangle size={14} color="#EF4444" />
              <Text style={styles.ruleTitleRed}>🚨 절대 사용 금지 상위 개념 (선행 차단):</Text>
            </View>
            <Text style={styles.ruleBodyRed}>{currentCurriculum.strictlyBanned}</Text>
          </View>

          <View style={[styles.ruleItem, { borderLeftColor: '#8B5CF6' }]}>
            <View style={styles.ruleHeader}>
              <Sparkles size={14} color="#A78BFA" />
              <Text style={styles.ruleTitlePurple}>권장 시각화 도구:</Text>
            </View>
            <Text style={styles.ruleBody}>{currentCurriculum.recommendedPedagogy}</Text>
          </View>
        </View>

        {/* Stage 1: Elementary Lower (초1, 초2) */}
        <Text style={styles.stageSectionTitle}>🌱 초등 저학년 (구체물 & 연산 직관)</Text>
        <View style={styles.gradeGrid}>
          {ELEMENTARY_LOWER_GRADES.map((g) => {
            const isSelected = grade === g;
            return (
              <TouchableOpacity
                key={g}
                style={[styles.gradeChip, isSelected && styles.gradeChipSelected]}
                onPress={() => setGrade(g)}
                activeOpacity={0.8}
              >
                <Text style={[styles.gradeChipText, isSelected && styles.gradeChipTextSelected]}>
                  {g}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>

        {/* Stage 2: Elementary Upper (초3 ~ 초6) */}
        <Text style={styles.stageSectionTitle}>🏫 초등 중·고학년 (분수·소수 & 도형·비례)</Text>
        <View style={styles.gradeGrid}>
          {ELEMENTARY_UPPER_GRADES.map((g) => {
            const isSelected = grade === g;
            return (
              <TouchableOpacity
                key={g}
                style={[styles.gradeChip, isSelected && styles.gradeChipSelected]}
                onPress={() => setGrade(g)}
                activeOpacity={0.8}
              >
                <Text style={[styles.gradeChipText, isSelected && styles.gradeChipTextSelected]}>
                  {g}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>

        {/* Stage 3: Middle School (중1 ~ 중3) */}
        <Text style={styles.stageSectionTitle}>🏛️ 중등 과정 (대수 방정식 & 논증 기하)</Text>
        <View style={styles.gradeGrid}>
          {MIDDLE_GRADES.map((g) => {
            const isSelected = grade === g;
            return (
              <TouchableOpacity
                key={g}
                style={[styles.gradeChip, isSelected && styles.gradeChipSelected]}
                onPress={() => setGrade(g)}
                activeOpacity={0.8}
              >
                <Text style={[styles.gradeChipText, isSelected && styles.gradeChipTextSelected]}>
                  {g}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>

        {/* Stage 4: High School & Exam (고1, 고2, 고3/N수) */}
        <Text style={styles.stageSectionTitle}>🎓 고등 / 수능 과정 (개념 결합 킬러 추론)</Text>
        <View style={styles.gradeGrid}>
          {HIGH_GRADES.map((g) => {
            const isSelected = grade === g;
            return (
              <TouchableOpacity
                key={g}
                style={[styles.gradeChip, isSelected && styles.gradeChipSelected]}
                onPress={() => setGrade(g)}
                activeOpacity={0.8}
              >
                <Text style={[styles.gradeChipText, isSelected && styles.gradeChipTextSelected]}>
                  {g}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>
      </View>

      {/* 2. Google Gemini API Key Config */}
      <View style={styles.sectionCard}>
        <View style={styles.cardHeader}>
          <Key size={18} color="#F59E0B" />
          <Text style={styles.cardTitle}>AI Vision & 시각화 엔진 API Key</Text>
        </View>
        <Text style={styles.cardDesc}>
          Gemini 1.5 Pro의 초정밀 수식/도형 인식 및 1:1 대화형 SVG 생성을 위해 API Key를 설정합니다.
        </Text>

        <TextInput
          style={styles.input}
          placeholder="AIzaSy..."
          placeholderTextColor="#64748B"
          value={inputApiKey}
          onChangeText={setInputApiKey}
          secureTextEntry={true}
          autoCapitalize="none"
        />

        <TouchableOpacity
          style={styles.saveKeyButton}
          onPress={handleSaveApiKey}
          activeOpacity={0.8}
        >
          <Text style={styles.saveKeyButtonText}>API Key 저장</Text>
        </TouchableOpacity>
      </View>

      {/* 3. RootMath Educational Philosophy Manifesto */}
      <View style={styles.manifestoCard}>
        <View style={styles.manifestoHeader}>
          <Sparkles size={18} color="#FBBF24" />
          <Text style={styles.manifestoTitle}>RootMath의 수학교육 철학</Text>
        </View>
        <Text style={styles.manifestoParagraph}>
          1. <Text style={styles.manifestoHighlight}>상위 교육과정 남용 금지:</Text> 초등학생에게 중등 방정식을 쓰거나, 고1에게 미분을 가르치는 것은 수학적 사고력을 파괴합니다. 해당 학년 도구로 끝까지 증명해야 합니다.
        </Text>
        <Text style={styles.manifestoParagraph}>
          2. <Text style={styles.manifestoHighlight}>모든 설명에 그림 동원:</Text> 수식을 머리로만 외우지 않고 그래프, 수직선, 도형으로 손수 도식화하는 것이 성적 도약의 유일한 길입니다.
        </Text>
        <Text style={styles.manifestoParagraph}>
          3. <Text style={styles.manifestoHighlight}>사고 정지 지점 분해 (RCA):</Text> 단어 단위로 문제를 해체하여 자신이 왜 막혔는지 스스로 진단합니다.
        </Text>
      </View>
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
    paddingTop: 50,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 18,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 4,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: '#F8FAFC',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#94A3B8',
  },
  sectionCard: {
    backgroundColor: '#111827',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#1F2937',
    padding: 16,
    marginBottom: 16,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 6,
  },
  cardTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#E0E7FF',
  },
  cardDesc: {
    fontSize: 12,
    color: '#94A3B8',
    lineHeight: 18,
    marginBottom: 12,
  },
  activeCurriculumCard: {
    backgroundColor: '#1E1B4B',
    borderRadius: 14,
    padding: 14,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#4338CA',
  },
  curriculumTopRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 10,
    paddingBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.1)',
  },
  badgeStage: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: 'rgba(245, 158, 11, 0.2)',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  badgeStageText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#FBBF24',
  },
  curriculumGradeName: {
    fontSize: 14,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  ruleItem: {
    backgroundColor: '#0F172A',
    borderRadius: 8,
    padding: 8,
    marginBottom: 8,
    borderLeftWidth: 3,
    borderLeftColor: '#10B981',
  },
  ruleHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 2,
  },
  ruleTitleGreen: {
    fontSize: 11,
    fontWeight: '800',
    color: '#34D399',
  },
  ruleTitleRed: {
    fontSize: 11,
    fontWeight: '800',
    color: '#F87171',
  },
  ruleTitlePurple: {
    fontSize: 11,
    fontWeight: '800',
    color: '#C7D2FE',
  },
  ruleBody: {
    fontSize: 11,
    color: '#CBD5E1',
    lineHeight: 16,
  },
  ruleBodyRed: {
    fontSize: 11,
    color: '#FCA5A5',
    lineHeight: 16,
    fontWeight: '600',
  },
  stageSectionTitle: {
    fontSize: 12,
    fontWeight: '700',
    color: '#818CF8',
    marginTop: 8,
    marginBottom: 6,
  },
  gradeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 10,
  },
  gradeChip: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 16,
    paddingVertical: 9,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#334155',
  },
  gradeChipSelected: {
    backgroundColor: '#4F46E5',
    borderColor: '#818CF8',
  },
  gradeChipText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#94A3B8',
  },
  gradeChipTextSelected: {
    color: '#FFFFFF',
  },
  input: {
    backgroundColor: '#0F172A',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 10,
    padding: 12,
    color: '#F1F5F9',
    fontSize: 14,
    marginBottom: 12,
  },
  saveKeyButton: {
    backgroundColor: '#374151',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  saveKeyButtonText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#E2E8F0',
  },
  manifestoCard: {
    backgroundColor: '#1E1B4B',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#4338CA',
  },
  manifestoHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 10,
  },
  manifestoTitle: {
    fontSize: 14,
    fontWeight: '800',
    color: '#FDE047',
  },
  manifestoParagraph: {
    fontSize: 12,
    color: '#CBD5E1',
    lineHeight: 19,
    marginBottom: 8,
  },
  manifestoHighlight: {
    fontWeight: '700',
    color: '#E0E7FF',
  },
});
