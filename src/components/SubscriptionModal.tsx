import React, { useState } from 'react';
import {
  StyleSheet,
  View,
  Text,
  Modal,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';
import {
  X,
  Crown,
  CheckCircle2,
  Sparkles,
  Zap,
  ShieldCheck,
  Flame,
} from 'lucide-react-native';
import { useAuthStore } from '../store/useAuthStore';

interface SubscriptionModalProps {
  visible: boolean;
  onClose: () => void;
}

export const SubscriptionModal: React.FC<SubscriptionModalProps> = ({
  visible,
  onClose,
}) => {
  const { upgradeToPro } = useAuthStore();
  const [selectedPlan, setSelectedPlan] = useState<'annual' | 'monthly'>('annual');

  const handleSubscribe = () => {
    upgradeToPro(selectedPlan);
    Alert.alert(
      '🎉 RootMath Pro 구독 완료!',
      '모든 제한이 해제되었습니다. 이제 무제한 문제 풀이와 루트 쌤과의 1:1 시각화 대화를 마음껏 이용하세요!'
    );
  };

  return (
    <Modal visible={visible} transparent={true} animationType="slide" onRequestClose={onClose}>
      <View style={styles.overlay}>
        <View style={styles.content}>
          {/* Close Button */}
          <TouchableOpacity style={styles.closeBtn} onPress={onClose}>
            <X size={20} color="#94A3B8" />
          </TouchableOpacity>

          <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollContent}>
            {/* Header Crown */}
            <View style={styles.headerArea}>
              <View style={styles.crownCircle}>
                <Crown size={28} color="#FBBF24" />
              </View>
              <Text style={styles.title}>RootMath Pro 무제한 패스</Text>
              <Text style={styles.subtitle}>
                한 달 40만 원 과외보다 강력한 나만의 1:1 AI 수학 멘토
              </Text>
            </View>

            {/* Plan Selector Cards */}
            <View style={styles.planContainer}>
              {/* Annual Plan (Best Value) */}
              <TouchableOpacity
                style={[
                  styles.planCard,
                  selectedPlan === 'annual' && styles.planCardSelected,
                ]}
                onPress={() => setSelectedPlan('annual')}
                activeOpacity={0.8}
              >
                <View style={styles.saveBadge}>
                  <Text style={styles.saveBadgeText}>37% 할인 + 7일 무료체험</Text>
                </View>
                <View style={styles.planRow}>
                  <View>
                    <Text style={styles.planName}>연간 구독 (추천 👑)</Text>
                    <Text style={styles.planSubPrice}>월 12,400원 상당 (연 149,000원)</Text>
                  </View>
                  <Text style={styles.planPrice}>월 1.2만</Text>
                </View>
              </TouchableOpacity>

              {/* Monthly Plan */}
              <TouchableOpacity
                style={[
                  styles.planCard,
                  selectedPlan === 'monthly' && styles.planCardSelected,
                ]}
                onPress={() => setSelectedPlan('monthly')}
                activeOpacity={0.8}
              >
                <View style={styles.planRow}>
                  <View>
                    <Text style={styles.planName}>월간 구독</Text>
                    <Text style={styles.planSubPrice}>언제든 해지 가능</Text>
                  </View>
                  <Text style={styles.planPrice}>19,800원<Text style={styles.perMonth}>/월</Text></Text>
                </View>
              </TouchableOpacity>
            </View>

            {/* Features Checklist */}
            <View style={styles.featuresCard}>
              <Text style={styles.featuresTitle}>👑 Pro 회원 독점 혜택</Text>
              
              <View style={styles.featureItem}>
                <CheckCircle2 size={16} color="#10B981" />
                <Text style={styles.featureText}>Vision 문제 촬영 및 단계별 풀이 <Text style={styles.boldWhite}>무제한</Text></Text>
              </View>

              <View style={styles.featureItem}>
                <CheckCircle2 size={16} color="#10B981" />
                <Text style={styles.featureText}>실시간 SVG 함수 그래프 & 도형 도식화 <Text style={styles.boldWhite}>무제한</Text></Text>
              </View>

              <View style={styles.featureItem}>
                <CheckCircle2 size={16} color="#10B981" />
                <Text style={styles.featureText}>'루트 쌤' 1:1 시각화 문답 & 약점 지적 <Text style={styles.boldWhite}>무제한</Text></Text>
              </View>

              <View style={styles.featureItem}>
                <CheckCircle2 size={16} color="#10B981" />
                <Text style={styles.featureText}>누적 오답노트 & 취약점 분석 리포트 평생 보관</Text>
              </View>

              <View style={styles.featureItem}>
                <CheckCircle2 size={16} color="#10B981" />
                <Text style={styles.featureText}>초1부터 고3/N수 전 학년 교과과정 자유 전환</Text>
              </View>
            </View>

            {/* Subscribe Action Button */}
            <TouchableOpacity style={styles.subscribeBtn} onPress={handleSubscribe} activeOpacity={0.85}>
              <Sparkles size={18} color="#FFFFFF" />
              <Text style={styles.subscribeBtnText}>
                {selectedPlan === 'annual' ? '7일 무료체험 시작하기' : 'RootMath Pro 시작하기'}
              </Text>
            </TouchableOpacity>

            <Text style={styles.guaranteeText}>
              🛡️ 언제든 앱스토어 / 플레이스토어 설정에서 클릭 한 번으로 해지 가능
            </Text>
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    justifyContent: 'flex-end',
  },
  content: {
    backgroundColor: '#0F172A',
    borderTopLeftRadius: 28,
    borderTopRightRadius: 28,
    maxHeight: '90%',
    paddingHorizontal: 20,
    paddingTop: 18,
    paddingBottom: 34,
    borderWidth: 1,
    borderColor: '#334155',
  },
  closeBtn: {
    alignSelf: 'flex-end',
    padding: 6,
    borderRadius: 16,
    backgroundColor: '#1E293B',
  },
  scrollContent: {
    paddingBottom: 20,
  },
  headerArea: {
    alignItems: 'center',
    marginBottom: 16,
  },
  crownCircle: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: 'rgba(245, 158, 11, 0.15)',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
    borderWidth: 1,
    borderColor: 'rgba(245, 158, 11, 0.3)',
  },
  title: {
    fontSize: 20,
    fontWeight: '900',
    color: '#F8FAFC',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 12,
    color: '#94A3B8',
    textAlign: 'center',
    marginTop: 4,
    lineHeight: 18,
  },
  planContainer: {
    gap: 10,
    marginBottom: 16,
  },
  planCard: {
    backgroundColor: '#1E293B',
    borderRadius: 16,
    padding: 14,
    borderWidth: 2,
    borderColor: '#334155',
    position: 'relative',
  },
  planCardSelected: {
    borderColor: '#6366F1',
    backgroundColor: '#1E1B4B',
  },
  saveBadge: {
    position: 'absolute',
    top: -10,
    right: 14,
    backgroundColor: '#EF4444',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
  },
  saveBadgeText: {
    fontSize: 10,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  planRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  planName: {
    fontSize: 14,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  planSubPrice: {
    fontSize: 11,
    color: '#94A3B8',
    marginTop: 2,
  },
  planPrice: {
    fontSize: 18,
    fontWeight: '900',
    color: '#818CF8',
  },
  perMonth: {
    fontSize: 12,
    color: '#94A3B8',
    fontWeight: '400',
  },
  featuresCard: {
    backgroundColor: '#111827',
    borderRadius: 14,
    padding: 14,
    marginBottom: 18,
    borderWidth: 1,
    borderColor: '#1F2937',
    gap: 10,
  },
  featuresTitle: {
    fontSize: 13,
    fontWeight: '800',
    color: '#FBBF24',
    marginBottom: 2,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  featureText: {
    fontSize: 12,
    color: '#CBD5E1',
    flex: 1,
  },
  boldWhite: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  subscribeBtn: {
    backgroundColor: '#4F46E5',
    paddingVertical: 16,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
    gap: 8,
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.4,
    shadowRadius: 10,
  },
  subscribeBtnText: {
    fontSize: 16,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  guaranteeText: {
    fontSize: 11,
    color: '#64748B',
    textAlign: 'center',
    marginTop: 10,
  },
});
