import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  TextInput,
} from 'react-native';
import {
  BookMarked,
  Search,
  CheckCircle2,
  Circle,
  Scissors,
  Layers,
  Sparkles,
  ArrowRight,
  BookOpen,
  Sigma,
  LineChart,
  SearchCode,
} from 'lucide-react-native';
import { useHistoryStore } from '../store/useHistoryStore';
import { useMathStore } from '../store/useMathStore';
import { FailureType, FAILURE_TYPE_MAP } from '../types/math';

interface HistoryScreenProps {
  navigation: any;
}

export const HistoryScreen: React.FC<HistoryScreenProps> = ({ navigation }) => {
  const {
    savedProblems,
    activeFilter,
    searchQuery,
    setActiveFilter,
    setSearchQuery,
    toggleResolved,
  } = useHistoryStore();

  const filteredProblems = savedProblems.filter((p) => {
    // Search query matching
    const matchSearch =
      searchQuery === '' ||
      p.ocr_text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.concepts_used.some((c) => c.toLowerCase().includes(searchQuery.toLowerCase()));

    if (!matchSearch) return false;

    // Filter matching
    if (activeFilter === 'all') return true;
    if (activeFilter === 'resolved') return p.weakness?.is_resolved === true;
    return p.weakness?.failure_type === activeFilter;
  });

  const getFailureIcon = (type?: FailureType) => {
    switch (type) {
      case 'concept':
        return <BookOpen size={14} color="#EF4444" />;
      case 'modeling':
        return <Sigma size={14} color="#F59E0B" />;
      case 'visual':
        return <LineChart size={14} color="#3B82F6" />;
      case 'interpretation':
        return <SearchCode size={14} color="#8B5CF6" />;
      default:
        return <Layers size={14} color="#818CF8" />;
    }
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerTitleRow}>
          <BookMarked size={22} color="#818CF8" />
          <Text style={styles.headerTitle}>오답노트 & 문제 보관함</Text>
        </View>
        <Text style={styles.headerSubtitle}>
          풀었던 문제와 RCA 자가진단 기록을 다시 복습하세요.
        </Text>

        {/* Search Bar */}
        <View style={styles.searchContainer}>
          <Search size={16} color="#64748B" />
          <TextInput
            style={styles.searchInput}
            placeholder="개념, 키워드, 문제 검색..."
            placeholderTextColor="#64748B"
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>

        {/* Filter Scroll */}
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
          <TouchableOpacity
            style={[styles.filterChip, activeFilter === 'all' && styles.filterChipSelected]}
            onPress={() => setActiveFilter('all')}
          >
            <Text style={[styles.filterText, activeFilter === 'all' && styles.filterTextSelected]}>
              전체 ({savedProblems.length})
            </Text>
          </TouchableOpacity>

          {(Object.keys(FAILURE_TYPE_MAP) as FailureType[]).map((typeKey) => {
            const info = FAILURE_TYPE_MAP[typeKey];
            const isSelected = activeFilter === typeKey;
            return (
              <TouchableOpacity
                key={typeKey}
                style={[styles.filterChip, isSelected && styles.filterChipSelected]}
                onPress={() => setActiveFilter(typeKey)}
              >
                <Text style={[styles.filterText, isSelected && styles.filterTextSelected]}>
                  {info.label}
                </Text>
              </TouchableOpacity>
            );
          })}

          <TouchableOpacity
            style={[styles.filterChip, activeFilter === 'resolved' && styles.filterChipSelected]}
            onPress={() => setActiveFilter('resolved')}
          >
            <Text style={[styles.filterText, activeFilter === 'resolved' && styles.filterTextSelected]}>
              ✓ 해결 완료
            </Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      {/* Problem Cards List */}
      <ScrollView contentContainerStyle={styles.listContent} showsVerticalScrollIndicator={false}>
        {filteredProblems.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyTitle}>저장된 문제가 없습니다.</Text>
            <Text style={styles.emptyDesc}>새로운 수학 문제를 촬영하여 풀고 자가진단해보세요!</Text>
          </View>
        ) : (
          filteredProblems.map((item) => {
            const weaknessInfo = item.weakness
              ? FAILURE_TYPE_MAP[item.weakness.failure_type]
              : null;
            const isResolved = item.weakness?.is_resolved;

            return (
              <View key={item.id} style={styles.card}>
                {/* Card Top */}
                <View style={styles.cardTop}>
                  <View style={styles.tagRow}>
                    {weaknessInfo ? (
                      <View style={[styles.badge, { backgroundColor: `${weaknessInfo.color}22` }]}>
                        {getFailureIcon(item.weakness?.failure_type)}
                        <Text style={[styles.badgeText, { color: weaknessInfo.color }]}>
                          {weaknessInfo.label}
                        </Text>
                      </View>
                    ) : null}
                    <Text style={styles.conceptMainText}>
                      {item.concepts_used[0] || '수학 문제'}
                    </Text>
                  </View>

                  {/* Resolved Toggle Button */}
                  <TouchableOpacity
                    style={styles.resolvedToggle}
                    onPress={() => toggleResolved(item.id)}
                  >
                    {isResolved ? (
                      <CheckCircle2 size={18} color="#10B981" />
                    ) : (
                      <Circle size={18} color="#475569" />
                    )}
                    <Text style={[styles.resolvedToggleText, isResolved && { color: '#10B981' }]}>
                      {isResolved ? '복습 완료' : '미완료'}
                    </Text>
                  </TouchableOpacity>
                </View>

                {/* Problem Statement */}
                <Text style={styles.cardOcrText} numberOfLines={2}>
                  {item.ocr_text.replace(/\$/g, '')}
                </Text>

                {/* Card Footer */}
                <View style={styles.cardFooter}>
                  <Text style={styles.cardAnswer}>정답: {item.answer}</Text>
                  <TouchableOpacity
                    style={styles.reviewBtn}
                    onPress={() => navigation.navigate('Solution')}
                  >
                    <Text style={styles.reviewBtnText}>풀이 & 1:1 대화</Text>
                    <ArrowRight size={14} color="#818CF8" />
                  </TouchableOpacity>
                </View>
              </View>
            );
          })
        )}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F19',
  },
  header: {
    paddingHorizontal: 16,
    paddingTop: 50,
    paddingBottom: 10,
    backgroundColor: '#0F172A',
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
  },
  headerTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '800',
    color: '#F8FAFC',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#94A3B8',
    marginBottom: 12,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#1E293B',
    borderRadius: 12,
    paddingHorizontal: 12,
    paddingVertical: 8,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#334155',
  },
  searchInput: {
    flex: 1,
    color: '#F8FAFC',
    fontSize: 13,
    padding: 0,
  },
  filterScroll: {
    flexDirection: 'row',
    paddingBottom: 6,
  },
  filterChip: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 10,
    marginRight: 6,
    borderWidth: 1,
    borderColor: '#334155',
  },
  filterChipSelected: {
    backgroundColor: '#4F46E5',
    borderColor: '#818CF8',
  },
  filterText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#94A3B8',
  },
  filterTextSelected: {
    color: '#FFFFFF',
  },
  listContent: {
    padding: 16,
    paddingBottom: 30,
    gap: 12,
  },
  card: {
    backgroundColor: '#111827',
    borderRadius: 16,
    padding: 14,
    borderWidth: 1,
    borderColor: '#1F2937',
  },
  cardTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  tagRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    flex: 1,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6,
  },
  badgeText: {
    fontSize: 10,
    fontWeight: '700',
  },
  conceptMainText: {
    fontSize: 11,
    color: '#CBD5E1',
    fontWeight: '600',
  },
  resolvedToggle: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  resolvedToggleText: {
    fontSize: 11,
    color: '#64748B',
    fontWeight: '600',
  },
  cardOcrText: {
    fontSize: 13,
    color: '#F1F5F9',
    lineHeight: 18,
    marginBottom: 10,
  },
  cardFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#1E293B',
  },
  cardAnswer: {
    fontSize: 12,
    fontWeight: '700',
    color: '#34D399',
  },
  reviewBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  reviewBtnText: {
    fontSize: 12,
    color: '#818CF8',
    fontWeight: '700',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
  },
  emptyTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#94A3B8',
    marginBottom: 4,
  },
  emptyDesc: {
    fontSize: 12,
    color: '#64748B',
  },
});
