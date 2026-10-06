import React from 'react';
import { StyleSheet, View, Text, ActivityIndicator } from 'react-native';
import { SvgXml } from 'react-native-svg';
import { Eye, Layers } from 'lucide-react-native';

interface GraphRendererProps {
  svgXml?: string | null;
  width?: number | string;
  height?: number;
  title?: string;
  caption?: string;
}

export const GraphRenderer: React.FC<GraphRendererProps> = ({
  svgXml,
  width = '100%',
  height = 260,
  title = 'AI 수학 도식화 & 기하 그래프',
  caption = '함수의 대칭축과 정의구역의 기하학적 관계를 시각화한 자료입니다.',
}) => {
  if (!svgXml) {
    return (
      <View style={[styles.card, { height }]}>
        <ActivityIndicator size="small" color="#6366F1" />
        <Text style={styles.placeholderText}>도식화 그래프를 생성하는 중입니다...</Text>
      </View>
    );
  }

  // Ensure svg XML has proper encoding and trim
  const cleanXml = svgXml.trim();

  return (
    <View style={styles.card}>
      {/* Header bar */}
      <View style={styles.header}>
        <View style={styles.titleRow}>
          <Layers size={18} color="#818CF8" />
          <Text style={styles.title}>{title}</Text>
        </View>
        <View style={styles.badge}>
          <Eye size={12} color="#10B981" />
          <Text style={styles.badgeText}>시각화 완료</Text>
        </View>
      </View>

      {/* SVG Canvas */}
      <View style={[styles.svgWrapper, { height }]}>
        <SvgXml xml={cleanXml} width="100%" height={height} />
      </View>

      {/* Caption footer */}
      {caption ? (
        <View style={styles.captionContainer}>
          <Text style={styles.captionText}>💡 {caption}</Text>
        </View>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#111827',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#1F2937',
    padding: 14,
    marginVertical: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 4,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
    paddingBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#1F2937',
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  title: {
    fontSize: 15,
    fontWeight: '700',
    color: '#E0E7FF',
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(16, 185, 129, 0.15)',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 12,
  },
  badgeText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#10B981',
  },
  svgWrapper: {
    width: '100%',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 10,
    overflow: 'hidden',
    backgroundColor: '#0F172A',
  },
  captionContainer: {
    marginTop: 10,
    backgroundColor: '#1E293B',
    borderRadius: 8,
    padding: 10,
  },
  captionText: {
    fontSize: 12,
    lineHeight: 18,
    color: '#94A3B8',
  },
  placeholderText: {
    marginTop: 10,
    fontSize: 13,
    color: '#64748B',
  },
});
