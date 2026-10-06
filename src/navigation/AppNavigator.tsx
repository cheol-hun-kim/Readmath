import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Camera, BookMarked, BarChart3, Settings } from 'lucide-react-native';

import { CameraScreen } from '../screens/CameraScreen';
import { SolutionScreen } from '../screens/SolutionScreen';
import { DiagnosisScreen } from '../screens/DiagnosisScreen';
import { ChatTutorScreen } from '../screens/ChatTutorScreen';
import { HistoryScreen } from '../screens/HistoryScreen';
import { WeaknessReportScreen } from '../screens/WeaknessReportScreen';
import { SettingsScreen } from '../screens/SettingsScreen';
import { SubscriptionModal } from '../components/SubscriptionModal';
import { SocialLoginModal } from '../components/SocialLoginModal';
import { useAuthStore } from '../store/useAuthStore';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

function BottomTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: '#0F172A',
          borderTopColor: '#1E293B',
          borderTopWidth: 1,
          height: 64,
          paddingBottom: 10,
          paddingTop: 8,
        },
        tabBarActiveTintColor: '#818CF8',
        tabBarInactiveTintColor: '#64748B',
        tabBarLabelStyle: {
          fontSize: 10,
          fontWeight: '700',
        },
      }}
    >
      <Tab.Screen
        name="SolveTab"
        component={CameraScreen}
        options={{
          tabBarLabel: '문제 풀기',
          tabBarIcon: ({ color }) => <Camera color={color} size={20} />,
        }}
      />
      <Tab.Screen
        name="HistoryTab"
        component={HistoryScreen}
        options={{
          tabBarLabel: '오답노트',
          tabBarIcon: ({ color }) => <BookMarked color={color} size={20} />,
        }}
      />
      <Tab.Screen
        name="ReportTab"
        component={WeaknessReportScreen}
        options={{
          tabBarLabel: '취약점 리포트',
          tabBarIcon: ({ color }) => <BarChart3 color={color} size={20} />,
        }}
      />
      <Tab.Screen
        name="SettingsTab"
        component={SettingsScreen}
        options={{
          tabBarLabel: '설정',
          tabBarIcon: ({ color }) => <Settings color={color} size={20} />,
        }}
      />
    </Tab.Navigator>
  );
}

export const AppNavigator = () => {
  const { isSubModalOpen, setSubModalOpen, isLoginModalOpen, setLoginModalOpen } = useAuthStore();

  return (
    <>
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: '#0B0F19' },
        }}
      >
        <Stack.Screen name="MainTabs" component={BottomTabs} />
        <Stack.Screen
          name="Solution"
          component={SolutionScreen}
          options={{ animation: 'slide_from_right' }}
        />
        <Stack.Screen
          name="Diagnosis"
          component={DiagnosisScreen}
          options={{ animation: 'slide_from_bottom' }}
        />
        <Stack.Screen
          name="ChatTutor"
          component={ChatTutorScreen}
          options={{ animation: 'slide_from_right' }}
        />
      </Stack.Navigator>

      {/* Global Modals */}
      <SubscriptionModal
        visible={isSubModalOpen}
        onClose={() => setSubModalOpen(false)}
      />
      <SocialLoginModal
        visible={isLoginModalOpen}
        onClose={() => setLoginModalOpen(false)}
      />
    </>
  );
};
