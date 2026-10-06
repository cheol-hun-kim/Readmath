import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { Scissors, AlertCircle } from 'lucide-react-native';

interface ProblemDecompositionViewProps {
  ocrText: string;
  decomposedClauses?: string[];
  selectedClause: string | null;
  selectedKeyword: string | null;
  onSelectClause: (clause: string, keyword: string) => void;
}

export const ProblemDecompositionView: React.FC<ProblemDecompositionViewProps> = ({
  ocrText,
  decomposedClauses,
  selectedClause,
  selectedKeyword,
  onSelectClause,
}) => {
  // If clauses are not pre-decomposed by AI, split by punctuation/conditions
  const clauses = decomposedClauses && decomposedClauses.length > 0
    ? decomposedClauses
    : ocrText.split(/(?<=[,.\n]|때,)/).map((s) => s.trim()).filter(Boolean);

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.headerRow}>
        <View style={styles.titleWithIcon}>
          <Scissors size={16} color="#A78BFA" />
          <Text style={styles.title}>조건 단위 문제 해체 (RCA)</Text>
        </View>
        <Text style={styles.subtitle}>막혔던 조건이나 단어를 터치하세요</Text>
      </View>

      <Text style={styles.guideMessage}>
        수학 문제는 조건들의 결합입니다. 어느 단어/조건에서 사고가 멈췄나요?
      </Text>

      {/* Clauses Chips */}
      <View style={styles.clausesContainer}>
        {clauses.map((clause, index) => {
          const isSelected = selectedClause === clause;
          
          // Split clause into individual words/tokens for granular sub-selection
          const words = clause.split(' ').filter(Boolean);

          return (
            <View
              key={`clause_${index}`}
              style={[
                styles.clauseCard,
                isSelected && styles.clauseCardSelected,
              ]}
            >
              {/* Clause Header / Full Clause Touch */}
              <TouchableOpacity
                style={styles.clauseMainTouchable}
                onPress={() => onSelectClause(clause, words[0] || clause)}
                activeOpacity={0.7}
              >
                <View style={styles.clauseNumberBadge}>
                  <Text style={styles.clauseNumberText}>조건 {index + 1}</Text>
                </View>
                <Text
                  style={[
                    styles.clauseText,
                    isSelected && styles.clauseTextSelected,
                  ]}
                >
                  {clause}
                </Text>
              </TouchableOpacity>

              {/* Granular Word Chips inside Clause */}
              <View style={styles.wordChipsRow}>
                {words.map((word, wIdx) => {
                  const isWordSelected = isSelected && selectedKeyword === word;
                  return (
                    <TouchableOpacity
                      key={`w_${index}_${wIdx}`}
                      style={[
                        styles.wordChip,
                        isWordSelected && styles.wordChipSelected,
                      ]}
                      onPress={() => onSelectClause(clause, word)}
                      activeOpacity={0.8}
                    >
                      <Text
                        style={[
                          styles.wordChipText,
                          isWordSelected && styles.wordChipTextSelected,
                        ]}
                      >
                        {word}
                      </Text>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>
          );
        })}
      </View>

      {/* Selected Indicator */}
      {selectedClause ? (
        <View style={styles.selectionNotification}>
          <AlertCircle size={16} color="#60A5FA" />
          <Text style={styles.selectionText}>
            선택된 막힘 지점: <Text style={styles.boldKeyword}>{selectedKeyword || selectedClause}</Text>
          </Text>
        </View>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#111827',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#1F2937',
    padding: 16,
    marginVertical: 10,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  titleWithIcon: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  title: {
    fontSize: 15,
    fontWeight: '700',
    color: '#E0E7FF',
  },
  subtitle: {
    fontSize: 12,
    color: '#818CF8',
    fontWeight: '600',
  },
  guideMessage: {
    fontSize: 12,
    color: '#9CA3AF',
    marginBottom: 14,
    lineHeight: 18,
  },
  clausesContainer: {
    gap: 10,
  },
  clauseCard: {
    backgroundColor: '#1E293B',
    borderRadius: 12,
    padding: 12,
    borderWidth: 1.5,
    borderColor: 'transparent',
  },
  clauseCardSelected: {
    borderColor: '#6366F1',
    backgroundColor: '#1E1B4B',
  },
  clauseMainTouchable: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    marginBottom: 8,
  },
  clauseNumberBadge: {
    backgroundColor: '#374151',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6,
  },
  clauseNumberText: {
    fontSize: 10,
    fontWeight: '700',
    color: '#D1D5DB',
  },
  clauseText: {
    fontSize: 14,
    color: '#F3F4F6',
    flex: 1,
    lineHeight: 20,
    fontWeight: '500',
  },
  clauseTextSelected: {
    color: '#C7D2FE',
    fontWeight: '700',
  },
  wordChipsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    paddingTop: 4,
    borderTopWidth: 1,
    borderTopColor: 'rgba(255, 255, 255, 0.06)',
  },
  wordChip: {
    backgroundColor: '#0F172A',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  wordChipSelected: {
    backgroundColor: '#4F46E5',
    borderColor: '#818CF8',
  },
  wordChipText: {
    fontSize: 12,
    color: '#CBD5E1',
  },
  wordChipTextSelected: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  selectionNotification: {
    marginTop: 12,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: 'rgba(59, 130, 246, 0.12)',
    padding: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(59, 130, 246, 0.3)',
  },
  selectionText: {
    fontSize: 12,
    color: '#93C5FD',
    flex: 1,
  },
  boldKeyword: {
    fontWeight: '700',
    color: '#BFDBFE',
  },
});
