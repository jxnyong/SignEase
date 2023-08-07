import { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Linking } from "react-native";
import { useRouter } from "expo-router";
import config from "../url.json";
import storage from "../storage";
import axios from "axios";
import LogoSVG from './logo'
import { COLORS, FONT, SIZES } from "../../constants";
// import useFetch from "../../hook/useFetch";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const onPressLogin = () => {
    const url = `${config.backendUrl}/login`;
    axios.post(url, { username, password })
      .then((response) => {
        // Handle the response from the server
        console.log('Response:', response.data);
        storage.save({key:'user',
          data: {'username':username}})
        router.push("/checkMembership");
        // You can perform further actions based on the response, such as setting state or redirecting the user.
      })
      .catch((error) => {
        // Handle errors
        // console.error('Error:', error);
        alert("Username or Password Incorrect");
      });
  };
  return (
    <View>
      <View style={styles.container}>
        <Text style={styles.title}>Login Page</Text>
      </View>
      <Text></Text>
      <LogoSVG/>
      <View style={styles.inputContainer}>
        <TextInput
          placeholder=" Username"
          onChangeText={(text) => setUsername(text)}
          style={styles.inputWrapper}
        />
      </View>
      <View style={styles.inputContainer}>
        <TextInput
          placeholder=" Password"
          secureTextEntry
          onChangeText={(text) => setPassword(text)}
          style={styles.inputWrapper}
        />
      </View>
      <View style={styles.btnWrapper}>
      <TouchableOpacity onPress={onPressLogin} style={styles.inputBtn}>
          <Text>Login </Text>
        </TouchableOpacity>
      <TouchableOpacity style={styles.inputBtn} onPress={()=>{Linking.openURL(`${config.react_web}/signup`)}}>
        <Text>Signup</Text>
      </TouchableOpacity>
      </View>
    </View>
  );
}
const styles = StyleSheet.create({
  container: {
    width: "100%",
  },
  title: {
    fontFamily: FONT.bold,
    fontSize: SIZES.xLarge,
    color: COLORS.primary,
    marginTop: 2,
    textAlign:"center",
  },
  inputContainer: {
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
    marginTop: SIZES.large,
    margin: SIZES.xSmall,
    height: 50,
  },
  inputWrapper: {
    flex: 1,
    backgroundColor: COLORS.white,
    marginRight: SIZES.small,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: SIZES.medium,
    height: "100%",
  },
  input: {
    fontFamily: FONT.regular,
    width: "100%",
    height: "100%",
    paddingHorizontal: SIZES.medium,
  },
  btnWrapper: {
    flex: 1,
    marginRight: SIZES.small,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: SIZES.medium,
    height: "100%",
  },
  inputBtn: {
    width: "95%",
    backgroundColor: COLORS.tertiary,
    borderRadius: SIZES.medium,
    justifyContent: "center",
    alignItems: "center",
    textAlign:"center",
    padding: SIZES.medium,
    margin: SIZES.small,
  },
  tabsContainer: {
    width: "100%",
    marginTop: SIZES.medium,
  },
  tab: (activeJobType, item) => ({
    paddingVertical: SIZES.small / 2,
    paddingHorizontal: SIZES.small,
    borderRadius: SIZES.medium,
    borderWidth: 1,
    borderColor: activeJobType === item ? COLORS.secondary : COLORS.gray2,
  }),
  tabText: (activeJobType, item) => ({
    fontFamily: FONT.medium,
    color: activeJobType === item ? COLORS.secondary : COLORS.gray2,
  }),
});
