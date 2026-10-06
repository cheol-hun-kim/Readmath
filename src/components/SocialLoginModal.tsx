import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  Modal,
  TouchableOpacity,
} from 'react-native';
import { X, LogIn, Sparkles } from 'lucide-react-native';
import { useAuthStore, AuthProvider } from '../store/useAuthStore';

interface SocialLoginModalProps {
  visible: boolean;
  onClose: () => void;
}

export const SocialLoginModal: React.FC<SocialLoginModalProps> = ({
  visible,
  onClose,
}) => {
  const { loginWithSocial } = useAuthStore();

  const handleLogin = (provider: AuthProvider) => {
    loginWithSocial(provider);
    onClose();
  };

  return (
    <Modal visible={visible} transparent={true} animationType="slide" onRequestClose={onClose}>
      <View style={styles.overlay}>
        <View style={styles.content}>
          <TouchableOpacity style={styles.closeBtn} onPress={onClose}>
            <X size={20} color="#94A3B8" />
          </TouchableOpacity>

          <View style={styles.header}>
            <View style={styles.logoBadge}>
              <Text style={styles.logoSymbol}>R</Text>
            </View>
            <Text style={styles.title}>3초 만에 시작하기</Text>
            <Text style={styles.subtitle}>
              로그인하고 나의 오답노트와 취약점 진단 데이터를 기기 간에 안전하게 보관하세요.
            </Text>
          </View>

          {/* Social Buttons */}
          <View style={styles.buttonList}>
            {/* Kakao */}
            <TouchableOpacity
              style={[styles.socialBtn, styles.kakaoBtn]}
              onPress={() => handleLogin('kakao')}
              activeOpacity={0.8}
            >
              <Text style={styles.kakaoText}>💬 카카오로 3초 로그인</Text>
            </TouchableOpacity>

            {/* Apple */}
            <TouchableOpacity
              style={[styles.socialBtn, styles.appleBtn]}
              onPress={() => handleLogin('apple')}
              activeOpacity={0.8}
            >
              <Text style={styles.appleText}> Apple로 계속하기</Text>
            </TouchableOpacity>

            {/* Google */}
            <TouchableOpacity
              style={[styles.socialBtn, styles.googleBtn]}
              onPress={() => handleLogin('google')}
              activeOpacity={0.8}
            >
              <Text style={styles.googleText}>G Google로 계속하기</Text>
            </TouchableOpacity>

            {/* Guest */}
            <TouchableOpacity
              style={styles.guestBtn}
              onPress={() => handleLogin('guest')}
              activeOpacity={0.8}
            >
              <Text style={styles.guestText}>로그인 없이 체험하기</Text>
            </TouchableOpacity>
          </View>

          <Text style={styles.termsText}>
            계속 진행 시 RootMath의 이용약관 및 개인정보처리방침에 동의하게 됩니다.
          </Text>
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
  header: {
    alignItems: 'center',
    marginBottom: 20,
  },
  logoBadge: {
    width: 52,
    height: 52,
    borderRadius: 16,
    backgroundColor: '#4F46E5',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
  },
  logoSymbol: {
    fontSize: 24,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  title: {
    fontSize: 20,
    fontWeight: '900',
    color: '#F8FAFC',
  },
  subtitle: {
    fontSize: 12,
    color: '#94A3B8',
    textAlign: 'center',
    marginTop: 4,
    lineHeight: 18,
  },
  buttonList: {
    gap: 10,
    marginBottom: 16,
  },
  socialBtn: {
    paddingVertical: 14,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
  },
  kakaoBtn: {
    backgroundColor: '#FEE500',
  },
  kakaoText: {
    color: '#000000',
    fontSize: 14,
    fontWeight: '800',
  },
  appleBtn: {
    backgroundColor: '#FFFFFF',
  },
  appleText: {
    color: '#000000',
    fontSize: 14,
    fontWeight: '800',
  },
  googleBtn: {
    backgroundColor: '#1E293B',
    borderWidth: 1,
    borderColor: '#334155',
  },
  googleText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '800',
  },
  guestBtn: {
    paddingVertical: 10,
    alignItems: 'center',
  },
  guestText: {
    fontSize: 12,
    color: '#64748B',
    fontWeight: '600',
  },
  termsText: {
    fontSize: 10,
    color: '#64748B',
    textAlign: 'center',
    lineHeight: 14,
  },
});
