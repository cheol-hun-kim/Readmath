import React, { useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import {
  PieChart,
  Flame,
  BookOpen,
  Sigma,
  LineChart,
  SearchCode,
  CheckCircle2,
  Calendar,
  AlertTriangle,
} from 'lucide-react-native';
import { useWeaknessStore } from '../store/useWeaknessStore';
import { useAuthStore } from '../store/useAuthStore';
import { FailureType, FAILURE_TYPE_MAP } from '../types/math';

export const WeaknessReportScreen: React.FC = () => {
  const { userId, grade } = useAuthStore();
  const { stats, weaknesses, loadWeaknessStats } = useWeaknessStore();

  useEffect(() => {
    loadWeaknessStats(userId);
  }, [userId]);

  const totalCount = Math.max(stats.total, 1);

  const getPercentage = (count: number) => {
    return Math.round((count / totalCount) * 100);
  };

  const getIcon = (type: FailureType) => {
    switch (type) {
      case 'concept':
        return <BookOpen size={18} color={FAILURE_TYPE_MAP.concept.color} />;
      case 'modeling':
        return <Sigma size={18} color={FAILURE_TYPE_MAP.modeling.color} />;
      case 'visual':
        return <LineChart size={18} color={FAILURE_TYPE_MAP.visual.color} />;
      case 'interpretation':
        return <SearchCode size={18} color={FAILURE_TYPE_MAP.interpretation.color} />;
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      {/* Top Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.headerTitle}>나의 취약점 분석 리포트</Text>
          <Text style={styles.headerSubtitle}>
            유형 암기 탈피를 위한 사고력 누적 진단
          </Text>
        </View>
        <View style={styles.gradeBadge}>
          <Text style={styles.gradeText}>{grade}</Text>
        </View>
      </View>

      {/* Summary KPI Cards */}
      <View style={styles.kpiRow}>
        <View style={styles.kpiCard}>
          <Text style={styles.kpiLabel}>총 자가진단(RCA)</Text>
          <Text style={styles.kpiValue}>{stats.total}회</Text>
        </View>
        <View style={[styles.kpiCard, { borderColor: '#4338CA' }]}>
          <Text style={styles.kpiLabel}>최다 취약 원인</Text>
          <Text style={[styles.kpiValue, { color: '#818CF8', fontSize: 16 }]}>
            도식화(그래프) 실패
          </Text>
        </View>
      </View>

      {/* 1. Failure Type Distribution Breakdown */}
      <View style={styles.sectionCard}>
        <View style={styles.sectionHeader}>
          <PieChart size={18} color="#818CF8" />
          <Text style={styles.sectionTitle}>근본 원인별 취약점 분포</Text>
        </View>

        <View style={styles.barList}>
          {(Object.keys(FAILURE_TYPE_MAP) as FailureType[]).map((typeKey) => {
            const info = FAILURE_TYPE_MAP[typeKey];
            const count = stats.byType[typeKey] || 0;
            const percentage = getPercentage(count);

            return (
              <View key={typeKey} style={styles.barItem}>
                <View style={styles.barItemHeader}>
                  <View style={styles.barLabelRow}>
                    {getIcon(typeKey)}
                    <Text style={styles.barLabel}>{info.label}</Text>
                  </View>
                  <Text style={styles.barPercentText}>
                    {count}건 ({percentage}%)
                  </Text>
                </View>

                {/* Progress Bar */}
                <View style={styles.progressTrack}>
                  <View
                    style={[
                      styles.progressFill,
                      {
                        width: `${Math.max(percentage, 4)}%`,
                        backgroundColor: info.color,
                      },
                    ]}
                  />
                </View>
              </View>
            );
          })}
        </View>
      </View>

      {/* 2. Top Missed Concepts / Recurring Pitfalls */}
      <View style={styles.sectionCard}>
        <View style={styles.sectionHeader}>
          <Flame size={18} color="#EF4444" />
          <Text style={styles.sectionTitle}>반복 감지된 취약 키워드</Text>
        </View>

        <View style={styles.keywordsGrid}>
          {stats.topKeywords.map((item, idx) => (
            <View key={`kw_${idx}`} style={styles.keywordCard}>
              <View style={styles.keywordRankBadge}>
                <Text style={styles.rankNumber}>{idx + 1}</Text>
              </View>
              <View style={styles.keywordInfo}>
                <Text style={styles.keywordName}>{item.keyword}</Text>
                <Text style={styles.keywordCount}>{item.count}회 반복 실수</Text>
              </View>
            </View>
          ))}
        </View>
      </View>

      {/* 3. RCA History Log */}
      <View style={styles.sectionCard}>
        <View style={styles.sectionHeader}>
          <Calendar size={18} color="#34D399" />
          <Text style={styles.sectionTitle}>최근 자가진단 기록 (RCA Log)</Text>
        </View>

        <View style={styles.historyList}>
          {weaknesses.map((item) => {
            const info = FAILURE_TYPE_MAP[item.failure_type] || FAILURE_TYPE_MAP.concept;
            const dateStr = new Date(item.created_at).toLocaleDateString('ko-KR', {
              month: 'short',
              day: 'numeric',
            });

            return (
              <View key={item.id} style={styles.historyItem}>
                <View style={styles.historyItemHeader}>
                  <View style={[styles.historyTypeBadge, { backgroundColor: `${info.color}22` }]}>
                    <Text style={[styles.historyTypeText, { color: info.color }]}>
                      {info.label}
                    </Text>
                  </View>
                  <Text style={styles.historyDate}>{dateStr}</Text>
                </View>

                <Text style={styles.historyKeyword}>
                  막힌 단어: <Text style={styles.highlightWord}>"{item.missed_keyword}"</Text>
                </Text>

                {item.prescription_notes ? (
                  <Text style={styles.historyNotes} numberOfLines={2}>
                    💡 {item.prescription_notes.replace(/###/g, '').trim()}
                  </Text>
                ) : null}
              </View>
            );
          })}
        </View>
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: '#F8FAFC',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#94A3B8',
    marginTop: 2,
  },
  gradeBadge: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#334155',
  },
  gradeText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#818CF8',
  },
  kpiRow: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 14,
  },
  kpiCard: {
    flex: 1,
    backgroundColor: '#111827',
    borderRadius: 14,
    padding: 14,
    borderWidth: 1,
    borderColor: '#1F2937',
  },
  kpiLabel: {
    fontSize: 12,
    color: '#94A3B8',
    marginBottom: 6,
  },
  kpiValue: {
    fontSize: 20,
    fontWeight: '800',
    color: '#F8FAFC',
  },
  sectionCard: {
    backgroundColor: '#111827',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#1F2937',
    padding: 16,
    marginBottom: 14,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 14,
  },
  sectionTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#E0E7FF',
  },
  barList: {
    gap: 14,
  },
  barItem: {},
  barItemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  barLabelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  barLabel: {
    fontSize: 13,
    fontWeight: '600',
    color: '#E2E8F0',
  },
  barPercentText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#94A3B8',
  },
  progressTrack: {
    height: 8,
    backgroundColor: '#1E293B',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  keywordsGrid: {
    gap: 8,
  },
  keywordCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1E293B',
    padding: 12,
    borderRadius: 12,
    gap: 12,
  },
  keywordRankBadge: {
    width: 26,
    height: 26,
    borderRadius: 13,
    backgroundColor: '#374151',
    alignItems: 'center',
    justifyContent: 'center',
  },
  rankNumber: {
    fontSize: 12,
    fontWeight: '800',
    color: '#F87171',
  },
  keywordInfo: {
    flex: 1,
  },
  keywordName: {
    fontSize: 13,
    fontWeight: '700',
    color: '#F1F5F9',
  },
  keywordCount: {
    fontSize: 11,
    color: '#94A3B8',
    marginTop: 2,
  },
  historyList: {
    gap: 10,
  },
  historyItem: {
    backgroundColor: '#1E293B',
    borderRadius: 12,
    padding: 12,
    borderLeftWidth: 3,
    borderLeftColor: '#6366F1',
  },
  historyItemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  historyTypeBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  historyTypeText: {
    fontSize: 11,
    fontWeight: '700',
  },
  historyDate: {
    fontSize: 11,
    color: '#64748B',
  },
  historyKeyword: {
    fontSize: 13,
    color: '#CBD5E1',
    marginBottom: 4,
  },
  highlightWord: {
    color: '#FDE047',
    fontWeight: '700',
  },
  historyNotes: {
    fontSize: 12,
    color: '#94A3B8',
    lineHeight: 16,
  },
});
