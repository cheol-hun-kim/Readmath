import React, { useState } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Image,
  ActivityIndicator,
  ScrollView,
  Alert,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import {
  Camera,
  Image as ImageIcon,
  Sparkles,
  HelpCircle,
  ArrowRight,
  BookOpen,
  Crop,
  Crown,
  Zap,
} from 'lucide-react-native';
import { useMathStore } from '../store/useMathStore';
import { useAuthStore } from '../store/useAuthStore';
import { ImageCropperModal } from '../components/ImageCropperModal';

interface CameraScreenProps {
  navigation: any;
}

export const CameraScreen: React.FC<CameraScreenProps> = ({ navigation }) => {
  const { grade, userId, isPro, dailySolvesRemaining, consumeSolveQuota, setSubModalOpen } = useAuthStore();
  const {
    currentImageUri,
    isSolving,
    setImage,
    solveProblem,
    resetCurrentProblem,
  } = useMathStore();

  const [previewUri, setPreviewUri] = useState<string | null>(null);
  const [previewBase64, setPreviewBase64] = useState<string | null>(null);
  const [isCropperVisible, setIsCropperVisible] = useState(false);

  const handlePickImage = async () => {
    try {
      const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (!permissionResult.granted) {
        Alert.alert('권한 필요', '수학 문제를 불러오기 위해 갤러리 접근 권한이 필요합니다.');
        return;
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: false,
        quality: 0.8,
        base64: true,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const asset = result.assets[0];
        setPreviewUri(asset.uri);
        setPreviewBase64(asset.base64 || null);
        setImage(asset.uri, asset.base64 || null);
        setIsCropperVisible(true);
      }
    } catch (err) {
      console.error('Image picker error:', err);
    }
  };

  const handleTakePhoto = async () => {
    try {
      const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
      if (!permissionResult.granted) {
        Alert.alert('권한 필요', '수학 문제를 촬영하기 위해 카메라 권한이 필요합니다.');
        return;
      }

      const result = await ImagePicker.launchCameraAsync({
        allowsEditing: false,
        quality: 0.8,
        base64: true,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const asset = result.assets[0];
        setPreviewUri(asset.uri);
        setPreviewBase64(asset.base64 || null);
        setImage(asset.uri, asset.base64 || null);
        setIsCropperVisible(true);
      }
    } catch (err) {
      console.error('Camera capture error:', err);
    }
  };

  const handleSolve = async () => {
    const allowed = consumeSolveQuota();
    if (!allowed) return;

    const success = await solveProblem(grade, userId);
    if (success) {
      navigation.navigate('Solution');
    } else {
      Alert.alert('오류', '문제 분석 중 문제가 발생했습니다. 다시 시도해주세요.');
    }
  };

  const handleDemoSolve = async () => {
    resetCurrentProblem();
    setPreviewUri(null);
    setPreviewBase64(null);
    const success = await solveProblem(grade, userId);
    if (success) {
      navigation.navigate('Solution');
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      {/* Header Banner */}
      <View style={styles.header}>
        <View style={styles.logoRow}>
          <View style={styles.logoBadge}>
            <Text style={styles.logoSymbol}>R</Text>
          </View>
          <View>
            <Text style={styles.appName}>ReadMath</Text>
            <Text style={styles.tagline}>수학은 해석의 대상이다</Text>
          </View>
        </View>

        {/* Quota & Grade Badges */}
        <View style={styles.headerRight}>
          <TouchableOpacity
            style={[styles.quotaBadge, isPro && styles.proQuotaBadge]}
            onPress={() => setSubModalOpen(true)}
          >
            {isPro ? (
              <>
                <Crown size={12} color="#FBBF24" />
                <Text style={styles.proQuotaText}>PRO 무제한</Text>
              </>
            ) : (
              <>
                <Zap size={12} color="#818CF8" />
                <Text style={styles.quotaText}>오늘 {dailySolvesRemaining}회 무료</Text>
              </>
            )}
          </TouchableOpacity>

          <View style={styles.gradeBadge}>
            <Text style={styles.gradeText}>{grade}</Text>
          </View>
        </View>
      </View>

      {/* Philosophy Callout */}
      <View style={styles.philosophyCard}>
        <Sparkles size={18} color="#818CF8" />
        <Text style={styles.philosophyText}>
          "유형을 외우지 마세요. 막힌 조건과 도식화(그래프)의 근본 원인을 찾아냅니다."
        </Text>
      </View>

      {/* Camera/Photo Capture Area */}
      <View style={styles.cameraBox}>
        {previewUri ? (
          <View style={styles.previewContainer}>
            <Image source={{ uri: previewUri }} style={styles.previewImage} resizeMode="contain" />
            
            <View style={styles.previewButtonRow}>
              <TouchableOpacity
                style={styles.cropActionBtn}
                onPress={() => setIsCropperVisible(true)}
              >
                <Crop size={14} color="#CBD5E1" />
                <Text style={styles.cropBtnText}>영역 다시 자르기</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.retakeButton}
                onPress={() => {
                  setPreviewUri(null);
                  setPreviewBase64(null);
                  setImage(null, null);
                }}
              >
                <Text style={styles.retakeText}>다시 선택</Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : (
          <View style={styles.emptyPrompt}>
            <View style={styles.cameraIconCircle}>
              <Camera size={36} color="#818CF8" />
            </View>
            <Text style={styles.promptTitle}>수학 문제를 촬영하세요</Text>
            <Text style={styles.promptDesc}>
              수식, 기하 도형, 킬러 문항을 AI가 인식하고 도식화합니다.
            </Text>

            <View style={styles.buttonRow}>
              <TouchableOpacity style={styles.actionBtn} onPress={handleTakePhoto} activeOpacity={0.8}>
                <Camera size={18} color="#FFFFFF" />
                <Text style={styles.actionBtnText}>카메라 촬영</Text>
              </TouchableOpacity>

              <TouchableOpacity style={styles.actionBtnOutline} onPress={handlePickImage} activeOpacity={0.8}>
                <ImageIcon size={18} color="#818CF8" />
                <Text style={styles.actionBtnOutlineText}>앨범에서 선택</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
      </View>

      {/* Primary Solve Button */}
      {previewUri ? (
        <TouchableOpacity
          style={[styles.primarySolveBtn, isSolving && styles.btnDisabled]}
          onPress={handleSolve}
          disabled={isSolving}
          activeOpacity={0.85}
        >
          {isSolving ? (
            <View style={styles.loadingRow}>
              <ActivityIndicator size="small" color="#FFFFFF" />
              <Text style={styles.primarySolveBtnText}>AI가 개념과 도식화를 분석 중...</Text>
            </View>
          ) : (
            <View style={styles.loadingRow}>
              <Sparkles size={20} color="#FFFFFF" />
              <Text style={styles.primarySolveBtnText}>AI 풀이 & 시각화 시작하기</Text>
            </View>
          )}
        </TouchableOpacity>
      ) : (
        /* Quick Sample Demo Solve Button */
        <TouchableOpacity style={styles.demoCard} onPress={handleDemoSolve} activeOpacity={0.8}>
          <View style={styles.demoLeft}>
            <BookOpen size={20} color="#34D399" />
            <View>
              <Text style={styles.demoTitle}>고1 킬러 문항 샘플로 즉시 체험</Text>
              <Text style={styles.demoDesc}>미분 배제! 완전제곱식 & SVG 포물선 그래프</Text>
            </View>
          </View>
          <ArrowRight size={18} color="#94A3B8" />
        </TouchableOpacity>
      )}

      {/* Guide Tips */}
      <View style={styles.guideBox}>
        <View style={styles.guideTitleRow}>
          <HelpCircle size={14} color="#64748B" />
          <Text style={styles.guideTitle}>RootMath 풀이 프로세스</Text>
        </View>
        <Text style={styles.guideItem}>1. 문제 이미지 촬영 및 영역 자르기 (Crop)</Text>
        <Text style={styles.guideItem}>2. 핵심 개념 + 단계별 풀이 + 실시간 SVG 그래프 확인</Text>
        <Text style={styles.guideItem}>3. 🧑‍🏫 '루트 쌤'과 1:1 시각화 대화로 모르는 점 질문</Text>
        <Text style={styles.guideItem}>4. [단어 단위 해체] 자가진단(RCA) 및 오답노트 자동 저장</Text>
      </View>

      {/* Image Cropper Modal */}
      <ImageCropperModal
        visible={isCropperVisible}
        imageUri={previewUri}
        onConfirmCrop={() => setIsCropperVisible(false)}
        onCancel={() => setIsCropperVisible(false)}
      />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F19',
  },
  contentContainer: {
    padding: 20,
    paddingTop: 50,
    paddingBottom: 40,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  logoBadge: {
    width: 44,
    height: 44,
    borderRadius: 14,
    backgroundColor: '#4F46E5',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoSymbol: {
    fontSize: 20,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  appName: {
    fontSize: 20,
    fontWeight: '800',
    color: '#F8FAFC',
  },
  tagline: {
    fontSize: 11,
    color: '#94A3B8',
    marginTop: 2,
  },
  headerRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  quotaBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: 'rgba(99, 102, 241, 0.15)',
    paddingHorizontal: 8,
    paddingVertical: 5,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#4338CA',
  },
  proQuotaBadge: {
    backgroundColor: 'rgba(245, 158, 11, 0.2)',
    borderColor: '#F59E0B',
  },
  quotaText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#A5B4FC',
  },
  proQuotaText: {
    fontSize: 11,
    fontWeight: '800',
    color: '#FBBF24',
  },
  gradeBadge: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#334155',
  },
  gradeText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#818CF8',
  },
  philosophyCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    backgroundColor: 'rgba(99, 102, 241, 0.1)',
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: 'rgba(99, 102, 241, 0.25)',
    marginBottom: 20,
  },
  philosophyText: {
    fontSize: 12,
    color: '#C7D2FE',
    flex: 1,
    lineHeight: 18,
    fontWeight: '500',
  },
  cameraBox: {
    backgroundColor: '#111827',
    borderRadius: 20,
    borderWidth: 2,
    borderColor: '#1F2937',
    borderStyle: 'dashed',
    minHeight: 280,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    marginBottom: 20,
  },
  emptyPrompt: {
    alignItems: 'center',
    width: '100%',
  },
  cameraIconCircle: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: '#1E1B4B',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#4338CA',
  },
  promptTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#F1F5F9',
    marginBottom: 6,
  },
  promptDesc: {
    fontSize: 12,
    color: '#94A3B8',
    textAlign: 'center',
    lineHeight: 18,
    marginBottom: 20,
    paddingHorizontal: 10,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 12,
    width: '100%',
  },
  actionBtn: {
    flex: 1,
    backgroundColor: '#4F46E5',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 14,
    borderRadius: 12,
  },
  actionBtnText: {
    fontSize: 14,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  actionBtnOutline: {
    flex: 1,
    backgroundColor: '#1E293B',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 14,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#4338CA',
  },
  actionBtnOutlineText: {
    fontSize: 14,
    fontWeight: '700',
    color: '#A5B4FC',
  },
  previewContainer: {
    width: '100%',
    alignItems: 'center',
  },
  previewImage: {
    width: '100%',
    height: 220,
    borderRadius: 12,
  },
  previewButtonRow: {
    flexDirection: 'row',
    gap: 10,
    marginTop: 12,
  },
  cropActionBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#374151',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 8,
  },
  cropBtnText: {
    fontSize: 12,
    color: '#E5E7EB',
    fontWeight: '600',
  },
  retakeButton: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#475569',
  },
  retakeText: {
    fontSize: 12,
    color: '#94A3B8',
    fontWeight: '600',
  },
  primarySolveBtn: {
    backgroundColor: '#4F46E5',
    paddingVertical: 16,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.35,
    shadowRadius: 10,
    elevation: 6,
    marginBottom: 16,
  },
  btnDisabled: {
    backgroundColor: '#334155',
    shadowOpacity: 0,
  },
  loadingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  primarySolveBtnText: {
    fontSize: 16,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  demoCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#13221B',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#065F46',
    marginBottom: 20,
  },
  demoLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
  },
  demoTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#6EE7B7',
  },
  demoDesc: {
    fontSize: 11,
    color: '#A7F3D0',
    marginTop: 2,
  },
  guideBox: {
    backgroundColor: '#111827',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#1F2937',
  },
  guideTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 10,
  },
  guideTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: '#94A3B8',
  },
  guideItem: {
    fontSize: 12,
    color: '#64748B',
    lineHeight: 20,
  },
});
