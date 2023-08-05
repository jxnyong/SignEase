
import { View, SafeAreaView, ScrollView } from 'react-native';
import { Stack, useRouter } from 'expo-router';
import { LoginPage,hexToRgbA } from '../components';
export default function Home() {
  const router = useRouter();
  return (
    <SafeAreaView style={{flex:1, backgroundColor:hexToRgbA('#24303F')}}>
      <Stack.Screen
        options={{
          headerStyle: {backgroundColor:hexToRgbA('#24303F'),color:hexToRgbA('#000000'),},
          headerShadowVisible:false,
          headerTitle:"SignEase"
        }}
      />
      <ScrollView showsVerticalScrollIndicator={false}>
        <View
         style={{
          flex:1,
         }}>
        <LoginPage/>
        </View>
      </ScrollView>
    </SafeAreaView>
  )
}
