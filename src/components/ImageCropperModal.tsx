import React, { useState } from 'react';
import {
  StyleSheet,
  View,
  Text,
  Modal,
  TouchableOpacity,
  Image,
  Dimensions,
} from 'react-native';
import { Crop, X, Check, Move, Sparkles } from 'lucide-react-native';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

interface ImageCropperModalProps {
  visible: boolean;
  imageUri: string | null;
  onConfirmCrop: () => void;
  onCancel: () => void;
}

export const ImageCropperModal: React.FC<ImageCropperModalProps> = ({
  visible,
  imageUri,
  onConfirmCrop,
  onCancel,
}) => {
  if (!imageUri) return null;

  return (
    <Modal visible={visible} transparent={true} animationType="fade" onRequestClose={onCancel}>
      <View style={styles.overlay}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={onCancel} style={styles.iconBtn}>
            <X size={22} color="#CBD5E1" />
          </TouchableOpacity>
          <View style={styles.titleContainer}>
            <Text style={styles.headerTitle}>문제 영역 자르기</Text>
            <Text style={styles.headerSubtitle}>풀고자 하는 문제 하나만 사각형 안에 맞춰주세요</Text>
          </View>
          <TouchableOpacity onPress={onConfirmCrop} style={styles.confirmBtn}>
            <Check size={20} color="#FFFFFF" />
          </TouchableOpacity>
        </View>

        {/* Crop Area */}
        <View style={styles.imageContainer}>
          <Image source={{ uri: imageUri }} style={styles.fullImage} resizeMode="contain" />

          {/* Shaded Outer Overlay */}
          <View style={styles.shadeTop} />
          <View style={styles.shadeBottom} />
          <View style={styles.shadeLeft} />
          <View style={styles.shadeRight} />

          {/* Interactive Crop Box Window */}
          <View style={styles.cropBox}>
            {/* Grid Lines */}
            <View style={styles.gridH1} />
            <View style={styles.gridH2} />
            <View style={styles.gridV1} />
            <View style={styles.gridV2} />

            {/* Corner Handles */}
            <View style={[styles.corner, styles.cornerTL]} />
            <View style={[styles.corner, styles.cornerTR]} />
            <View style={[styles.corner, styles.cornerBL]} />
            <View style={[styles.corner, styles.cornerBR]} />

            {/* Center Hint */}
            <View style={styles.centerBadge}>
              <Move size={12} color="#A78BFA" />
              <Text style={styles.centerBadgeText}>문제 맞춤 영역</Text>
            </View>
          </View>
        </View>

        {/* Footer Actions */}
        <View style={styles.footer}>
          <TouchableOpacity style={styles.primaryCropBtn} onPress={onConfirmCrop} activeOpacity={0.85}>
            <Sparkles size={18} color="#FFFFFF" />
            <Text style={styles.primaryCropBtnText}>이 영역으로 풀이 및 도식화 시작</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: '#0B0F19',
    justifyContent: 'space-between',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingTop: 50,
    paddingBottom: 14,
    backgroundColor: '#0F172A',
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
    zIndex: 10,
  },
  iconBtn: {
    padding: 6,
  },
  titleContainer: {
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 15,
    fontWeight: '800',
    color: '#F8FAFC',
  },
  headerSubtitle: {
    fontSize: 11,
    color: '#94A3B8',
    marginTop: 2,
  },
  confirmBtn: {
    backgroundColor: '#4F46E5',
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  imageContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
    backgroundColor: '#000000',
  },
  fullImage: {
    width: SCREEN_WIDTH,
    height: '100%',
  },
  shadeTop: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '25%',
    backgroundColor: 'rgba(0, 0, 0, 0.65)',
  },
  shadeBottom: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: '25%',
    backgroundColor: 'rgba(0, 0, 0, 0.65)',
  },
  shadeLeft: {
    position: 'absolute',
    top: '25%',
    bottom: '25%',
    left: 0,
    width: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.65)',
  },
  shadeRight: {
    position: 'absolute',
    top: '25%',
    bottom: '25%',
    right: 0,
    width: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.65)',
  },
  cropBox: {
    position: 'absolute',
    top: '25%',
    left: 20,
    right: 20,
    bottom: '25%',
    borderWidth: 2,
    borderColor: '#6366F1',
    alignItems: 'center',
    justifyContent: 'center',
  },
  gridH1: {
    position: 'absolute',
    top: '33.3%',
    left: 0,
    right: 0,
    height: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  gridH2: {
    position: 'absolute',
    top: '66.6%',
    left: 0,
    right: 0,
    height: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  gridV1: {
    position: 'absolute',
    left: '33.3%',
    top: 0,
    bottom: 0,
    width: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  gridV2: {
    position: 'absolute',
    left: '66.6%',
    top: 0,
    bottom: 0,
    width: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  corner: {
    position: 'absolute',
    width: 20,
    height: 20,
    borderColor: '#FFFFFF',
  },
  cornerTL: { top: -2, left: -2, borderTopWidth: 4, borderLeftWidth: 4 },
  cornerTR: { top: -2, right: -2, borderTopWidth: 4, borderRightWidth: 4 },
  cornerBL: { bottom: -2, left: -2, borderBottomWidth: 4, borderLeftWidth: 4 },
  cornerBR: { bottom: -2, right: -2, borderBottomWidth: 4, borderRightWidth: 4 },
  centerBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(15, 23, 42, 0.8)',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#4338CA',
  },
  centerBadgeText: {
    fontSize: 11,
    color: '#C7D2FE',
    fontWeight: '700',
  },
  footer: {
    padding: 16,
    paddingBottom: 34,
    backgroundColor: '#0F172A',
    borderTopWidth: 1,
    borderTopColor: '#1E293B',
  },
  primaryCropBtn: {
    backgroundColor: '#4F46E5',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 15,
    borderRadius: 14,
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.35,
    shadowRadius: 8,
  },
  primaryCropBtnText: {
    fontSize: 15,
    fontWeight: '800',
    color: '#FFFFFF',
  },
});
