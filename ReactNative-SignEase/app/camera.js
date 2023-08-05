import { Camera } from "expo-camera";
import { useEffect, useState, useRef } from "react";
import { StyleSheet, Text, TouchableOpacity, View, Image, SafeAreaView } from "react-native";
import { hexToRgbA, config, storage } from "../components";
import axios from "axios";

export default function CameraSign() {
  const username = 'testing'; 
  const [type, setType] = useState(Camera.Constants.Type.front);
  const emptyImage =
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=";
  const [overlayImage, setOverlayImage] = useState(emptyImage);
  const [sentence, setSentence] = useState("");
  const cameraRef = useRef(null);

  let screenshotTimeout;
  const clearSentence = async () => {
    axios.post(`${config.backendUrl}/clear`, {username});
  }
  
  const toggleCameraType = () => {
    setType((current) =>
      current === Camera.Constants.Type.back
        ? Camera.Constants.Type.front
        : Camera.Constants.Type.back
    );
  };

  const takeAndSendScreenshot = async () => {
    try {
      if (cameraRef.current) {
        const photo = await cameraRef.current.takePictureAsync();
        sendScreenshotToServer(photo.uri);
      }
    } catch (error) {
      console.error("Error taking screenshot:", error);
      scheduleScreenshot();
    }
  };

  const sendScreenshotToServer = async (imageUri) => {
    try {
      const formData = new FormData();
      formData.append("screenshot", {
        uri: imageUri,
        name: "screenshot.jpg",
        type: "image/jpg",
      });
      formData.append("name", username);

      const response = await axios.post(`${config.backendUrl}/video`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.data.image) {
        const dataUri = response.data.image;
        setOverlayImage(dataUri);
        setSentence(response.data.sentence);
      }

      scheduleScreenshot();
    } catch (error) {
      console.error("Error sending screenshot to server:", error);
      scheduleScreenshot();
    }
  };

  const scheduleScreenshot = () => {
    screenshotTimeout = setTimeout(takeAndSendScreenshot, 750);
  };

  useEffect(() => {
    takeAndSendScreenshot();

    return () => {
      clearTimeout(screenshotTimeout);
    };
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.cameraContainer}>
        <Camera style={styles.camera} type={type} ref={cameraRef}></Camera>
        {overlayImage !== emptyImage && (
          <View style={styles.overlayContainer}>
            <Image
              source={{ uri: overlayImage }}
              style={styles.overlayImage}
              resizeMode="contain"
            />
          </View>
        )}
      </View>
      <View style={styles.sentenceContainer}>
        <Text style={styles.sentenceText}>{sentence}</Text>
      </View>
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={toggleCameraType}>
          <Text style={styles.text}>🔄</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={clearSentence}>
          <Text style={styles.text}>🗑</Text>
        </TouchableOpacity>
      </View>
      
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: hexToRgbA("#000000"),
  },
  cameraContainer: {
    flex: 1,
  },
  camera: {
    width: "100%", // Adjust the size as needed
    height: "77%", // Adjust the size as needed
  },
  buttonContainer: {
    flexDirection: "row",
    justifyContent: "flex-end",
    alignItems: "center",
    padding: 16,
    bottom: 50,
  },
  button: {},
  text: {
    fontSize: 24,
    fontWeight: "bold",
    color: "white",
  },
  overlayContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: "center",
    alignItems: "center",
    bottom: 160, // adjust accordingly
  },
  overlayImage: {
    width: "100%", // Adjust the size as needed
    height: "100%", // Adjust the size as needed
    opacity: 0.6,
  },
  sentenceContainer: {
    justifyContent: "center",
    alignItems: "center",
    bottom:129, // same as the overlay
  },
  sentenceText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "white",
    textAlign: "center",
  },
});