import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { StyleSheet, Text, View } from 'react-native';
import { useRouter } from 'expo-router';
import { hexToRgbA, config, storage } from '../components';

export default function CameraSign() {
  const router = useRouter();
  const [loadingItem, setLoadingItem] = useState(true);
  const [membershipExpired, setMembershipExpired] = useState(false);

  useEffect(() => {
    storage.load({
      key: 'user',
      autoSync: true,
    }).then(user => {
      const username = user.username;
      const url = `${config.backendUrl}/checkMembership`;
      axios.post(url, { 'username': username })
        .then(response => {
          if (response.data.validity === true) {
            router.push("/camera");
          } else {
            setMembershipExpired(true);
          }
          setLoadingItem(false);
        })
        .catch(error => {
          console.error('Error checking membership:', error);
          setLoadingItem(false);
        });
    });
  }, []); // Empty dependency array to run the effect once

  return (
    <View style={styles.container}>
      {loadingItem ? (
        <Text style={styles.text}>Checking Your membership...</Text>
      ) : (
        membershipExpired ? (
          <Text style={styles.text}>Your Membership has expired!</Text>
        ) : (
          <Text style={styles.text}>Membership is valid!</Text>
        )
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: hexToRgbA('#000000'),
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
});
