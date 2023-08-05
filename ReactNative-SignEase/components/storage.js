import Storage from 'react-native-storage';
import AsyncStorage from '@react-native-async-storage/async-storage';
const storage = new Storage({
  // maximum capacity, default 5 key-ids
  size: 5,

  // Use AsyncStorage for RN apps, or window.localStorage for web apps.
  // If storageBackend is not set, data will be lost after reload.
  storageBackend: AsyncStorage, // for web: window.localStorage

  // cache data in the memory. default is true.
  enableCache: true,

  // if data was not found in storage or expired data was found,
  // the corresponding sync method will be invoked returning
  // the latest data.
});

export default storage;